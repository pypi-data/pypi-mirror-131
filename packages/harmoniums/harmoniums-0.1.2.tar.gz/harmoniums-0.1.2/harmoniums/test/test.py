from typing import Optional

import numpy as np

from harmoniums.utils import reset_random_state


class TestHarmonium:
    """
    Unit tests for Harmoniums/Restricted Boltzmann Machines.
    """

    def reset_random_state(self, seed: Optional[int] = None):
        """
        Reset internal state of both NumPy and Numba.
        """
        if seed is None:
            seed = self.random_state
        if seed is None:
            raise ValueError("random_state not set!")

        reset_random_state(seed)

    def setUp(self):
        """
        Initialise seed.
        """
        self.random_state = 1234
        self.reset_random_state()

    def reset_model_parameters(self, model, how: str = "randomly"):
        """
        Reset _all_ trainable parameters.

        args:
            how (str): {"randomly", "zeros", "ones"}

        Helpfull when doing tests, because some biases may be 0 by default.
        """
        if not getattr(model, "is_parameters_initialised_", False):
            model.initialise_parameters()

        how = how.lower()
        for param_name in model.parameters:
            matrix_shape = getattr(model, param_name).shape
            if how.lower() == "randomly":
                filler = np.random.random(size=matrix_shape)
            elif how == "zeros":
                filler = np.zeros(shape=matrix_shape)
            elif how == "ones":
                filler = np.ones(shape=matrix_shape)
            setattr(model, param_name, filler)
        return model
