import pandas as pd
from scipy.stats import ttest_ind

# Load the data
df = pd.read_csv("processed_data73.csv")

# Define emotion columns for the target emotions
emotion_columns = {
    "Joy": "LIKERT_video1JOY_Joy",
    "Fear": "LIKERT_video2FEAR_Fear",
    "Anger": "LIKERT_video3ANGER_Anger",
    "Sadness": "LIKERT_video4SADNESS_Sadness"
}

# Loop through emotions: print means and perform t-test
for emotion, col in emotion_columns.items():
    sound_group = df[df["Condition"] == "withsound"][col].dropna()
    nosound_group = df[df["Condition"] == "nosound"][col].dropna()

    # Calculate means
    sound_mean = sound_group.mean()
    nosound_mean = nosound_group.mean()

    # Print means
    print(f"{emotion}:")
    print(f"  With Sound Mean:  {sound_mean: }")
    print(f"  No Sound Mean:    {nosound_mean: }")

    # Perform independent t-test (one-sided: greater in sound group)
    t_stat, p_val = ttest_ind(sound_group, nosound_group, equal_var=False, alternative='greater')

    # Print test result
    if p_val < 0.05:
        print(f"Significant difference (p = {p_val:.4f}) — higher in With Sound group\n")
    else:
        print(f"No significant difference (p = {p_val:.4f})\n")