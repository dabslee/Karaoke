import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
import yt_dlp
from mp3_similarity import calculate_similarity_from_audio_segments

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
TEMP_DIR = os.path.join('../temp_audio')
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

    user_audio_file_like = request.files['audio']
    video_id = request.form['videoId']

    if not video_id:
        return jsonify({"error": "videoId cannot be empty"}), 400

    unique_id = str(uuid.uuid4())
    youtube_audio_mp3_path = None
    files_to_clean = []
    user_audio_segment = None
    user_audio_segment = None
    youtube_audio_segment = None

    try:
        # 1. Load user audio directly into AudioSegment
        app.logger.info("Loading user audio into AudioSegment in memory...")
        try:
            user_audio_segment = AudioSegment.from_file(user_audio_file_like, format="webm")
            app.logger.info("User audio loaded into AudioSegment in memory.")
        except Exception as e:
            app.logger.error(f"Error loading user audio into AudioSegment: {e}", exc_info=True)
            return jsonify({"error": "Failed to process user audio file", "details": str(e)}), 400

        # 2. Download YouTube audio as MP3
        # Path for yt-dlp to save the file
        youtube_audio_dl_path_template = os.path.join(TEMP_DIR, f"{unique_id}_youtube")
        # Actual path after download (yt-dlp adds .mp3)
        youtube_audio_mp3_path = f"{youtube_audio_dl_path_template}.mp3"
        
        # Add to cleanup only if download is attempted
        files_to_clean.append(youtube_audio_mp3_path) 

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': youtube_audio_dl_path_template, # yt-dlp appends .mp3 based on preferredcodec
            'noplaylist': True,
            'quiet': True,
            'noprogress': True,
        }
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        app.logger.info(f"Downloading YouTube audio for video ID: {video_id} to {youtube_audio_mp3_path}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([youtube_url])
            if error_code != 0:
                app.logger.error(f"yt-dlp failed to download or convert video {video_id}. Error code: {error_code}")
                return jsonify({"error": f"Failed to download or process YouTube video. yt-dlp error code: {error_code}"}), 500
        
        if not os.path.exists(youtube_audio_mp3_path):
            app.logger.error(f"YouTube audio MP3 file not found after download attempt: {youtube_audio_mp3_path}")
            # This case should ideally be caught by ydl.download error_code, but as a safeguard:
            return jsonify({"error": "YouTube audio MP3 file not found after download attempt."}), 500
        app.logger.info(f"YouTube audio downloaded: {youtube_audio_mp3_path}")

        # Load YouTube audio into AudioSegment
        app.logger.info(f"Loading YouTube audio {youtube_audio_mp3_path} into AudioSegment...")
        try:
            youtube_audio_segment = AudioSegment.from_mp3(youtube_audio_mp3_path) # Or from_file if format might vary
            app.logger.info(f"YouTube audio {youtube_audio_mp3_path} loaded into AudioSegment.")
        except Exception as e:
            app.logger.error(f"Error loading YouTube audio {youtube_audio_mp3_path} into AudioSegment: {e}", exc_info=True)
            return jsonify({"error": "Failed to process downloaded YouTube audio", "details": str(e)}), 500

        # 3. Calculate Similarity using imported function
        app.logger.info("Calculating similarity using in-memory function...")
        # Assuming default target_dbfs = -20.0 is acceptable
        score = calculate_similarity_from_audio_segments(user_audio_segment, youtube_audio_segment)
        app.logger.info(f"Similarity score calculated in memory: {score}")

        if score == -1.0:
            app.logger.error("Failed to calculate similarity using in-memory function. calculate_similarity_from_audio_segments returned -1.0.")
            return jsonify({"error": "Failed to calculate similarity"}), 500
        
        # 4. Return score (score is already a float)
        app.logger.info(f"Successfully calculated score: {score}")
        return jsonify({"score": score}), 200

    # FileNotFoundError might still occur if yt-dlp fails in a way that doesn't create the file
    # but also doesn't return an error code, though less likely.
    # Or if TEMP_DIR is somehow not writable/accessible initially for yt-dlp.
    except FileNotFoundError as fnf_error: 
        app.logger.error(f"File not found during processing: {fnf_error}", exc_info=True)
        return jsonify({"error": f"A required file operation failed: {fnf_error.filename}", "details": str(fnf_error)}), 500
    except Exception as e: 
        # This is a general catch-all. Specific errors for audio loading are handled above.
        # yt-dlp errors are also handled specifically.
        app.logger.error(f"An unexpected error occurred in calculate_score: {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500
    finally:
        # 5. Cleanup
        # files_to_clean now only contains youtube_audio_mp3_path if download was attempted.
        app.logger.info(f"Attempting to cleanup files: {files_to_clean}")
        cleanup_files(files_to_clean)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
