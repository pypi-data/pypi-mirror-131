from unittest import TestCase

from numpy import (
    array,
    concatenate,
    e,
    errstate,
    exp,
    float64,
    isnan,
    linspace,
    nan,
    pi,
    prod,
    random,
    testing,
)
import pandas as pd
from pandas.testing import assert_series_equal

from harmoniums import SurvivalHarmonium
from harmoniums.distributions import (
    normalisation_gamma_interval_distribution as normalisation,
)
from harmoniums.test.test_survival import TestSuperimposedgamma


class TestDiscriminateAnalyticallyTime(TestCase):
    """
    Test predict functions against analytical expressions.

    Consider only the time-to-event variables.
    """

    def setUp(self):
        """
        Set specific parameters that make it analytically tractable.
        """
        random.seed(1234)

        # Our model: p_1 * p_2 + p'_1 * p'_2,
        # where the parameters for the first term are:
        self.alpha = array([e, e ** 2]).reshape(-1, 1)
        self.beta = array([1 / e, 1 / e ** 2]).reshape(-1, 1)

        # And for the second term, we define:
        # \alpha'= \alpha + \Delta \alpha;
        # (Note that \Delta \alpha must be positive because of |V|).
        delta_alpha = array([pi, 0.75 * pi]).reshape(-1, 1)
        self.alpha_prime = self.alpha + delta_alpha
        # \beta' = \beta + \Delta \beta.
        delta_beta = array([1.0, 1.2]).reshape(-1, 1)
        self.beta_prime = self.beta + delta_beta

        # Set parameters of the model to match the alpha and beta above.
        self.harmonium = SurvivalHarmonium(
            survival_columns=[0, 1],
            event_columns=[2, 3],
            n_hidden_units=1,
            n_event_units=2,
        )
        self.harmonium.initialise_parameters()
        self.harmonium.c = self.alpha - 1
        self.harmonium.a_B = self.beta
        self.harmonium.V = delta_alpha
        self.harmonium.W_B = delta_beta
        self.harmonium.b = array([[0.0]], dtype=float64, order="C")
        self.harmonium.is_parameters_initialised_ = True
        self.harmonium.risk_score_time_point_ = (0.5, 0.5)

        # Verify that the settings were correctly set.
        H = array([[0], [1]])
        a, b = self.harmonium.alpha_beta(H)
        testing.assert_array_equal(a[0], self.alpha.flatten())
        testing.assert_array_equal(a[1], self.alpha_prime.flatten())
        testing.assert_array_equal(b[0], self.beta.flatten())
        testing.assert_array_equal(b[1], self.beta_prime.flatten())

    def p_tilde(self, x, a, b):
        """ Unnormalised probability density. """
        return x ** (a - 1) * exp(-b * x)

    def p_exact_x1_cond_x2_observed(self, t, phase_factor: float = 1.0):
        r"""
        Evaluate analytically p(x_1|x_2) for a single latent state.

        In terms of the unnormalised probabilities:
        p(x_1|x_2)
            = \tilde{p}(x_1, x_2) / \tilde{p}(x_2).

        The extra phase factor corresponds to additional conditioning on other
        variables,  i.e., p(x_1|x_2, x_i)):
            phase_factor = exp[-sum_i x_i W_i1 h_1] with h_1=1.
        (for h_1=0 the phase is trivially zero.)
        """
        # 1) Calculate \tilde{p}(x_1, x_2).
        numerator = prod(self.p_tilde(t, self.alpha, self.beta)) + phase_factor * prod(
            self.p_tilde(t, self.alpha_prime, self.beta_prime)
        )

        # b) Calculate \tilde{p}(x_2).
        denominator = (
            # Integral dx_1 over [0, 1].
            normalisation(self.alpha, self.beta)[0]
            * self.p_tilde(t, self.alpha, self.beta)[1]
            # Integral dx_1 over [0, 1].
            + phase_factor
            * normalisation(self.alpha_prime, self.beta_prime)[0]
            * self.p_tilde(t, self.alpha_prime, self.beta_prime)[1]
        )
        return numerator / denominator

    def p_exact_x1_cond_x2_censored(self, t, phase_factor: float = 1.0):
        r"""
        Evaluate analytically p(x_1|x_2 > t_2) for a single latent state.

        In terms of the unnormalised probabilities:
        p(x_1|x_2 > t_2)
            = \tilde{p}(x_1, x_2 > t_2) / \tilde{p}(x_2 > t_2).

        The extra phase corresponds to additional conditioning on other
        variables,  i.e., p(x_1|x_2 > t_2, x_i)):
            phase_factor = exp[-sum_i x_i W_i1 h_1] with h_1=1.
        (for h_1=0 the phase is trivially zero.)
        """
        # 1) Calculate \tilde{p}(x_1, x_2 > t_2).
        numerator = (
            self.p_tilde(t, self.alpha, self.beta)[0]
            # Integral over x_2 from [t_2, 1]
            * normalisation(self.alpha, self.beta, t_left=t)[1]
            + phase_factor * self.p_tilde(t, self.alpha_prime, self.beta_prime)[0]
            # Integral over x_2 from [t_2, 1]
            * normalisation(self.alpha_prime, self.beta_prime, t_left=t)[1]
        )
        # 2) Calculate \tilde{p}(x_2 > t_2).
        denominator = (
            # Integral dx_1 over [0, 1].
            normalisation(self.alpha, self.beta)[0]
            # Integral over x_2 from [t_2, 1]
            * normalisation(self.alpha, self.beta, t_left=t)[1]
            # Integral dx_1 over [0, 1].
            + phase_factor * normalisation(self.alpha_prime, self.beta_prime)[0]
            # Integral over x_2 from [t_2, 1]
            * normalisation(self.alpha_prime, self.beta_prime, t_left=t)[1]
        )
        return numerator / denominator

    def S_exact_x1_cond_x2_observed(self, t, phase_factor: float = 1.0):
        r"""
        Evaluate analytically p(x_1 > t_1|x_2).

        In terms of the unnormalised probabilities:
        p(x_1 > t_1|x_2)
            = \tilde{p}(x_1 > t_1, x_2) / \tilde{p}(x_2).

        The extra phase corresponds to additional conditioning on other
        variables,  i.e., p(x_1 > t_1 |x_2, x_i)):
            phase_factor = exp[-sum_i x_i W_i1 h_1] with h_1=1.
        (for h_1=0 the phase is trivially zero.)
        """
        # 1) Calculate \tilde{p}(x_1 > t_1, x_2).
        numerator = (
            # Integral dx_1 over [t_1, 1].
            normalisation(self.alpha, self.beta, t_left=t)[0]
            * self.p_tilde(t, self.alpha, self.beta)[1]
            # Additional h=1 phase coming from conditioning on other variables.
            # Integral dx_1 over [t_1, 1].
            + phase_factor
            * normalisation(self.alpha_prime, self.beta_prime, t_left=t)[0]
            * self.p_tilde(t, self.alpha_prime, self.beta_prime)[1]
        )
        # b) Calculate \tilde{p}(x_2).
        denominator = (
            # Integral dx_1 over [0, 1].
            normalisation(self.alpha, self.beta)[0]
            * self.p_tilde(t, self.alpha, self.beta)[1]
            # Integral dx_1 over [0, 1].
            + phase_factor
            * normalisation(self.alpha_prime, self.beta_prime)[0]
            * self.p_tilde(t, self.alpha_prime, self.beta_prime)[1]
        )
        return numerator / denominator

    def S_exact_x1_cond_x2_censored(self, t, phase_factor: float = 1.0):
        r"""
        Evaluate analytically p(x_1 > t_1|x_2 > t_2).

        In terms of the unnormalised probabilities:
        p(x_1 > t_1|x_2 > t_2)
          = \tilde{p}(x_1 > t_1, x_2 > t_2) / \tilde{p}(x_2 > t_2).

        The extra phase corresponds to additional conditioning on other
        variables,  i.e., p(x_1 > t_1 |x_2 > t_2, x_i)):
            phase_factor = exp[-sum_i x_i W_i1 h_1] with h_1=1.
        (for h_1=0 the phase is trivially zero.)
        """
        # 1) Calculate \tilde{p}(x_1 > t_1, x_2 > t_2).
        numerator = prod(
            normalisation(self.alpha, self.beta, t_left=t)
        ) + phase_factor * prod(
            normalisation(self.alpha_prime, self.beta_prime, t_left=t)
        )
        # 2) Calculate \tilde{p}(x_2 > t_2).
        denominator = (
            # Integral dx_1 over [0, 1].
            normalisation(self.alpha, self.beta)[0]
            # Integral over x_2 from [t_2, 1]
            * normalisation(self.alpha, self.beta, t_left=t)[1]
            # Integral dx_1 over [0, 1].
            + phase_factor * normalisation(self.alpha_prime, self.beta_prime)[0]
            # Integral over x_2 from [t_2, 1]
            * normalisation(self.alpha_prime, self.beta_prime, t_left=t)[1]
        )
        return numerator / denominator

    def test_predict_proba_no_censor(self):
        """
        Test that p(x_1|x_2) (i.e., no censoring) equals analytic expr.
        """
        t = random.uniform(size=(2, 1))
        # No censoring (everything observed).
        event = array([[1, 1]])
        X = concatenate([t.T, event], axis=1)
        p_analytic = self.p_exact_x1_cond_x2_observed(t)

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # Verify correctness with harmonium `predict_proba` function.
                testing.assert_almost_equal(
                    p_analytic,
                    self.harmonium.predict_proba(X, survival_distribution=False)[:, 0],
                )

    def test_predict_proba_condition_censor(self):
        """
        Test that p(x_1|x_2 > t_2) (i.e., x_2 censored) equals analytic expr.
        """
        t = random.uniform(size=(2, 1))
        # Censor x_2 observation.
        event = array([[1, 0]])
        X = concatenate([t.T, event], axis=1)

        p_analytic = self.p_exact_x1_cond_x2_censored(t)

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # Verify correctness with harmonium `predict_proba` function.
                testing.assert_almost_equal(
                    p_analytic,
                    self.harmonium.predict_proba(X, survival_distribution=False)[:, 0],
                )

    def test_predict_survival_observed(self):
        """
        Test survival distribution p(x_1 > t_1|x_2) equals analytic expr.

        That is, x_2 is observed.
        """
        t = random.uniform(size=(2, 1))
        event = array([[1, 1]])
        X = concatenate([t.T, event], axis=1)

        S_analytic = self.S_exact_x1_cond_x2_observed(t)

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # Verify correctness with harmonium `predict` function.
                testing.assert_almost_equal(
                    S_analytic, self.harmonium.predict_proba(X)[:, 0]
                )

    def test_predict_survival_condition_censor(self):
        """
        Test survival distribution p(x_1 > t_1|x_2 > t_2) equals analytic expr.

        That is, x_2 is censored at t_2.
        """
        t = random.uniform(size=(2, 1))
        event = array([[1, 0]])  # Censor x_2 observation.
        X = concatenate([t.T, event], axis=1)

        S_analytic = self.S_exact_x1_cond_x2_censored(t)

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # Verify correctness with harmonium `predict` function.
                testing.assert_almost_equal(
                    S_analytic, self.harmonium.predict_proba(X)[:, 0]
                )


class TestDiscriminateCategory(TestDiscriminateAnalyticallyTime, TestCase):
    """
    Test predict against analytical expressions with a category.
    """

    def setUp(self):
        """
        Expand harmonium to include one categorical variable.
        """
        super().setUp()
        self.harmonium.n_categorical_units = 1
        self.harmonium.categorical_columns = [4]
        self.harmonium.a_A = random.uniform(size=(1, 1))
        self.harmonium.W_A = random.normal(size=(1, 1))

    def test_predict_proba_no_censor(self):
        """
        Test that p(x_1|x_2, x_cat) equals analytic expr.
        """
        t = random.uniform(size=(2, 1))
        # No event censoring (everything observed).
        event = array([[1, 1]])

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # 1)
                # Missing categorical value.
                category = array([[nan]])
                X = concatenate([t.T, event, category], axis=1)

                # Test that marginalising the missing value accounts for the
                # following phase.
                phase_factor = (
                    (exp(-self.harmonium.W_A - self.harmonium.a_A) + 1)
                    / (1 + exp(-self.harmonium.a_A))
                ).flatten()

                p_analytic = self.p_exact_x1_cond_x2_observed(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic,
                    self.harmonium.predict_proba(X, survival_distribution=False)[:, 0],
                )

                # 2)
                # Observed categorical value.
                category = array([[1]])
                X = concatenate([t.T, event, category], axis=1)

                # Test that the observation accounts for the following phase.
                phase_factor = float(exp(-category @ self.harmonium.W_A))
                p_analytic = self.p_exact_x1_cond_x2_observed(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic,
                    self.harmonium.predict_proba(X, survival_distribution=False)[:, 0],
                )

    def test_predict_proba_condition_censor(self):
        """
        Test that p(x_1|x_2 > t_2, x_cat) equals analytic expr.

        That is, x_2 is censored at t_2.
        """
        t = random.uniform(size=(2, 1))
        # Censor x_2 observation.
        event = array([[1, 0]])

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # 1)
                # Missing categorical value.
                category = array([[nan]])
                X = concatenate([t.T, event, category], axis=1)

                # Test that marginalising the missing value accounts for the
                # following phase.
                phase_factor = (
                    (exp(-self.harmonium.W_A - self.harmonium.a_A) + 1)
                    / (1 + exp(-self.harmonium.a_A))
                ).flatten()
                p_analytic = self.p_exact_x1_cond_x2_censored(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic,
                    self.harmonium.predict_proba(X, survival_distribution=False)[:, 0],
                )

                # 2)
                # Observed categorical value.
                category = array([[1]])
                X = concatenate([t.T, event, category], axis=1)

                # Test that the observation accounts for the following phase.
                phase_factor = float(exp(-category @ self.harmonium.W_A))
                p_analytic = self.p_exact_x1_cond_x2_censored(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic,
                    self.harmonium.predict_proba(X, survival_distribution=False)[:, 0],
                )

    def test_predict_survival_observed(self):
        """
        Test p(x_1 > t_1|x_2,x_cat) equals analytic expr.

        That is, the survival distribution conditioned on a categorical variable
        and x_2 that is observed.
        """
        t = random.uniform(size=(2, 1))
        event = array([[1, 1]])

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # 1)
                # Missing categorical value.
                category = array([[nan]])
                X = concatenate([t.T, event, category], axis=1)

                # Test that marginalising the missing value accounts for the
                # following phase.
                phase_factor = (
                    (exp(-self.harmonium.W_A - self.harmonium.a_A) + 1)
                    / (1 + exp(-self.harmonium.a_A))
                ).flatten()
                p_analytic = self.S_exact_x1_cond_x2_observed(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic, self.harmonium.predict_proba(X)[:, 0]
                )

                # 2)
                # Observed categorical value.
                category = array([[1]])
                X = concatenate([t.T, event, category], axis=1)

                # Test that the observation accounts for the following phase.
                phase_factor = float(exp(-category @ self.harmonium.W_A))
                p_analytic = self.S_exact_x1_cond_x2_observed(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic, self.harmonium.predict_proba(X)[:, 0]
                )

    def test_predict_survival_condition_censor(self):
        """
        Test  p(x_1 > t_1|x_2 > t_2,x_cat) equals analytic expr.

        That is, the survival distribution conditioned on a categorical variable
        and x_2 that is censored at t_2.
        """
        t = random.uniform(size=(2, 1))
        event = array([[1, 0]])  # Censor x_2 observation.

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # 1)
                # Missing categorical value.
                category = array([[nan]])
                X = concatenate([t.T, event, category], axis=1)

                # Test that marginalising the missing value accounts for the
                # following phase.
                phase_factor = (
                    (exp(-self.harmonium.W_A - self.harmonium.a_A) + 1)
                    / (1 + exp(-self.harmonium.a_A))
                ).flatten()
                p_analytic = self.S_exact_x1_cond_x2_censored(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic, self.harmonium.predict_proba(X)[:, 0]
                )

                # 2)
                # Observed categorical value.
                category = array([[1]])
                X = concatenate([t.T, event, category], axis=1)

                # Test that the observation accounts for the following phase.
                phase_factor = float(exp(-category @ self.harmonium.W_A))
                p_analytic = self.S_exact_x1_cond_x2_censored(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic, self.harmonium.predict_proba(X)[:, 0]
                )


class TestDiscriminateNumeric(TestDiscriminateAnalyticallyTime, TestCase):
    """
    Test predict against analytical exprs with numeric values.
    """

    def setUp(self):
        """
        Expand harmonium to include one numeric variable.
        """
        super().setUp()
        self.harmonium.numeric_columns = [4]
        self.harmonium.n_numeric_units = 1
        self.harmonium.sigma = array([[1.0]], dtype=float64, order="C")
        self.harmonium.a_C = random.normal(size=(1, 1))
        self.harmonium.W_C = random.normal(size=(1, 1))

    def test_predict_proba_no_censor(self):
        """
        Test that p(x_1|x_2, x_num) equals analytic expr.
        """
        t = random.uniform(size=(2, 1))
        # No censoring (everything observed).
        event = array([[1, 1]])

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # 1)
                # Missing numeric value.
                numeric = array([[nan]])
                X = concatenate([t.T, event, numeric], axis=1)

                # Test that marginalising the missing value accounts for the following
                # phase.
                # integral_(-∞)^∞ exp(-1/2 (x - a)^2 - x w h) dx
                #   = sqrt(2 π) e^(1/2 h w (h w - 2 a))
                phase_factor = float(
                    exp(
                        self.harmonium.W_C
                        * (self.harmonium.W_C - 2 * self.harmonium.a_C)
                        / 2
                    )
                )
                p_analytic = self.p_exact_x1_cond_x2_observed(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic,
                    self.harmonium.predict_proba(X, survival_distribution=False)[:, 0],
                )

                # 2)
                # Observed numeric value.
                numeric = random.normal(size=(1, 1))
                X = concatenate([t.T, event, numeric], axis=1)

                # Test that the observation accounts for the following phase.
                phase_factor = float(exp(-numeric @ self.harmonium.W_C))
                p_analytic = self.p_exact_x1_cond_x2_observed(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic,
                    self.harmonium.predict_proba(X, survival_distribution=False)[:, 0],
                )

    def test_predict_proba_condition_censor(self):
        """
        Test that p(x_1|x_2 > t_2, x_num) equals analytic expr.

        That is, x_2 is censored at t_2.
        """
        t = random.uniform(size=(2, 1))
        # Censor x_2 observation.
        event = array([[1, 0]])

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # 1)
                # Missing numeric value.
                numeric = array([[nan]])
                X = concatenate([t.T, event, numeric], axis=1)

                # Test that marginalising the missing value accounts for the following
                # phase.
                # integral_(-∞)^∞ exp(-1/2 (x - a)^2 - x w h) dx
                #   = sqrt(2 π) e^(1/2 h w (h w - 2 a))
                phase_factor = float(
                    exp(
                        self.harmonium.W_C
                        * (self.harmonium.W_C - 2 * self.harmonium.a_C)
                        / 2
                    )
                )
                p_analytic = self.p_exact_x1_cond_x2_censored(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic,
                    self.harmonium.predict_proba(X, survival_distribution=False)[:, 0],
                )

                # 2)
                # Observed numeric value.
                numeric = random.normal(size=(1, 1))
                X = concatenate([t.T, event, numeric], axis=1)

                # Test that the observation accounts for the following phase.
                phase_factor = float(exp(-numeric @ self.harmonium.W_C))
                p_analytic = self.p_exact_x1_cond_x2_censored(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic,
                    self.harmonium.predict_proba(X, survival_distribution=False)[:, 0],
                )

    def test_predict_survival_observed(self):
        """
        Test p(x_1 > t_1|x_2,x_num) equals analytic expr.

        That is, the survival distribution conditioned on a numeric variable and
        x_2 that is observed.
        """
        t = random.uniform(size=(2, 1))
        event = array([[1, 1]])

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # 1)
                # Missing numeric value.
                numeric = array([[nan]])
                X = concatenate([t.T, event, numeric], axis=1)

                # Test that marginalising the missing value accounts for the following
                # phase.
                # integral_(-∞)^∞ exp(-1/2 (x - a)^2 - x w h) dx
                #   = sqrt(2 π) e^(1/2 h w (h w - 2 a))
                phase_factor = float(
                    exp(
                        self.harmonium.W_C
                        * (self.harmonium.W_C - 2 * self.harmonium.a_C)
                        / 2
                    )
                )
                p_analytic = self.S_exact_x1_cond_x2_observed(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic, self.harmonium.predict_proba(X)[:, 0]
                )

                # 2)
                # Observed numeric value.
                numeric = random.normal(size=(1, 1))
                X = concatenate([t.T, event, numeric], axis=1)

                # Test that the observation accounts for the following phase.
                phase_factor = float(exp(-numeric @ self.harmonium.W_C))
                p_analytic = self.S_exact_x1_cond_x2_observed(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic, self.harmonium.predict_proba(X)[:, 0]
                )

    def test_predict_survival_condition_censor(self):
        """
        Test  p(x_1 > t_1|x_2 > t_2,x_num=nan) equals analytic expr.

        That is, the survival distribution conditioned on a missing numeric
        variable and x_2 that is censored at t_2.
        """
        t = random.uniform(size=(2, 1))
        event = array([[1, 0]])  # Censor x_2 observation.

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.harmonium._hidden_state_partition_function_sum,
            self.harmonium._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.harmonium._hidden_state_partition_function = method

                # 1)
                # Missing numeric value.
                numeric = array([[nan]])
                X = concatenate([t.T, event, numeric], axis=1)

                # Test that marginalising the missing value accounts for the following
                # phase.
                # integral_(-∞)^∞ exp(-1/2 (x - a)^2 - x w h) dx
                #   = sqrt(2 π) e^(1/2 h w (h w - 2 a))
                phase_factor = float(
                    exp(
                        self.harmonium.W_C
                        * (self.harmonium.W_C - 2 * self.harmonium.a_C)
                        / 2
                    )
                )
                p_analytic = self.S_exact_x1_cond_x2_censored(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic, self.harmonium.predict_proba(X)[:, 0]
                )

                # 2)
                # Observed numeric value.
                numeric = random.normal(size=(1, 1))
                X = concatenate([t.T, event, numeric], axis=1)

                # Test that the observation accounts for the following phase.
                phase_factor = float(exp(-numeric @ self.harmonium.W_C))
                p_analytic = self.S_exact_x1_cond_x2_censored(t, phase_factor)
                testing.assert_almost_equal(
                    p_analytic, self.harmonium.predict_proba(X)[:, 0]
                )


class TestDiscriminativeEdgeCases(TestSuperimposedgamma, TestCase):
    """
    Test the discriminative probability and survival calculations on boundaries.
    """

    def setUp(self):
        super().setUp()
        model_parameters = self.default_parameters
        model_parameters.update(
            {
                "learning_rate": 1.0,
                "mini_batch_size": 500,
                "n_epochs": 200,
                "weight_decay": 1e-4,
                "momentum_fraction": 0.1,
                "categorical_columns": ["category"],
                "numeric_columns": ["numeric"],
                "dry_run": True,
            }
        )
        self.model = SurvivalHarmonium(**model_parameters)
        # Initialise model parameters using a few records.
        X, _ = self.dataset.load(m=10)
        self.model.fit(X)

    def _constant_dataset(self, m: int = 100) -> pd.DataFrame:
        """
        Make a dataset of m identical records.
        """
        x, _ = self.dataset.load(m=1)
        data = pd.DataFrame(columns=x.columns, index=range(m))
        # Fill columns with the single value.
        for c in x.columns:
            data[c] = x.iloc[0][c]

        return data

    def test_zero_measure_proba_singletons_survival(self):
        """
        Test that the probability for event with measure zero does not blow up.
        """
        X = pd.DataFrame(
            {
                "category": [0],
                "numeric": [0],
                # A survival function at t_0=1 is exactly 0.
                "t_0": [1],
                "t_1": [0.5],
                "event_0": [False],
                "event_1": [True],
            },
        )

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.model._hidden_state_partition_function_sum,
            self.model._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.model._hidden_state_partition_function = method

                with errstate(all="raise"):
                    P = self.model._proba_singletons(X, survival_distribution=True)

                self.assertEqual(P[0, 0], 0)

    def test_normalisation_proba_singletons_survival(self):
        """
        Test that the survival distribution from `proba` is normalised.
        """
        # Make a constant array so that we can compare S(x_i|o\o_i) for constant
        # o\o_i.
        m = 100
        X = self._constant_dataset(m)

        # Calculate p(x_0|o\o_0) for x_0 in (0, 1].
        X0 = X.copy()
        X0["t_0"] = linspace(0, 1, m)

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.model._hidden_state_partition_function_sum,
            self.model._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.model._hidden_state_partition_function = method

                with errstate(all="raise"):
                    S_t0 = self.model._proba_singletons(X0, survival_distribution=True)

                # Test S(x_0=0|o\o_0) = 1 and S(x_1=1|o\o_0) = 0.
                self.assertEqual(S_t0[0, 0], 1.0)
                self.assertEqual(S_t0[-1, 0], 0.0)
                self.assertFalse(isnan(S_t0).any())

                # Now do the same for the other coordinate.
                X1 = X.copy()
                X1["t_1"] = linspace(0, 1, m)
                with errstate(all="raise"):
                    S_t1 = self.model._proba_singletons(X1, survival_distribution=True)

                # Test S(x_1=0|o\o_1) = 1 and S(x_1=1|o\o_1) = 0.
                self.assertEqual(S_t1[0, 1], 1.0)
                self.assertEqual(S_t1[-1, 1], 0.0)
                self.assertFalse(isnan(S_t1).any())

    def test_normalisation_proba_singletons_density(self):
        """
        Test that the probability density from `proba` is normalised.
        """
        # Make a constant array so that we can compare p(x_i|o\o_i) for constant
        # o\o_i.
        m = 100
        X = self._constant_dataset(m)

        # Calculate p(x_0|o\o_0) for x_0 in (0, 1].
        X0 = X.copy()
        X0["t_0"] = linspace(1e-16, 1, m)

        # Test the computation using both the sum and integral method.
        computation_methods = (
            self.model._hidden_state_partition_function_sum,
            self.model._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                self.model._hidden_state_partition_function = method

                with errstate(all="raise"):
                    p_t0 = self.model._proba_singletons(X0, survival_distribution=False)

                self.assertFalse(isnan(p_t0).any())
                # Test that p is normalised, up to order of grid spacing.
                dt = 1.0 / m
                self.assertLess(dt * p_t0[:, 0].sum() - 1, dt)

                # Now do the same for the other coordinate.
                X1 = X.copy()
                X1["t_1"] = linspace(1e-16, 1, m)
                with errstate(all="raise"):
                    p_t1 = self.model._proba_singletons(X1, survival_distribution=False)

                self.assertLess(dt * p_t1[:, 1].sum() - 1, dt)
                self.assertFalse(isnan(p_t1).any())


class TestScoreConsistency(TestSuperimposedgamma, TestCase):
    def setUp(self):
        super().setUp()
        self.params_t0_t1 = self.default_parameters
        self.params_t0_t1.update(
            {
                "learning_rate": 1.0,
                "mini_batch_size": 500,
                "n_epochs": 200,
                "weight_decay": 1e-4,
                "momentum_fraction": 0.1,
                "categorical_columns": ["category"],
                "numeric_columns": ["numeric"],
            }
        )
        # Model that only takes into account `t_0`.
        self.params_t0 = self.params_t0_t1.copy()
        self.params_t0.update(
            {"survival_columns": ["t_0"], "event_columns": ["event_0"]}
        )

    def test_score_no_labels(self):
        """
        Test that score doesn't secretly use the labels.
        """
        X, _ = self.dataset.load(m=100)
        model = SurvivalHarmonium(
            # Initialise but don't train model.
            dry_run=True,
            **self.params_t0_t1,
        ).fit(X)

        # Test the computation using both the sum and integral method.
        computation_methods = (
            model._hidden_state_partition_function_sum,
            model._hidden_state_partition_function_integral,
        )
        for method in computation_methods:
            with self.subTest(computation_method=method):
                # Monkey patch the computation method before doing the
                # calculation.
                model._hidden_state_partition_function = method

                S = model.predict(X, time_point="all")

                # Removing the values of time-to-event variable `t_0` may not change the
                # predictions S(x_0|o_{-0}) for that variable (but it can for the other
                # variable, because the risk is conditioned on it).
                X_conceal0 = X.copy()
                X_conceal0[model.survival_columns[:1] + model.event_columns[:1]] = 0
                S_conceal0 = model.predict(X_conceal0, time_point="all")
                assert_series_equal(S["t_0"], S_conceal0["t_0"])

                # And vice versa for the other variable.
                X_conceal1 = X.copy()
                X_conceal1[model.survival_columns[1:] + model.event_columns[1:]] = 0
                S_conceal1 = model.predict(X_conceal1, time_point="all")
                assert_series_equal(S["t_1"], S_conceal1["t_1"])

    def test_decoupled_score(self):
        """
        Test that decoupled `t_1` variable does not affect concordance score.
        """
        X, _ = self.dataset.load(m=100)

        self.reset_random_state()
        model_t0_and_t1 = SurvivalHarmonium(
            # Initialise but don't train model.
            dry_run=True,
            **self.params_t0_t1,
        ).fit(X)

        self.reset_random_state()
        model_t0 = SurvivalHarmonium(
            # Initialise but don't train model.
            dry_run=True,
            **self.params_t0,
        ).fit(X)

        # Decouple `t_1` parameter.
        model_t0_and_t1.V[1, :] = 0
        model_t0_and_t1.c[1, :] = 0
        model_t0_and_t1.W_B[1, :] = 0
        model_t0_and_t1.a_B[1, :] = 0
        # Make first parameter settings identical.
        model_t0_and_t1.V[0, :] = model_t0.V
        model_t0_and_t1.c[0, :] = model_t0.c
        model_t0_and_t1.W_B[0, :] = model_t0.W_B
        model_t0_and_t1.a_B[0, :] = model_t0.a_B

        model_t0_and_t1.W_C = model_t0.W_C.copy()
        model_t0_and_t1.a_C = model_t0.a_C.copy()

        # Test the computation using both the sum and integral method.
        computation_methods = (
            "_hidden_state_partition_function_sum",
            "_hidden_state_partition_function_integral",
        )
        for method_name in computation_methods:
            with self.subTest(computation_method=method_name):
                # Monkey patch the computation methods before doing the
                # calculation.
                model_t0._hidden_state_partition_function = getattr(
                    model_t0, method_name
                )
                model_t0_and_t1._hidden_state_partition_function = getattr(
                    model_t0_and_t1, method_name
                )

                # The concordance for `t_0` must be equal.
                self.assertEqual(
                    model_t0_and_t1.conditional_score(self.X), model_t0.score(self.X)
                )

    def test_score(self):
        """
        Test score conditioned on other non-informing survival variable.
        """
        # Dataset in which all variables are non-informative (t0 and t1 are
        # independend).
        X_no_info = self.dataset.load_group(0, m=100)

        self.reset_random_state()
        model_t0_and_t1 = SurvivalHarmonium(**self.params_t0_t1).fit(X_no_info)

        self.reset_random_state()
        model_t0 = SurvivalHarmonium(**self.params_t0).fit(X_no_info)

        # Test the computation using both the sum and integral method.
        computation_methods = (
            "_hidden_state_partition_function_sum",
            "_hidden_state_partition_function_integral",
        )
        for method_name in computation_methods:
            with self.subTest(computation_method=method_name):
                # Monkey patch the computation methods before doing the
                # calculation.
                model_t0._hidden_state_partition_function = getattr(
                    model_t0, method_name
                )
                model_t0_and_t1._hidden_state_partition_function = getattr(
                    model_t0_and_t1, method_name
                )

                scores_dict = model_t0_and_t1.conditional_score(
                    X_no_info, time_point="all"
                )
                testing.assert_array_almost_equal(
                    0.5, list(scores_dict.values()), decimal=1,
                )

                # Not a dict, because it is only one variable.
                testing.assert_almost_equal(
                    0.5,
                    model_t0.conditional_score(X_no_info, time_point="all"),
                    decimal=1,
                )
