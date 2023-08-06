# Survival harmonium
![Graphical representation of model][model_layout]
Survival analysis powered by generative modelling.
## Features
- Analyse multiple survival variables in one framework.
- Incorporate data with missing values.
- Monitor training on [TensorBoard](https://www.tensorflow.org/tensorboard).
- Integrate with [sci-kit learn](https://scikit-learn.org/) to build pipelines and tune hyperparameters.

# Installation
```Bash
pip3 install survival-harmonium
```

# Usage
```python
from harmoniums import SurvivalHarmonium
from harmoniums.views import plot


model = SurvivalHarmonium(
    # Columns of the time-to-event variables.
    survival_columns=['overall_survival', 'progression_free_survival',..],
    # Event indicator columns of the survival variables.
    event_columns=['os_censored', 'pfs_censored', ..],
    # Columns of the (time-independent) numeric variables.
    numeric_columns=['age', 'weight', ..],
    # Columns of the (time-independent) categorical (i.c., binary) variables.
    categorical_columns=['gender', 'smoking_status', ..],
    # Train for this many epochs.
    n_epochs=100,
    # Number of (binary valued) latent states.
    n_hidden_units=1,
)
model.fit(X_train)

# Visualise model.
plot(model)

# Compute concordance index on test set.
model.score(X_test)
```

# Tutorial
As an example, the Rossi *et al.* dataset is analysed in [Example.ipynb](Example.ipynb), completely with hyperparameter tuning.

# Datasets
This package is bundled with the [NVALT-8](https://www.nature.com/articles/s41416-019-0533-3) and [NVALT-11](https://ascopubs.org/doi/10.1200/JCO.2017.77.5817) datasets, which both contain more than one survival variable. Details can be foud in the [readme](harmoniums/datasets/readme.md) file.
```python
from harmoniums.datasets import load_nvalt8, load_nvalt11


X8 = load_nvalt8()
X11 = load_nvalt11()
```

# How to cite
```
H. C. Donker & H. J. M. Groen, A new harmonium for pattern recognition in
survival data,  arXiv preprint arXiv:2110.01960 (2021).
```

# Requirements
To use the model:
- Python 3.8+
- numpy 1.20+
- pandas 1+
- Numba 0.52+
- scikit-learn 0.24+
- lifelines 0.25+
- scikit-survival

## Optional:

To run the jupyter notebooks and examples:
- matplotlib
- seaborn
- tensorboard

[model_layout]: figures/survival_harmonium_receptive_fields.svg "Model layout"

# License
All code and data is made publicly available under the _Apache License 2.0_, see [LICENSE.txt](LICENSE.txt) for details.