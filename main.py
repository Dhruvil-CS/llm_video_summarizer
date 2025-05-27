import os
import shutil
import time
import logging
from frame_extractor import extract_key_frames
from text_summarizer import summarize_captions
from generate_captions import generate_caption_blip,generate_caption_git
from audio_transcriber import transcribe_audio
from ocr_text_extractor import extract_ocr_text

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def cleanup_temp_files(directory):
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            logging.info(f"Cleaned up temp directory: {directory}")
    except Exception as e:
        logging.error(f"Error cleaning up files: {str(e)}")

def summarize_video(video_path):
    frames_dir = "temp_frames_" + str(int(time.time()))
    os.makedirs(frames_dir, exist_ok=True)
    logging.info(f"Temporary frames directory: {frames_dir}")
    try:
        logging.info("Step 0: Transcribing audio from video..")
        transcript = transcribe_audio(video_path)
        logging.info(f"Transcription : {transcript}")

        logging.info("Step 1: Extracting key frames...")
        key_frames,frames = extract_key_frames(video_path, frames_dir)
        # key_frames = [i for i in os.listdir(frames_dir)]
        print(key_frames)
        if not key_frames:
            return "Error: No key frames could be extracted from the video"
        logging.info(f"Extracted {len(key_frames)} key frames.")
        
        #Here we will generate OCR
        ocr_texts = []
        for frame in key_frames:
            frame_path = os.path.join(frames_dir,frame)
            ocr = extract_ocr_text(frame_path)
            if ocr:
                ocr_texts.append(f"Frame {frame}: {ocr}")
                logging.info(f"OCR from {frame}: {ocr}")
        logging.info("Step 2: Generating captions from both BLIP and GIT...")
        captions_blip = []
        captions_git = []
        for i, frame in enumerate(key_frames):
            frame_path = os.path.join(frames_dir, frame)
            caption_blip = generate_caption_blip(frame_path)
            caption_git = generate_caption_git(frame_path)

            logging.info(f"Frame {i + 1} - BLIP: {caption_blip}")
            logging.info(f"Frame {i + 1} - GIT:  {caption_git}")

            captions_blip.append(f"Frame {i+1}: {caption_blip}")
            captions_git.append(f"Frame {i+1}: {caption_git}")

        # logging.info("Step 3: Summarizing GIT captions with LLaMa-3...")
        # summary_git = summarize_captions(captions_git)
        # logging.info("Step 4: Summarizing BLIP captions with LLaMa-3...")
        # summary_blip = summarize_captions(captions_blip)

        print("------------------------------------------------------------")
        print(caption_git)
        summary = summarize_captions(captions_git=captions_git,captions_blip=captions_blip,transcript=transcript,ocr_texts=ocr_texts)
        return summary

    except Exception as e:
        logging.error(f"Error processing video: {str(e)}")
        return f"Error: {str(e)}"

    finally:
        cleanup_temp_files(frames_dir)