from lifelines.datasets import load_rossi
import pandas as pd
from sklearn.preprocessing import StandardScaler

from examples import get_output_flag
from examples.benchmark import Benchmark
from harmoniums.utils import reset_random_state


reset_random_state(1234)

X = load_rossi()

# Make dummy categories for the number of prior convictions.
prior_dummies = ["prio_0", "prio_1", "prio_2", "prio_3", "prio_4", "prio_5", "prio>5"]
X[prior_dummies] = pd.get_dummies(X["prio"].apply(lambda x: ">5" if x > 5 else x))
X = X.drop("prio", axis=1)

# Standardise the numeric value `age`.
X[["age"]] = StandardScaler().fit_transform(X[["age"]])

max_t = max(X["week"])
# Compare different models.
b = Benchmark(
    X,
    survival_columns=["week"],
    event_columns=["arrest"],
    categorical_columns=["fin", "race", "wexp", "mar", "paro"] + prior_dummies,
    numeric_columns=["age"],
    output_folder=get_output_flag(default_location="output/arrest"),
    n_iter=50,
    # Don't use median value for calculating Brier score, because this value is
    # not observed in the dataset (see Kaplan-Meier).
    scoring_time_point=0.5 * max_t,
)
b.cox()
b.harmonium(harmonium_params={"time_horizon": [max_t]})
b.support_vector_machine()
b.random_survival_forest()
