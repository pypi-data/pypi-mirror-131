import os
from pathlib import Path
import dill as pickle
from pprint import pprint
from typing import Union

from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.utils.sklearn_adapter import sklearn_adapter
import numpy as np
from numpy import ascontiguousarray, concatenate, float64
import pandas as pd
from scipy.stats import uniform
from sklearn.utils.fixes import loguniform
from sksurv.ensemble import RandomSurvivalForest
from sksurv.metrics import concordance_index_censored
from sksurv.svm import FastSurvivalSVM
from sksurv.util import Surv

from harmoniums import SurvivalHarmonium
from harmoniums.utils import brier_loss, double_cross_validate, reset_random_state


class Benchmark:
    """
    Benchmark models on a dataset.
    """

    def __init__(
        self,
        X,
        survival_columns: list,
        event_columns: list,
        categorical_columns: list = [],
        numeric_columns: list = [],
        output_folder: str = "output",
        # Consume all cores.
        n_jobs: int = -1,
        # Test this much hyperparameter settings.
        n_iter: int = 50,
        # Perform m x n cross validation.
        m_x_n: tuple = (5, 5),
        random_state: int = 1234,
        verbose: bool = True,
        scoring_time_point: Union[str, float, np.ndarray] = "median",
    ):
        if isinstance(scoring_time_point, str) and scoring_time_point == "median":
            # Determine median survival using Kaplan-Meier.
            median_survivals = []
            for i in range(len(survival_columns)):
                km = KaplanMeierFitter().fit(
                    durations=X[survival_columns[i]], event_observed=X[event_columns[i]]
                )
                median_survivals.append(km.median_survival_time_)
            self.scoring_time_point_ = np.array(median_survivals)
        elif isinstance(scoring_time_point, np.ndarray):
            self.scoring_time_point_ = scoring_time_point
        else:
            self.scoring_time_point_ = np.array(
                [scoring_time_point] * len(survival_columns)
            )

        self.X = X
        self.survival_columns = survival_columns
        self.event_columns = event_columns
        self.categorical_columns = categorical_columns
        self.numeric_columns = numeric_columns
        self.random_state = random_state

        self.n_jobs = n_jobs
        if n_jobs == -1:
            self.n_jobs = int(os.environ.get("SLURM_JOB_CPUS_PER_NODE", -1))

        self.n_iter = n_iter
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose

        self.m_x_n = m_x_n

        self.scores_file = self.output_folder / "scores.csv"
        self.scores = pd.DataFrame()
        # Try to load existing scores, so that the values are updated instead of
        # overwritten.
        if self.scores_file.exists():
            self.scores = pd.read_csv(self.scores_file, index_col=0)

    def brier_score(self, time, event, predictions, survival_column_index: int = 0):
        """
        Calculate the Brier loss at `scoring_time_point`.
        """
        time_column = self.survival_columns[survival_column_index]
        event_column = self.event_columns[survival_column_index]
        tau = self.scoring_time_point_[survival_column_index]
        # Score is negation of loss.
        return -brier_loss(
            train_time=self.X[time_column],
            train_event=self.X[event_column],
            test_time=time,
            test_event=event,
            S_pred=predictions,
            tau=tau,
        )

    def _cox_brier_score(self, estimator, X, y, survival_column_index: int = 0):
        """
        Brier scoring function for lifelines CoxPHFitter.
        """
        if hasattr(estimator, "lifelines_model"):
            model = estimator.lifelines_model
        else:
            # Extract model from cross-validation estimator.
            model = estimator.best_estimator_.lifelines_model

        event_column = self.event_columns[survival_column_index]
        tau = self.scoring_time_point_[survival_column_index]
        S_pred = model.predict_survival_function(
            X.drop(columns=event_column), tau
        ).T.values
        return self.brier_score(
            y,
            event=X[event_column],
            predictions=S_pred,
            survival_column_index=survival_column_index,
        )

    def _random_forest_brier_score(
        self, estimator, X, y, survival_column_index: int = 0
    ):
        """
        Brier scoring function of scikit survival random survival forest.
        """
        tau = self.scoring_time_point_[survival_column_index]
        time_column = self.survival_columns[survival_column_index]
        event_column = self.event_columns[survival_column_index]

        if not hasattr(estimator, "predict_survival_function"):
            # Extract model from cross-validation estimator.
            estimator = estimator.best_estimator_

        # Calculate survival distribution at tau.
        survs = estimator.predict_survival_function(X, return_array=False)
        preds = [fn(tau) for fn in survs]

        return self.brier_score(
            time=y[time_column],
            event=y[event_column],
            predictions=preds,
            survival_column_index=survival_column_index,
        )

    def _harmonium_brier_score(
        self,
        estimator,
        X,
        y=None,
        conditional_probability: bool = False,
        survival_column_index: int = 0,
    ):
        """
        Brier scoring for harmonium.
        """
        n_A = len(self.categorical_columns)
        n_B = len(self.survival_columns)
        n_C = len(self.numeric_columns)
        # Column names after converting DataFrame to Numpy matrix.
        time_column = n_A
        event_column = n_A + n_B + n_C

        # Extract model from cross-validation estimator.
        if not isinstance(estimator, SurvivalHarmonium):
            estimator = estimator.best_estimator_

        time_point = {time_column: self.scoring_time_point_[survival_column_index]}
        preds = estimator.predict(
            X,
            conditional_probability=conditional_probability,
            time_point=time_point,
        )

        return self.brier_score(
            time=X[:, time_column],
            event=X[:, event_column],
            predictions=preds[time_column],
            survival_column_index=survival_column_index,
        )

    def _harmonium_concordance_score(self, estimator, X, y=None):
        """
        Calculate concordance index, ignoring all other survival variables.
        """
        # Extract model from cross-validation estimator.
        if not isinstance(estimator, SurvivalHarmonium):
            estimator = estimator.best_estimator_
        # Compute score for first survival variable (indexed as the n_A'th
        # column after converting DataFrame to Numpy matrix).
        n_A = len(self.categorical_columns)
        time_point = {n_A: self.scoring_time_point_[0]}
        return estimator.concordance_index(
            X, conditional_probability=False, time_point=time_point
        )

    def _harmonium_conditional_concordance_score(self, estimator, X, y=None):
        """
        Calculate concordance index, conditioning on other survival variables.
        """
        # Extract model from cross-validation estimator.
        if not isinstance(estimator, SurvivalHarmonium):
            estimator = estimator.best_estimator_
        # Compute score for first survival variable (indexed as the n_A'th
        # column after converting DataFrame to Numpy matrix)
        n_A = len(self.categorical_columns)
        time_point = {n_A: self.scoring_time_point_[0]}
        return estimator.concordance_index(
            X, conditional_probability=True, time_point=time_point
        )

    def _sksurv_concordance_score(self, model, X, y):
        """Scoring function specifically for sksurv estimators."""
        prediction = model.predict(X)
        result = concordance_index_censored(
            y[self.event_columns[0]], y[self.survival_columns[0]], prediction
        )
        return result[0]

    def _cox_concordance_score(self, estimator, X, y):
        """
        Concordance scoring for Cox model.
        """
        if not hasattr(estimator, "lifelines_model"):
            estimator = estimator.best_estimator_
        return estimator.score(X, y)

    def _sksurv_dataset(self):
        """
        Convert dataset to scikit-surv compatible feature-label pair.
        """
        if self.X.isnull().values.any():
            print("Warning: Dropping columns with missing data!")

        covariates = self.categorical_columns + self.numeric_columns
        X = self.X[covariates].dropna(axis=1)
        y = Surv.from_dataframe(
            event=self.event_columns[0], time=self.survival_columns[0], data=self.X
        )
        return X, y

    def double_cross_validate(
        self, model, X, y, param_distributions, metrics=None, pickle_location=None
    ) -> pd.Series:
        """
        Perform double cross validation, store result, and return scores.
        """
        selection_metric = "concordance"
        if "conditional_concordance" in metrics.keys():
            selection_metric = "conditional_concordance"

        s = double_cross_validate(
            model,
            X,
            y,
            param_distributions,
            m=self.m_x_n[0],
            n=self.m_x_n[1],
            scoring=metrics,
            refit=selection_metric,
            n_iter=self.n_iter,
            n_jobs=self.n_jobs,
            random_state=self.random_state,
        )
        if self.verbose:
            print("fit_time:", s["fit_time"])
            print("score_time:", s["score_time"])

        if pickle_location is not None:
            estimator_fold = []
            for fold_number, est in enumerate(s["estimator"]):
                model = getattr(est, "best_estimator_", None)
                params = getattr(est, "best_params_", None)
                score = getattr(est, "best_score_", None)
                estimator_fold.append(
                    {"estimator": model, "params": params, "score": score}
                )
                if self.verbose:
                    print(f"Fold {fold_number+1}")
                    print("Best params:")
                    pprint(params)
                    print("Best score:", score)
                    print("==" * 10)

            data = {
                "folds": estimator_fold,
                "m": self.m_x_n[0],
                "n": self.m_x_n[1],
                "n_iter": self.n_iter,
                "param_grid": param_distributions,
            }
            with open(pickle_location, mode="wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

        # Collect all test results.
        results = {}
        for key in s.keys():
            if key.startswith("test_"):
                metric_name = key[len("test_") :]
                results[metric_name] = s[key].mean()
                results[f"{metric_name}_std"] = s[key].std()
        return pd.Series(results)

    def _update_scores(self, new_scores: pd.Series, model_name: str):
        """
        Update and store current benchmark scoreboard.
        """
        # Expand the number of columns if needed.
        missing_columns = sorted(set(new_scores.index) - set(self.scores.columns))
        if missing_columns:
            self.scores = self.scores.join(
                pd.DataFrame(columns=missing_columns, index=self.scores.index)
            )

        self.scores.loc[model_name] = new_scores
        self.scores.to_csv(self.scores_file)

        if self.verbose:
            pprint(self.scores)

    def cox(self, hyper_params={}):
        """
        Double cross-validated concordance index of Cox model.
        """
        reset_random_state(self.random_state)

        if self.X.isnull().values.any():
            print("Warning: Dropping columns with missing data!")

        # The sklearn adapter requires the event indicator as covariate.
        covariates = (
            self.categorical_columns + self.numeric_columns + self.event_columns[:1]
        )
        X = self.X[covariates].dropna(axis=1)
        y = self.X[self.survival_columns[0]]

        # 1)
        # Do score scaling for the Cox model.
        CoxRegression = sklearn_adapter(CoxPHFitter, event_col=self.event_columns[0])
        cph = CoxRegression(step_size=0.01)
        cox_hyperparams = {
            "penalizer": loguniform(1e-5, 1e3),
            "l1_ratio": loguniform(1e-5, 1),
        }
        cox_hyperparams.update(hyper_params)

        # Temporarily set number of jobs to 1, to prevent lifelines from
        # crashing.
        n_jobs = self.n_jobs
        self.n_jobs = 1

        metrics = {
            "brier": self._cox_brier_score,
            "concordance": self._cox_concordance_score,
        }
        score = self.double_cross_validate(
            cph,
            X,
            y,
            param_distributions=cox_hyperparams,
            metrics=metrics,
            pickle_location=str(self.output_folder / "cox.pickle"),
        )
        # Restore number of jobs.
        self.n_jobs = n_jobs

        self._update_scores(score, model_name="cox")

    def support_vector_machine(self, hyper_params={}):
        """
        Double cross-validated concordance index of support vector machine.
        """
        reset_random_state(self.random_state)

        X, y = self._sksurv_dataset()
        svm = FastSurvivalSVM(
            max_iter=1000000, tol=1e-5, random_state=self.random_state
        )
        # Hyperparameters according to:
        # Pölsterl et al., In Joint European Conference on Machine Learning and
        # Knowledge Discovery in Databases, pp. 243-259. Springer, Cham, 2015.
        svm_hyperparams = {
            "alpha": loguniform(2e-12, 2e12),
            "rank_ratio": np.linspace(0.0, 1, 21),
        }
        svm_hyperparams.update(hyper_params)

        metrics = {"concordance": None}
        score = self.double_cross_validate(
            svm,
            X,
            y,
            param_distributions=svm_hyperparams,
            metrics=metrics,
            pickle_location=str(self.output_folder / "svm.pickle"),
        )

        self._update_scores(score, model_name="svm")

    def random_survival_forest(self, hyper_params={}):
        """
        Double cross-validated concordance index of random survival forest.
        """
        reset_random_state(self.random_state)

        X, y = self._sksurv_dataset()
        rsf = RandomSurvivalForest(
            random_state=self.random_state,
            # Restrict memory foot print to prevent crashes.
            max_depth=7,
        )
        rsf_hyperparams = {
            "n_estimators": 2 ** np.arange(0, 11, 1),
            "min_samples_split": 2 ** np.arange(1, 6, 1),
            "min_samples_leaf": 2 ** np.arange(0, 6, 1),
            "max_features": ["sqrt", "log2", None],
        }
        rsf_hyperparams.update(hyper_params)

        metrics = {
            "brier": self._random_forest_brier_score,
            "concordance": self._sksurv_concordance_score,
        }
        score = self.double_cross_validate(
            rsf,
            X,
            y,
            param_distributions=rsf_hyperparams,
            metrics=metrics,
            pickle_location=str(self.output_folder / "random_forest.pickle"),
        )
        self._update_scores(score, model_name="random_forest")

    def harmonium(self, harmonium_params={}, hyper_params={}):
        """
        Double cross-validated concordance index of harmonium.
        """
        reset_random_state(self.random_state)

        # Convert to numpy to reduce overhead.
        X = concatenate(
            (
                self.X[self.categorical_columns].to_numpy(),
                self.X[self.survival_columns].to_numpy(),
                self.X[self.numeric_columns].to_numpy(),
                self.X[self.event_columns].to_numpy(),
            ),
            axis=1,
        )
        X = ascontiguousarray(X, dtype=float64)
        n_A = len(self.categorical_columns)
        n_B = len(self.survival_columns)
        n_C = len(self.numeric_columns)

        # Model parameters to keep fixed.
        harm_params = {
            "categorical_columns": list(range(n_A)),
            "survival_columns": list(range(n_A, n_A + n_B)),
            "numeric_columns": list(range(n_A + n_B, n_A + n_B + n_C)),
            "event_columns": list(range(n_A + n_B + n_C, n_A + n_B + n_C + n_B)),
            "verbose": self.verbose,
            "log_every_n_iterations": None,
            "time_horizon": 2.0,
            "metrics": tuple(),
            "risk_score_time_point": self.scoring_time_point_,
            "maximum_iteration": -1,
            "guess_weights": False,
        }
        # Model parameters and respective distribution for hyperparameter
        # tuning.
        harm_hyperparams = {
            "learning_rate": loguniform(1e-5, 0.05),
            "n_epochs": loguniform(500, 1e5),
            "n_hidden_units": loguniform(1, 128),
            # "n_epochs": loguniform(1e1, 1e3),
            # "n_hidden_units": [1],
            "CD_steps": [1],
            "momentum_fraction": uniform(0, 0.9),
            "mini_batch_size": loguniform(25, 1000),
            "weight_decay": loguniform(1e-5, 0.1),
            "persistent": [True, False],
        }

        # Override parameters supplied to this function.
        harm_params.update(harmonium_params)
        harm_hyperparams.update(hyper_params)

        harmonium = SurvivalHarmonium(**harm_params)
        harmonium.fit(X)
        self._harmonium_concordance_score(harmonium, X)
        self._harmonium_brier_score(harmonium, X)

        metrics = {
            "concordance": self._harmonium_concordance_score,
            "brier": self._harmonium_brier_score,
        }
        if len(self.survival_columns) > 1:
            metrics[
                "conditional_concordance"
            ] = self._harmonium_conditional_concordance_score
            metrics["conditional_brier"] = lambda est, x: self._harmonium_brier_score(
                est, x, conditional_probability=True
            )

        score = self.double_cross_validate(
            harmonium,
            X,
            y=None,
            param_distributions=harm_hyperparams,
            metrics=metrics,
            pickle_location=str(self.output_folder / "harmonium.pickle"),
        )

        self._update_scores(score, model_name="harmonium")
