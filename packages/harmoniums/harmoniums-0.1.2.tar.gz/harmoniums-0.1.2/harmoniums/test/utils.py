from collections import defaultdict
from copy import copy


def perturbed_models(model, epsilon=1e-7):
    """Shift all parameters (weights and biases) by epsilon."""
    models = defaultdict(list)
    # Shift all parameters by epsilon.

    for param_name in model.parameters:
        parameter = getattr(model, param_name)
        for idx in range(parameter.size):
            model_eps = copy(model)

            # Flatten so that we can update single index.
            perturbed = parameter.copy().flatten()
            perturbed[idx] += epsilon
            perturbed = perturbed.reshape(parameter.shape)

            setattr(model_eps, param_name, perturbed)
            models[param_name].append(model_eps)
    return models


def numerical_gradient(model, X, H, epsilon=1e-6) -> dict:
    model_eps = perturbed_models(model, epsilon)
    E_1 = model.energy(X, H)
    gradient = defaultdict(list)
    for param_name, models in model_eps.items():
        for model_i in models:
            E_2 = model_i.energy(X, H)
            grad = (E_2 - E_1).mean(axis=0) / epsilon
            gradient[param_name].append(grad)
    return gradient
