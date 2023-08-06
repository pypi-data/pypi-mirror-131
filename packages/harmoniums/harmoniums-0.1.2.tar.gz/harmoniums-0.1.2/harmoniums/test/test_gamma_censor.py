from tempfile import mkdtemp
from unittest import TestCase

import numpy as np
from numpy import array, concatenate, copy, log, ones_like, zeros_like
import pandas as pd
from sklearn.metrics import accuracy_score

from harmoniums import CensorGammaHarmonium, GammaHarmonium
from harmoniums.distributions import (
    truncated_gamma_cumulative_distribution,
    truncated_gamma_distribution,
)
from harmoniums.samplers import sample_right_truncated_gamma_distribution
from harmoniums.test import TestHarmonium
from harmoniums.test.datasets import SuperImposedGamma


class TestObservedGammaHarmonium(TestHarmonium, TestCase):
    """
    Verify that `CensorGammaHarmonium` reduces to `GammaHarmonium` without censoring.

    This is the case for, e.g., the cost function (i.e., the `log_likelihood`) as well
    as the free energy F(x).
    """

    def copy_parameters(self, from_model, to_model):
        """
        Copy training parameters from `from_model` to `to_model`.
        """
        for param_name in from_model.parameters:
            parameter = getattr(from_model, param_name)
            setattr(to_model, param_name, copy(parameter))

    def setUp(self):
        """
        Init the censor model and the non-censor model.
        """
        self.random_state = 1234
        np.random.seed(self.random_state)

        xi = array([[0.5, 0.2, 0.9], [0.3, 0.8, 0.1]])
        event = ones_like(xi)
        self.X = concatenate([xi, event], axis=1)
        # All events are observed.
        n_visible = xi.shape[1]
        column_indices = list(range(n_visible))  # [0,..,n_v-1]
        model_parameters = {
            "visible_columns": column_indices,
            "n_visible_units": n_visible,
            "n_hidden_units": 3,
            "dry_run": True,
            "output": mkdtemp(),
        }
        self.model_plain = GammaHarmonium(**model_parameters)
        self.model_censor = CensorGammaHarmonium(
            event_columns=list(range(n_visible, n_visible * 2)),  # [n_v,..,2n_v - 1].
            **model_parameters,
        )

        self.model_plain.fit(self.X)
        self.model_censor.fit(self.X)
        # Make sure that the model parameters are identical.
        self.copy_parameters(from_model=self.model_plain, to_model=self.model_censor)

    def test_free_energy_x(self):
        """
        Test that the free energies F(x) for both models are the same without censoring.
        """
        F_no_censor = self.model_censor.modified_free_energy_x(self.X)
        F_reference = self.model_plain.free_energy_x(self.X)
        np.testing.assert_array_almost_equal(F_no_censor, F_reference)

    def test_log_likelihood(self):
        """
        Test that the log likelihood for both models are the same without censoring.
        """
        ll_no_censor = self.model_censor.log_likelihood(self.X)
        ll_reference = self.model_plain.log_likelihood(self.X)
        np.testing.assert_array_almost_equal(ll_no_censor, ll_reference)


class TestLikelihoodCensoredHarmonium(TestHarmonium, TestCase):
    """
    Test the log likelihood when some events are censored.

    Check for the limiting case when either h=1 or h=0 is the dominant term. That is,
    when the latent variable becomes superfluous. The likelihood is then simply a
    product of the survival functions of the truncated gamma distribution.
    """

    def setUp(self):
        """
        Initialise model for a small dataset.
        """
        self.random_state = 1234
        np.random.seed(self.random_state)

        # Time-to-event data.
        n_visible = 2

        self.model = CensorGammaHarmonium(
            n_visible_units=n_visible,
            visible_columns=list(range(n_visible)),
            event_columns=list(range(n_visible, 2 * n_visible)),
            n_hidden_units=1,
            dry_run=True,
            log_every_n_iterations=None,
        )

    def test_likelihood_all_censored(self):
        """
        Test the log likelihood when all events are censored.
        """
        xi = array([[0.5, 0.2], [0.3, 0.8]])
        event = zeros_like(xi)
        X = concatenate([xi, event], axis=1)
        self.model.fit(X)

        for b in [-1, 1]:
            with self.subTest(f"Model where h={(1-b)/2} term is dominant.", b=b * 100):
                # Large negative (positive) bias to ensure that h=1 (h=0) always.
                self.model.b = 100 * b * ones_like(self.model.b)
                H = self.model.transform(X)
                # Verify that this is the case.
                np.testing.assert_array_almost_equal(H, (1 - b) / 2)

                # Paramters for reference distributions.
                alpha, beta = self.model.alpha_beta(H)

                # Calculate survival distributions.
                S_gamma = 1.0 - truncated_gamma_cumulative_distribution(xi, alpha, beta)
                ll_censored_true = np.log(S_gamma).sum()
                np.testing.assert_almost_equal(
                    ll_censored_true, self.model.log_likelihood(X).sum()
                )

    def test_likelihood_mix_censored(self):
        """
        Test the log likelihood when half the events are censored.
        """
        # A mix of censored and observed events.
        xi = array([[0.5, 0.2], [0.3, 0.8]])
        event = np.array([[1, 0], [0, 1]])
        X = concatenate([xi, event], axis=1)
        self.model.fit(X)

        for b in [-1, 1]:
            with self.subTest(f"Model where h={(1-b)/2} term is dominant.", b=b * 100):
                # Large negative (positive) bias to ensure that h=1 (h=0) always.
                self.model.b = 100 * b * ones_like(self.model.b)
                H = self.model.transform(X)
                # Verify that this is the case.
                np.testing.assert_array_almost_equal(H, (1 - b) / 2)

                # Paramters for reference distributions.
                alpha, beta = self.model.alpha_beta(H)

                # Calculate survival distributions.
                S_gamma = 1.0 - truncated_gamma_cumulative_distribution(xi, alpha, beta)
                # Calculate probability densities.
                p_gamma = truncated_gamma_distribution(xi, alpha, beta)
                event_mask = event.astype(bool)
                ll_true = (
                    log(S_gamma[~event_mask]).sum() + log(p_gamma[event_mask]).sum()
                )
                np.testing.assert_almost_equal(
                    ll_true, self.model.log_likelihood(X).sum()
                )


class TestFitUnivariateEvent(TestHarmonium, TestCase):
    """
    Test model training when some of the observations are censored.

    In this simple test, we use only a single time-to-event variable (univariate).
    """

    def setUp(self):
        """
        Generate samples and initialise model.
        """
        super().setUp()
        self.a, self.b = 1.5, 5.0
        self.X = pd.DataFrame(columns=["t", "event"])
        self.X["t"] = np.array(
            [
                sample_right_truncated_gamma_distribution(self.a, self.b, 1.0)
                for _ in range(5000)
            ]
        )

        # Fit model.
        model_parameters = {
            "n_visible_units": 1,
            "n_hidden_units": 1,
            "verbose": False,
            "mini_batch_size": 250,
            "n_epochs": 250,
            "learning_rate": 1.0,
            # "log_every_n_iterations": 25,
            "metrics": ("reconstruct_alpha_beta", "log_likelihood"),
            "output": mkdtemp(),
            "visible_columns": ["t"],
            "event_columns": ["event"],
        }
        self.model = CensorGammaHarmonium(**model_parameters)

    def assert_model_parameters_converged_to_distribution(self, model, data, decimal=1):
        """
        Assert that the distribution parameters almost coincide with those of the model.
        """
        # Parameters according to model.
        alpha, beta = model.reconstruct_alpha_beta(data)
        np.testing.assert_almost_equal(alpha, self.a, decimal=decimal)
        np.testing.assert_almost_equal(beta, self.b, decimal=decimal)

    def test_fit_no_censored_gamma_distribution(self):
        """
        Fit a truncated gamma distribution without censoring.
        """
        # All events are observed.
        self.X["event"] = 1
        self.model.fit(self.X)
        self.assert_model_parameters_converged_to_distribution(self.model, self.X)

    def test_fit_censored_gamma_distribtion(self):
        """
        Fit a truncated gamma distribution in which t >= 0.5 observations are censored.
        """
        # Censor observations t >= 0.5, and replace their values with time of censoring.
        self.X["event"] = self.X["t"].apply(lambda x: 1 if x < 0.5 else 0)
        self.X["t"] = self.X["t"].apply(lambda x: x if x < 0.5 else 0.5)

        self.model.fit(self.X)
        self.assert_model_parameters_converged_to_distribution(self.model, self.X)


class TestFitMixedDistribution(TestHarmonium, TestCase):
    """
    Test the deconvolution of two pairs of distributions with censored observations.

    Generate 2-d data from a truncated gamma distribution coming from two groups
    g={0,1}, i.e., p(x1, x2, g) = p(x1, x2|g) p(g).
    - Censor observations: x(i) > `study_duration`(i),
    - Remove the labels `g`.
    - Compare model `CensorGammaHarmonium` which takes into account censoring, and
      `GammaHarmonium` which does not.
    """

    def setUp(self):
        """
        Generate data for the mixed model.
        """
        super().setUp()

        # Load the data.
        self.dataset = SuperImposedGamma()
        self.X, self.y = self.dataset.load(m=400)

        # Split according to group label.
        self.X1 = self.dataset.load_group(0)
        self.X2 = self.dataset.load_group(1)

        # Compare models taking into account and ignoring censoring.
        model_parameters = {
            "n_hidden_units": 1,
            "verbose": False,
            "learning_rate": 0.25,
            "mini_batch_size": 250,
            "n_epochs": 25,
            "log_every_n_iterations": 10,
            "output": mkdtemp(),
            "metrics": ("log_likelihood",),
            "visible_columns": ["t_0", "t_1"],
        }
        self.reset_random_state()
        self.censor_model = CensorGammaHarmonium(
            event_columns=["event_0", "event_1"], **model_parameters
        ).fit(self.X)
        self.reset_random_state()
        self.ignore_model = GammaHarmonium(**model_parameters).fit(self.X)

    def test_parameter_reconstruction(self):
        """
        Test reconstruction of the distribution parameters.
        """
        # Check data from group 2, because this is where almost all censoring occurs.
        _, b2_censor = self.censor_model.reconstruct_alpha_beta(self.X2)
        _, b2_ignore = self.ignore_model.reconstruct_alpha_beta(self.X2)

        _, b2_true = self.dataset.get_params(group=1)
        # Deviation from actual distribution parameters.
        db2_censor = abs(b2_censor - b2_true)
        db2_ignore = abs(b2_ignore - b2_true)

        # Taking into account censoring leads to a better estimation of the distribution
        # near the x=[1, 1] region.
        self.assertTrue(np.all(db2_censor < db2_ignore))

    def test_latent_structure_identification(self):
        """
        Check that the model can recover the original groups.
        """
        h_censor = self.censor_model.transform(self.X)
        h_ignore = self.ignore_model.transform(self.X)

        censor_accuracy = accuracy_score(self.y, h_censor > 0.5)
        ignore_accuracy = accuracy_score(self.y, h_ignore > 0.5)
        self.assertGreater(censor_accuracy, ignore_accuracy)

        # The model should be much more likely to assign the data `x1` to h=0, and `x2`
        # to h=1 (or the other way around).
        p1_censor = self.censor_model.transform(self.X1).mean()
        p2_censor = self.censor_model.transform(self.X2).mean()

        # Probability of assigning a given class.
        p1_ignore = self.ignore_model.transform(self.X1).mean()
        p2_ignore = self.ignore_model.transform(self.X2).mean()

        # Seperation in probability assignments of the groups.
        prob_difference_censor = abs(p1_censor - p2_censor)
        prob_difference_ignore = abs(p1_ignore - p2_ignore)

        # Check that the model can correctly identify the different distributions.
        self.assertGreater(prob_difference_censor, 0.3)
        # And check that taking into account censoring leads to better identification.
        self.assertGreater(prob_difference_censor, prob_difference_ignore)
