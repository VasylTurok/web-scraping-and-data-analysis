import numpy as np
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame

from config import TECHNOLOGIES


def show_technologies(df: DataFrame) -> None:
    for tech in TECHNOLOGIES:
        df[tech] = df["stack"].apply(lambda x: 1 if tech in str(x) else 0)

    tech_counts = df[TECHNOLOGIES].sum().sort_values(
        ascending=False
    ).head(20)
    tech_columns_array = tech_counts.index.values
    tech_values_array = tech_counts.values

    plt.bar(tech_columns_array, tech_values_array)
    plt.title(f"Top 20 Technologies for Python Developers")
    plt.xlabel("Technologies")
    plt.ylabel("Number of vacancies")
    plt.xticks(rotation=45)
    plt.show()


def correlation(df: DataFrame) -> None:
    df["minSalary"] = df["salary"].apply(
        lambda x: int(
            pd.Series(x).str.extract(
                '(\d+)', expand=False
            )
        ) if pd.notna(x) else np.nan
    )

    numbers = df[[
        "experience_years",
        "minSalary",
        "reviews_count",
        "english_level"
    ]]
    numbers = numbers.rename(columns={
        "minSalary": "salary",
        "experience_years": "experience",
        "reviews_count": "reviews",
        "english_level": "english"

    })
    plt.figure(figsize=(5, 3))
    ax = sns.heatmap(numbers.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=90)
    plt.title("Correlation Heatmap")
    plt.show()


if __name__ == '__main__':
    subprocess.run(["scrapy", "crawl", "vacancies_spider", "-O", "vacancies.csv"])
    df = pd.read_csv("vacancies.csv")
    show_technologies(df)
    correlation(df)
