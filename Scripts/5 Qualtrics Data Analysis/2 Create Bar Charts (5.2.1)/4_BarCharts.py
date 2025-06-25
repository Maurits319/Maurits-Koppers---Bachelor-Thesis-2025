import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Define emotion labels
emotions = [
    "Joy", "Sadness", "Fear", "Anger", "Disgust", "Surprise",
    "Confusion", "Embarrassment", "Curiosity", "Frustration",
    "Enthusiasm", "Relaxed"
]

# Ground truth per video
video_to_emotion = {
    1: "JOY",
    2: "FEAR",
    3: "ANGER",
    4: "SADNESS"
}

# File paths
sound_file = "processed_data73_withsound.csv"
nosound_file = "processed_data73_nosound.csv"

# Output folders
base_folder = "4 Staafdiagrammen aantal stemmen 12 opties"
sound_folder = os.path.join(base_folder, "Sound")
nosound_folder = os.path.join(base_folder, "Nosound")
combined_folder = os.path.join(base_folder, "Combined")
os.makedirs(sound_folder, exist_ok=True)
os.makedirs(nosound_folder, exist_ok=True)
os.makedirs(combined_folder, exist_ok=True)

# Load data
df_sound = pd.read_csv(sound_file)
df_nosound = pd.read_csv(nosound_file)

# Color mapping
condition_colors = {
    "sound": "dodgerblue",
    "nosound": "indianred"
}

# INDIVIDUAL plots (with accuracy) — based on which file the data comes from
for condition, df, folder in [("sound", df_sound, sound_folder), ("nosound", df_nosound, nosound_folder)]:
    for video_num, true_emotion in video_to_emotion.items():
        col = f"FORCED_video{video_num}{true_emotion}"
        if col not in df.columns:
            continue

        counts = df[col].value_counts().reindex(emotions, fill_value=0)
        total = counts.sum()
        correct = counts.get(true_emotion.capitalize(), 0)
        acc = (correct / total) * 100 if total > 0 else 0

        plt.figure(figsize=(10, 6))
        counts.plot(kind='bar', color=condition_colors[condition])
        plt.title(f"{true_emotion.capitalize()} ground truth (Video {video_num}) - {condition.capitalize()}")
        plt.ylabel("Number of Votes")
        plt.xticks(rotation=45, ha="right")
        plt.legend([f"Accuracy: {acc:.1f}% ({correct}/{total})"])
        plt.tight_layout()

        plot_path = os.path.join(folder, f"video{video_num}_{true_emotion}_{condition}.png")
        plt.savefig(plot_path)
        plt.close()

# COMBINED plots (compare sound and nosound side-by-side)
for video_num, true_emotion in video_to_emotion.items():
    col = f"FORCED_video{video_num}{true_emotion}"
    if col not in df_sound.columns or col not in df_nosound.columns:
        continue

    sound_counts = df_sound[col].value_counts().reindex(emotions, fill_value=0)
    nosound_counts = df_nosound[col].value_counts().reindex(emotions, fill_value=0)

    total_sound = sound_counts.sum()
    correct_sound = sound_counts.get(true_emotion.capitalize(), 0)
    acc_sound = (correct_sound / total_sound) * 100 if total_sound > 0 else 0

    total_nosound = nosound_counts.sum()
    correct_nosound = nosound_counts.get(true_emotion.capitalize(), 0)
    acc_nosound = (correct_nosound / total_nosound) * 100 if total_nosound > 0 else 0

    x = np.arange(len(emotions))
    width = 0.35

    plt.figure(figsize=(8, 6))
    plt.bar(x - width/2, nosound_counts, width,
            label=f"No Sound (Acc: {acc_nosound:.1f}% | {correct_nosound}/{total_nosound})", color='indianred')
    plt.bar(x + width/2, sound_counts, width,
            label=f"With Sound (Acc: {acc_sound:.1f}% | {correct_sound}/{total_sound})", color='dodgerblue')

    plt.xticks(x, emotions, rotation=45, ha="right")
    plt.ylabel("Number of Votes")
    plt.title(f"{true_emotion.capitalize()} ground truth (Video {video_num}) - With vs Without Sound")
    plt.legend()
    plt.tight_layout()

    combined_path = os.path.join(combined_folder, f"video{video_num}_{true_emotion}_combined.png")
    plt.savefig(combined_path)
    plt.close()