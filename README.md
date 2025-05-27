

#  AI - Video Summarizer

An AI-powered video summarization tool that extracts **key frames** from videos, generates **image captions** using state-of-the-art models (BLIP and GIT), and summarizes the content using **LLaMA-3** via **Ollama**.
 
 Built with Python · Transformers · Gradio · OpenCV · ffmpeg · Ollama

---

##  Features

* Upload a video and extract **visually distinct key frames**
* Generate **natural language captions** from frames using BLIP and GIT
* Summarize those captions with **LLaMA-3 (via Ollama)** using a **clean, concise bullet summary** format
* Easy-to-use **Gradio web interface**

---

## Project Structure

```plaintext
├── app.py                   # Gradio web interface
├── frame_extractor.py       # Key frame extraction logic using SSIM & ffmpeg
├── generate_captions.py     # Caption generation using BLIP & GIT
├── main.py                  # Core pipeline: extraction, captioning, summarization
├── text_summarizer.py       # Bullet-point summarization using LLaMA-3 via Ollama
├── run_summarizer.py        # CLI version for local testing
├── requirements.txt         # Python dependencies
````

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Dhruvil-CS/llm_video_summarizer.git
cd llm_video_summarizer
```

### 2. Set Up Python Environment

```bash
pip install -r requirements.txt
```

### 3. Install and Run Ollama (for LLaMA-3)

Make sure [Ollama](https://ollama.com/) is installed and running locally:

```bash
ollama pull llama3
```

Verify it:

```bash
ollama run llama3
```

---

## How It Works

The Intelligent Video Summarizer processes a video through three main stages—frame extraction, caption generation, and text summarization—each leveraging specialized tools and models to produce a concise, informative summary.

### 1. Frame Extraction

1. **Frame Sampling with FFmpeg**

   * The video file is passed to FFmpeg, which decodes the video stream and extracts frames at a user-specified rate (frames per second).
   * Frames are saved as sequential image files (e.g., `frame_0001.jpg`, `frame_0002.jpg`, etc.).
2. **Structural Similarity Analysis (SSIM)**

   * To eliminate visually redundant frames, each newly extracted frame is converted to grayscale and compared to the last selected “key frame.”
   * The SSIM metric quantifies how similar two images are. If the SSIM score falls below a defined threshold (for example, 0.8), the new frame is deemed sufficiently different and is marked as a key frame.
   * This step ensures that only frames representing significant scene changes—for example, a shift in camera angle, lighting, or subject—are kept for further processing.

### 2. Caption Generation

1. **Model Inference**

   * Each key frame image is fed independently to two vision-language models:

     * **BLIP** (`Salesforce/blip-image-captioning-base`)
     * **GIT** (`microsoft/git-base`)
   * Both models generate short, descriptive captions in natural language, capturing the primary objects, actions, and context visible in the frame.
2. **Caption Consolidation**

   * Captions from both models are collected and deduplicated.
   * Where BLIP and GIT produce slightly different descriptions of the same scene, both variants are retained to give the summarization model richer textual input.

### 3. Text Summarization

1. **Prompt Assembly**

   * All available inputs—BLIP captions, GIT captions, optional OCR text detected in the frames, and an audio transcript if available—are formatted into a structured prompt.
   * Each section is clearly labeled (for example, “Visual Captions (BLIP):”, “Audio Transcript:”) and presented as bullet lists or paragraphs.
2. **LLaMA-3 via Ollama**

   * The assembled prompt is sent to the locally hosted LLaMA-3 model through the Ollama API.
   * The system prompt instructs LLaMA-3 to produce exactly four concise bullet points, each no more than one sentence long, using fresh language and omitting any mention of missing or unavailable data.
3. **Output Formatting**

   * The bullet points returned by LLaMA-3 form the final summary.
   * This summary is displayed in the Gradio interface or printed in the CLI, providing a clear, high-level overview of the video’s contents.

---

## Demo (Gradio App)

Launch the app:

```bash
python app.py
```

Then open [http://localhost:7860](http://localhost:7860) in your browser.

---

## Run from CLI

To test without the UI:

```bash
python run_summarizer.py
```

Be sure to set your `video_path` in `run_summarizer.py`.

---

## Requirements

* Python 3.8 or higher
* FFmpeg installed and added to PATH
* Ollama installed and running locally with the `llama3` model
* GPU recommended for faster inference

---

## Clean Up

Temporary frames are automatically deleted after summarization.

---

## License

N/A

---

## Author

**Dhruvil Kotecha**
[LinkedIn](https://www.linkedin.com/in/dhruvil-kamleshkumar-kotecha-a627a31b1/) · [GitHub](https://github.com/Dhruvil-CS)

