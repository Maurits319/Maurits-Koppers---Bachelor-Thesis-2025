from statsmodels.stats.proportion import proportions_ztest

# Data for each emotion
data = {
    "Joy":      {"sound": (4, 20), "nosound": (4, 27)},
    "Fear":     {"sound": (5, 20), "nosound": (2, 27)},
    "Anger":    {"sound": (10, 20), "nosound": (7, 27)},
    "Sadness":  {"sound": (5, 20), "nosound": (5, 27)}
}

for emotion, values in data.items():
    count = [values["sound"][0], values["nosound"][0]]
    nobs = [values["sound"][1], values["nosound"][1]]
    stat, pval = proportions_ztest(count, nobs, alternative='larger')  # one-sided test
    result = "Significant" if pval < 0.05 else "Not Significant"
    print(f"{emotion}: p = {pval:.4f} → {result}")