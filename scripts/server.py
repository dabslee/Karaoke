import os
import uuid
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
import yt_dlp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
TEMP_DIR = os.path.join('../temp_audio')

# Ensure temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

def cleanup_files(files_to_delete):
    """Removes a list of files."""
    for f_path in files_to_delete:
        if f_path and os.path.exists(f_path):
            try:
                os.remove(f_path)
                app.logger.info(f"Successfully deleted temp file: {f_path}")
            except Exception as e:
                app.logger.error(f"Error deleting temp file {f_path}: {e}")

@app.route('/api/calculate_score', methods=['POST'])
def calculate_score():
    if 'audio' not in request.files or 'videoId' not in request.form:
        return jsonify({"error": "Missing audio file or videoId"}), 400

    user_audio_file = request.files['audio']
    video_id = request.form['videoId']

    if not video_id:
        return jsonify({"error": "videoId cannot be empty"}), 400

    unique_id = str(uuid.uuid4())
    user_audio_webm_path = None
    user_audio_mp3_path = None
    youtube_audio_mp3_path = None
    files_to_clean = []

    try:
        # 1. Save and convert user audio
        user_audio_webm_path = os.path.join(TEMP_DIR, f"{unique_id}_user.webm")
        files_to_clean.append(user_audio_webm_path)
        user_audio_file.save(user_audio_webm_path)
        app.logger.info(f"User audio saved to {user_audio_webm_path}")

        user_audio_mp3_path = os.path.join(TEMP_DIR, f"{unique_id}_user.mp3")
        files_to_clean.append(user_audio_mp3_path)
        audio = AudioSegment.from_file(user_audio_webm_path, format="webm")
        audio.export(user_audio_mp3_path, format="mp3")
        app.logger.info(f"User audio converted to MP3: {user_audio_mp3_path}")

        # 2. Download YouTube audio as MP3
        youtube_audio_mp3_path = os.path.join(TEMP_DIR, f"{unique_id}_youtube.mp3")
        files_to_clean.append(youtube_audio_mp3_path)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(TEMP_DIR, f"{unique_id}_youtube"), # yt-dlp appends .mp3
            'noplaylist': True,
            'quiet': True,
            'noprogress': True,
        }
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        app.logger.info(f"Downloading YouTube audio for video ID: {video_id}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([youtube_url])
            if error_code != 0:
                app.logger.error(f"yt-dlp failed to download or convert video {video_id}. Error code: {error_code}")
                # Ensure the specific path yt-dlp would create is added for cleanup, even if it failed.
                # yt-dlp might create the file before failing or leave partial files.
                # The base name is unique_id_youtube, and .mp3 is added by postprocessor.
                potential_failed_path = os.path.join(TEMP_DIR, f"{unique_id}_youtube.mp3")
                if potential_failed_path not in files_to_clean:
                     files_to_clean.append(potential_failed_path)
                return jsonify({"error": f"Failed to download or process YouTube video. yt-dlp error code: {error_code}"}), 500
        
        # yt-dlp should have created youtube_audio_mp3_path (e.g. TEMP_DIR/unique_id_youtube.mp3)
        if not os.path.exists(youtube_audio_mp3_path):
            # Check for common variations if yt-dlp naming is unexpected
            # This is a fallback, usually outtmpl + .mp3 is reliable
            app.logger.warning(f"Expected YouTube MP3 path not found: {youtube_audio_mp3_path}. Checking for alternatives.")
            # If the file isn't there, it's a critical issue.
            return jsonify({"error": "YouTube audio MP3 file not found after download attempt."}), 500
        app.logger.info(f"YouTube audio downloaded and converted to MP3: {youtube_audio_mp3_path}")


        # 3. Execute mp3_similarity.py
        similarity_script_path = 'mp3_similarity.py'
        if not os.path.exists(similarity_script_path):
            app.logger.error(f"Similarity script not found at {similarity_script_path}")
            return jsonify({"error": "Similarity script not found"}), 500

        command = [
            'python3', 
            similarity_script_path,
            user_audio_mp3_path,
            youtube_audio_mp3_path
        ]
        app.logger.info(f"Executing similarity script: {' '.join(command)}")
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            app.logger.error(f"Similarity script execution failed. Return code: {process.returncode}")
            app.logger.error(f"Script stderr: {stderr}")
            return jsonify({"error": "Failed to calculate similarity", "details": stderr}), 500
        
        app.logger.info(f"Similarity script stdout: {stdout}")

        # 4. Parse score
        try:
            # Expected output: "Similarity Score: XX.YY%"
            score_line = stdout.strip().splitlines()[-1] # Get the last line
            if "Similarity Score:" in score_line:
                score_str = score_line.split("Similarity Score:")[1].strip().replace('%', '')
                score = float(score_str)
            else:
                raise ValueError("Output format from script is unexpected.")
        except Exception as e:
            app.logger.error(f"Failed to parse score from script output: {stdout}. Error: {e}")
            return jsonify({"error": "Failed to parse similarity score", "details": str(e)}), 500

        # 5. Return score
        app.logger.info(f"Successfully calculated score: {score}")
        return jsonify({"score": score}), 200

    except FileNotFoundError as fnf_error:
        app.logger.error(f"File not found during processing: {fnf_error}")
        return jsonify({"error": f"A required file was not found: {fnf_error.filename}", "details": str(fnf_error)}), 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500
    finally:
        # 6. Cleanup
        app.logger.info(f"Attempting to cleanup files: {files_to_clean}")
        cleanup_files(files_to_clean)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
