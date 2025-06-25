import pandas as pd

# Load the dataset
file_path = "data.csv"
df = pd.read_csv(file_path)

# List of emotions to process
emotions = ["anger", "sadness", "joy", "fear", "disgust", "surprise"]

# Compute purity scores for each emotion
for emotion in emotions:
    intensity_column = f"{emotion}_intensity"

    # Compute total intensity across all emotion columns
    total_intensity = df[[f"{e}_intensity" for e in emotions]].sum(axis=1).replace(0, 1)

    # Compute base purity
    purity = df[intensity_column] / total_intensity

    # Save to new column
    df[f"{emotion}_purity"] = purity

# Save updated dataset
output_file = "data_with_purity.csv"
df.to_csv(output_file, index=False)
print(f"Saved new dataset with enhanced purity scores: {output_file}")