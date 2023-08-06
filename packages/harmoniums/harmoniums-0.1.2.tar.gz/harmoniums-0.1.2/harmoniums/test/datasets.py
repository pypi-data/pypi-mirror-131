from typing import Tuple, Union

import numpy as np
from numpy import array, concatenate, logical_xor, random, ones, ones_like
import pandas as pd
from sklearn.utils import shuffle

from harmoniums.const import Matrix, MatrixTriplet
from harmoniums.samplers import sample_right_truncated_gamma_distribution

TripletEventPair = Tuple[MatrixTriplet, Matrix]
TripletEventLabelTriplet = Tuple[MatrixTriplet, Matrix, np.ndarray]


class SuperImposedGamma:
    """
    Toy dataset composed of two super imposed truncated gamma distributions.

    Two time-to-event variables coming from groups (g={0,1,..}), in which each group is
    distributed according to the truncated gamma distribution, i.e., p(x1, x2, g) =
    p(x1, x2|g) p(g). Observations: x(i) > `study_duration`(i) are (right) censored.
    """

    def __init__(
        self,
        study_duration: Tuple[float, float] = (0.75, 0.95),
        parameters_group0: tuple = ([1.5, 2.5], [3.0, 5.0]),
        parameters_group1: tuple = ([1.0, 1.0], [-3.0, -7.0]),
        *args
    ):
        """
        Store parameters of the two distributions.

        parameters_group{0,1}: First element corresponds to alpha, second to beta.
        """
        a, b = zip(parameters_group0, parameters_group1, *args)
        self.number_of_groups = len(args) + 2
        self.a = tuple(a)
        self.b = tuple(b)
        self.study_duration = array(study_duration).reshape(1, -1)

    def get_params(self, group: int = -1) -> tuple:
        """
        Get the distribution parameters.
        """
        if group > 0:
            return self.a[group], self.b[group]
        return tuple(zip(self.a, self.b))

    def generate_random_AND_pair(self, group) -> tuple:
        """
        Generate random pairs of switches, that are only both turned on for group 1.
        """
        switch_a = ones_like(group)
        switch_b = ones_like(group)

        # Two cases:
        # 1) Group 0: Some of the switches may be on (randomly), but not both.
        g0 = group == 0
        switch_a[g0] = random.randint(0, 2, switch_a[g0].shape)
        # Randomly switch other lever, ensuring that not both are on.
        switch_b[g0] = logical_xor(
            switch_a[g0], random.randint(0, 2, switch_a[g0].shape)
        )

        # 2) Group 1: Both switches are on.
        # No further action needed, because we initialised with ones.
        return switch_a, switch_b

    def load_group(self, group: int, m: int = 200) -> pd.DataFrame:
        """
        Generate `m` samples from group
        """
        x = array(
            [
                sample_right_truncated_gamma_distribution(
                    np.array(self.a[group]), np.array(self.b[group]), 1.0
                )
                for _ in range(m)
            ]
        )
        study_duration = ones_like(x) * self.study_duration
        event = x < study_duration
        # Replace event with time of censor.
        x[~event] = study_duration[~event]

        gauss_distance = 2.0
        g = ones(m) * group
        cat_switch, gauss_switch_on = self.generate_random_AND_pair(g)
        gauss_switch = random.normal(loc=gauss_switch_on * gauss_distance)

        return pd.DataFrame(
            {
                # When both switches are activated, the sample belongs to group 1.
                "category": cat_switch,
                "numeric": gauss_switch,
                # Time-to-event variables.
                "t_0": x[:, 0],
                "t_1": x[:, 1],
                # Are the events censored?
                "event_0": event[:, 0],
                "event_1": event[:, 1],
            }
        )

    def load(self, m: int = 400) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Generate dataset.
        """
        X = []
        group = []
        for i in range(self.number_of_groups):
            x_i = self.load_group(i, max(1, m // self.number_of_groups))
            X.append(x_i)
            group.append(ones(x_i.shape[0]) * i)

        # Combine and shuffle data.
        data_frame = pd.concat(X, axis=0).reset_index()
        group = pd.Series(concatenate(group, axis=0))
        data_frame, y = shuffle(data_frame, group)
        if data_frame.shape[0] > m:
            return data_frame[:m], y[:m]
        return data_frame, y


def laplace_mixtures(
    average: Union[float, np.ndarray] = 0.0,
    scale: Union[float, np.ndarray] = 1.0 / np.sqrt(2.0),
    size: Tuple[int, int] = (100000, 2),
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate samples from a mixture of Laplace distributions.
    """
    # Number of laplace mixtures.
    n = size[1]
    # Generate samples from laplace distribution.
    s = np.random.laplace(loc=average, scale=scale, size=size)
    # Random matrix `A` with range [-0.5, 0.5].
    A = np.random.random(size=(n, n)) - 0.5
    # Mix the variables.
    X = s @ A.T
    return X, A
