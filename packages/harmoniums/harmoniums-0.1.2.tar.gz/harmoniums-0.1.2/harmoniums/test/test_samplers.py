from math import ceil
import unittest

from matplotlib import pyplot as plt

import numpy as np

from harmoniums.distributions import (
    g,
    interval_truncated_gamma_distribution,
    truncated_gamma_cumulative_distribution,
    truncated_gamma_distribution,
)
from harmoniums.samplers import (
    _choose_number_of_components_right_truncated_gamma,
    sample_truncated_exponential,
    sample_g,
    sample_interval_truncated_gamma_distribution,
    sample_right_truncated_gamma_distribution,
)
from harmoniums.test import TestHarmonium


class TestSampler(TestHarmonium, unittest.TestCase):
    """
    Common shared function for sampler test cases.
    """

    def _distribution_from_samples(
        self,
        samples: np.ndarray,
        bins: int = 100,
        left_truncation_point: float = 0.0,
        right_truncation_point: float = 1.0,
        normalise: bool = True,
    ):
        """
        Generate a distribution on the interval [0, t] from a sample set.
        """
        # Equidistant bins on the unit interval.
        x = np.linspace(left_truncation_point, right_truncation_point, bins + 1)
        sample_distribution, _ = np.histogram(samples, bins=x)
        if normalise:
            sample_distribution = sample_distribution / sum(sample_distribution)
        return x, sample_distribution.astype(float)

    def _cumulative_distribution_from_samples(
        self,
        samples: np.ndarray,
        bins: int = 100,
        left_truncation_point: float = 0.0,
        right_truncation_point: float = 1.0,
        normalise: bool = True,
    ):
        """
        Generate a cumulative distribution on the interval [0, t] from a sample set.
        """
        bins, prob_density = self._distribution_from_samples(
            samples,
            bins=bins,
            left_truncation_point=left_truncation_point,
            right_truncation_point=right_truncation_point,
            normalise=False,
        )
        cumul_distribution = np.cumsum(prob_density)
        if cumul_distribution[-1] == 0:
            raise ValueError("Cumulative distribution not normalised.")
        if normalise:
            cumul_distribution /= cumul_distribution[-1]
        return bins, cumul_distribution

    def _plot(self, v_1, v_2, x=None):
        """
        Make a plot for visual inspection.
        """
        plt.figure()
        if x is None:
            plt.plot(v_1, "-")
            plt.plot(v_2, "--")
        else:
            plt.plot(x, v_1, "-")
            plt.plot(x, v_2, "--")
        plt.legend()
        plt.show()


class TestExponentialDistributionSampler(TestSampler):
    """
    Test truncated exponential distribution sampler.
    """

    def test_sample_exponential_unit_range(self):
        """
        Test that this sampler correctly limits the samples to the [0, t] range.
        """
        parameters = [-0.1, 0.0, 0.001, 0.1, 1.0, 10.0]
        truncation_points = [0.25, 0.5, 0.75, 1.0]

        for t in truncation_points:
            x = np.linspace(0, t, 200)
            for b in parameters:

                with self.subTest(b=b):
                    # Generate distribution from samples.
                    samples = np.array(
                        tuple(
                            sample_truncated_exponential(lambda_=b, t=t)
                            for _ in range(100000)
                        )
                    )
                    _, sample_distribution = self._distribution_from_samples(
                        samples, bins=200, right_truncation_point=t
                    )

                    # Check that the samples are in the unit range [0, 1]
                    self.assertTrue(np.all(samples >= 0))
                    self.assertTrue(np.all(samples <= t))

                    # Generate distribution according to function.
                    y = np.exp(-b * x)
                    # Normalise distribution.
                    y /= sum(y)
                    np.testing.assert_almost_equal(sample_distribution, y, decimal=2)


class TestGammaDistributionSampler(TestSampler):
    """
    Verify the generation of samples from the right truncated gamma distribution.

    References:
        [1]: A. Philippe, Stat. Comp. 7, 173 ('97).
    """

    def test_number_of_operations_choice(self):
        """
        Compare the choices of number of operations with those in Table 1, Ref. [1].
        """
        self.assertEqual(_choose_number_of_components_right_truncated_gamma(0.1), 2)
        self.assertEqual(_choose_number_of_components_right_truncated_gamma(1.0), 4)
        self.assertEqual(_choose_number_of_components_right_truncated_gamma(5.0), 10)
        self.assertEqual(_choose_number_of_components_right_truncated_gamma(10.0), 16)

    def test_g(self):
        """
        Test that the series in `g` converges to the truncated gamma distribution.

        I.e., the lim n-> inf g_n(x) = gamma-(x)
        """
        parameters = [
            (0.1, 0.1, 4),
            (10, 1, 8),
            (0.1, 10, 32),
        ]
        # Ignore x=0, which is a singular point when a < 1.
        x = np.linspace(0, 1, 100)[1:]

        # Do the test for each set of the parameters.
        for a, b, N in parameters:
            with self.subTest(a=a, b=b, N=N):
                y = g(x, a, b, N)
                f_min = truncated_gamma_distribution(x, a, b)
                np.testing.assert_almost_equal(y, f_min, decimal=2)

    def test_g_sampler(self):
        """
        Test that the g function sampler converges to the distribution.
        """
        parameters = [(10.1, 0.1, 4), (1.1, 0.1, 8), (1.1, 10.1, 4)]
        x = np.linspace(0, 1, 100)

        for a, b, N in parameters:
            # Generate distribution from samples.
            samples = np.array(tuple(sample_g(a, b, N) for _ in range(100000)))
            _, sample_distribution = self._distribution_from_samples(samples)

            # Generate distribution according to function.
            y = g(x, a, b, N)
            # Normalise distribution.
            y /= sum(y)

            # The distributions must coincide, for parameters that give a sufficiently
            # smooth distribution.
            with self.subTest(a=a, b=b, N=N):
                # Ignore x=0, because technically this is a singular point.
                np.testing.assert_almost_equal(
                    sample_distribution[1:], y[1:], decimal=2
                )

    def test_input_truncated_gamma_distribution_sampler(self):
        """
        Test the sampler's handling of arrays.
        """
        a = np.arange(1, 4)
        b = np.arange(4, 7)

        # Generate samples directly using the array.
        self.reset_random_state()
        x_array = sample_right_truncated_gamma_distribution(a, b)

        # Generated samples pair-by-pair.
        self.reset_random_state()
        x_individual = []
        for a_i, b_i in zip(a, b):
            x_individual.append(sample_right_truncated_gamma_distribution(a_i, b_i))

        # Make sure that the samples are generated pair-wise from the arrays [i.e.,
        # (a_i, b_i) instead of (a_i, b_j) for all pairs (i, j).]
        np.testing.assert_array_equal(x_array, x_individual)

    def test_convergence_interval_truncated_gamma_distribution_sampler(self):
        """
        Test the generation of samples on various intervals [t<, 1] and a > 1.
        """
        parameters = [
            # Positive values of b.
            (10.1, 0.1),
            (1.1, 0.1),
            (2.1, 8.1),
            # Negative values of b.
            (10.1, -0.1),
            (1.1, -0.1),
            (2.1, -2.5),
        ]
        t_lower = 0.5
        x = np.linspace(t_lower, 1, 100)

        for a, b in parameters:
            # Generate distribution of samples.
            samples = np.array(
                tuple(
                    sample_interval_truncated_gamma_distribution(a, b, t_lower)
                    for _ in range(100000)
                )
            )
            _, sample_distribution = self._distribution_from_samples(
                samples, left_truncation_point=t_lower, right_truncation_point=1.0
            )

            # Generate distribution according to function.
            y = interval_truncated_gamma_distribution(x, a, b, t_left=t_lower)
            # Normalise distribution.
            y /= sum(y)

            # The distributions must coincide, for parameters that give a sufficiently
            # smooth distribution.
            with self.subTest(a=a, b=b):
                np.testing.assert_almost_equal(sample_distribution, y, decimal=2)

    def test_convergence_truncated_gamma_distribution_sampler(self):
        """
        Test the convergence of the right truncated gamma samples to its distribution.
        """
        parameters = [
            # Positive values of b.
            (10.1, 0.1),
            (1.1, 0.1),
            (0.5, 1.0),
            (2.1, 8.1),
            # Negative values of b.
            (10.1, -0.1),
            (1.1, -0.1),
            (2.1, -2.5),
            # Edge case, for problems with
            # `sample_right_truncated_gamma_distribution_positive_b`.
            (1.0, 0.0),
        ]
        # Tolerance of numerical calculation.
        decimals = 2

        truncation_points = np.array([0.5, 1.0, 2.0, 5.0])
        for t in truncation_points:
            with self.subTest(truncation_point=t):
                # Determine how many samples for given precision (`decimals`).
                grid_points = int(ceil(t)) * 10 ** (decimals + 1)
                num_samples = grid_points * 10 ** decimals

                for a, b in parameters:
                    # Generate distribution of samples.
                    samples = np.array(
                        tuple(
                            sample_right_truncated_gamma_distribution(a, b, t)
                            for _ in range(num_samples)
                        )
                    )
                    bins, cumul_distrib = self._cumulative_distribution_from_samples(
                        samples, bins=grid_points, right_truncation_point=t
                    )
                    x_centre = (bins[1:] + bins[:-1]) / 2.0

                    # The cumulative histogram of the samples should converge to the
                    # cumulative distribution.
                    with self.subTest(a=a, b=b):
                        np.testing.assert_almost_equal(
                            cumul_distrib,
                            truncated_gamma_cumulative_distribution(x_centre, a, b, t),
                            decimal=decimals,
                        )
