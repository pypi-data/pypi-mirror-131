from math import gamma
from tempfile import mkdtemp
from typing import Tuple, Union
import unittest

import numpy as np
from numpy import exp, log, ones_like, pi, random, zeros_like
from numpy.testing import assert_allclose
from scipy.special import gammainc
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle

from harmoniums import GammaHarmonium
from harmoniums.const import Matrix
from harmoniums.distributions import truncated_gamma_distribution
from harmoniums.samplers import sample_right_truncated_gamma_distribution
from harmoniums.test import TestHarmonium
from harmoniums.test.utils import numerical_gradient
from harmoniums.utils import generate_binary_permutations


class TestGammaHarmonium(TestHarmonium, unittest.TestCase):
    """
    Helper functions for the GammaHarmonium tests.
    """

    def mean_squared_error_gamma_distribution(
        self, model, sample_params: Tuple[Matrix, Matrix], samples: Matrix
    ) -> Union[float, np.array]:
        """
        Mean squared error between estimated gamma and actual gamma distribution.
        """
        alpha, beta = model.reconstruct_alpha_beta(samples)
        a, b = sample_params

        y_model = truncated_gamma_distribution(samples, alpha, beta)
        y_true = truncated_gamma_distribution(samples, a, b)
        mse = mean_squared_error(y_true, y_model, multioutput="raw_values")
        return mse


class TestFitParametersGammaHarmonium(TestGammaHarmonium, unittest.TestCase):
    """
    Fit individual parameters (V, W, a, b, and c) of `GammaHarmonium`.

    Test this on a single truncated Gamma distribution, for simplicity. We use the fact
    that, when h=0, the model and the distribution should coincide exactly.
    """

    def setUp(self):
        """
        Generate samples of a a single truncated Gamma distribution.
        """
        super().setUp()
        self.a, self.b = 1.5, 5.0
        self.samples = np.array(
            [
                sample_right_truncated_gamma_distribution(self.a, self.b, 1.0)
                for _ in range(10000)
            ]
        ).reshape(-1, 1)

        self.model_parameters = {
            "n_visible_units": 1,
            "n_hidden_units": 1,
            "verbose": True,
            "mini_batch_size": 250,
            "n_epochs": 175,
            "log_every_n_iterations": 25,
            "output": mkdtemp(),
            # "metrics": (
            #     "log_likelihood",
            #     "reconstruction_error",
            #     "reconstruct_alpha_beta",
            # ),
            "metrics": tuple(),
            "dry_run": True,
            "random_state": self.random_state,
        }

    def mean_squared_error_gamma_distribution(self, model) -> float:
        """
        Calculate mean squared error with the single truncated Gamma distribution.
        """
        return super().mean_squared_error_gamma_distribution(
            model, sample_params=(self.a, self.b), samples=self.samples
        )

    def assert_parameters_converged(self, model, decimal=1):
        """
        Assert that the distribution parameters almost coincide with the model.
        """
        # Parameters according to model.
        alpha, beta = model.reconstruct_alpha_beta(self.samples)
        np.testing.assert_almost_equal(alpha, self.a, decimal=decimal)
        np.testing.assert_almost_equal(beta, self.b, decimal=decimal)

    def test_energy_gradient(self):
        """Test gradient implementation."""
        model = GammaHarmonium(
            n_visible_units=2, n_hidden_units=3, log_every_n_iterations=None
        )
        self.reset_model_parameters(model, how="randomly")

        X = random.uniform(size=(4, 2))
        H = random.uniform(size=(4, 3))
        gradient = model.energy_gradient(X, H)
        approx_grad = numerical_gradient(model, X, H)

        assert_allclose(gradient["V"].flatten(), approx_grad["V"], rtol=1e-3)
        assert_allclose(gradient["W"].flatten(), approx_grad["W"], rtol=1e-3)
        assert_allclose(gradient["a"].flatten(), approx_grad["a"], rtol=1e-3)
        assert_allclose(gradient["b"].flatten(), approx_grad["b"], rtol=1e-3)
        assert_allclose(gradient["c"].flatten(), approx_grad["c"], rtol=1e-3)

    def test_fit_x_bias(self):
        """
        Fit the gamma RBM using bias `a` and `V` (W=c=0 fixed).
        """
        self.model_parameters["learning_rate"] = (
            0.0,  # Learning rate `W`.
            0.125,
            0.125,
            0.125,
            0.0,  # Learning rate `c`.
        )
        model = GammaHarmonium(**self.model_parameters)
        model.fit(self.samples)  # Dry run: init but don't train.
        model.W = zeros_like(model.W)
        model.c = zeros_like(model.c)

        # Train model.
        model.persistent_constrastive_divergence(self.samples)

        # Check convergence.
        self.assert_parameters_converged(model, decimal=1)
        mse = self.mean_squared_error_gamma_distribution(model)
        self.assertLess(mse, 0.01)

    def test_fit_lnx_bias(self):
        """
        Test fit the `c` bias, with  W = |V| =0 fixed.
        """
        # Learning rate |V| and |W| = 0.
        self.model_parameters["learning_rate"] = (
            0.0,  # Learning rate `W`.
            0.0,  # Learning rate `V`.
            0.125,
            0.125,
            0.125,
        )
        model = GammaHarmonium(**self.model_parameters)
        model.fit(self.samples)  # Dry run: init but don't train.
        model.W = zeros_like(model.W)
        model.V = zeros_like(model.V)

        # Train model.
        model.persistent_constrastive_divergence(self.samples)

        # Check convergence.
        self.assert_parameters_converged(model, decimal=1)
        mse = self.mean_squared_error_gamma_distribution(model)
        self.assertLess(mse, 0.01)

    def test_fit_W(self):
        """
        Fit the `W` coupling with bias a=c=0 fixed.
        """
        self.model_parameters["learning_rate"] = (
            0.1,
            0.1,
            0.0,  # Learning rate `a`.
            0.1,
            0.0,  # Learning rate `c`.
        )
        model = GammaHarmonium(**self.model_parameters)
        model.fit(self.samples)  # Dry run: init but don't train.
        model.a = zeros_like(model.a)
        model.c = zeros_like(model.c)

        # Train model.
        model.persistent_constrastive_divergence(self.samples)

        # Assert convergence of parameters.
        self.assert_parameters_converged(model, decimal=1)
        # Assert convergence of probability density.
        mse = self.mean_squared_error_gamma_distribution(model)
        self.assertLess(mse, 0.01)


class TestThermodynamicsGammaHarmonium(TestGammaHarmonium, unittest.TestCase):
    """
    Verify thermodynamic quantities like free energy and log likelihood.
    """

    def test_free_energy_x(self):
        """
        Test the free energy F(x) by exhaustive computation.
        """
        m = 10  # Number of records.
        n_visible = 3
        X = np.random.random((m, n_visible))

        # Initialise model for the parent function.
        model = GammaHarmonium(
            n_visible_units=n_visible,
            n_hidden_units=2,
            dry_run=True,
            log_every_n_iterations=None,
        ).fit(X)

        Z = np.zeros(shape=(m,))

        # exp[-F(x)] = sum_h exp[-E(x,h)].
        for h in generate_binary_permutations(model.n_hidden_units):
            H = np.ones(shape=(m, model.n_hidden_units)) * h.T
            energy = model.energy(X, H)
            Z += np.exp(-energy)

        F = -np.log(Z)

        # Test that the analytic expression, and the explicit calculate are identical.
        np.testing.assert_array_almost_equal(model.free_energy_x(X), F)

    def test_free_energy_h(self):
        """
        Test the calculation of the free energy of the hidden units F(h).
        """
        n_h = 3
        n_v = 2
        model_parameters = {"n_visible_units": n_v, "n_hidden_units": n_h}
        model = GammaHarmonium(**model_parameters)
        model.initialise_parameters()

        # 1) First calculate with biases `a` and `b` zero.
        model.a = zeros_like(model.a)
        model.b = zeros_like(model.b)
        model.V = ones_like(model.V) * pi ** 2
        model.W = ones_like(model.W) * exp(2)
        c = 2
        model.c = ones_like(model.c) * c

        # Calculate free energy for two specific hidden unit configurations.
        H = np.array([(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)])
        ALPHA, BETA = model.alpha_beta(H)
        F = model.free_energy_h(H)

        # exp[-F(h)] = integral dx exp[-E(x,h)].
        # => exp[-F(h=0)] = integral dx x^c.
        # F(h=0) = n_v ln[gamma(1 + c, 0)].
        F_h0 = n_v * log(c + 1)
        np.testing.assert_almost_equal(F[0], F_h0)

        # First check that alpha and beta values are correctly calculated.
        a = n_h * pi ** 2 + c + 1
        b = n_h * np.exp(2)
        # Normalisation constant equals: integral_0^1 dx exp(-bx) x^(a-1).
        normalisation_constant = gamma(a) * gammainc(a, b) * b ** (-a)
        np.testing.assert_almost_equal(ALPHA[1, :], a)
        np.testing.assert_almost_equal(BETA[1, :], b)
        # The free energy is -2x the normalisation constant.
        np.testing.assert_almost_equal(F[1], -2 * log(normalisation_constant))

        # 2) Now check with hidden bias set.
        model.b = np.array([[1.0], [2.0], [3.0]])
        ALPHA, BETA = model.alpha_beta(H)
        F = model.free_energy_h(H)
        np.testing.assert_almost_equal(F[0], F_h0)
        np.testing.assert_almost_equal(
            F[1], sum(model.b) + -2 * log(normalisation_constant)
        )


class TestGammaHarmoniumMixedEvents(TestGammaHarmonium, unittest.TestCase):
    """
    Test fitting the harmonium when the input is a vector of distributions.
    """

    def test_fit_multi_independent_gamma_distributions(self):
        """
        Test that the gamma RBM can fit multiple independent gamma distributions.
        """
        a = np.array([1.0, 1.5])
        b = np.array([5.0, -0.2])
        samples = np.array(
            [sample_right_truncated_gamma_distribution(a, b, 1.0) for _ in range(10000)]
        )

        # Fit model on data from test distribution.
        model = GammaHarmonium(
            n_visible_units=a.shape[0],
            n_hidden_units=1,
            verbose=False,
            guess_weights=True,
            learning_rate=(0.1, 0.1, 0.25, 0.25, 0.25),
            mini_batch_size=150,
            n_epochs=50,
            weight_decay=0.0,
            log_every_n_iterations=10,
            output=mkdtemp(),
            metrics=tuple(),
        )

        model.fit(samples)

        # Calculate error between sample distribution and distribution based on fitted
        # parameters in model.
        mse = self.mean_squared_error_gamma_distribution(
            model, sample_params=(a, b), samples=samples
        )

        # N.B. We require that the distributions are close, not that the parameters are
        # close.
        self.assertTrue(np.all(mse < 0.1))

    def test_fit_mixed_model(self):
        """
        Test the deconvolution of two pairs of distributions.

        Generate 2-d data from a truncated gamma distribution coming from two groups
        g={0,1}, i.e., p(x1, x2, g) = p(x1, x2|g) p(g). Remove the labels `g`, and check
        that the model can recover the original labels.
        """
        # Data from group 1.
        a1 = [1.5, 2.5]
        b1 = [3.0, 5.0]
        x1 = np.array(
            [
                sample_right_truncated_gamma_distribution(a1, b1, 1.0)
                for _ in range(5000)
            ]
        )
        # Data from group 2.
        a2 = [1.0, 1.0]
        b2 = [-3.0, -7.0]
        x2 = np.array(
            [
                sample_right_truncated_gamma_distribution(a2, b2, 1.0)
                for _ in range(5000)
            ]
        )
        x = np.concatenate((x1, x2), axis=0)
        group = np.concatenate((np.zeros(x1.shape[0]), np.ones(x2.shape[0])), axis=0)
        x, group = shuffle(x, group)

        model = GammaHarmonium(
            n_visible_units=x.shape[1],
            n_hidden_units=1,
            verbose=False,
            learning_rate=0.25,
            mini_batch_size=250,
            n_epochs=25,
            log_every_n_iterations=10,
            # metrics=("log_likelihood", "reconstruction_error",),
            metrics=tuple(),
            output=mkdtemp(),
        )

        model.fit(x)

        # The model should be much more likely to assign the data `x1` to h=0, and `x2`
        # to h=1 (or the other way around).
        p1 = model.transform(x1).mean()
        p2 = model.transform(x2).mean()

        # The difference in probability should be at least two quantiles.
        prob_difference = abs(p1 - p2)
        self.assertGreater(prob_difference, 0.5)
