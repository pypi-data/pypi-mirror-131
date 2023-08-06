from lifelines.datasets import load_dd
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from examples import get_output_flag
from examples.benchmark import Benchmark
from harmoniums.utils import reset_random_state


reset_random_state(1234)

X = load_dd()
# Focus only on the following categorical features.
X = X[["un_continent_name", "regime", "duration", "observed"]]
c = OneHotEncoder(drop="first")
Xenc = c.fit_transform(X[["un_continent_name", "regime"]])
category_labels = [lab for cs in c.categories_ for lab in cs[1:]]
df = pd.DataFrame(Xenc.todense(), columns=category_labels)
df[["duration", "observed"]] = X[["duration", "observed"]]
# Superfluous column that prevents the data matrix from being invertible.
category_labels.remove("Oceania")
X = df.drop("Oceania", axis=1)

max_t = max(X["duration"])
b = Benchmark(
    X,
    survival_columns=["duration"],
    event_columns=["observed"],
    categorical_columns=category_labels,
    output_folder=get_output_flag(default_location="output/democracy"),
    n_iter=50,
    scoring_time_point=0.5 * max_t,
)
b.cox()
b.harmonium(harmonium_params={"time_horizon": [max_t]})
b.support_vector_machine()
b.random_survival_forest()
