import pandas as pd
import os
import matplotlib.pyplot as plt

# Load the dataset
file_path = "data.csv"
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
output_folder = "intensity_videos"
os.makedirs(output_folder, exist_ok=True)

for emotion in emotions:
    intensity_column = f"{emotion}_intensity"  # Column name for intensity

    # Compute the average intensity per video
    avg_df = df.groupby("video_id")[intensity_column].mean().reset_index()
    
    # Rename the column to indicate it's an average
    avg_df.rename(columns={intensity_column: f"avg_{emotion}_intensity"}, inplace=True)

    # Sort videos by highest average intensity
    avg_df = avg_df.sort_values(by=f"avg_{emotion}_intensity", ascending=False)

    # Keep only the top N videos
    top_videos = avg_df.head(N)

    # Merge back with the original dataset to keep related details
    merged_df = df.merge(top_videos, on="video_id", how="inner")

    # Create emotion-specific folder
    emotion_folder = os.path.join(output_folder, f"filtered_{emotion}")
    os.makedirs(emotion_folder, exist_ok=True)

    # Save filtered CSV
    output_file = os.path.join(emotion_folder, f"filtered_{emotion}_videos.csv")
    merged_df.to_csv(output_file, index=False)
    print(f"Saved {output_file}")

    # Generate and save histograms for each parameter
    for param in parameters:
        if param in merged_df.columns:  # Ensure the parameter exists in the dataset
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