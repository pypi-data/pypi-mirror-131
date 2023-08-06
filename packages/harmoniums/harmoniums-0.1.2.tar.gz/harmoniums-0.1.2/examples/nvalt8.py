import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.utils.fixes import loguniform

from examples import get_output_flag
from examples.benchmark import Benchmark
from harmoniums.utils import reset_random_state
from harmoniums.datasets import load_nvalt8


reset_random_state(1234)

df = load_nvalt8()
# We will use the 'FDG-PET SUVmax>=10' variable instead.
df = df.drop(columns="FDG-PET SUVmax")


survival_columns = ["os_mth", "rfs_mth"]
event_columns = ["os_event", "rfs_event"]
numeric_columns = ["bmi", "age"]

to_encode = ["T-stage", "N-stage", "performance_status", "histology", "smoker", "stage"]
X = pd.get_dummies(df[to_encode]).astype("category")
X["M-stage"] = df["M-stage"].replace({"M0": 0, "Mx": 1}).astype(float)
X["arm"] = df["arm"].replace({"CP/CG": 0, "CP/CG+N": 1})

# Remove low variance features.
p = 0.95
slct = VarianceThreshold(threshold=p * (1 - p)).fit(X)
X = X.loc[:, slct.get_support()]

other_categories = sorted(
    set(df.columns)
    - set(to_encode)
    - {"arm", "M-stage"}
    - set(survival_columns)
    - set(event_columns)
    - set(numeric_columns)
)
X = X.join(df[other_categories])
categorical_columns = sorted(X.columns)
X[categorical_columns] = X[categorical_columns].astype(float)

X = X.join(
    pd.DataFrame(
        StandardScaler().fit_transform(df[numeric_columns]),
        columns=numeric_columns,
        index=df.index,
    )
)
X = X.join(df[survival_columns + event_columns])
max_t = X[survival_columns].max(axis=0).values

# Compare different models.
b = Benchmark(
    X,
    survival_columns=survival_columns,
    event_columns=event_columns,
    categorical_columns=categorical_columns,
    numeric_columns=numeric_columns,
    output_folder=get_output_flag(default_location="output/nvalt8"),
    n_iter=50,
    # Don't use median value because only a tiny fraction is observed after
    # median survival (thereby causing problems in computing the Brier score).
    # (see Kaplan-Meier).
    scoring_time_point=0.5 * max_t,
)
b.cox()
b.harmonium(
    hyper_params={"learning_rate": loguniform(1e-5, 0.0125)},
    harmonium_params={"time_horizon": max_t},
)
b.support_vector_machine()
b.random_survival_forest()
