import os
import subprocess
import re

# Path to ffmpeg
ffmpeg_path = "/opt/homebrew/bin/ffmpeg"

# Define the four emotion folders
emotion_folders = ["Anger", "Fear", "Joy", "Sadness"]

# Loop through each emotion folder
for emotion_folder in emotion_folders:
    if os.path.isdir(emotion_folder):
        for file in os.listdir(emotion_folder):
            if file.endswith(".mov") and not file.startswith("cut_"):
                input_path = os.path.join(emotion_folder, file)
                base, ext = os.path.splitext(file)

                match = re.match(r"(sound|no_sound)_(\d+)", base)
                if not match:
                    continue  # Skip files that do not match naming pattern

                prefix, number = match.groups()
                output_file = f"cut_{prefix}_{number}{ext}"
                output_path = os.path.join(emotion_folder, output_file)

                # Temp files
                temp_video = os.path.join(emotion_folder, "temp_video.mp4")
                temp_audio_quiet = os.path.join(emotion_folder, "temp_audio_quiet.aac")
                temp_audio_loud = os.path.join(emotion_folder, "temp_audio_loud.aac")
                temp_audio_mix = os.path.join(emotion_folder, "temp_audio_mix.aac")

                print(f"🎬 Processing {input_path}...")

                # 1. Extract first 20s of video (with no audio)
                subprocess.run([
                    ffmpeg_path, "-i", input_path,
                    "-ss", "0", "-t", "20",
                    "-an", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    temp_video
                ], check=True)

                # 2. Extract quiet audio from first 20s
                subprocess.run([
                    ffmpeg_path, "-i", input_path,
                    "-ss", "0", "-t", "20",
                    "-vn", "-af", "volume=0.15",
                    "-c:a", "aac",
                    temp_audio_quiet
                ], check=True)

                if prefix == "sound":
                    # 3. Extract loud audio from last 20s
                    subprocess.run([
                        ffmpeg_path, "-i", input_path,
                        "-ss", "23", "-t", "20",
                        "-vn", "-af", "volume=5.1",
                        "-c:a", "aac",
                        temp_audio_loud
                    ], check=True)

                    # 4. Mix quiet + loud audio together
                    subprocess.run([
                        ffmpeg_path,
                        "-i", temp_audio_quiet,
                        "-i", temp_audio_loud,
                        "-filter_complex", "amix=inputs=2:duration=first:dropout_transition=0",
                        "-c:a", "aac",
                        temp_audio_mix
                    ], check=True)

                    # 5. Combine video and mixed audio
                    subprocess.run([
                        ffmpeg_path,
                        "-i", temp_video,
                        "-i", temp_audio_mix,
                        "-c:v", "copy",
                        "-c:a", "aac",
                        "-movflags", "+faststart",
                        output_path
                    ], check=True)

                elif prefix == "no_sound":
                    # 3. Combine video and quiet audio only
                    subprocess.run([
                        ffmpeg_path,
                        "-i", temp_video,
                        "-i", temp_audio_quiet,
                        "-c:v", "copy",
                        "-c:a", "aac",
                        "-movflags", "+faststart",
                        output_path
                    ], check=True)

                # 6. Clean up
                for f in [temp_video, temp_audio_quiet, temp_audio_loud, temp_audio_mix]:
                    if os.path.exists(f):
                        os.remove(f)

                print(f"Saved trimmed file: {output_path}\n")