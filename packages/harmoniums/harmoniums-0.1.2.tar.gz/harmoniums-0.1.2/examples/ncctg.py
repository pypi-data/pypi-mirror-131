from lifelines.datasets import load_lung
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import StandardScaler
from sklearn.utils.fixes import loguniform

from examples import get_output_flag
from examples.benchmark import Benchmark
from harmoniums.utils import reset_random_state


reset_random_state(1234)

# Drop weight loss and meal.cal become some values are missing. Although the
# harmonium can handle these values, the other models can not.
X = load_lung().drop(columns=["inst"]).drop(columns=["wt.loss", "meal.cal"])
# Binary encode gender.
X["sex"] = (X["sex"] == 2).astype(int)

X = pd.get_dummies(data=X, columns=["ph.ecog", "ph.karno", "pat.karno"])
# Remove low variance features.
p = 0.95
slct = VarianceThreshold(threshold=p * (1 - p)).fit(X)
X = X.loc[:, slct.get_support()]

numeric_columns = ["age"]
event_columns = ["status"]
survival_columns = ["time"]
categorical_columns = [
    c for c in X.columns if c not in numeric_columns + event_columns + survival_columns
]

X[numeric_columns] = StandardScaler().fit_transform(X[numeric_columns])

max_t = max(X["time"])
b = Benchmark(
    X,
    survival_columns=survival_columns,
    event_columns=event_columns,
    categorical_columns=categorical_columns,
    numeric_columns=numeric_columns,
    output_folder=get_output_flag(default_location="output/ncctg"),
    n_iter=50,
    scoring_time_point=0.5 * max_t,
)
b.cox()
b.harmonium(
    harmonium_params={"time_horizon": [max_t]},
    hyper_params={"n_epochs": loguniform(500, 5e4)},
)
b.support_vector_machine()
b.random_survival_forest()
