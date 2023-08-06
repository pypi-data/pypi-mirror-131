from unittest import TestCase

import numpy as np
import pandas as pd
from sksurv.datasets import load_gbsg2
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.preprocessing import OneHotEncoder

from harmoniums.samplers import sample_right_truncated_gamma_distribution_positive_b
from harmoniums.utils import (
    brier_loss,
    generate_binary_permutations,
    generate_binary_spin_permutations,
    reset_random_state,
    MiniBatchIterator,
)


class TestMiniBatchIterator(TestCase):
    def setUp(self):
        """
        Initialise random seed.
        """
        np.random.seed(1234)

    def test_periodic_iterator_numpy(self):
        """
        Test that a periodic NumPy iterator can go beyond the last element.
        """
        X = np.random.random(size=[5, 2])
        mini_batcher = MiniBatchIterator(X, number_of_epochs=None, mini_batch_size=2)
        iterator = iter(mini_batcher)
        for _ in range(2):
            next(iterator)
        np.testing.assert_array_equal(np.vstack((X[-1], X[0])), next(iterator))

    def test_periodic_iterator_pandas(self):
        """
        Test that a periodic Pandas iterator can go beyond the last element.
        """
        X = pd.DataFrame(np.random.random(size=[5, 2]), columns=["a", "b"])
        mini_batcher = MiniBatchIterator(
            X, number_of_epochs=None, shuffle_each_epoch=False, mini_batch_size=2
        )
        iterator = iter(mini_batcher)
        for _ in range(2):
            next(iterator)
        pd.testing.assert_frame_equal(
            pd.concat((X.iloc[-1], X.iloc[0]), axis=1).T, next(iterator)
        )

    def test_periodic_iterator_with_shuffle(self):
        """
        Test that a periodic Pandas iterator that is shuffled after each epoch.
        """
        X = np.array(
            [
                [0.191519, 0.622109],
                [0.437728, 0.785359],
                [0.779976, 0.272593],
                [0.276464, 0.801872],
                [0.958139, 0.875933],
            ]
        )
        data_frame = pd.DataFrame(X, columns=["a", "b"])
        mini_batcher = MiniBatchIterator(
            data_frame,
            number_of_epochs=None,
            shuffle_each_epoch=True,
            mini_batch_size=2,
        )
        iterator = iter(mini_batcher)
        for _ in range(3):
            next(iterator)
        pd.testing.assert_frame_equal(
            pd.concat((data_frame.iloc[0], data_frame.iloc[1]), axis=1).T,
            next(iterator),
        )

    def test_non_periodic_iterator(self):
        """
        Test that the last mini batch is shrunken to accomodate the array size.
        """
        X = np.random.random(size=[3, 2])
        mini_batcher = MiniBatchIterator(X, number_of_epochs=1, mini_batch_size=2)
        iterator = iter(mini_batcher)
        next(iterator)
        next(iterator)

        # Test that array is exhausted therafter.
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_mini_batch_size_too_large(self):
        """
        Verify that a mini batch size exceeding the dataset returns everything.
        """
        X = np.random.random(size=[4, 2])
        mini_batcher = MiniBatchIterator(X, mini_batch_size=10)
        iterator = iter(mini_batcher)
        # Test that the entire set is returned.
        np.testing.assert_array_equal(next(iterator), X)
        # For each iteration.
        np.testing.assert_array_equal(next(iterator), X)

    def test_args(self):
        """
        Test that multiple arrays can be passed.
        """
        # Iterate over 3 arrays simulateneously.
        a = np.random.random(size=(4, 3))
        b = (a > 0.5).astype(int)
        y = np.random.random(size=(a.shape[0],))

        m = 2  # Batch size.
        batcher = MiniBatchIterator(a, b, y, number_of_epochs=1, mini_batch_size=m,)
        iterator = iter(batcher)
        first_batch = next(iterator)

        self.assertEqual(len(first_batch), 3)
        # Mini batch size.
        self.assertEqual(first_batch[0].shape[0], m)
        # Column consistency.
        self.assertEqual(first_batch[1].shape[1], b.shape[1])
        # y remains 1D.
        self.assertEqual(len(first_batch[2].shape), 1)

    def test_none_args(self):
        """
        Test passing of multiple args, some of which are None.
        """
        # Array `b` is empty.
        a = np.random.random(size=(4, 3))
        b = None
        y = np.random.random(size=(a.shape[0],))

        m = 2  # Batch size.
        batcher = MiniBatchIterator(
            a, b, y, number_of_epochs=1, mini_batch_size=m, shuffle_data_once=True
        )
        iterator = iter(batcher)
        first_batch = next(iterator)

        self.assertEqual(len(first_batch), 3)
        # Mini batch size.
        self.assertEqual(first_batch[2].shape[0], m)
        # Second column is None.
        self.assertIsNone(first_batch[1])


class TestMisc(TestCase):
    """
    Test miscellaneous other helper functions.
    """

    def test_random_state(self):
        """
        Check that Numba random state is reset.
        """
        reset_random_state(1234)
        s1 = sample_right_truncated_gamma_distribution_positive_b(0.5, 2.5)
        reset_random_state(1234)
        s2 = sample_right_truncated_gamma_distribution_positive_b(0.5, 2.5)
        self.assertEqual(s1, s2)


class TestProductStates(TestCase):
    """
    Test the generation of binary product states.
    """

    def test_generate_binary_permutations(self):
        """
        Test the generation of all possible hidden states {0, 1}.
        """
        H = generate_binary_permutations(n=2)
        # On average, all hidden units are turned on half the time.
        np.testing.assert_array_equal(H.mean(axis=0), np.ones(H.shape[1]) * 0.5)
        # Check that all permutations are covered.
        np.testing.assert_array_equal(H, np.array([[0, 0], [1, 0], [0, 1], [1, 1]]))

    def test_generate_binary_spin_permutations(self):
        """
        Test the generation of spin binary states {-1, 1}.
        """
        H = generate_binary_spin_permutations(n=2)
        # On average, all hidden units are turned on half the time, summing to zero.
        np.testing.assert_array_equal(H.mean(axis=0), np.zeros(H.shape[1]))
        # Check that all permutations are covered.
        np.testing.assert_array_equal(H, np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]]))


class TestBrierScore(TestCase):
    """
    Test the Brier score computation.
    """

    def test_brier_gbsbg2(self):
        """
        Test calculation on  the German Breast Cancer Study Group 2 dataset.

        This test is re-implementation of scikit-survival `brier_score` test.
        """
        X, y = load_gbsg2()
        X.loc[:, "tgrade"] = X.loc[:, "tgrade"].map(len).astype(int)
        time = y["time"]
        event = y["cens"]

        Xt = OneHotEncoder().fit_transform(X)

        est = CoxPHSurvivalAnalysis(ties="efron").fit(Xt, y)
        survs = est.predict_survival_function(Xt)

        # Calculate survival distribution at this time point.
        time_point = 1825
        preds = [fn(time_point) for fn in survs]

        score = brier_loss(
            train_time=time,
            train_event=event,
            test_time=time,
            test_event=event,
            S_pred=preds,
            tau=time_point,
        )

        assert round(abs(score - 0.208817407492645), 5) == 0
