from lifelines.datasets import load_gbsg2
import pandas as pd
from sklearn.preprocessing import StandardScaler

from examples import get_output_flag
from examples.benchmark import Benchmark
from harmoniums.utils import reset_random_state

reset_random_state(1234)

df = load_gbsg2()
X = df.copy()

# Normalise numeric values.
numeric_columns = ["age", "tsize", "estrec", "progrec", "pnodes"]
X[numeric_columns] = StandardScaler().fit_transform(X[numeric_columns])

# Encode categorical variables.
X["horTh"] = X["horTh"].astype("category").cat.codes
X["menostat"] = X["menostat"].astype("category").cat.codes
X[["tgrade0", "tgrade1", "tgrade2"]] = pd.get_dummies(X["tgrade"])
X = X.drop(columns=["tgrade"])

max_t = max(X["time"])
b = Benchmark(
    X,
    survival_columns=["time"],
    event_columns=["cens"],
    categorical_columns=["horTh", "menostat", "tgrade0", "tgrade1", "tgrade2"],
    numeric_columns=numeric_columns,
    output_folder=get_output_flag(default_location="output/gbsg2"),
    n_iter=50,
    scoring_time_point=0.5 * max_t,
)
b.cox()
b.harmonium(harmonium_params={"time_horizon": [max_t]})
b.support_vector_machine()
b.random_survival_forest()
