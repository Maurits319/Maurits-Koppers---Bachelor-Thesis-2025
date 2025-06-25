import pandas as pd
import os

selected_videos = {
    "anger": [141, 101, 308, 73],
    "disgust": [286, 234, 188, 409],
    "fear": [217, 29, 281,17],
    "joy": [92, 295, 248, 200],
    "sadness": [442, 218, 327, 130],
    "surprise": [404, 389, 393, 166]
}

columns_base = [
    "participant_id", "video_id", "wander_speed", "wander_roundness", "wander_cycle_rate",
    "blink_temperature", "blink_slope", "blink_cycle_rate", "beep_pitch", "beep_slope", "beep_cycle_rate",
    "joy_intensity", "sadness_intensity", "fear_intensity", "anger_intensity",
    "disgust_intensity", "surprise_intensity", "pleasure", "arousal", "dominance", "appraisal"
]

output_root = "4 videos csvs"
os.makedirs(output_root, exist_ok=True)

for emotion, video_ids in selected_videos.items():
    try:
        df_intensity = pd.read_csv(f"promising_videos/filtered_{emotion}/filtered_{emotion}_videos.csv")
        df_purity = pd.read_csv(f"purity_videos/filtered_{emotion}/filtered_{emotion}_videos.csv")
    except FileNotFoundError:
        print(f"Missing files for {emotion}")
        continue

    df_intensity = df_intensity[df_intensity["video_id"].isin(video_ids)].drop_duplicates("video_id")
    df_purity = df_purity[df_purity["video_id"].isin(video_ids)].drop_duplicates("video_id")

    merged = pd.merge(df_intensity, df_purity, on="video_id", suffixes=('_int', '_pur'), how="outer")

    for col in columns_base:
        if col not in merged and f"{col}_int" in merged:
            merged[col] = merged[f"{col}_int"]
        elif col not in merged and f"{col}_pur" in merged:
            merged[col] = merged[f"{col}_pur"]

    merged[f"avg_{emotion}_intensity"] = merged.get(f"avg_{emotion}_intensity", pd.NA)
    merged[f"{emotion}_purity"] = merged.get(f"{emotion}_purity", pd.NA)

    cols_to_save = [col for col in columns_base + [f"avg_{emotion}_intensity", f"{emotion}_purity"] if col in merged]
    
    # Apply custom video_id order
    custom_order = pd.Categorical(merged["video_id"], categories=video_ids, ordered=True)
    final = merged[cols_to_save].copy()
    final["video_id_order"] = custom_order
    final = final.sort_values("video_id_order").drop(columns="video_id_order")

    out_folder = os.path.join(output_root, emotion)
    os.makedirs(out_folder, exist_ok=True)

    output_csv = os.path.join(out_folder, f"{emotion}_selected_videos.csv")
    final.to_csv(output_csv, index=False)
    print(f"Saved {emotion} to {output_csv}")

    # Save summary statistics
    summary = final.describe()
    summary_path = os.path.join(out_folder, f"summary_{emotion}.csv")
    summary.to_csv(summary_path)
    print(f"Summary stats saved to {summary_path}")