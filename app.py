import gradio as gr
from main import summarize_video
import os
import tempfile
import shutil

def process_video(video_file):
    """Process the video and summarize it."""
    try:
        if video_file is None:
            return "No video file uploaded"

        # Save video to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            shutil.copyfile(video_file, tmp.name)
            temp_path = tmp.name

        result = summarize_video(temp_path)

        # Clean up
        os.remove(temp_path)
        return result

    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks(title="Video Summarizer") as app:
    gr.Markdown("## Intelligent Video Summarizer\nUpload a video to get a concise summary generated using AI.")

    with gr.Row():
        video_input = gr.Video(label="Upload Video")
        summary_output = gr.Textbox(label="AI Summary", lines=8, interactive=False)

    submit_btn = gr.Button("Summarize")
    submit_btn.click(fn=process_video, inputs=video_input, outputs=summary_output)

if __name__ == "__main__":
    app.launch(server_port=7860, share=False)
