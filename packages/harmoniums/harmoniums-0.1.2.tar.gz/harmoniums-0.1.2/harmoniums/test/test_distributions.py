import unittest

import numpy as np
from numpy import array, ceil, exp

from sklearn.metrics import mean_squared_error

from harmoniums.distributions import (
    fit_truncated_gamma_parameters,
    gamma_star_negative_z,
    interval_truncated_gamma_distribution,
    interval_truncated_gamma_cumulative_distribution,
    normalisation_gamma_distribution,
    truncated_gamma_cumulative_distribution,
    truncated_gamma_distribution,
)
from harmoniums.samplers import sample_right_truncated_gamma_distribution
from harmoniums.test import TestHarmonium


class TestTruncatedGammaDistribution(unittest.TestCase):
    """
    Test consistency of the truncated gamma distribution and its normalisation constant.
    """

    def setUp(self):
        # Perform tests for various truncation values, and both b > 0 and b <= 0.
        self.truncations = array([0.5, 1.0, 2.0, 5.0])
        self.alpha = array([1.0, 10.0, 1.1, 1.0])
        self.beta = array([5.0, -10.0, 3.2, -2.5])

    def test_distribution_consistency(self):
        """
        Test internal consistency of `{truncated, renormalised}_gamma_distribution`.

        Check, on a grid, the shape and the normalisation of the probability density and
        its consistency with the cumulative distribution.
        """
        # Our numerical tolerance is `decimals`-1.
        decimals = 3

        # Check for various parameter triplets (a, b, t).
        for t in self.truncations:
            for a, b in zip(self.alpha, self.beta):
                # Grid coordinates for numerical comparison.
                x = np.linspace(0.0, t, int(ceil(t)) * 10 ** decimals)
                dx = x[1] - x[0]
                prob_unnormed = lambda x, a, b: x ** (a - 1) * exp(-b * x)
                p_unnormalised = prob_unnormed(x, a, b)
                with self.subTest(alpha=a, beta=b, truncation_point=t):
                    # 1.
                    # Test that the probability density is normalised.
                    # integral_0^t dx p(x) = 1.
                    np.testing.assert_almost_equal(
                        dx * sum(truncated_gamma_distribution(x, a, b, t)),
                        1.0,
                        decimal=decimals - 1,
                    )
                    # 2.
                    # Test that the probability density follows the unnormalised
                    # distribution.
                    Z = dx * sum(p_unnormalised)
                    error = abs(
                        truncated_gamma_distribution(x, a, b, t) - (p_unnormalised / Z)
                    )
                    p_max = p_unnormalised[np.argmax(error)] / Z
                    np.testing.assert_array_almost_equal(
                        error / p_max, 0.0, decimal=decimals - 1
                    )
                    # 3.
                    # Test that the Riemann sum of the density is the cumulative
                    # distribution.
                    # integral_0^x dt p(t) = F(x).
                    prob_cum = truncated_gamma_cumulative_distribution(x, a, b, t)
                    np.testing.assert_array_almost_equal(
                        dx * np.cumsum(truncated_gamma_distribution(x, a, b, t)),
                        prob_cum,
                        decimal=decimals - 1,
                    )
                    # 4.
                    # Test that the derivative of the cumulative distribution is
                    # the probability density.
                    # d/dx F(x) = p(x).
                    x_centre = (x[1:] + x[:-1]) / 2.0
                    # Ignore the first element, that is more prone to numerical
                    # instability.
                    np.testing.assert_array_almost_equal(
                        np.diff(truncated_gamma_cumulative_distribution(x[1:], a, b, t))
                        / dx,
                        # `diff` returns n - 1 elements, so use centered coords.
                        truncated_gamma_distribution(x_centre[1:], a, b, t),
                        decimal=decimals - 1,
                    )

    def test_interval_truncated_gamma_distribution(self):
        """
        Test the gamma distribution truncated to a fixed interval.
        """
        # Our numerical tolerance is `decimals`-1.
        decimals = 3
        t_left = 0.25
        t_right = 1.3
        # Grid coordinates for numerical comparison.
        x = np.linspace(t_left, t_right, int(ceil(t_right - t_left)) * 10 ** decimals)
        dx = x[1] - x[0]
        for a, b in zip(self.alpha, self.beta):
            p_unnormalised = x ** (a - 1) * exp(-b * x)
            with self.subTest(alpha=a, beta=b, t_left=t_left, t_right=t_right):
                # Probability density and cumulative distribution.
                p_x = interval_truncated_gamma_distribution(x, a, b, t_left, t_right)
                p_cum = interval_truncated_gamma_cumulative_distribution(
                    x, a, b, t_left, t_right
                )

                # 1.
                # Test that the probability density is normalised.
                # integral_0^t dx p(x) = 1.
                np.testing.assert_almost_equal(dx * sum(p_x), 1.0, decimal=decimals - 1)
                # 2.
                # Test that the probability density follows the unnormalised
                # distribution.
                Z = dx * sum(p_unnormalised)
                error = abs(p_x - (p_unnormalised / Z))
                p_max = p_unnormalised[np.argmax(error)] / Z
                np.testing.assert_array_almost_equal(
                    error / p_max, 0.0, decimal=decimals - 1
                )
                # 3.
                # Test that the Riemann sum of the density is the cumulative
                # distribution.
                # integral_0^x dt p(t) = F(x).
                np.testing.assert_array_almost_equal(
                    dx
                    * np.cumsum(
                        interval_truncated_gamma_distribution(x, a, b, t_left, t_right)
                    ),
                    p_cum,
                    decimal=decimals - 1,
                )
                # 4.
                # Test that the derivative of the cumulative distribution is
                # the probability density.
                # d/dx F(x) = p(x).
                x_centre = (x[1:] + x[:-1]) / 2.0
                # Ignore the first element, that is more prone to numerical
                # instability.
                np.testing.assert_array_almost_equal(
                    np.diff(p_cum[1:]) / dx,
                    # `diff` returns n - 1 elements, so use centered coords.
                    interval_truncated_gamma_distribution(
                        x_centre[1:], a, b, t_left, t_right
                    ),
                    decimal=decimals - 1,
                )

    def test_gamma_distribution_normalisation_constant(self):
        """
        Test the calculation of `gamma_distribution_normalisation_constant`.

        Compare function with Riemann sum on a grid.
        """
        decimals = 3
        for t in self.truncations:
            x = np.linspace(0.0, t, int(ceil(t)) * 10 ** decimals)
            dx = x[1] - x[0]
            for a, b in zip(self.alpha, self.beta):
                p_unnormalised = x ** (a - 1) * exp(-b * x)
                with self.subTest(truncation_point=t, alpha=a, beta=b):
                    Z = dx * sum(p_unnormalised)
                    np.testing.assert_almost_equal(
                        normalisation_gamma_distribution(a, b, t) / Z,
                        1.0,
                        decimal=decimals - 1,
                    )


class TestIncompleteGammaFunction(unittest.TestCase):
    """
    Test the implementation of the lower incomplete gamma function for negative `z`.
    """

    def test_gamma_star(self):
        """
        Test the implementation on the domain a > 0, z < 0.
        """
        parameter_value_pairs = [
            ([1, -10], (exp(10) - 1) / 10),
            ([1, -100], (exp(100) - 1) / 100),
            ([2, -10], (1 + 9 * exp(10)) / 100),
        ]
        for (a, z), y in parameter_value_pairs:
            with self.subTest(a=a, z=z, ground_truth=y):
                np.testing.assert_almost_equal(
                    gamma_star_negative_z(a, z), y, decimal=2
                )

    def test_vectorised_normalisation_constant(self):
        """
        Test the vectorisation of the normalisation constant function.
        """
        a = array([[1.0, 10.0, 0.1], [2.0, 20.0, 0.2]])
        b = array([[5.0, -10.0, 1.0], [10.0, -20.0, 2.0]])

        desired_vector = array(
            [
                [normalisation_gamma_distribution(i, j) for i, j in zip(alpha, beta)]
                for alpha, beta in zip(a, b)
            ]
        )
        # The vectorised function should evaluate the function pair-by-pair.
        np.testing.assert_array_equal(
            normalisation_gamma_distribution(a, b), desired_vector
        )


class TestTruncatedGammaSolve(TestHarmonium):
    """
    Test fitting of `a` and `b` parameters of the truncated gamma distribution.
    """

    def test_fit_truncated_gamma_parameters(self):
        """
        Test the parameter solver by calculating MSE with actual distribution.
        """
        a, b = np.array([1.5, 3.0]), np.array([2.5, -0.5])
        X = np.array(
            [sample_right_truncated_gamma_distribution(a, b, 1.0) for _ in range(3000)]
        )
        alpha, beta = fit_truncated_gamma_parameters(X)

        t = np.linspace(0, 1, 100)
        # Distribution according to fitted parameters.
        pemp_0 = truncated_gamma_distribution(t, alpha[0], beta[0])
        pemp_1 = truncated_gamma_distribution(t, alpha[1], beta[1])

        # Distribution according to actual parameters.
        p_0 = truncated_gamma_distribution(t, a[0], b[0])
        p_1 = truncated_gamma_distribution(t, a[1], b[1])

        # Check that the distributions almost coincide.
        self.assertLess(mean_squared_error(p_0, pemp_0), 1e-3)
        self.assertLess(mean_squared_error(p_1, pemp_1), 1e-3)
