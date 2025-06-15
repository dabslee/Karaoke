import argparse
import sys
import librosa
import numpy as np
from pydub import AudioSegment

MIN_FRAMES_THRESHOLD = 10 # Minimum number of valid frames for comparison

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
    Calculates similarity between two MP3s based on their F0 pitch contours using DTW.
    Volume is normalized before F0 extraction.

    Args:
        file1_path (str): Path to the first MP3 file.
        file2_path (str): Path to the second MP3 file.
        target_dbfs (float): Target dBFS for volume normalization.

    Returns:
        float: Similarity percentage (0-100%).
               Returns -1.0 if an error occurs.
    """
    try:
        f0_contours = []
        for file_path in [file1_path, file2_path]:
            try:
                audio = AudioSegment.from_mp3(file_path)
            except FileNotFoundError:
                 raise FileNotFoundError(f"Audio file not found: {file_path}")
            except Exception as e:
                print(f"Error loading MP3 with pydub: {file_path}. Ensure ffmpeg is installed. Error: {e}", file=sys.stderr)
                return -1.0

            normalized_audio = audio.apply_gain(target_dbfs - audio.dBFS)
            samples = np.array(normalized_audio.get_array_of_samples()).astype(np.float32)
            if normalized_audio.channels == 2:
                samples = samples.reshape((-1, 2)).mean(axis=1)
            
            if normalized_audio.sample_width == 2: # 16-bit
                samples /= np.iinfo(np.int16).max
            elif normalized_audio.sample_width == 4: # 32-bit
                samples /= np.iinfo(np.int32).max
            # Add other sample widths if necessary

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
        # wp is a list of pairs (idx1, idx2)
        idx1 = wp[:, 0]
        idx2 = wp[:, 1]
        aligned_f0_1 = f0_1[idx1]
        aligned_f0_2 = f0_2[idx2]

        # Filter out pairs where either F0 is close to zero (unvoiced/silence)
        # Use a small threshold to avoid division by zero or issues with log(0)
        valid_indices = np.where((aligned_f0_1 > 1e-6) & (aligned_f0_2 > 1e-6))[0]

        if len(valid_indices) < MIN_FRAMES_THRESHOLD:
            print(f"Warning: Insufficient number of valid voiced frames for comparison (found {len(valid_indices)}, need {MIN_FRAMES_THRESHOLD}). Similarity set to 0.", file=sys.stderr)
            return 0.0

        f0_1_valid = aligned_f0_1[valid_indices]
        f0_2_valid = aligned_f0_2[valid_indices]

        # Calculate difference in cents
        # cent_diff = 1200 * |log2(f1/f2)|
        # Avoid division by zero if any f0 is still zero after filtering (shouldn't happen with >1e-6)
        cent_diffs = 1200 * np.abs(np.log2(f0_1_valid / f0_2_valid))
        
        avg_cent_diff = np.mean(cent_diffs)

        if np.isnan(avg_cent_diff): # Should not happen if valid_indices check is robust
            print("Warning: Average cent difference is NaN. Setting similarity to 0.", file=sys.stderr)
            return 0.0

        # Convert average cent difference to similarity percentage
        # Max diff of 500 cents -> 0% similarity. 0 cents diff -> 100%.
        # This means 1 cent diff reduces similarity by 0.2 points (100/500).
        # Or, using the provided formula: similarity = max(0, 100 - avg_cent_diff / 5.0)
        # A divisor of 5.0 means that if avg_cent_diff is 50, similarity is 90.
        # If avg_cent_diff is 500, similarity is 0.
        similarity_tuning_factor = 5.0 
        similarity_percentage = max(0.0, 100.0 - (avg_cent_diff / similarity_tuning_factor))

        return similarity_percentage

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return -1.0
    except Exception as e:
        print(f"An error occurred during processing: {e}", file=sys.stderr)
        # import traceback
        # print(traceback.format_exc(), file=sys.stderr) # Useful for debugging
        return -1.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate pitch-based similarity between two MP3 files using F0 contours and DTW."
    )
    parser.add_argument("file1", help="Path to the first MP3 file.")
    parser.add_argument("file2", help="Path to the second MP3 file.")
    parser.add_argument(
        "--target_dbfs",
        type=float,
        default=-20.0,
        help="Target dBFS for volume normalization (default: -20.0)."
    )
    # Consider adding --fmin and --fmax for YIN if needed later

    args = parser.parse_args()

    try:
        similarity = calculate_similarity(args.file1, args.file2, args.target_dbfs)
        if similarity >= 0: # calculate_similarity returns -1.0 on error
            # Print only the numerical score to stdout for machine readability
            print(f"{similarity:.2f}")
        else:
            # If calculate_similarity returned an error code like -1.0,
            # it would have already printed to stderr.
            # Optionally, print a generic error to stderr here if no specific error was printed by the function.
            # For now, we assume calculate_similarity handles its own error reporting to stderr.
            # If calculate_similarity is supposed to always print to stderr on error,
            # then we might not need an else here, or just exit with an error code.
            # Example:
            # print("Error: Failed to calculate similarity.", file=sys.stderr)
            sys.exit(1) # Exit with a non-zero status code to indicate failure
    except Exception as e:
        # This catches errors not handled within calculate_similarity or arg parsing issues
        print(f"An unexpected error occurred in main: {e}", file=sys.stderr)
        sys.exit(1) # Exit with a non-zero status code
