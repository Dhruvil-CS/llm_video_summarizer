import logging
from main import summarize_video

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# video_path = "/Users/dhruvilkotecha/Downloads/vecteezy_corgi-dogs-play-and-walk-outdoor_8041488.mp4"
video_path = "/Users/dhruvilkotecha/Downloads/vecteezy_multiracial-coworkers-team-and-colleagues-brainstormed_5264383.mov"  # Update this path accordingly
# video_path = "/Users/dhruvilkotecha/Downloads/abc.mp4"
# video_path = "/Users/dhruvilkotecha/Downloads/DevOps.mp4"
logging.info("Starting summarization process...")

summary = summarize_video(video_path)

logging.info("Summarization complete.\n")
print("📄 Final Summary:\n", summary)
