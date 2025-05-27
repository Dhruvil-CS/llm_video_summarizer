# audio_transcriber.py

import os
import tempfile
import ffmpeg
import whisper

def transcribe_audio(video_path):
    """
    Extracts the audio from the given video file and transcribes it using Whisper.
    
    Returns:
        transcript (str): The transcribed text from the video audio.
    """
    # Create a temporary file to save the extracted audio
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_audio_file.close()  # close the file so ffmpeg can write to it
    try:
        # Extract audio from the video and save it to the temporary file
        ffmpeg.input(video_path).output(temp_audio_file.name).run(quiet=True, overwrite_output=True)
        
        # Load the Whisper model (using the "base" model, adjust if needed)
        model = whisper.load_model("base")
        result = model.transcribe(temp_audio_file.name)
        transcript = result.get("text", "")
    except Exception as e:
        transcript = f"Error transcribing audio: {str(e)}"
    finally:
        # Clean up the temporary audio file
        os.remove(temp_audio_file.name)
    # print(transcript)
    return transcript

# transcribe_audio("/Users/dhruvilkotecha/Downloads/abc.mp4")