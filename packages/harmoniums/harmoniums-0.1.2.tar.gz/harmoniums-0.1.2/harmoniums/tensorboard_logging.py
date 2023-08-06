"""Simple example on how to log scalars and images to tensorboard without tensor ops.
License: BSD License 2.0
"""
__author__ = "Michael Gygli"

from io import StringIO

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np


class Logger:
    """Logging in tensorboard without tensorflow ops."""

    def __init__(self, log_dir):
        """Creates a summary writer logging to log_dir."""
        self.writer = tf.summary.create_file_writer(log_dir)

    def log_scaler(self, tag, value, step):
        """Log a scalar variable.
        Parameter
        ----------
        tag : basestring
            Name of the scalar
        value
        step : int
            training iteration
        """
        with self.writer.as_default():
            tf.summary.scalar(tag, value, step)

    def log_histogram(self, tag, values, step:
        """Logs the histogram of a list/vector of values."""
        with self.writer.as_default():
            tf.summary.histogram(tag, values, step)


from numpy import exp

logger = Logger("/tmp/test")
for i in range(1000):
    logger.log_scaler("log_likelihood", 1 - exp(-i), step=i)
    logger.log_histogram("gradient", np.random.uniform(size=[4, 100]), step=i)
