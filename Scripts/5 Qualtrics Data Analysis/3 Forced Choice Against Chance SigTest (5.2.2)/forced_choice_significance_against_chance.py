from scipy.stats import binomtest

# Format: (correct_answers, total_answers)
data = {
    "Joy": {
        "Sound": (4, 20),
        "No Sound": (4, 27)
    },
    "Fear": {
        "Sound": (5, 20),
        "No Sound": (2, 27)
    },
    "Anger": {
        "Sound": (10, 20),
        "No Sound": (7, 27)
    },
    "Sadness": {
        "Sound": (5, 20),
        "No Sound": (5, 27)
    }
}

# Binomial test for each case against chance level (1/12)
chance_level = 1 / 12
results = {}

for emotion, conditions in data.items():
    results[emotion] = {}
    for condition, (x, n) in conditions.items():
        test_result = binomtest(x, n, chance_level, alternative='greater')
        results[emotion][condition] = {
            "correct": x,
            "total": n,
            "p_value": test_result.pvalue,
            "significant": test_result.pvalue < 0.05
        }

print(results)