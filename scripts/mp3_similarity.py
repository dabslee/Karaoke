import argparse
import sys
import librosa
import numpy as np
from pydub import AudioSegment

MIN_FRAMES_THRESHOLD = 10 # Minimum number of valid frames for comparison

# Define the new function to calculate similarity from audio segments
def calculate_similarity_from_audio_segments(audio_segment1, audio_segment2, target_dbfs=-20.0):
    """
    Calculates similarity between two audio segments based on their F0 pitch contours using DTW.
    Volume is normalized before F0 extraction.

    Args:
        audio_segment1 (AudioSegment): The first audio segment.
        audio_segment2 (AudioSegment): The second audio segment.
        target_dbfs (float): Target dBFS for volume normalization.

    Returns:
        float: Similarity percentage (0-100%).
               Returns -1.0 if an error occurs.
    """
    try:
        f0_contours = []
        for audio_segment in [audio_segment1, audio_segment2]:
            normalized_audio = audio_segment.apply_gain(target_dbfs - audio_segment.dBFS)
            samples = np.array(normalized_audio.get_array_of_samples()).astype(np.float32)
            
            if normalized_audio.channels == 2:
                samples = samples.reshape((-1, 2)).mean(axis=1)
            
            # Normalize sample values
            if normalized_audio.sample_width == 1: # 8-bit
                samples /= np.iinfo(np.int8).max 
            elif normalized_audio.sample_width == 2: # 16-bit
                samples /= np.iinfo(np.int16).max
            elif normalized_audio.sample_width == 4: # 32-bit
                samples /= np.iinfo(np.int32).max
            # Add other sample widths if necessary, though pydub often converts to 16-bit internally for many ops

            sr = normalized_audio.frame_rate
            f0 = _calculate_f0_contour(samples, sr)
            f0_contours.append(f0)

        f0_1, f0_2 = f0_contours

        # DTW expects 2D arrays of shape (n_features, n_frames)
        # For F0, n_features is 1.
        D, wp = librosa.sequence.dtw(
            X=f0_1.reshape(1, -1),
            Y=f0_2.reshape(1, -1),
            metric='euclidean' # Euclidean distance between Hz values
        )

        # Extract aligned F0 values using the warping path
        idx1 = wp[:, 0]
        idx2 = wp[:, 1]
        aligned_f0_1 = f0_1[idx1]
        aligned_f0_2 = f0_2[idx2]

        valid_indices = np.where((aligned_f0_1 > 1e-6) & (aligned_f0_2 > 1e-6))[0]

        if len(valid_indices) < MIN_FRAMES_THRESHOLD:
            print(f"Warning: Insufficient number of valid voiced frames for comparison (found {len(valid_indices)}, need {MIN_FRAMES_THRESHOLD}). Similarity set to 0.", file=sys.stderr)
            return 0.0

        f0_1_valid = aligned_f0_1[valid_indices]
        f0_2_valid = aligned_f0_2[valid_indices]

        cent_diffs = 1200 * np.abs(np.log2(f0_1_valid / f0_2_valid))
        avg_cent_diff = np.mean(cent_diffs)

        if np.isnan(avg_cent_diff):
            print("Warning: Average cent difference is NaN. Setting similarity to 0.", file=sys.stderr)
            return 0.0

        similarity_tuning_factor = 5.0
        similarity_percentage = max(0.0, 100.0 - (avg_cent_diff / similarity_tuning_factor))

        return similarity_percentage

    except Exception as e:
        print(f"An error occurred during F0 contour processing or DTW: {e}", file=sys.stderr)
        # import traceback
        # print(traceback.format_exc(), file=sys.stderr) # Useful for debugging
        return -1.0

def _calculate_f0_contour(samples, sr, fmin_note='C2', fmax_note='C7'):
    """Calculates and interpolates the F0 contour for given audio samples."""
    f0, voiced_flag, voiced_probs = librosa.pyin(
        samples,
        fmin=librosa.note_to_hz(fmin_note),
        fmax=librosa.note_to_hz(fmax_note)
    )

    # Interpolate NaN values in f0
    non_nan_indices = np.where(~np.isnan(f0))[0]
    if len(non_nan_indices) == 0:  # All NaN, maybe complete silence or unvoiced
        f0 = np.zeros_like(f0)  # Set all to 0
    else:
        nan_indices = np.where(np.isnan(f0))[0]
        if len(nan_indices) > 0:
            # Use first and last non-NaN value for extrapolation if NaNs are at edges
            first_non_nan_val = f0[non_nan_indices[0]]
            last_non_nan_val = f0[non_nan_indices[-1]]
            f0[nan_indices] = np.interp(
                nan_indices,
                non_nan_indices,
                f0[non_nan_indices],
                left=first_non_nan_val,  # Extrapolate left
                right=last_non_nan_val   # Extrapolate right
            )
    # Safeguard if any NaNs remain after interpolation (e.g. if all input was NaN initially)
    f0[np.isnan(f0)] = 0.0
    return f0

def calculate_similarity(file1_path, file2_path, target_dbfs=-20.0):
    """
    Loads two audio files and calculates their similarity based on F0 pitch contours.

    Args:
        file1_path (str): Path to the first audio file.
        file2_path (str): Path to the second audio file.
        target_dbfs (float): Target dBFS for volume normalization.

    Returns:
        float: Similarity percentage (0-100%).
               Returns -1.0 if an error occurs.
    """
    try:
        # Load audio files
        audio1 = AudioSegment.from_file(file1_path)
        audio2 = AudioSegment.from_file(file2_path)

        # Call the new function that works with AudioSegment objects
        return calculate_similarity_from_audio_segments(audio1, audio2, target_dbfs)

    except FileNotFoundError as e:
        print(f"Error: Audio file not found: {e.filename}", file=sys.stderr)
        return -1.0
    except Exception as e: # Catch other pydub loading errors (e.g., format not supported)
        print(f"Error loading audio file. Ensure ffmpeg is installed and supports the file format. File: {e}", file=sys.stderr)
        # Consider more specific exception handling for pydub if needed, e.g. CouldntDecodeError
        return -1.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate pitch-based similarity between two audio files using F0 contours and DTW."
    )
    parser.add_argument("file1", help="Path to the first audio file.")
    parser.add_argument("file2", help="Path to the second audio file.")
    parser.add_argument(
        "--target_dbfs",
        type=float,
        default=-20.0,
        help="Target dBFS for volume normalization (default: -20.0)."
    )
    # Consider adding --fmin and --fmax for YIN if needed later

    args = parser.parse_args()

    similarity = calculate_similarity(args.file1, args.file2, args.target_dbfs)
    
    if similarity >= 0:
        print(f"{similarity:.2f}") # Print similarity to stdout for machine readability
    else:
        # Errors should have been printed to stderr by the functions.
        # Exit with a non-zero status code to indicate failure to calling scripts/processes.
        sys.exit(1)
