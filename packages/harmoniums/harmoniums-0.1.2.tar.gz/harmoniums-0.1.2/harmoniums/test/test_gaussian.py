from tempfile import mkdtemp
from unittest import TestCase

import numpy as np
from numpy import exp, pi, random, zeros_like
from numpy.linalg import norm
from numpy.testing import assert_allclose
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

from harmoniums import GaussianHarmonium
from harmoniums.test import TestHarmonium
from harmoniums.test.utils import numerical_gradient
from harmoniums.test.datasets import laplace_mixtures
from harmoniums.utils import generate_binary_permutations


class TestGaussianHarmonium(TestHarmonium, TestCase):
    def setUp(self):
        """
        Set up a random initialisation of a 2x2 Gaussian Harmonium.
        """
        self.model = GaussianHarmonium(
            n_visible_units=2,
            n_hidden_units=2,
            dry_run=True,
            log_every_n_iterations=None,
        )
        self.reset_model_parameters(self.model, how="randomly")

        # Call parent `setUp` method.
        super().setUp()

    def test_energy(self):
        """
        Test the calculation of the energy.
        """
        X = np.array([[1, 1], [0, 0], [1, 1]])
        H = np.array([[1, 1], [1, 1], [0, 0]])

        # E(x=[1,1], h=[1,1]):
        # E = sum_i,j Wij/sigma_i + sum_i(1-a_i)^2/(2 sigma_i^2) + sum_j b_j.
        E_11 = (
            (self.model.W / self.model.sigma).sum()
            + norm((1 - self.model.a) / self.model.sigma) ** 2 / 2.0
            + self.model.b.sum()
        )
        # E(x=[0,0], h=[1,1]): sum_i a_i^2/(2 sigma_i^2)/2.
        E_01 = ((self.model.a / self.model.sigma) ** 2 / 2.0 + self.model.b).sum()
        # E(x=[1,1], h=[0,0]): sum_i [(1-a_i)/sigma_i]^2
        E_10 = norm((1 - self.model.a) / self.model.sigma) ** 2 / 2.0

        np.testing.assert_array_almost_equal(
            self.model.energy(X, H), np.array([E_11, E_01, E_10])
        )

    def test_energy_gradient(self):
        """Test gradient implementation."""
        model = GaussianHarmonium(
            n_visible_units=2, n_hidden_units=3, log_every_n_iterations=None
        )
        self.reset_model_parameters(model, how="randomly")

        X = generate_binary_permutations(2)
        H = random.uniform(size=(4, 3))
        gradient = model.energy_gradient(X, H)
        approx_grad = numerical_gradient(model, X, H)

        assert_allclose(gradient["W"].flatten(), approx_grad["W"], rtol=1e-3)
        assert_allclose(gradient["a"].flatten(), approx_grad["a"], rtol=1e-3)
        assert_allclose(gradient["b"].flatten(), approx_grad["b"], rtol=1e-3)
        assert_allclose(gradient["sigma"].flatten(), approx_grad["sigma"], rtol=1e-3)

    def test_training_with_reconstruction(self):
        """
        Test that more training decreases the reconstruction error.
        """
        # Load scikit learn training set.
        X, y = datasets.load_digits(return_X_y=True)
        X = np.asarray(X, "float32")

        parameters = {
            "n_visible_units": X.shape[1],
            "n_hidden_units": 100,
            "learning_rate": 0.000006,
            "maximum_iteration": 100000,
            "verbose": False,
            "CD_steps": 1,
            "metrics": ("reconstruction_error",),
            "mini_batch_size": 100,
            "log_every_n_iterations": 50,
        }
        # Long training (100 epochs).
        rbm = GaussianHarmonium(n_epochs=100, output=mkdtemp(), **parameters).fit(X)
        # Short training (25 epochs).
        rbm2 = GaussianHarmonium(n_epochs=25, output=mkdtemp(), **parameters).fit(X)

        rbm_metrics = rbm.get_train_metrics()
        rbm2_metrics = rbm2.get_train_metrics()
        self.assertLess(
            rbm_metrics["reconstruction_error"].iloc[-1],
            rbm2_metrics["reconstruction_error"].iloc[-1],
        )

    def test_free_energy_h(self):
        """
        Compare the free energy F(h) with analytical identities.

        Use the fact that:
        exp[-F(h)] = integral dx exp[-E(x, h)].
        """
        H = generate_binary_permutations(n=self.model.n_hidden_units)

        # Set weights to zero: non-interacting model.
        self.model.W = zeros_like(self.model.W)
        #  Use: integral dx exp[-(x-a)^2/2 sigma^2] = 1/sqrt[2pi sigma^2].
        np.testing.assert_array_almost_equal(
            self.model.free_energy_h(H),
            (H @ self.model.b).flatten()
            - 1 / 2 * np.log(2 * pi * self.model.sigma ** 2).sum(),
        )

        # Reset W weights.
        self.model.W = np.random.random((2, 2))
        # And now put `a` to zero.
        self.model.a = zeros_like(self.model.a)

        w = self.model.W @ H.T
        # Use: integral dx exp[-x^2/2 sigma^2 -x*w/sigma]
        # = exp[w^2/2]/sqrt[2pi sigma^2].
        np.testing.assert_array_almost_equal(
            self.model.free_energy_h(H),
            (H @ self.model.b).flatten()
            - (w.T @ w / 2.0).diagonal()
            - 1 / 2 * np.log(2 * pi * self.model.sigma ** 2).sum(),
        )

        # Reset weights of `a`.
        self.model.a = np.random.random(self.model.a.shape)
        # And put weights of `b` to zero.
        self.model.b = zeros_like(self.model.b)
        w = self.model.W @ H.T
        # Use: integral dx exp[-(x-a)^2/sigma^2 - x*w/sigma] =
        # exp[w^2/2 + aw/sigma] / sqrt[2pi sigma^2].
        np.testing.assert_array_almost_equal(
            self.model.free_energy_h(H),
            ((w / self.model.sigma).T @ self.model.a).flatten()
            - (w.T @ w / 2.0).diagonal()
            - 1 / 2.0 * np.log(2 * pi * self.model.sigma ** 2).sum(),
        )

    def test_free_energy_x(self):
        """
        Test the calculation of the free energy F(x) by exhaustive computation.
        """
        # Initialise model for the parent function.
        model = GaussianHarmonium(n_visible_units=3, n_hidden_units=2)
        # Make sure the biases are non-zero.
        self.reset_model_parameters(model, how="randomly")

        m = 10  # Number of records.
        X = np.random.random((m, model.n_visible_units))
        Z = np.zeros(shape=(m,))

        # exp[-F(x)] = sum_h exp[-E(x,h)].
        for h in generate_binary_permutations(model.n_hidden_units):
            H = np.ones(shape=(m, model.n_hidden_units)) * h.T
            energy = model.energy(X, H)
            Z += np.exp(-energy)

        F = -np.log(Z)

        # Test that the analytic expression, and the explicit calculate are identical.
        np.testing.assert_array_almost_equal(model.free_energy_x(X), F)

    def test_likelihood_laplace_mixtures_non_interacting(self):
        """
        Test the calculation of the likelihood for a non-interacting Harmonium.
        """
        # Non-interacting means: W, a, and b are zero.
        self.model.W = zeros_like(self.model.W)
        self.model.a = zeros_like(self.model.a)
        self.model.b = zeros_like(self.model.b)

        # The free energy F(x) should now only contain a quadratic term F(x) =
        # x^2/sigma^2 2 + n_h ln 2.
        # Or put differently:
        # Z = sum_h integral dx exp[-x^2/(2sigma^2)] =
        # 2^n_h * Prod_i sqrt(2pi sigma_i^2).
        lnZ = np.log(self.model.partition_function())
        self.assertEqual(
            lnZ,
            1 / 2 * np.log(2 * pi * self.model.sigma ** 2).sum()
            + self.model.n_hidden_units * np.log(2),
        )

        np.random.seed(42)

        # Make a mixture model of `n` independent laplace distributions:
        #  p(s) = exp[-sqrt(2)|s|_1]/2
        # using x = As.
        n = 2
        X, mixture_matrix = laplace_mixtures(
            average=0.0, scale=1 / np.sqrt(2), size=(100000, n)
        )

        mixture_matrix_inverse = np.linalg.inv(mixture_matrix)
        s = X @ mixture_matrix_inverse.T
        np.testing.assert_almost_equal(
            np.var(s, axis=0).sum(), self.model.n_hidden_units, decimal=2
        )

        # First check the calculation of the variance.
        np.testing.assert_almost_equal(
            np.var(X, axis=0).sum(), (mixture_matrix ** 2).sum(), decimal=2
        )
        # Check the calculation of the free energy.
        # <F(x)> = 1/2 <x^2/sigma^2> - n_h ln 2.
        # But x=As and for the Laplace distribution p(s) = exp(-a|s|)a/2 we have
        # <s_i s_j> = delta_i,j (2/a^2)^2
        # and therefore [since a = sqrt(2), see above]:
        # <(x/sigma)^2> = <(As/sigma)^2> = sum_i,j (A_ij/ sigma_i)^2.
        np.testing.assert_almost_equal(
            self.model.free_energy_x(X).mean(),
            ((mixture_matrix / self.model.sigma) ** 2).sum() / 2
            - self.model.n_hidden_units * np.log(2),
            decimal=2,
        )

        # <ln p(x)> = -<F> - ln Z = -(<(x/sigma)^2>/2 - n_h ln 2)
        # - (n_h ln 2 + 1/2 sum_i ln [2pi sigma^2_i]).
        # Using the details outlined above we have for our Laplace mixtures:
        # -<ln p(x)> = 1/2 sum_i,j (A_ij/sigma_i)^2  + 1/2 sum_i ln [2pi sigma_i^2].
        np.testing.assert_almost_equal(
            -self.model.average_log_likelihood(X),
            ((mixture_matrix / self.model.sigma) ** 2).sum() / 2
            + 1 / 2 * np.log(2 * pi * self.model.sigma ** 2).sum(),
            decimal=2,
        )

        # -<ln p(s)> = 1/2 sum_i <(s_i/sigma_i)^2> + 1/2 sum_i log(2pi sigma_i^2)
        # where
        # <(s_i/sigma_i)^2> = 1/sigma_i^2.
        np.testing.assert_almost_equal(
            -self.model.average_log_likelihood(s),
            (1 / self.model.sigma ** 2).sum() / 2
            + 1 / 2 * np.log(2 * pi * self.model.sigma ** 2).sum(),
            decimal=2,
        )

    def test_likelihood_laplace_mixtures(self):
        """
        Try to fit a mixture model of `n` independent Laplace distributions.
        """
        np.random.seed(42)

        # Laplace distributions:
        #  p(s) = exp[-sqrt(2)|s|_1]/2
        # using x = As <==>
        # p(x) = exp[-sqrt(2) |x|_1]/2 * |det A|.
        X, mixture_matrix = laplace_mixtures(
            average=0.0, scale=1 / np.sqrt(2), size=(100000, self.model.n_visible_units)
        )

        # Whiten the data for enhanced performance.
        X = PCA(whiten=True).fit_transform(X)
        X_train, X_test = train_test_split(X, train_size=0.5)

        # Analytica exact expression of the model.
        log_likelihood_exact = (
            -self.model.n_visible_units - self.model.n_visible_units / 2 * np.log(2)
        )

        model = GaussianHarmonium(
            n_visible_units=2,
            n_hidden_units=4,
            learning_rate=(1.0, 0.0, 1.0, 0.1),
            random_state=1234,
            CD_steps=1,
            mini_batch_size=1000,
            n_epochs=50,
            log_every_n_iterations=200,
            maximum_iteration=10000000,
            tolerance=1.0e-12,
            persistent=False,
            verbose=False,
            output=mkdtemp(),
            metrics=("log_likelihood",),
            X_validation=X_test,
        )

        model.fit(X_train)
        model_likelihood = model.average_log_likelihood(X_test)

        # The likelihood is bounded from above by the exact likelihood.
        self.assertLess(model_likelihood.mean(), log_likelihood_exact)
        # We should, approximately, be able to reproduce the likelihood as in
        # https://pydeep.readthedocs.io/en/latest/tutorials/GRBM_2D_example.html.
        self.assertGreater(model_likelihood.mean(), -2.75)


class TestFitGaussian(TestHarmonium, TestCase):
    """
    Test fitting the model on two independent Gaussians.
    """

    def setUp(self):
        """
        Generate training data consisting of two gaussian with mean -1 and 2.
        """
        super().setUp()
        self.mean = np.array((-1, 2))
        self.std = np.array((exp(1), exp(2)))
        m = 10000
        self.X = np.random.normal(
            loc=self.mean, scale=self.std, size=(m, self.mean.shape[0])
        )
        self.model_parameters = {
            "n_hidden_units": 1,
            "n_visible_units": 2,
            "random_state": 1234,
            "CD_steps": 1,
            "mini_batch_size": 500,
            "n_epochs": 500,
            "log_every_n_iterations": 100,
            "output": mkdtemp(),
            "maximum_iteration": 10000000,
            "tolerance": 1.0e-12,
            "persistent": True,
            "verbose": False,
            "metrics": ("log_likelihood", "reconstruct_mu_sigma"),
            "dry_run": True,
        }

    def test_fit_bias(self):
        """
        Test fitting of `a` vector by training on a Gaussian.
        """
        model = GaussianHarmonium(
            # Only learn `a` (learning rate `W` and `b` are zero).
            learning_rate=(0.0, 0.1, 0.0, 0.0),
            **self.model_parameters,
        )
        model.fit(self.X)  # Dry run: init but don't train.
        # A Gaussian model is recovered upon setting weights `W` and `b` to zero.
        model.W = zeros_like(model.W)
        # Train model.
        model.persistent_constrastive_divergence(self.X)

        # Check that training gives the correct means after training.
        np.testing.assert_almost_equal(model.a.flatten(), self.mean, decimal=1)

    def test_fit_weight_matrix(self):
        """
        Test fitting of `W` by training on a Gaussian.
        """
        model = GaussianHarmonium(
            # Only learn `W` (learning rate `a` and `b` are zero).
            learning_rate=(0.1, 0.0, 0.0, 0.0),
            **self.model_parameters,
        )
        model.fit(self.X)  # Dry run: init but don't train.
        model.a = zeros_like(model.a)
        model.b = zeros_like(model.b)
        # Set the correct standard deviations in advance.
        model.sigma = self.std.reshape(-1, 1)

        model.persistent_constrastive_divergence(self.X)

        # The model should learn a diagonal W encoding the means of the distribution.
        ll_exact = (
            -1 / 2 * (model.n_visible_units + np.log(2 * pi * self.std ** 2).sum())
        )
        np.testing.assert_almost_equal(
            model.log_likelihood(self.X).mean(), ll_exact, decimal=2
        )
        # Check that training gives the correct means after training.
        mu, sigma = model.reconstruct_mu_sigma(self.X)
        np.testing.assert_almost_equal(mu, self.mean, decimal=1)

    def test_fit_weight_and_standard_deviation(self):
        """
        Test the simultaneous training of `W` and `sigma` on a Gaussian.
        """
        model = GaussianHarmonium(
            # Only learn `W` and `sigma` (learning rate `a` and `b` are zero).
            learning_rate=(0.01, 0.0, 0.075, 0.075),
            **self.model_parameters,
        )
        model.fit(self.X)  # Dry run: init but don't train.
        model.W = zeros_like(model.W)
        model.a = zeros_like(model.a)
        model.b = zeros_like(model.b)

        # The model should learn a diagonal W encoding the means of the distribution.
        model.persistent_constrastive_divergence(self.X)

        # Check that training gives the correct mean and standard deviation.
        mu, sigma = model.reconstruct_mu_sigma(self.X)
        np.testing.assert_almost_equal(mu, self.mean, decimal=1)
        np.testing.assert_array_almost_equal(sigma, self.std, decimal=1)

    def test_fit_standard_deviation(self):
        """
        Test fitting of both `sigma` and means `mu` by training on a Gaussian.
        """
        model = GaussianHarmonium(
            # Only learn `a` and `sigma` (learning rate `W` and `b` are zero).
            learning_rate=(0.0, 0.01, 0.0, 0.01),
            **self.model_parameters,
        )
        model.fit(self.X)  # Dry run: init but don't train.
        model.W = zeros_like(model.W)
        model.a = zeros_like(model.a)
        model.b = zeros_like(model.b)

        # The model should learn a diagonal W encoding the means of the distribution.
        model.persistent_constrastive_divergence(self.X)

        ll = model.log_likelihood(self.X).mean()

        # Check that the correct standard deviations are learned.
        np.testing.assert_array_almost_equal(model.sigma.flatten(), self.std, decimal=1)
        # Check that training gives the correct means after training.
        np.testing.assert_array_almost_equal(model.a.flatten(), self.mean, decimal=1)
        # The log likelihood L = -sum_i<(x_i-a_i)^2/sigma_i^2> - ln Z
        # = -n_v/2 - ln Z = -1/2(n_v + sum_i ln[2pi sigma_i^2]) /
        np.testing.assert_almost_equal(
            ll,
            -0.5 * (model.n_visible_units + np.log(2 * pi * model.sigma ** 2).sum()),
            decimal=1,
        )
