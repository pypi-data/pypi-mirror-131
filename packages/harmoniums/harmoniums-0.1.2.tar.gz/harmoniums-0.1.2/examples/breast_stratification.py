import os
from pathlib import Path
import pickle

from lifelines import KaplanMeierFitter
from lifelines.datasets import load_gbsg2
from lifelines.statistics import logrank_test
from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText
import numpy as np
import pandas as pd
from scipy.stats import uniform
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.utils.fixes import loguniform

from harmoniums import SurvivalHarmonium
from harmoniums.views import plot


output_folder = Path("output/breast/")
output_figs = output_folder / "figs"
output_figs.mkdir(parents=True, exist_ok=True)
np.random.seed(1234)

df = load_gbsg2()
X = df.copy()

categorical_columns = ["horTh", "menostat", "tgrade0", "tgrade1", "tgrade2"]
numeric_columns = ["age", "tsize", "estrec", "progrec", "pnodes"]
survival_columns = ["time"]
event_columns = ["cens"]

# Normalise numeric values.
X[numeric_columns] = StandardScaler().fit_transform(X[numeric_columns])

# Encode categorical variables.
X["horTh"] = X["horTh"].astype("category").cat.codes
X["menostat"] = X["menostat"].astype("category").cat.codes
X[["tgrade0", "tgrade1", "tgrade2"]] = pd.get_dummies(X["tgrade"])
X = X.drop(columns=["tgrade"])

# Reserve 70 % for training, remainder for Kaplan-Meier.
X_train, X_test = train_test_split(X, train_size=0.7)

# Hyperparameter tune model.
harmonium = SurvivalHarmonium(
    categorical_columns=categorical_columns,
    survival_columns=survival_columns,
    numeric_columns=numeric_columns,
    event_columns=event_columns,
    verbose=True,
    log_every_n_iterations=None,
    time_horizon=[max(X[survival_columns[0]])],
    metrics=tuple(),
    risk_score_time_point="median",
    guess_weights=False,
    n_hidden_units=1,
)
param_distributions = {
    "learning_rate": loguniform(1e-5, 0.1),
    "n_epochs": loguniform(1e1, 1e4),
    "CD_steps": [1, 2, 4, 8],
    "momentum_fraction": uniform(0, 0.9),
    "mini_batch_size": loguniform(25, 1000),
    "weight_decay": loguniform(1e-5, 0.1),
    "persistent": [True, False],
}

cvsearch_kwargs = {
    "param_distributions": param_distributions,
    "cv": 5,
    "n_iter": 50,
    "n_jobs": int(os.environ.get("SLURM_JOB_CPUS_PER_NODE", -1)),
}
cv = RandomizedSearchCV(harmonium, **cvsearch_kwargs).fit(X_train)
harmonium = cv.best_estimator_


# Store result.
with open(output_folder / "stratification.pickle", "wb") as file_object:
    pickle.dump({"model": harmonium, "X_train": X_train, "X_test": X_test}, file_object)


# Test latent group identification on test set.
X_test_concealed = X_test.copy()
# Conceal survival information by censoring time-to-event variables at t=0.
X_test_concealed[survival_columns + event_columns] = 0
with np.errstate(all="raise"):
    H = harmonium.transform(X_test_concealed, reconstruction_steps=50) > 0.5

X1 = X_test[~H]
X2 = X_test[H]

test_result = logrank_test(
    X1[survival_columns[0]],
    X2[survival_columns[0]],
    X1[event_columns[0]],
    X2[event_columns[0]],
)

# Make Kaplan-Meier plot of two groups.
plt.rc("font", family="serif")
fig = plt.figure(figsize=(4, 3))
KaplanMeierFitter().fit(X1[survival_columns[0]], X1[event_columns[0]]).plot(
    label=f"Group 2 (n={X1.shape[0]})"
)
KaplanMeierFitter().fit(X2[survival_columns[0]], X2[event_columns[0]]).plot(
    label=f"Group 2 (n={X2.shape[0]})"
)
plt.legend(frameon=False)
pvalue_txt = AnchoredText(
    r"$p$={:.3f}".format(test_result.p_value), loc="lower left", frameon=False
)
plt.gca().add_artist(pvalue_txt)

plt.ylabel("Survival")
plt.savefig(output_figs / "kaplan_meier.png", bbox_inches="tight")
plt.savefig(output_figs / "kaplan_meier.pdf", bbox_inches="tight")
plt.gca().set_rasterized(True)
plt.savefig(output_figs / "kaplan_meier.eps", dpi=300, bbox_inches="tight")

# Make figure of learned parameters.
plot(harmonium)
plt.tight_layout()
plt.savefig(output_figs / "weights.eps", bbox_inches="tight")
plt.savefig(output_figs / "weights.png", bbox_inches="tight")
