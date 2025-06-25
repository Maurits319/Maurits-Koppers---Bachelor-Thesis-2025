import pandas as pd

# Emotion label mapping
emotions = {
    1: "Joy", 2: "Sadness", 3: "Fear", 4: "Anger", 5: "Disgust", 6: "Surprise",
    7: "Confusion", 8: "Embarrassment", 9: "Curiosity", 10: "Frustration",
    11: "Enthusiasm", 12: "Relaxed"
}

# Block-to-emotion mapping for Likert questions (no sound version)
main_emotion_map = {
    39: "JOY",
    44: "FEAR",
    49: "ANGER",
    54: "SADNESS"
}

# Forced choice question mapping (no sound version)
forced_mapping = {
    40: "JOY",
    45: "FEAR",
    50: "ANGER",
    55: "SADNESS"
}

# Read CSV, skip unnecessary rows
df = pd.read_csv("data73.csv", sep=';', skiprows=[1, 2])

# Define block and question numbers
likert_blocks = [39, 44, 49, 54]
forced_questions = [40, 45, 50, 55]

# Build new DataFrame
new_df = pd.DataFrame()

# Process Likert blocks
for idx, block in enumerate(likert_blocks, start=1):
    main_emotion = main_emotion_map[block]
    for i in range(1, 13):
        col = f"Q{block}_{i}"
        if col in df.columns:
            new_name = f"LIKERT_video{idx}{main_emotion}_{emotions[i]}"
            new_df[new_name] = df[col]

# Process Forced-choice questions
for idx, q in enumerate(forced_questions, start=1):
    main_emotion = forced_mapping[q]
    col = f"Q{q}"
    if col in df.columns:
        new_name = f"FORCED_video{idx}{main_emotion}"
        new_df[new_name] = df[col]

# Add User column after filtering
new_df.insert(0, "User", range(1, len(new_df) + 1))

# Save to new CSV
new_df.to_csv("nosound_processed_survey_data.csv", index=False)