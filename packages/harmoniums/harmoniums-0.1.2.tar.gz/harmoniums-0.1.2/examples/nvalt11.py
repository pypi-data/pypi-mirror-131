from numpy import nan
import pandas as pd
from sklearn.preprocessing import StandardScaler

from examples import get_output_flag
from examples.benchmark import Benchmark
from harmoniums.datasets import load_nvalt11
from harmoniums.utils import reset_random_state


reset_random_state(1234)

df = load_nvalt11()

survival_columns = ["os_mth", "bmet_mth", "nsymp_mth", "pfs_mth", "sympbmets_mth"]
event_columns = [
    "os_event",
    "bmet_event",
    "nsymp_event",
    "pfs_event",
    "sympbmets_event",
]
numeric_columns = ["bmi", "age"]

# Dummy encode the following three variables, and determine the total number of
# categorical variables (after encoding).
X = pd.get_dummies(df[["performance_status", "smoker"]].astype("category"))
X["stage_IIIB"] = nan
stage_na = df["stage"].isnull()
X.loc[~stage_na, "stage_IIIB"] = (df.loc[~stage_na, "stage"] == "IIIB").astype(int)
other_categories = sorted(
    set(df.columns)
    - {"performance_status", "smoker", "stage"}
    - set(survival_columns)
    - set(event_columns)
    - set(numeric_columns)
)
X = X.join(df[other_categories])
categorical_columns = sorted(X.columns)
X = X.join(
    pd.DataFrame(
        StandardScaler().fit_transform(df[numeric_columns]),
        columns=numeric_columns,
        index=df.index,
    )
)
X = X.join(df[survival_columns + event_columns])

# For now, restrict analysis to the following two variables:
survival_columns = [
    "os_mth",
    "sympbmets_mth",
]
event_columns = [
    "os_event",
    "sympbmets_event",
]

max_t = X[survival_columns].max(axis=0).values
# Compare different models.
b = Benchmark(
    X,
    survival_columns=survival_columns,
    event_columns=event_columns,
    categorical_columns=categorical_columns,
    numeric_columns=numeric_columns,
    output_folder=get_output_flag(default_location="output/nvalt11"),
    n_iter=50,
    # Don't use median value because this value is not observed in the dataset
    # (see Kaplan-Meier).
    scoring_time_point=0.5 * max_t,
)
b.cox()
b.harmonium(harmonium_params={"time_horizon": max_t})
b.support_vector_machine()
b.random_survival_forest()
