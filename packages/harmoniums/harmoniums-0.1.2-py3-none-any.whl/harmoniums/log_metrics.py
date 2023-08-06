from datetime import datetime
from functools import wraps
from io import BytesIO
import logging
from pathlib import Path
from typing import Union
import re
import uuid

from matplotlib import pyplot as plt
from numpy import array, ndarray, printoptions

LOG_TENSORBOARD = False
try:
    from tensorboard.plugins.hparams import api as hp
    import tensorflow as tf
except ImportError:
    logging.warning("Unable to import tensorflow!")
else:
    LOG_TENSORBOARD = True

TF_WRITER = None


def get_tf_writer():
    global TF_WRITER
    return TF_WRITER


def set_tf_writer(writer):
    global TF_WRITER
    if TF_WRITER is not None:
        del TF_WRITER
    TF_WRITER = writer


def suggest_log_dir(base_dir: Path = Path()) -> Path:
    """Generate log dir for a run."""
    # If we're suggesting a new log dir, delete old tf_writer so that a new one
    # will be initialised.
    set_tf_writer(None)

    run_id = str(uuid.uuid1().int)[:6]
    run_date = datetime.now().strftime(r"%Y%m%d_%H%M")
    output_dir = base_dir / "log" / f"{run_date}_run_{run_id}"
    output_dir.mkdir(exist_ok=True, parents=True)
    return output_dir


def plot_to_tensor(figure):
    """Convert matplotlib figure to tensor flow image."""
    # Save the plot to a PNG in memory.
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(figure)
    buf.seek(0)
    # Convert PNG buffer to TF image
    image = tf.image.decode_png(buf.getvalue(), channels=4)
    # Add the batch dimension
    return tf.expand_dims(image, 0)


def to_disk(output: Union[str, Path], verbose: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(estimator, X_train, X_val, step: int, epoch: int):
            """Store computed metrics on disk and to tensorboard."""
            step, epoch, metrics = func(estimator, X_train, X_val, step, epoch)

            # No metrics to track.
            if not metrics:
                return step, epoch, metrics

            # Split into train and val sets for printing and storing to csv.
            train_metrics = {
                key.removesuffix("/train"): value
                for key, value in metrics.items()
                if "/train" in key
            }
            val_metrics = {
                key.removesuffix("/validation"): value
                for key, value in metrics.items()
                if "/validation" in key
            }

            if verbose:
                print_metrics(step, epoch, train_metrics, val_metrics)
            metrics_to_csv(output, step, epoch, train_metrics, val_metrics)

            if LOG_TENSORBOARD:
                metrics_to_tensorboard(estimator, output, step, epoch, metrics)

            return step, epoch, metrics

        return wrapper

    return decorator


def log_metrics_callback(
    estimator,
    X_train,
    X_val,
    step: int,
    epoch: int,
    *metrics,
):
    """Callback function that computes metrics."""
    metric_values = {}
    for metric_function_name in metrics:
        metric_function = getattr(estimator, metric_function_name)

        # For training data.
        metric_value = metric_function(X_train)

        if isinstance(metric_value, ndarray):
            metric_value = metric_value.mean()
        metric_values[f"{metric_function_name}/train"] = metric_value

        # And for validation set.
        if X_val is not None:
            metric_value = metric_function(X_val)
            if isinstance(metric_value, ndarray):
                metric_value = metric_value.mean()
            metric_values[f"{metric_function_name}/validation"] = metric_value

    return step, epoch, metric_values


def log_weights_gradients_likelihood_callback(
    estimator, X_train, X_validation, step: int, epoch: int
):
    """Log likelihood and weight and gradient histograms to tensorboard."""

    metrics = {
        "log_likelihood/train": estimator.log_likelihood(X_train).mean(axis=0),
    }
    # Filter weights and gradients that do not partake in model (i.e., size: 0).
    weights = {
        name: value
        for name, value in estimator.get_parameters().items()
        if value.size > 0
    }
    metrics.update(weights)
    gradients = {
        f"{name}/gradient": value
        for name, value in estimator.previous_update.items()
        if value.size > 0
    }
    metrics.update(gradients)

    if X_validation is not None:
        metrics["log_likelihood/validation"] = estimator.log_likelihood(
            X_validation
        ).mean(axis=0)
    return step, epoch, metrics


def metrics_to_tensorboard(
    estimator, output: Path, step: int, epoch: int, metrics: dict
):
    """Log metrics to tensorboard."""
    tf_writer = get_tf_writer()
    if tf_writer is None:
        tensorboard_dir = output / "tensorboard"
        tf_writer = tf.summary.create_file_writer(str(tensorboard_dir))

        # Include hyperparameters.
        params = {
            "n_epochs": estimator.n_epochs,
            "momentum_fraction": estimator.momentum_fraction,
            "mini_batch_size": estimator.mini_batch_size,
            "weight_decay": estimator.weight_decay,
            "persistent": estimator.persistent,
            "CD_steps": estimator.CD_steps,
        }
        if isinstance(estimator.learning_rate, float):
            params["learning_rate"] = estimator.learning_rate
        else:
            logging.warning(
                "WARNING: Non scalar learning rate can not be stored to tensor board."
            )

        with tf_writer.as_default():
            hp.hparams(hparams=params)

        set_tf_writer(tf_writer)
        print(f"Tensorboard metrics: {tensorboard_dir}")

    with tf_writer.as_default():
        for name, value in metrics.items():
            if isinstance(value, (float, int)):
                tf.summary.scalar(name, value, step)
            elif isinstance(value, tf.Tensor) and len(value.shape) >= 3:
                tf.summary.image(name, value, step=step)
            elif isinstance(value, (ndarray, tuple, list)):
                if isinstance(value, (tuple, list)):
                    value = array(value)
                tf.summary.histogram(name, value.flatten(), step)


def metrics_to_csv(destination_dir, step, epoch, training_metrics, validation_metrics):
    """Save metrics to CSV file."""
    if not training_metrics:
        return

    if isinstance(destination_dir, str):
        destination_dir = Path(destination_dir)

    destination_dir.mkdir(exist_ok=True, parents=True)

    with open(destination_dir / "train.csv", mode="a") as fo:
        # Write header.
        if step == 0:
            train_columns = ["step", "epoch"] + list(training_metrics.keys())
            fo.write(",".join(train_columns) + "\n")
        values = [step, epoch] + list(training_metrics.values())
        fo.write(",".join([str(v) for v in values]) + "\n")

    if validation_metrics:
        with open(destination_dir / "validation.csv", mode="a") as fo:
            # Write header.
            if step == 0:
                val_columns = ["step", "epoch"] + list(validation_metrics.keys())
                fo.write(",".join(val_columns) + "\n")
            values = [step, epoch] + list(validation_metrics.values())
            fo.write(",".join([str(v) for v in values]) + "\n")


def print_metrics(step: int, epoch: int, training_metrics, validation_metrics):
    """
    Print metric values.
    """
    metrics_combined = list(training_metrics.values()) + list(
        validation_metrics.values()
    )

    # Don't print anything if no metrics are calculated.
    if len(metrics_combined) == 0:
        return

    # Make a table combining train and validation fields.
    # 1) Determine column format based on metric type (float v.s. array).
    column_format = "{0:<5}"
    for i, value in enumerate(metrics_combined):
        if isinstance(value, float):
            column_format += "{" + str(i + 1) + ":<22.4f}"
        elif isinstance(value, (tuple, list)):
            # Make columns for individual elements of array.
            column_format += "".join(
                "{" + str(i + 1) + "[" + str(k) + "]}   " for k in range(len(value))
            )
        else:
            column_format += "{" + str(i + 1) + "}"

    # Print header.
    if step == 0:
        header_train = [f"{key}_train" for key in training_metrics.keys()]
        header_valid = [f"{key}_val" for key in validation_metrics.keys()]
        header = ["Epoch"] + header_train + header_valid
        header_format = re.sub(r"\[\d+\]", "", column_format.replace(".4f", ""))
        print(header_format.format(*header))

    with printoptions(precision=4, floatmode="fixed"):
        print(column_format.format(epoch, *metrics_combined))
