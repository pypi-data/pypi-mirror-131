from glob import glob
from pathlib import Path
import sys

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


OUTPUT_DIR = "output"
if len(sys.argv) > 1:
    OUTPUT_DIR = sys.argv[1]


scores = pd.DataFrame(
    columns=[
        "model",
        "dataset",
        "brier",
        "brier_std",
        "concordance",
        "concordance_std",
        "conditional_brier",
        "conditional_brier_std",
        "conditional_concordance",
        "conditional_concordance_std",
    ]
)
for csv in glob(f"{OUTPUT_DIR}/*/scores.csv"):
    csv_path = Path(csv)
    df = pd.read_csv(csv_path)
    df.rename(columns={"Unnamed: 0": "model"}, inplace=True)
    df["dataset"] = csv_path.parent.stem
    scores = scores.append(df, ignore_index=True)

datasets = sorted(scores["dataset"].unique())
models = sorted(scores["model"].unique())
scores.set_index(["model", "dataset"], inplace=True)
# From score to loss.
scores["brier"] = -scores["brier"]
scores["conditional_brier"] = -scores["conditional_brier"]


def plot_metric(metric):
    plt.rc("font", family="serif")
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_subplot(1, 1, 1)

    # Set dataset labels on x axis.
    dataset_locations = np.arange(len(datasets))
    ax.set_xticks(dataset_locations)
    ax.set_xticklabels(datasets, rotation=30)
    ax.set_xlabel("Dataset")

    markers = ["o", "s", "v", "D", "*"]
    models_not_na = scores[scores[metric].notnull()].index.get_level_values(0).unique()
    models = sorted(models_not_na)
    models.append("harmonium*")
    models.sort()
    spacing = 0.5 / len(models)

    # Plot metrics for each model, for each dataset.
    for cnt, model in enumerate(models):
        # Slice off the *, because it is the same model.
        if "*" in model:
            model_name = model[:-1]
        else:
            model_name = model

        # Don't take model into account, if no metrics were computed.
        if scores.loc[model_name][metric].isnull().all():
            continue

        # Compute coordinates so that metrics are grouped per dataset.
        x = []
        c = []
        cerr = []

        # For each model, plot the values for individual datasets.
        for i, data in enumerate(datasets):
            if data not in scores.loc[model_name].index:
                continue
            left_offset = len(models) // 2
            j = models.index(model) - left_offset
            row = scores.loc[model_name, data]

            metric_prefix = ""
            if "*" in model:
                metric_prefix = "conditional_"

            value = row[f"{metric_prefix}{metric}"]
            if pd.isnull(value):
                continue
            error = row[f"{metric_prefix}{metric}_std"]
            x.append(dataset_locations[i] + spacing * j)
            c.append(value)
            cerr.append(error)

        plt.errorbar(
            x,
            y=c,
            yerr=cerr,
            fmt=markers[cnt],
            label=model.replace("_", " "),
        )

    plt.legend(frameon=False, loc="upper left", prop={"size": 8})


plot_metric("concordance")
plt.ylabel("Harrell's concordance index")
plt.ylim([0.5, 1.0])
plt.tight_layout()
plt.savefig("figs/concordance.png")
plt.savefig("figs/concordance.eps")


plot_metric("brier")
plt.ylabel("Brier loss")
plt.ylim([0, 0.5])
plt.tight_layout()
plt.savefig("figs/brier.png")
plt.savefig("figs/brier.eps")
