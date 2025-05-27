import cv2
import os
import ffmpeg
import numpy as np
from skimage.metrics import structural_similarity as ssim

def extract_key_frames(video_path, output_dir="frames", fps=1, similarity_threshold=0.8):
    """
    Extract key frames based on SSIM, and also store the frame immediately before each detected key frame.
    Returns a sorted list of selected frame filenames.
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. Extract frames via FFmpeg
    (
        ffmpeg.input(video_path)
              .filter('fps', fps=fps)
              .output(os.path.join(output_dir, 'frame_%04d.jpg'), vsync='vfr')
              .run(quiet=True, overwrite_output=True)
    )

    # 2. Gather and sort frame files
    frames = sorted([f for f in os.listdir(output_dir) if f.lower().endswith('.jpg')])
    if not frames:
        raise ValueError("No frames extracted")

    key_frames = []
    prev_gray = None
    prev_file = None

    for frame_file in frames:
        frame_path = os.path.join(output_dir, frame_file)
        img = cv2.imread(frame_path)
        if img is None:
            continue

        # Convert to grayscale for SSIM comparison
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (320, 240))  # downscale for speed

        if prev_gray is None:
            # Always take the first frame
            key_frames.append(frame_file)
        else:
            score = ssim(prev_gray, gray)
            if score < similarity_threshold:
                # Store the previous frame (context) if not already added
                if prev_file and prev_file not in key_frames:
                    key_frames.append(prev_file)
                # Then store the current key frame
                key_frames.append(frame_file)

        # Update previous for next iteration
        prev_gray = gray
        prev_file = frame_file

    # Return unique, sorted list
    selected = sorted(dict.fromkeys(key_frames), key=lambda x: frames.index(x))
    return selected, frames

# if __name__ == '__main__':
#     video = 'input.mp4'
#     keys, all_frames = extract_key_frames_with_context(video, fps=1, similarity_threshold=0.75)
#     print('Selected key frames:', keys)
