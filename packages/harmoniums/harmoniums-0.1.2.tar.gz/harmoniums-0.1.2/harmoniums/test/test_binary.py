import unittest

import numpy as np
from numpy import random
from numpy.testing import assert_array_almost_equal
from sklearn import datasets

from harmoniums import BinaryHarmonium
from harmoniums.test import TestHarmonium
from harmoniums.test.utils import numerical_gradient
from harmoniums.utils import generate_binary_permutations


class TestBinaryHarmonium(TestHarmonium, unittest.TestCase):
    """
    Unit tests for the binary Harmonium (or Restricted Boltzmann Machine).
    """

    def setUp(self):
        """
        Initialize a simple RBM.
        """
        self.model = BinaryHarmonium(
            n_visible_units=2, n_hidden_units=2, log_every_n_iterations=None
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

        E = self.model.energy(X, H)
        np.testing.assert_array_equal(
            E,
            np.array(
                [
                    self.model.W.sum() + self.model.a.sum() + self.model.b.sum(),
                    self.model.b.sum(),
                    self.model.a.sum(),
                ]
            ),
        )

    def test_energy_gradient(self):
        """Test gradient implementation."""
        model = BinaryHarmonium(
            n_visible_units=2, n_hidden_units=3, log_every_n_iterations=None
        )
        self.reset_model_parameters(model, how="randomly")

        X = generate_binary_permutations(2)
        H = random.uniform(size=(4, 3))
        gradient = model.energy_gradient(X, H)
        approx_grad = numerical_gradient(model, X, H)

        assert_array_almost_equal(gradient["W"].flatten(), approx_grad["W"])
        assert_array_almost_equal(gradient["a"].flatten(), approx_grad["a"])
        assert_array_almost_equal(gradient["b"].flatten(), approx_grad["b"])

    def test_pseudo_likelihood(self):
        """
        Sanity checks for the pseudo likelihood.
        """
        column = 0
        # Test the the probabilities are properly normalised.
        X = generate_binary_permutations(self.model.n_visible_units).astype(int)
        X_prime = X.copy()
        X_prime[:, column] ^= 1

        P = self.model.pseudo_likelihood(X, column)
        P_prime = self.model.pseudo_likelihood(X_prime, column)

        # Check that proabilities are larger than 0.
        self.assertTrue(np.all(P > 0))
        # And sum to one.
        np.testing.assert_array_almost_equal(P + P_prime, np.ones(shape=P.shape))

    def test_stochastic_log_likelihood(self):
        """
        Test the stochastic pseudo log likelihood.
        """
        X = generate_binary_permutations(self.model.n_visible_units)
        self.model.fit(X)

        # Sampling over `n` features should reduce to the exact pseudo log likelihood.
        avg_pseudo_log_likeli = self.model.stochastic_log_likelihood(
            X, s=self.model.n_visible_units
        )
        exact_pseudo_log_likeli = self.model.pseudo_log_likelihood(X)

        # Check that the two arrays are equal.
        np.testing.assert_array_equal(avg_pseudo_log_likeli, exact_pseudo_log_likeli)

    def test_training_with_pseudo_likelihood(self):
        """
        Test that more training increases the log pseudo likelihood.
        """
        # Load scikit learn training set.
        X, y = datasets.load_digits(return_X_y=True)
        X = np.asarray(X, "float32")
        X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)  # 0-1 scaling

        # Train Harmonium 1 epoch.
        rbm = BinaryHarmonium(
            n_hidden_units=100,
            learning_rate=0.06,
            n_epochs=1,
            verbose=False,
            CD_steps=1,
            mini_batch_size=10,
            log_every_n_iterations=None,
        ).fit(X)
        # Train second Harmonium for 4 epochs.
        rbm2 = BinaryHarmonium(
            n_hidden_units=100,
            learning_rate=0.06,
            n_epochs=4,
            verbose=False,
            CD_steps=1,
            mini_batch_size=10,
            log_every_n_iterations=None,
        ).fit(X)

        # Test that the log pseudo likelihood is larger for the model which was trained
        # longer.
        self.assertGreater(
            rbm2.pseudo_log_likelihood(X).mean(), rbm.pseudo_log_likelihood(X).mean()
        )

    def test_transform(self):
        """
        Test the calculate of p(h|x).
        """
        X = np.array([[1, 1], [0, 0], [1, 1]])
        self.model.fit(X)
        # Calculate activations.
        a = self.model.transform(X)
        # Check that the variable shapes are consistent.
        self.assertEqual(a.shape, (X.shape[0], self.model.n_hidden_units))

    def test_gibbs_update(self):
        """
        Check that the update rules correctly converge for trivial solutions.
        """
        # Test convergence for all possible configurations of the visible units. A model
        # with W_ij = -10 (ferromagnet) tries to set all hidden and visible units to 1.
        self.model.W = np.ones(shape=(2, 2)) * -10
        self.model.a = np.zeros(shape=(2, 1))
        self.model.b = np.zeros(shape=(2, 1))

        X0 = generate_binary_permutations(self.model.n_visible_units)
        X_chain = X0.copy()

        # Sample a few times, to burn in.
        k = 100
        for _ in range(k):
            X_chain = self.model.gibbs_update(X_chain)

        m = X_chain.shape[0]
        X_avg = np.zeros(shape=X_chain.shape)
        H_avg = np.zeros(shape=(m, self.model.n_hidden_units))

        # Check that the solutions have converged.
        for _ in range(k):
            H = self.model.p_h_condition_x(X_chain)
            H_avg += H
            X_chain = self.model.p_x_condition_h(H)
            X_avg += X_chain

        X_avg /= k
        H_avg /= k

        # Check that on average it should have converged to the [1, 1] states.
        np.testing.assert_array_almost_equal(X_avg, np.ones(shape=X_avg.shape))
        np.testing.assert_array_almost_equal(H_avg, np.ones(shape=H_avg.shape))

    def test_partition_function(self):
        """
        Test the calculation of the partition function.
        """
        Z = 0.0
        # Z = sum_x sum_h exp[-E(x,h)].
        for x in generate_binary_permutations(n=self.model.n_visible_units):
            for h in generate_binary_permutations(n=self.model.n_hidden_units):
                Z += np.exp(-self.model.energy(x.reshape(1, -1), h.reshape(1, -1)))

        self.assertEqual(Z.shape, (1,))
        np.testing.assert_array_almost_equal(
            Z[0],
            # Turn into single element array for comparison.
            self.model.partition_function(),
        )

    def test_free_energy_h(self):
        """
        Test the calculation of the free energy F(h) by explicit calculation.
        """
        # Test free energy for all possible configurations of the hidden units.
        # Calculate parition function for each of the states, since -ln Z = F.

        H = generate_binary_permutations(self.model.n_hidden_units)
        Z = np.zeros(shape=(H.shape[0],))
        # exp[-F(h)] = sum_x exp[-E(x,h)].
        for x in generate_binary_permutations(self.model.n_visible_units):
            X = np.ones(shape=H.shape) * x  # Same x vector for each record in `H`.
            Z += np.exp(-self.model.energy(X, H))

        F = -np.log(Z)
        # Test that the analytic expression, and the explicit calculate are identical.
        np.testing.assert_array_almost_equal(self.model.free_energy_h(H), F)

    def test_free_energy_x(self):
        """
        Test the free energy F(X) by explicit calculation.
        """
        # Test free energy for all possible configurations of the visible units (using
        # `self.X_all`). Calculate parition function for each of the states, since -ln Z
        # = F.
        X = generate_binary_permutations(self.model.n_visible_units)
        Z = np.zeros(shape=X.shape[0])

        # exp[-F(x)] = sum_h exp[-E(x,h)].
        for h in generate_binary_permutations(self.model.n_hidden_units):
            H = np.ones(shape=X.shape) * h.T
            energy = self.model.energy(X, H)
            Z += np.exp(-energy)

        F = -np.log(Z)
        # Test that the analytic expression, and the explicit calculate are identical.
        np.testing.assert_array_almost_equal(self.model.free_energy_x(X), F)

    def test_parameter_initialisation(self):
        """
        Check that the biases are correctly set for the visible units.
        """
        X = np.array([[1, 1], [0, 0], [1, 0]])
        model = BinaryHarmonium(
            n_hidden_units=1,
            # Initialise the model without fitting directly.
            dry_run=True,
            log_every_n_iterations=None,
        )

        model.fit(X)
        # Test the actual initialisation.
        np.testing.assert_array_almost_equal(
            model.a, np.array([np.log(2.0), -np.log(2.0)]).reshape(-1, 1)
        )
