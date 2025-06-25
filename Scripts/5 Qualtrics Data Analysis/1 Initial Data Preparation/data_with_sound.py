import pandas as pd

# Emotion label mapping
emotions = {
    1: "Joy", 2: "Sadness", 3: "Fear", 4: "Anger", 5: "Disgust", 6: "Surprise",
    7: "Confusion", 8: "Embarrassment", 9: "Curiosity", 10: "Frustration",
    11: "Enthusiasm", 12: "Relaxed"
}

# Block-to-emotion mapping for main emotion label per video
main_emotion_map = {
    12: "JOY",
    24: "FEAR",
    29: "ANGER",
    34: "SADNESS"
}

# Forced choice question mapping (by question number)
forced_mapping = {
    13: "JOY",
    25: "FEAR",
    30: "ANGER",
    35: "SADNESS"
}

# Read CSV
df = pd.read_csv("data73.csv", sep=';', skiprows=[1, 2])

# List of columns to extract
likert_blocks = [12, 24, 29, 34]
forced_questions = [13, 25, 30, 35]

# Build new DataFrame
new_df = pd.DataFrame()

# Add User column
new_df["User"] = range(1, len(df) + 1)

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

# Save to CSV
new_df.to_csv("sound_processed_survey_data.csv", index=False)