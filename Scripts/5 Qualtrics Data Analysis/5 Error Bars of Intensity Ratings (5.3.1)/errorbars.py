import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Input files
sound_file = "Data/sound_processed_survey_data.csv"
nosound_file = "Data/nosound_processed_survey_data.csv"

# Settings
emotions = ['JOY', 'FEAR', 'ANGER', 'SADNESS']
options = ['Joy', 'Sadness', 'Fear', 'Anger', 'Disgust', 'Surprise',
           'Confusion', 'Embarrassment', 'Curiosity', 'Frustration',
           'Enthusiasm', 'Relaxed']

# Output folders
os.makedirs("withsound_errorbars", exist_ok=True)
os.makedirs("nosound_errorbars", exist_ok=True)

# Load data
df_sound = pd.read_csv(sound_file)
df_nosound = pd.read_csv(nosound_file)

# Plotting function 
def make_plot(df, condition_name, folder):
    for i, emotion in enumerate(emotions, start=1):
        pattern = f"LIKERT_video{i}{emotion}_"
        emotion_cols = [col for col in df.columns if col.startswith(pattern)]
        x_labels = [col.replace(pattern, '') for col in emotion_cols]

        means = df[emotion_cols].mean()
        stds = df[emotion_cols].std()
        x_pos = np.arange(len(x_labels))

        # Compute lower and upper bounds of error bars
        lower_bounds = means - stds
        upper_bounds = means + stds

        # Default y-axis limits
        y_min = 0
        y_max = 4

        # Extend if needed
        if lower_bounds.min() < 0:
            y_min = -1
        if upper_bounds.max() > 4:
            y_max = 5

        # Plot
        fig, ax = plt.subplots(figsize=(9, 4))

        ax.yaxis.grid(True, linestyle='-', color='lightgray', linewidth=0.7, zorder=0)

        ax.errorbar(
            x_pos, means, yerr=stds,
            fmt='o', ecolor='black', color='deepskyblue',
            capsize=4, elinewidth=1.2, linestyle='none',
            markerfacecolor='deepskyblue', markeredgecolor='black', markersize=7, zorder=3
        )

        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_labels, rotation=45, ha='right')
        ax.set_yticks(np.arange(np.floor(y_min), np.ceil(y_max) + 1, 1))
        ax.set_ylim(y_min, y_max)
        ax.set_ylabel("Intensity Rating")
        ax.set_title(f"{emotion.capitalize()} ground truth - {condition_name}", fontsize=12)

        plt.tight_layout()
        plt.savefig(f"{folder}/{emotion}_errorbar.png", dpi=300)
        plt.close()

# === Generate plots ===
make_plot(df_sound, "With Sound", "withsound_errorbars")
make_plot(df_nosound, "No Sound", "nosound_errorbars")

print("Error bar plots generated.")