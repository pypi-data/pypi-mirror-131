from abc import ABC, abstractmethod
from typing import Tuple
from unittest import TestCase

import numpy as np
from numpy import array, concatenate, copy, exp, log, ones_like, nan, random, zeros_like
from scipy.special import expit as sigmoid
from sklearn import datasets
from sklearn.utils import shuffle

from harmoniums import (
    BinaryHarmonium,
    CensorGammaHarmonium,
    GaussianHarmonium,
    SurvivalHarmonium,
)
from harmoniums.const import Matrix, MatrixTriplet
from harmoniums.test import TestHarmonium


class TestMultimodalReduction(ABC, TestHarmonium):
    """
    Test that the multimodal model can reduce to its individual model components.
    """

    def setUp(self):
        """
        Initialise multimodal model.
        """
        super().setUp()
        self.n_v = 2
        self.n_h = 3
        self.model_parameters = {
            "n_hidden_units": self.n_h,
            "metrics": tuple(),
        }

    @property
    @abstractmethod
    def parameter_map(self) -> dict:
        """
        Mapping of the reference parameter name to the multimodal parameter name.
        """

    def initialise_model_parameters(self, reference_model, multimodal_model):
        """
        Init reference model parameters, and copy the values to the multimodal model.
        """
        self.reset_model_parameters(reference_model, how="randomly")
        self.reset_model_parameters(multimodal_model, how="zeros")
        for param_ref, param_multimodal in self.parameter_map.items():
            param_matrix = getattr(reference_model, param_ref)
            setattr(multimodal_model, param_multimodal, copy(param_matrix))
        reference_model.visible_columns_ = reference_model.visible_columns
        setattr(reference_model, "parameters_initialised_", True)
        setattr(multimodal_model, "parameters_initialised_", True)

    @abstractmethod
    def as_triplet(self, X: Matrix) -> MatrixTriplet:
        """
        Generate multimodal triplet consistent with reference harmonium.
        """

    @abstractmethod
    def from_triplet(self, X: MatrixTriplet) -> Matrix:
        """
        Extract visible states `X` from multimodal triplet.
        """

    def generate_test_states(self) -> Tuple[MatrixTriplet, Matrix, Matrix]:
        """
        Generate binary visible and hidden states.
        """
        m = min(self.n_v ** 2, self.n_h ** 2)
        X = random.uniform(size=(m, self.n_v))
        H = random.uniform(size=(m, self.n_h))
        # Make sure that `X` and `H` have the same number of records.
        H = shuffle(H[:m])
        return self.as_triplet(X), X, H

    def test_free_energy_h(self):
        """
        Test that the latent state free energy F(H) coincide.
        """
        _, _, H = self.generate_test_states()
        np.testing.assert_array_almost_equal(
            self.reference_model.free_energy_h(H),
            self.multimodal_model.free_energy_h(H),
        )

    def test_energy(self):
        """
        Test that the binary model energy values coincide with the multimodal harmonium.
        """
        XI, X, H = self.generate_test_states()
        np.testing.assert_array_almost_equal(
            self.reference_model.energy(X, H),
            self.multimodal_model.energy(XI, H),
        )

    def test_energy_gradient(self):
        """
        Test that the gradient updates are the same.
        """
        XI, X, H = self.generate_test_states()
        dE_ref = self.reference_model.energy_gradient(X, H)
        dE_multimodal = self.multimodal_model.energy_gradient(XI, H)

        # Verifiy the gradient calculation of each parameter.
        for param_ref, param_multimodal in self.parameter_map.items():
            np.testing.assert_array_almost_equal(
                dE_ref[param_ref], dE_multimodal[param_multimodal]
            )

    def test_sample_h(self):
        """
        Test that the same latent states are sampled.
        """
        XI, X, _ = self.generate_test_states()

        self.reset_random_state()
        H_binary = self.reference_model.sample_h(X)

        self.reset_random_state()
        H_multimodal = self.multimodal_model.sample_h(XI)

        np.testing.assert_array_almost_equal(H_binary, H_multimodal)

    def test_sample_x(self):
        """
        Test that the same visible states are sampled.
        """
        _, _, H = self.generate_test_states()

        self.reset_random_state()
        X_binary = self.reference_model.sample_x(H)

        self.reset_random_state()
        X_multimodal = self.multimodal_model.sample_x(H)

        np.testing.assert_array_almost_equal(X_binary, self.from_triplet(X_multimodal))


class TestMultimodalTimeInvariantReduction:
    """
    Time-invariant model (group A and group C) specific tests.
    """

    def test_free_energy_x_observed(self):
        """
        Test that the (modified) free energy F(X) coincides in absence missing data.
        """
        _, X, _ = self.generate_test_states()

        # First check that the free energies coincide.
        np.testing.assert_array_almost_equal(
            self.reference_model.free_energy_x(X),
            self.multimodal_model.free_energy_x(X),
        )
        # Secondly, verify that the modified free energy reduces to the free energy when
        # everything is observed.
        np.testing.assert_array_almost_equal(
            self.reference_model.free_energy_x(X),
            self.multimodal_model.modified_free_energy_x(X),
        )

    def test_transform(self):
        """
        Test that visible units are transformed to the same latent states.
        """
        _, X, _ = self.generate_test_states()
        np.testing.assert_array_almost_equal(
            self.reference_model.transform(X),
            self.multimodal_model.transform(X),
        )

    def test_log_likelihood(self):
        """
        Test that the observed data are equally likely in both models.
        """
        _, X, _ = self.generate_test_states()
        np.testing.assert_array_almost_equal(
            self.reference_model.log_likelihood(X),
            self.multimodal_model.log_likelihood(X),
        )

    def test_free_energy_x_unobserved(self):
        """
        Test that the free energy equals the partition function without observations.
        """
        # All observations are nan (i.e., missing).
        X = np.full(fill_value=nan, shape=(1, self.n_v))
        np.testing.assert_array_almost_equal(
            exp(-self.multimodal_model.modified_free_energy_x(X)),
            self.reference_model.partition_function(),
        )


class TestMultimodalAsGauss(
    TestMultimodalReduction, TestMultimodalTimeInvariantReduction, TestCase
):
    """
    Test that the multimodal model can reduce to a Gaussian-binary harmonium.
    """

    parameter_map = {
        "W": "W_C",
        "a": "a_C",
        "b": "b",
        "sigma": "sigma",
    }

    def as_triplet(self, X: Matrix) -> MatrixTriplet:
        """
        Generate multimodal triplet consistent with Gaussian harmonium.
        """
        empty_shape = (X.shape[0], 0)
        return (array([]).reshape(empty_shape), array([]).reshape(empty_shape), X)

    def from_triplet(self, X: MatrixTriplet) -> Matrix:
        """
        Extract visible states `X` from multimodal triplet.
        """
        return X[2]

    def setUp(self):
        """
        Initialise models to have the same set of parameters.
        """
        super().setUp()
        column_indices = list(range(self.n_v))  # [0,..,n_v-1]
        self.multimodal_model = SurvivalHarmonium(
            numeric_columns=column_indices,
            n_numeric_units=self.n_v,
            **self.model_parameters
        )
        self.reference_model = GaussianHarmonium(
            visible_columns=column_indices,
            n_visible_units=self.n_v,
            **self.model_parameters
        )
        self.initialise_model_parameters(self.reference_model, self.multimodal_model)

    def generate_gaussian_test_data(
        self, mu, sigma, m: int = 10000, missing_data: bool = True
    ):
        """
        Generate Gaussian test data, with optionally missing observations.
        """
        X = random.normal(loc=mu, scale=sigma, size=(m, mu.shape[0]))
        if missing_data:
            missing = random.randint(0, 2, size=(X.shape), dtype=bool)
            # Make half the data missing.
            X[missing] = nan
        return X

    def test_missing_data_training(self):
        """
        Test fitting of the parameters, when some data is missing.
        """
        mean = array((-1, 2))
        std = array((exp(1), exp(2)))
        X = self.generate_gaussian_test_data(mean, std, missing_data=True)
        X_test = self.generate_gaussian_test_data(mean, std, missing_data=False)
        n_numeric = X.shape[1]

        parameters = {
            "n_hidden_units": 1,
            "random_state": 1234,
            "CD_steps": 1,
            "learning_rate": 0.05,
            "mini_batch_size": 250,
            "n_epochs": 200,
            "maximum_iteration": 10000000,
            "tolerance": 1.0e-12,
            "persistent": True,
            "verbose": False,
            "metrics": tuple(),
            "fill_nan_method": np.nanmean,
            "numeric_columns": list(range(n_numeric)),
        }
        model = SurvivalHarmonium(n_numeric_units=n_numeric, **parameters)
        with np.errstate(all="raise"):
            model.fit(X)
            # Check that training gives the correct mean and standard deviation.
            mu, sigma = model.reconstruct_mu_sigma(X_test)
            np.testing.assert_almost_equal(mu, mean, decimal=1)
            np.testing.assert_array_almost_equal(sigma, std, decimal=1)


class TestMultimodalAsGamma(TestMultimodalReduction, TestCase):
    """
    Test that the multimodal model can reduce to a Gamma-binary harmonium.
    """

    parameter_map = {
        "W": "W_B",
        "a": "a_B",
        "b": "b",
        "V": "V",
        "c": "c",
    }

    def as_triplet(self, X: Matrix) -> MatrixTriplet:
        """
        Generate multimodal triplet consistent with Gamma harmonium.
        """
        empty_shape = (X.shape[0], 0)
        return (array([]).reshape(empty_shape), X, array([]).reshape(empty_shape))

    def from_triplet(self, X: MatrixTriplet) -> Matrix:
        """
        Extract visible states `X` from multimodal triplet.
        """
        return X[1]

    def setUp(self):
        """
        Initialise models to have the same set of parameters.
        """
        super().setUp()
        self.multimodal_model = SurvivalHarmonium(
            # The first `n_v` columns are the time variables.
            survival_columns=list(range(self.n_v)),
            # The next `n_v` columns are the event indicators.
            event_columns=list(range(self.n_v, 2 * self.n_v)),
            n_event_units=self.n_v,
            **self.model_parameters
        )
        self.reference_model = CensorGammaHarmonium(
            n_visible_units=self.n_v,
            # The first `n_v` columns are the time variables.
            visible_columns=list(range(self.n_v)),
            # The next `n_v` columns are the event indicators.
            event_columns=list(range(self.n_v, 2 * self.n_v)),
            **self.model_parameters
        )
        self.initialise_model_parameters(self.reference_model, self.multimodal_model)

    def generate_event_test_states(self) -> Tuple[Matrix, Matrix]:
        """
        Generate events, in adddition to the binary visible and hidden states.
        """
        _, X, H = self.generate_test_states()
        event = random.randint(0, 2, size=X.shape)
        return concatenate([X, event], axis=1), H

    def generate_fully_observed_states(self):
        """
        Generate matrix containing both the
        """
        _, X, _ = self.generate_test_states()
        return concatenate([X, ones_like(X)], axis=1)

    def test_free_energy_x_observed(self):
        """
        Test the reduction of modified free energy to the free energy.
        """
        X = self.generate_fully_observed_states()
        np.testing.assert_array_almost_equal(
            self.reference_model.free_energy_x(X),
            self.multimodal_model.modified_free_energy_x(X),
        )

    def test_free_energy_x_censored(self):
        """
        Test the calculation of the free energy F(x) for censored observations.
        """
        X, _ = self.generate_event_test_states()
        np.testing.assert_array_almost_equal(
            self.reference_model.modified_free_energy_x(X),
            self.multimodal_model.modified_free_energy_x(X),
        )

    def test_log_likelihood(self):
        """
        Test that the observed data are equally likely in both models.
        """
        X = self.generate_fully_observed_states()
        np.testing.assert_array_almost_equal(
            self.reference_model.log_likelihood(X),
            self.multimodal_model.log_likelihood(X),
        )

    def test_transform(self):
        """
        Test that visible units are transformed to the same latent states.
        """
        X = self.generate_fully_observed_states()
        np.testing.assert_array_almost_equal(
            self.reference_model.transform(X),
            self.multimodal_model.transform(X),
        )

    def test_log_likelihood_censored(self):
        """
        Test that the observed data are equally likely in both models.
        """
        X, _ = self.generate_event_test_states()
        np.testing.assert_array_almost_equal(
            self.reference_model.log_likelihood(X),
            self.multimodal_model.log_likelihood(X),
        )

    def test_free_energy_x_unobserved(self):
        """
        Test that the free energy equals the partition function when censored at t=0.
        """
        eps = 1.0e-16  # To prevent division by zero.
        xi = np.zeros(shape=(1, self.n_v)) + eps
        event = zeros_like(xi)
        X = concatenate([xi, event], axis=1)
        np.testing.assert_array_almost_equal(
            exp(-self.multimodal_model.modified_free_energy_x(X)),
            self.reference_model.partition_function(),
        )

    def test_transform_censored(self):
        """
        Test that visible units are transformed to the same latent states.
        """
        X, _ = self.generate_event_test_states()

        self.reset_random_state()
        H_ref = self.reference_model.transform(X)

        self.reset_random_state()
        H_test = self.multimodal_model.transform(X)

        np.testing.assert_array_almost_equal(H_ref, H_test)

    def test_predict_joint_proba(self):
        """
        Test `predict` as the likelihood function in absence of x_A and x_C.

        Predict calculates p(x_B|x_A,x_C) which is just the likelihood p(x_B) of the
        gamma harmonium without x_A and x_C.
        """
        _, xi, _ = self.generate_test_states()
        event = ones_like(xi)
        X = concatenate([xi, event], axis=1)
        p = self.multimodal_model.predict_joint_proba(X)
        np.testing.assert_array_almost_equal(
            self.reference_model.log_likelihood(X),
            log(p),
        )


class TestMultimodalAsBinary(
    TestMultimodalReduction, TestMultimodalTimeInvariantReduction, TestCase
):
    """
    Test that the multimodal model can reduce to a binary harmonium.
    """

    parameter_map = {
        "W": "W_A",
        "a": "a_A",
        "b": "b",
    }

    def setUp(self):
        """
        Initialise models to have the same set of parameters.
        """
        super().setUp()
        column_indices = list(range(self.n_v))  # [0,..,n_v-1].
        self.multimodal_model = SurvivalHarmonium(
            categorical_columns=column_indices,
            n_categorical_units=self.n_v,
            **self.model_parameters
        )
        self.reference_model = BinaryHarmonium(
            visible_columns=column_indices,
            n_visible_units=self.n_v,
            **self.model_parameters
        )
        self.initialise_model_parameters(self.reference_model, self.multimodal_model)

    def as_triplet(self, X: Matrix) -> MatrixTriplet:
        """
        Generate multimodal triplet consistent with binary harmonium.
        """
        empty_shape = (X.shape[0], 0)
        return (X, array([]).reshape(empty_shape), array([]).reshape(empty_shape))

    def from_triplet(self, X: MatrixTriplet) -> Matrix:
        """
        Extract visible states `X` from multimodal triplet.
        """
        return X[0]

    def generate_binary_test_data(
        self, parameters: np.ndarray, m: int = 10000, missing_data: bool = True
    ) -> Matrix:
        """
        Generate sigmoid data.
        """
        u = random.uniform(size=(m, parameters.shape[0]))
        X = (u > sigmoid(parameters)).astype(float)
        if missing_data:
            missing = random.randint(0, 2, size=(X.shape), dtype=bool)
            # Make half the data missing.
            X[missing] = nan
        return X

    def test_fit_sigmoid(self):
        """
        Test fitting on sigmoid data.
        """
        z = array([0.2, -0.4])
        X = self.generate_binary_test_data(parameters=z, missing_data=True)
        X_test = self.generate_binary_test_data(parameters=z, missing_data=False)
        parameters = {
            "n_hidden_units": 1,
            "verbose": False,
            "tolerance": 1e-40,
            "mini_batch_size": 250,
            "n_epochs": 450,
            "learning_rate": 0.05,
            "metrics": tuple(),
            "categorical_columns": list(range(X.shape[1])),
        }
        model = SurvivalHarmonium(**parameters)
        with np.errstate(invalid="raise"):
            model.fit(X)
            H_test = model.transform(X_test)
        np.testing.assert_array_almost_equal(model.z(H_test).mean(axis=0), z, decimal=1)

    def test_training_no_missing_data(self):
        """
        Test reduction to binary harmonium in absence of numeric or event variables.
        """
        # Load scikit learn training set.
        X, _ = datasets.load_digits(return_X_y=True)
        X = np.asarray(X, "float32")
        X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)  # 0-1 scaling

        parameters = {
            "n_hidden_units": 10,
            "verbose": True,
            "n_epochs": 2,
            "learning_rate": 1.0,
            "metrics": tuple(),
            "dry_run": True,
        }
        column_indices = list(range(X.shape[1]))
        self.reset_random_state()
        binary_model = BinaryHarmonium(
            n_visible_units=X.shape[1], visible_columns=column_indices, **parameters
        ).fit(X)
        self.reset_random_state()
        multi_model = SurvivalHarmonium(
            categorical_columns=column_indices, **parameters
        ).fit(X)

        # Reset parameters to be identical.
        self.reset_model_parameters(binary_model, how="randomly")
        self.initialise_model_parameters(binary_model, multi_model)

        # The generation of random numbers will be slightly different in the two models,
        # but nevertheless we can expect that training will give more or less the same
        # model.
        binary_model.persistent_constrastive_divergence(X)
        multi_model.persistent_constrastive_divergence(X)

        # Test that the likelihood of the data is by and large the same.
        np.testing.assert_array_almost_equal(
            binary_model.average_log_likelihood(X),
            multi_model.average_log_likelihood(X),
            decimal=1,
        )
