import os
from tempfile import mkstemp
from unittest import TestCase

import dill as pickle
import numpy as np
from numpy import (
    array,
    asfortranarray,
    concatenate,
    cumsum,
    e,
    exp,
    float32,
    float64,
    hstack,
    linspace,
    log,
    nan,
    ones,
    ones_like,
    pi,
    random,
    testing,
    zeros,
    zeros_like,
)
from numpy.random import uniform, randint, normal
import pandas as pd
from scipy.stats import cumfreq

from harmoniums import SurvivalHarmonium
from harmoniums.const import Matrix
from harmoniums.datasets import load_blobs
from harmoniums.distributions import (
    normalisation_gamma_interval_distribution,
    interval_truncated_gamma_distribution,
)
from harmoniums.test import TestHarmonium
from harmoniums.test.datasets import SuperImposedGamma
from harmoniums.utils import generate_binary_permutations, reset_random_state


class TestFunctionInput(TestCase):
    """
    Generic function tests of the survival harmonium.
    """

    def _generate_random_test_data(self, m: int = 10):
        """Generate categorical, survival, numeric and event samples."""
        X_cat = randint(low=0, high=2, size=(m, 2))
        X_surv = 2.0 * uniform(size=(m, 1))
        X_num = normal(size=(m, 3))
        event = randint(low=0, high=2, size=(m, 1)).astype(bool)
        return X_cat, X_surv, X_num, event

    def test_unpack_numpy(self):
        """
        Test unpacking of Numpy array into triplet and event matrix.
        """
        X_cat, X_surv, X_num, event = self._generate_random_test_data()
        X = concatenate((X_num, X_cat, event, X_surv), axis=1)
        model = SurvivalHarmonium(
            categorical_columns=[3, 4],
            survival_columns=[6],
            numeric_columns=[0, 1, 2],
            event_columns=[5],
        )
        xi, event = model._unpack(X, normalise=False, verify=False)
        np.testing.assert_array_equal(xi[0], X_cat)
        np.testing.assert_array_equal(xi[1], X_surv)
        np.testing.assert_array_equal(xi[2], X_num)
        np.testing.assert_array_equal(event, event)

    def test_compress_numpy(self):
        """
        Test that compressing is the inverse of unpacking.
        """
        X_cat, X_surv, X_num, event = self._generate_random_test_data()
        X = concatenate((X_num, X_cat, event, X_surv), axis=1)
        model = SurvivalHarmonium(
            categorical_columns=[3, 4],
            survival_columns=[6],
            numeric_columns=[0, 1, 2],
            event_columns=[5],
            dry_run=True,
        )
        model.fit(X)
        np.testing.assert_array_almost_equal(X, model._compress(*model._unpack(X)))

    def test_unpack_pandas_frame(self):
        """
        Test unpacking Pandas frame into triplet and event matrix.
        """
        X_cat, X_surv, X_num, event = self._generate_random_test_data()
        X = concatenate((X_num, X_cat, event, X_surv), axis=1)
        data_frame = pd.DataFrame(
            X, columns=["c1", "c2", "c3", "cat1", "cat2", "event", "t"]
        )
        model = SurvivalHarmonium(
            categorical_columns=["cat1", "cat2"],
            survival_columns=["t"],
            numeric_columns=["c1", "c2", "c3"],
            event_columns=["event"],
        )
        xi, event = model._unpack(data_frame, normalise=False, verify=False)
        np.testing.assert_array_equal(xi[0], X_cat)
        np.testing.assert_array_equal(xi[1], X_surv)
        np.testing.assert_array_equal(xi[2], X_num)
        np.testing.assert_array_equal(event, event)

    def test_compress_pandas_frame(self):
        """
        Test compressing triplet and event matrix into Pandas frame.
        """
        X_cat, X_surv, X_num, event = self._generate_random_test_data()
        X = concatenate((X_num, X_cat, event, X_surv), axis=1)
        data_frame = pd.DataFrame(
            X, columns=["c1", "c2", "c3", "cat1", "cat2", "event", "t"]
        )
        data_frame["event"] = data_frame["event"].astype(bool)

        model = SurvivalHarmonium(
            categorical_columns=["cat1", "cat2"],
            survival_columns=["t"],
            numeric_columns=["c1", "c2", "c3"],
            event_columns=["event"],
            dry_run=True,
        )

        model.fit(data_frame)
        # The data frames are not equal, because the order of the columns is not
        # guaranteed. Check instead for each type of variables.
        df_reconstr = model._compress(*model._unpack(data_frame))
        pd.testing.assert_frame_equal(
            data_frame[["cat1", "cat2"]], df_reconstr[["cat1", "cat2"]]
        )
        pd.testing.assert_frame_equal(data_frame[["t"]], df_reconstr[["t"]])
        pd.testing.assert_frame_equal(
            data_frame[["c1", "c2", "c3"]], df_reconstr[["c1", "c2", "c3"]]
        )
        pd.testing.assert_frame_equal(data_frame[["event"]], df_reconstr[["event"]])

    def test_normalise(self):
        """
        Test that the normalise function modifies the data inplace.
        """
        # Test for NumPy array.
        X = random.random([3, 3]) * 2
        m1 = SurvivalHarmonium(survival_columns=[1], dry_run=True)
        m1.fit(X)
        with self.assertRaises(AssertionError):
            np.testing.assert_array_equal(m1._normalise(X.copy()), X)

        # And Pandas dataframe.
        data_frame = pd.DataFrame(random.random([3, 3]) * 2, columns=["a", "b", "c"])
        m2 = SurvivalHarmonium(survival_columns=["b"], dry_run=True)
        m2.fit(data_frame)
        with self.assertRaises(AssertionError):
            pd.testing.assert_frame_equal(m2._normalise(data_frame.copy()), data_frame)

    def test_energy_factor_gamma(self):
        """
        Test exp[-E_B(x,h)] for various edge case input data.
        """
        model = SurvivalHarmonium(
            n_event_units=2, n_categorical_units=0, n_hidden_units=1, n_numeric_units=0
        )
        model.initialise_parameters()

        # Test the calculation on the boundaries.
        X = array([[0.0, 1.0]])
        H = array([[1.0]])

        # Raise error whenever infinite arises or illegitimate division arises.
        with np.errstate(all="raise"):
            # 1) Everything observed.
            factor = model.energy_factor_gamma(X, H, mask=ones_like(X, dtype=bool))
            # The factor x^a exp(-bx) with x=0 is zero.
            np.testing.assert_equal(factor[0], 0.0)

            # 2) Everything censored.
            factor = model.energy_factor_gamma(X, H, mask=zeros_like(X, dtype=bool))
            # The factor integral_1^1 dxp exp(-bx)x^a has measure zero, should
            # therefore be zero.
            np.testing.assert_equal(factor[0], 0.0)

    def test_fortran_order(self):
        """
        Test Fortran ordered arrays produce exceptions.
        """
        x_a = array([1.0, 0.0])
        x_b = array([0.25, 0.5])
        x_c = array([-0.1, -0.2])
        observe_mask = array([1, 1], dtype=bool)
        X = hstack([x_a, x_b, x_c, observe_mask]).reshape(1, -1)
        model = SurvivalHarmonium(
            categorical_columns=[0, 1],
            survival_columns=[2, 3],
            numeric_columns=[4, 5],
            event_columns=[6, 7],
            n_hidden_units=3,
            dry_run=True,
        ).fit(X)
        model.W_A = asfortranarray(model.W_A)

        # Verify that Fortan order memory layout raises exception.
        with self.assertRaises(TypeError):
            model._partition_function_i(
                tuple(), x_a, x_b, x_c, observe_mask, observe_mask, observe_mask
            )

        with self.assertRaises(TypeError):
            model._lambda_partition_function_i(
                tuple(), x_a, x_b, x_c, observe_mask, observe_mask, observe_mask
            )

    def test_array_dtype(self):
        """
        Test that the arrays have the right dtype.
        """
        model = SurvivalHarmonium(
            categorical_columns=[0, 1],
            survival_columns=[2, 3],
            numeric_columns=[4, 5],
            event_columns=[6, 7],
            n_hidden_units=3,
            dry_run=True,
        )

        for x_dtype, mask_dtype in [(float64, int), (float32, bool)]:
            with self.subTest():
                kwargs = {"dtype": x_dtype}
                x_a = array([1, 0], **kwargs)
                x_b = array([0.25, 0.5], **kwargs)
                x_c = array([-0.1, -0.2], **kwargs)
                observe_mask = array([1, 1], dtype=mask_dtype)
                X = hstack([x_a, x_b, x_c, observe_mask]).reshape(1, -1)
                model = model.fit(X)

                # Verify that the wrong dtype raises an exception.
                with self.assertRaises(TypeError):
                    model.W_A = asfortranarray(model.W_A)
                    model._partition_function_i(
                        tuple(), x_a, x_b, x_c, observe_mask, observe_mask, observe_mask
                    )

                with self.assertRaises(TypeError):
                    model._lambda_partition_function_i(
                        tuple(), x_a, x_b, x_c, observe_mask, observe_mask, observe_mask
                    )

    def test_check_X(self):
        """
        Test that incorrect input is correctly identified.
        """
        X_censor = load_blobs(censor=True).to_numpy()

        # Assume that we have made a mistake, where we accidentally point an
        # event column to survival variable.
        with self.assertRaises(ValueError):
            SurvivalHarmonium(
                categorical_columns=[0],
                survival_columns=[1, 2],
                event_columns=[2, 3],
                time_horizon=[1.0, 1.0],
                dry_run=True,
            ).fit(X_censor)

        # Similarly, we identically point survival column outside of unit
        # interval to categorical variable.
        with self.assertRaises(ValueError):
            X_censor[:, (1, 2)] = X_censor[:, (1, 2)] * 2
            SurvivalHarmonium(
                categorical_columns=[1],
                survival_columns=[1, 2],
                event_columns=[3, 4],
                time_horizon=[2.0, 2.0],
                dry_run=True,
            ).fit(X_censor)

    def test_numerical_stability_log_likelihood(self):
        """
        Test that log likelihood is numerically stable for large weights.
        """
        X_censor = load_blobs(censor=True).to_numpy()
        harmonium = SurvivalHarmonium(
            categorical_columns=[0],
            survival_columns=[1, 2],
            event_columns=[3, 4],
            n_hidden_units=4,
            time_horizon=[1.0, 1.0],
            dry_run=True,
        ).fit(X_censor)
        harmonium.c = zeros_like(harmonium.c)
        harmonium.a_A = zeros_like(harmonium.a_A)
        harmonium.a_B = zeros_like(harmonium.a_B)
        harmonium.W_B = array(
            [
                [53.72281323, 151.32168761, 53.72281323, 151.32168761],
                [53.72281323, 53.72281323, 151.32168761, 151.32168761],
            ]
        )
        harmonium.V = array(
            [
                [13.43070331, 113.49126571, 13.43070331, 113.49126571],
                [13.43070331, 13.43070331, 113.49126571, 113.49126571],
            ]
        )
        harmonium.W_A = array([5000.0, -5000.0, -5000.0, 5000.0]).reshape(1, -1)
        harmonium.b = array(
            [-74.09922314, 4811.8097202, 4811.8097202, -302.28133647]
        ).reshape(-1, 1)
        ll = harmonium.log_likelihood(array([[1.0, 0.22850372, 0.75, 1.0, 0.0]]))
        self.assertTrue(all(np.isfinite(ll)))


class TestLogEnergyFactor(TestCase):
    """
    Test that log implementation is equivalent to original function.
    """

    def setUp(self):
        """Basic initialisation of model and data."""
        reset_random_state(1234)

        X, _ = SuperImposedGamma().load(m=8)
        # Add extra categorical and numeric variable, to help check dimensional
        # consistency.
        X.drop(columns="index", inplace=True)
        X["category_2"] = 1 - X["category"]
        X["numeric_2"] = 1 - X["numeric"]

        self.X = X[
            [
                "category",
                "category_2",
                "numeric",
                "numeric_2",
                "t_0",
                "t_1",
                "event_0",
                "event_1",
            ]
        ].to_numpy(dtype=float64)
        self.harmonium = SurvivalHarmonium(
            categorical_columns=[0, 1],
            survival_columns=[4, 5],
            numeric_columns=[2, 3],
            event_columns=[6, 7],
            n_hidden_units=3,
            time_horizon=[1.0, 1.0],
            dry_run=True,
        ).fit(self.X)

        # Generate the same number H states as there are X states.
        self.H = generate_binary_permutations(3)

    def test_binary(self):
        """
        Test for categorical variables.
        """
        X_A = self.X[:, :2]
        # Let remove some values.
        mask_A = array([[0, 1] * 4, [0] * 4 + [1] * 4], dtype=np.bool_).T

        # Check equivalence.
        log_p = self.harmonium.log_energy_factor_binary(X_A, self.H, mask_A)
        p = self.harmonium.energy_factor_binary(X_A, self.H, mask_A)
        testing.assert_array_almost_equal(exp(log_p), p)

    def test_numeric(self):
        """
        Test for numeric variables.
        """
        X_C = self.X[:, 2:4]
        # Let remove some values.
        mask_C = array([[0, 1] * 4, [0] * 4 + [1] * 4], dtype=np.bool_).T

        # Check equivalence.
        log_p = self.harmonium.log_energy_factor_gauss(X_C, self.H, mask_C)
        p = self.harmonium.energy_factor_gauss(X_C, self.H, mask_C)
        testing.assert_array_almost_equal(exp(log_p), p)

    def test_event(self):
        """
        Test for time-to-event variables.
        """
        X_B = self.X[:, 4:6]
        mask_B = self.X[:, 6:].astype(np.bool_)

        # Check equivalence.
        log_p = self.harmonium.log_energy_factor_gamma(X_B, self.H, mask_B)
        p = self.harmonium.energy_factor_gamma(X_B, self.H, mask_B)
        testing.assert_array_almost_equal(exp(log_p), p)


class TestSuperimposedgamma(TestHarmonium):
    """
    Try to deconvolute two superimposed truncated gamma distributions.
    """

    def setUp(self):
        """
        Generate data for the mixed model.
        """
        super().setUp()
        self.verbose = bool(os.environ.get("VERBOSE", False))
        self.default_parameters = {
            "survival_columns": ["t_0", "t_1"],
            "event_columns": ["event_0", "event_1"],
            "n_hidden_units": 1,
            "verbose": self.verbose,
            "time_horizon": None,
            "metrics": tuple(),
            "log_every_n_iterations": None,
            # But for debugging purposes one might try:
            # "log_every_n_iterations": 20,
            # "metrics": ("log_likelihood", "score"),
        }

        # Distribution composed of two superimposed truncated gamma distributions.
        self.dataset = SuperImposedGamma()
        self.X, y = self.dataset.load()
        self.X["group"] = y.values

    def assert_more_likely(self, p_greater: Matrix, p_less: Matrix):
        """
        Assert that <ln p_greater> is greater than ln <p_less> for all elements.
        """
        ll_greater = log(p_greater).mean(axis=0)
        ll_less = log(p_less).mean(axis=0)
        try:
            self.assertTrue(np.all(ll_greater > ll_less))
        except AssertionError as e:
            e.args = (f"Not all elements larger:\n{ll_greater}\n >\n{ll_less}",)
            raise e


class TestCategoricalLever(TestSuperimposedgamma, TestCase):
    """
    Toy data in which a categorical variable activates a specific survival distribution.
    """

    def setUp(self):
        """
        Generate data for the mixed model.
        """
        super().setUp()

        model_parameters = self.default_parameters
        model_parameters.update(
            {
                "learning_rate": 0.125,
                "mini_batch_size": 100,
                "n_epochs": 100,
                "weight_decay": 5e-4,
                "momentum_fraction": 0.1,
            }
        )
        self.model_no_switch = SurvivalHarmonium(**model_parameters)
        self.model_switch = SurvivalHarmonium(
            categorical_columns=["group"], **model_parameters
        )
        random.seed(1234)
        self.model_no_switch.fit(self.X)
        random.seed(1234)
        self.model_switch.fit(self.X)

    def test_predict_joint_proba(self):
        """
        Test that discrimination is more likely E[ln p(x_B|X_C)] > E[ln p(X_B)].
        """
        for group_number in [0, 1]:
            with self.subTest(group=group_number):
                X = self.dataset.load_group(group_number)
                X["group"] = group_number
                self.assert_more_likely(
                    self.model_switch.predict_joint_proba(X),
                    self.model_no_switch.predict_joint_proba(X),
                )

    def test_score(self):
        """
        Test that discrimination gives better scores.
        """
        np.testing.assert_array_less(
            self.model_no_switch.score(self.X),
            self.model_switch.score(self.X),
        )

    def test_latent_group_identification(self):
        """
        Test latent group identification, and the improvement by the categorical switch.
        """
        X1 = self.dataset.load_group(0)
        X1["group"] = 0
        H1_yes = self.model_switch.transform(X1)
        H1_no = self.model_no_switch.transform(X1)

        X2 = self.dataset.load_group(1)
        X2["group"] = 1
        H2_yes = self.model_switch.transform(X2)
        H2_no = self.model_no_switch.transform(X2)

        dh_switch = abs(H2_yes - H1_yes).mean()
        dh_no_switch = abs(H2_no - H1_no).mean()

        if self.verbose:
            print("class distinction with categorical switch", dh_switch)
            print("class distinction no categorical switch", dh_no_switch)

        self.assertGreater(dh_switch - dh_no_switch, 0.2)


class TestNumericLever(TestSuperimposedgamma, TestCase):
    """
    Toy data in which a numerical variable activates a specific survival distribution.
    """

    def setUp(self):
        """
        Generate data for the mixed model.
        """
        super().setUp()

        model_parameters = self.default_parameters
        model_parameters.update(
            {
                "learning_rate": 0.1,
                "mini_batch_size": 500,
                "n_epochs": 200,
                "weight_decay": 1e-4,
                "momentum_fraction": 0.1,
                "log_every_n_iterations": 10,
                # "verbose": True,
                # "metrics": ("log_likelihood", "score",),
                # "dry_run": True,
            }
        )

        # Group g=1 is activated by a Gaussian switch: located at x=0 (group g=0) and
        # x=`gauss_distance` (group g=1).
        self.X["switch"] = self.as_gauss(self.X["group"])

        self.model_no_switch = SurvivalHarmonium(**model_parameters)
        self.model_switch = SurvivalHarmonium(
            numeric_columns=["switch"], **model_parameters
        )
        random.seed(1234)
        self.model_no_switch.fit(self.X)
        random.seed(1234)
        self.model_switch.fit(self.X)

    def as_gauss(self, group: np.ndarray):
        """
        Turn categorical group into Gaussian lever.
        """
        gauss_distance = 2.0
        return random.normal(loc=gauss_distance * group)

    def test_score(self):
        """
        Test that discrimination gives better scores.
        """
        np.testing.assert_array_less(
            self.model_no_switch.score(self.X),
            self.model_switch.score(self.X),
        )

    def test_latent_group_identification(self):
        """
        Test latent group identification, and the improvement by the numerical switch.
        """
        X1 = self.dataset.load_group(0)
        X1["switch"] = self.as_gauss(zeros((X1.shape[0], 1)))
        H1_yes = self.model_switch.transform(X1)
        H1_no = self.model_no_switch.transform(X1)

        X2 = self.dataset.load_group(1)
        X2["switch"] = self.as_gauss(ones((X2.shape[0], 1)))
        H2_yes = self.model_switch.transform(X2)
        H2_no = self.model_no_switch.transform(X2)

        dh_switch = abs(H2_yes - H1_yes).mean()
        dh_no_switch = abs(H2_no - H1_no).mean()

        if self.verbose:
            print("class distinction with gauss switch", dh_switch)
            print("class distinction no gauss switch", dh_no_switch)

        self.assertGreater(dh_switch - dh_no_switch, 0.2)

    def test_predict_joint_proba(self):
        """
        Test that discrimination is more likely E[ln p(x_B|X_C)] > E[ln p(X_B)].

        Where x_B are all time-to-event variables combined.
        """
        for group_number in [0, 1]:
            with self.subTest(group=group_number):
                X = self.dataset.load_group(group_number)
                # Make Gaussian switch with shifted mean.
                X["switch"] = self.as_gauss(group_number * ones((X.shape[0], 1)))
                self.assert_more_likely(
                    # Infer p(x_B|x_C)
                    self.model_switch.predict_joint_proba(X),
                    # Infer p(x_B|x_C) = p(x_B) in absence of x_C.
                    self.model_no_switch.predict_joint_proba(X),
                )

    def test_proba_singletons(self):
        """
        Test single event-variable discrimination p(t1| t2,x) > p(t1|t2).
        """
        for group_number in [0, 1]:
            with self.subTest(group=group_number):
                X = self.dataset.load_group(group_number)
                # Make Gaussian switch with shifted mean.
                X["switch"] = self.as_gauss(group_number * ones((X.shape[0], 1)))

                p_no_switch = self.model_no_switch._proba_singletons(
                    X,
                    survival_distribution=False,
                )
                p_switch = self.model_switch._proba_singletons(
                    X,
                    survival_distribution=False,
                )

                # Check that conditioning makes the data more likely, for each
                # time-to-event variable in x_B.
                self.assert_more_likely(p_switch, p_no_switch)


class TestDoubleLever(TestSuperimposedgamma, TestCase):
    """
    Toy data with group 2 activated when both the categorical and gauss switch are on.

    This data is in fact already in the toy dataset `test.datasets`.
    """

    def setUp(self):
        """
        Generate data for the mixed model.
        """
        super().setUp()

        model_parameters = self.default_parameters
        model_parameters.update(
            {
                "learning_rate": 0.5,
                "mini_batch_size": 500,
                "n_epochs": 1000,
                "weight_decay": 1e-4,
                "momentum_fraction": 0.1,
            }
        )
        self.model_no_switch = SurvivalHarmonium(**model_parameters)
        self.model_switch = SurvivalHarmonium(
            categorical_columns=["category"],
            numeric_columns=["numeric"],
            **model_parameters,
        )
        random.seed(1234)
        self.model_no_switch.fit(self.X)
        random.seed(1234)
        self.model_switch.fit(self.X)

    def test_latent_group_identification(self):
        """
        Test latent group identification is improved using the extra variables.
        """
        X1 = self.dataset.load_group(0)
        H1_yes = self.model_switch.transform(X1)
        H1_no = self.model_no_switch.transform(X1)

        X2 = self.dataset.load_group(1)
        H2_yes = self.model_switch.transform(X2)
        H2_no = self.model_no_switch.transform(X2)

        dh_switch = abs(H2_yes - H1_yes).mean()
        dh_no_switch = abs(H2_no - H1_no).mean()

        if self.verbose:
            print("class distinction with pair switch", dh_switch)
            print("class distinction no switch", dh_no_switch)

        # This test turns out to be a little more difficult, finding correlated
        # switches.
        self.assertGreater(dh_switch - dh_no_switch, 0.1)

    def test_predict_joint_proba(self):
        """
        Test that discrimination is more likely E[ln p(x_B|X_C)] > E[ln p(X_B)].

        Where x_B are all time-to-event variables combined.
        """
        for group_number in [0, 1]:
            with self.subTest(group=group_number):
                X = self.dataset.load_group(group_number)
                self.assert_more_likely(
                    self.model_switch.predict_joint_proba(X),
                    self.model_no_switch.predict_joint_proba(X),
                )

    def test_pickable(self):
        """Test that the model can be pickled to file."""
        _, pickle_location = mkstemp()
        with open(pickle_location, mode="wb") as f:
            pickle.dump(self.model_switch, f, protocol=pickle.HIGHEST_PROTOCOL)

    def test_score(self):
        """
        Test that discrimination gives better scores.
        """
        np.testing.assert_array_less(
            self.model_no_switch.score(self.X),
            self.model_switch.score(self.X),
        )


class TestHiddenStatePartitionFunction(TestHarmonium, TestCase):
    """
    Test equivalence of partition function computation.
    """

    def setUp(self):
        super().setUp()
        self.X, _ = SuperImposedGamma().load(m=10)

    def test_survival_only(self):
        """
        Test computation with only survival variables, some values are censored.
        """
        model = SurvivalHarmonium(
            survival_columns=["t_0", "t_1"],
            event_columns=["event_0", "event_1"],
            time_horizon=[1.0, 1.0],
            n_hidden_units=3,
            dry_run=True,
        )
        model.fit(self.X)
        xi, event = model._unpack(self.X[1:3])

        Z_sum = model._hidden_state_partition_function_sum(xi, event)
        Z_int = model._hidden_state_partition_function_integral(xi, event)
        np.testing.assert_array_almost_equal(Z_sum, Z_int)

    def test_numeric_only(self):
        """
        Test computation with only numeric variables, some are missing.
        """
        model = SurvivalHarmonium(
            numeric_columns=["numeric"],
            n_hidden_units=3,
            dry_run=True,
        )
        model.fit(self.X)

        # Corrupt some numeric values.
        censors = randint(0, 2, size=self.X.shape[0]).astype(bool)
        self.X.loc[censors, "numeric"] = nan

        xi, event = model._unpack(self.X)
        Z_sum = model._hidden_state_partition_function_sum(xi, event)
        Z_int = model._hidden_state_partition_function_integral(xi, event)
        np.testing.assert_array_almost_equal(Z_sum, Z_int)

    def test_categoric_only(self):
        """
        Test computation with only numeric variables, some censored.
        """
        model = SurvivalHarmonium(
            categorical_columns=["category"],
            n_hidden_units=3,
            dry_run=True,
        )
        model.fit(self.X)

        # Corrupt some categories.
        censors = randint(0, 2, size=self.X.shape[0]).astype(bool)
        self.X.loc[censors, "category"] = nan

        xi, event = model._unpack(self.X)
        Z_sum = model._hidden_state_partition_function_sum(xi, event)
        Z_int = model._hidden_state_partition_function_integral(xi, event)
        np.testing.assert_array_almost_equal(Z_sum, Z_int)

    def test_all_features(self):
        """
        Test computation with all features, where some are censored.
        """
        model = SurvivalHarmonium(
            survival_columns=["t_0", "t_1"],
            event_columns=["event_0", "event_1"],
            numeric_columns=["numeric"],
            categorical_columns=["category"],
            time_horizon=[1.0, 1.0],
            n_hidden_units=3,
            dry_run=True,
        )
        model.fit(self.X)

        # Corrupt some categories.
        censors = randint(0, 2, size=[self.X.shape[0], 2]).astype(bool)
        self.X.loc[censors[:, 0], "numeric"] = nan
        self.X.loc[censors[:, 1], "category"] = nan

        xi, event = model._unpack(self.X)

        Z_int = model._hidden_state_partition_function_integral(xi, event)
        Z_sum = model._hidden_state_partition_function_sum(xi, event)
        np.testing.assert_array_almost_equal(Z_sum, Z_int)

    def test_no_inplace_assignment(self):
        """
        Test that no inplace assignment occurs during computation.
        """
        model = SurvivalHarmonium(
            survival_columns=["t_0", "t_1"],
            event_columns=["event_0", "event_1"],
            numeric_columns=["numeric"],
            categorical_columns=["category"],
            time_horizon=[1.0, 1.0],
            n_hidden_units=3,
            dry_run=True,
        )
        model.fit(self.X)

        # Corrupt some categories.
        censors = randint(0, 2, size=[self.X.shape[0], 2]).astype(bool)
        self.X.loc[censors[:, 0], "numeric"] = nan
        self.X.loc[censors[:, 1], "category"] = nan

        # When any of the function calls alters `X`, then the values no longer
        # coincide.
        xi, event = model._unpack(self.X)
        Z_int1 = model._hidden_state_partition_function_integral(xi, event)
        Z_sum = model._hidden_state_partition_function_sum(xi, event)
        Z_int2 = model._hidden_state_partition_function_integral(xi, event)
        np.testing.assert_array_almost_equal(Z_sum, Z_int1)
        np.testing.assert_array_almost_equal(Z_sum, Z_int2)


class TestGibbsSamplers(TestHarmonium, TestCase):
    """
    Test that Gibbs samplers generate samples from correct distribution.

    This test case only considers time-to-event variables (no numeric or
    categoric variables).
    """

    def setUp(self):
        """
        Set specific parameters that make it analytically tracable.
        """
        super().setUp()

        # Our model: p_1 * p_2 + p'_1 * p'_2,
        # where the parameters for the first term are:
        self.alpha = array([1, 2]).reshape(-1, 1)
        self.beta = array([(e ** 2), e ** (-2)]).reshape(-1, 1)

        # And for the second term, we define:
        # \alpha'= \alpha + \Delta \alpha;
        # (Note that \Delta \alpha must be positive because of |V|).
        delta_alpha = array([0.75 * pi, 0.1]).reshape(-1, 1)
        self.alpha_prime = self.alpha + delta_alpha
        # \beta' = \beta + \Delta \beta.
        delta_beta = array([-(e ** 2), 1]).reshape(-1, 1)
        self.beta_prime = self.beta + delta_beta

        # Set parameters of the model to match the alpha and beta above.
        n_h = 1
        self.harmonium = SurvivalHarmonium(
            survival_columns=[0, 1],
            event_columns=[2, 3],
            n_event_units=2,
            n_hidden_units=n_h,
        )
        self.harmonium.initialise_parameters()
        self.harmonium.c = self.alpha - 1
        self.harmonium.a_B = self.beta
        self.harmonium.V = delta_alpha
        self.harmonium.W_B = delta_beta
        self.harmonium.b = array([[0]])

        self.harmonium.is_parameters_initialised_ = True

        # Verify that the settings were correctly set.
        H = array([[0], [1]])
        a, b = self.harmonium.alpha_beta(H)
        testing.assert_array_equal(a[0], self.alpha.flatten())
        testing.assert_array_equal(a[1], self.alpha_prime.flatten())
        testing.assert_array_equal(b[0], self.beta.flatten())
        testing.assert_array_equal(b[1], self.beta_prime.flatten())

    def _target_distribution(self, T: np.ndarray, t_left=None) -> np.ndarray:
        """
        Probability distribution corresponding to harmonium parameters.
        """
        if t_left is None:
            t_left = zeros_like(self.alpha)

        Z_1 = normalisation_gamma_interval_distribution(
            self.alpha,
            self.beta,
            t_left=t_left,
        ).prod()
        Z_2 = normalisation_gamma_interval_distribution(
            self.alpha_prime,
            self.beta_prime,
            t_left=t_left,
        ).prod()

        f1 = Z_1 / (Z_1 + Z_2)
        f2 = Z_2 / (Z_1 + Z_2)
        X = (
            f1
            * interval_truncated_gamma_distribution(
                T.T,
                self.alpha,
                self.beta,
                t_left=t_left,
            ).T
            + f2
            * interval_truncated_gamma_distribution(
                T.T,
                self.alpha_prime,
                self.beta_prime,
                t_left=t_left,
            ).T
        )
        return X

    def _target_cumulative_distribution(self, T: np.ndarray, t_left=None) -> np.ndarray:
        """
        Cumulative distribution corresponding to harmonium parameters.
        """
        P = self._target_distribution(T, t_left)
        C = cumsum(P, axis=0)
        return C / C[-1]

    def _to_cumulative_distribution(self, xi):
        """
        Calculate cumulative distribution of samples `xi`.
        """
        cum_xi0 = cumfreq(xi[:, 0], numbins=101, defaultreallimits=(0, 1))
        cum_xi1 = cumfreq(xi[:, 1], numbins=101, defaultreallimits=(0, 1))

        # Calculate bin positions.
        t0 = linspace(
            0, cum_xi0.binsize * cum_xi0.cumcount.size, cum_xi0.cumcount.size
        ).reshape(-1, 1)
        t1 = linspace(
            0, cum_xi1.binsize * cum_xi1.cumcount.size, cum_xi1.cumcount.size
        ).reshape(-1, 1)
        T = concatenate([t0, t1], axis=1)

        # Normalise counts to distirbution.
        C0 = cum_xi0.cumcount / cum_xi0.cumcount[-1]
        C1 = cum_xi1.cumcount / cum_xi1.cumcount[-1]
        C = concatenate([C0.reshape(-1, 1), C1.reshape(-1, 1)], axis=1)

        return T, C

    def test_gibbs_sleep(self):
        """
        Test samples Gibbs sleep update function with actual distribution.
        """
        # Gibbs samples, by definition, do not depend on the initial state. So
        # this value is as good as any.
        x = zeros(shape=(2000, 2))
        empty_array = array([])

        # Burn in for 50 iterations.
        for _ in range(50):
            (_, x, _) = self.harmonium.gibbs_sleep_update((empty_array, x, empty_array))

        T_data, C_data = self._to_cumulative_distribution(x)
        C_target = self._target_cumulative_distribution(T_data)

        # Maximal errors between cumulative distributions must not exceed 0.03.
        self.assertLess(abs(C_target - C_data).max(), 0.03)

    def test_gibbs_wake_as_sleep(self):
        """
        Test reduction of Gibbs wake update function to sleep function.

        In the special case when all observations are censored at t=0, we
        recover the Gibbs wake sampling function.
        """
        # Gibbs samples, by definition, do not depend on the initial state. So
        # this value is as good as any.
        x = zeros(shape=(2000, 2))
        empty_array = array([])
        empty_bool = empty_array.astype(bool)

        # Observations are censored at t=0.
        xi = (empty_array, ones_like(x) * array([0.0, 0.0]), empty_array)
        event = (empty_bool, zeros_like(xi[1]).astype(bool), empty_bool)

        # Burn in for 50 iterations.
        for _ in range(50):
            (_, x, _) = self.harmonium.gibbs_wake_update(
                (empty_array, x, empty_array), observation=(xi, event)
            )

        T_data, C_data = self._to_cumulative_distribution(x)
        C_target = self._target_cumulative_distribution(T_data)

        # Maximal errors between cumulative distributions must not exceed 0.03.
        self.assertLess(abs(C_target - C_data).max(), 0.03)

    def test_gibbs_wake(self):
        """
        Test Gibbs wake samples with interval truncated gamma distribution.
        """
        # Gibbs samples, by definition, do not depend on the initial state. So
        # this value is as good as any.

        x = zeros(shape=(2000, 2))
        empty_array = array([])
        empty_bool = empty_array.astype(bool)

        # Observations are censored at t=0.1 and 0.2.
        t_censor = array([0.15, 0.3]).reshape(-1, 1)
        xi = (empty_array, ones_like(x) * t_censor.T, empty_array)
        event = (
            empty_bool,
            zeros_like(xi[1]).astype(bool),
            empty_bool,
        )

        # Burn in for 60 iterations.
        for _ in range(60):
            (_, x, _) = self.harmonium.gibbs_wake_update(
                (empty_array, x, empty_array), observation=(xi, event)
            )

        T_data, C_data = self._to_cumulative_distribution(x)
        C_target = self._target_cumulative_distribution(T_data, t_left=t_censor)

        # Maximal errors between cumulative distributions must not exceed 0.03.
        self.assertLess(abs(C_target - C_data).max(), 0.03)
