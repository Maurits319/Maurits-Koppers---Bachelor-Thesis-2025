import pandas as pd
import os
import matplotlib.pyplot as plt

# Load the new dataset with purity scores
file_path = "data_with_purity.csv"
df = pd.read_csv(file_path)

# List of emotions to process
emotions = ["anger", "sadness", "joy", "fear", "disgust", "surprise"]

# Number of top videos to keep per emotion
N = 20

# Parameters
parameters = [
    "wander_speed", "wander_roundness", "wander_cycle_rate",
    "blink_temperature", "blink_slope", "blink_cycle_rate",
    "beep_pitch", "beep_slope", "beep_cycle_rate"
]

# Create output folder
output_folder = "purity_videos"
os.makedirs(output_folder, exist_ok=True)

for emotion in emotions:
    purity_column = f"{emotion}_purity"

    if purity_column not in df.columns:
        print(f"Error: Column '{purity_column}' not found in dataset.")
        continue

    # Compute average purity scores per video
    purity_avg_df = df.groupby("video_id", as_index=False)[purity_column].mean()

    # Sort by highest purity score
    purity_avg_df = purity_avg_df.sort_values(by=purity_column, ascending=False)

    # Keep only the top N videos
    top_videos = purity_avg_df.head(N)

    # Merge back with original dataset to retain details, keeping only the purity score from top_videos
    merged_df = df.merge(top_videos[["video_id", purity_column]], on="video_id", how="inner")

    # Rename the merged purity column to keep only the averaged purity value
    merged_df = merged_df.drop(columns=[purity_column + "_x"]).rename(columns={purity_column + "_y": purity_column})

    #Remove other purity columns except for the focus emotion
    purity_columns_to_drop = [f"{e}_purity" for e in emotions if e != emotion]
    merged_df = merged_df.drop(columns=purity_columns_to_drop, errors="ignore")

    # Keep only highest individual rating per video
    merged_df = merged_df.sort_values(by=[purity_column], ascending=False)
    merged_df = merged_df.drop_duplicates(subset=["video_id"], keep="first")

    # Create emotion-specific folder
    emotion_folder = os.path.join(output_folder, f"filtered_{emotion}")
    os.makedirs(emotion_folder, exist_ok=True)

    # Save final filtered CSV with 3 decimal places
    output_file = os.path.join(emotion_folder, f"filtered_{emotion}_videos.csv")
    merged_df.to_csv(output_file, index=False)
    print(f"Saved final filtered dataset for {emotion} to {output_file}")

    # Generate and save histograms for each parameter
    for param in parameters:
        if param in merged_df.columns:
            plt.figure(figsize=(8, 5))
            plt.hist(merged_df[param], bins=10, color='skyblue', edgecolor='black')
            plt.xlabel(param)
            plt.ylabel("Frequency")
            plt.title(f"Histogram of {param} - {emotion}")
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Save plot
            plot_path = os.path.join(emotion_folder, f"{param}_histogram.png")
            plt.savefig(plot_path)
            plt.close()
            print(f"Saved {plot_path}")

    # Compute and save summary statistics
    summary_stats = merged_df[parameters].describe()
    summary_stats_file = os.path.join(emotion_folder, f"summary_{emotion}.csv")
    summary_stats.to_csv(summary_stats_file)
    print(f"Saved {summary_stats_file}")