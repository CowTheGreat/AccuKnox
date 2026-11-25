import argparse
import json
from statistics import mean
from urllib.request import urlopen

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description="Fetch student scores, print the average, and save a bar chart.")
    parser.add_argument("url", help="API URL returning a JSON array of student scores")
    parser.add_argument("--chart", default="student_scores.png")
    args = parser.parse_args()

    with urlopen(args.url, timeout=10) as response:
        students = json.load(response)

    if not students:
        raise ValueError("The API returned no scores.")

    names = []
    scores = []
    for student in students:
        name = student["name"].strip()
        score = student["score"]
        if not name or type(score) not in (int, float) or not 0 <= score <= 100:
            raise ValueError("Each student needs a name and a numeric score from 0 to 100.")
        names.append(name)
        scores.append(score)

    average = mean(scores)
    positions = range(len(names))
    figure, axes = plt.subplots(figsize=(max(6, len(names) * 0.6), 4))
    axes.bar(positions, scores, color="steelblue")
    axes.set_xticks(list(positions), names, rotation=30, ha="right")
    axes.axhline(average, color="darkorange", linestyle="--", label=f"Average: {average:.2f}")
    axes.set(title="Student test scores", xlabel="Student", ylabel="Score", ylim=(0, 100))
    axes.legend()
    figure.tight_layout()
    figure.savefig(args.chart, dpi=150)
    plt.close(figure)

    print(f"Average score: {average:.2f}")
    print(f"Chart saved to {args.chart}")


if __name__ == "__main__":
    main()
