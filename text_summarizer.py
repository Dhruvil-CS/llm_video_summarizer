import ollama

def summarize_captions(captions_git=None, captions_blip=None,
                       transcript=None, ocr_texts=None):
    # Prepare each source as a clean bullet list (or “Not available.”)
    captions_text_git  = "\n".join(f"- {c}" for c in captions_git)  if captions_git  else "- Not available."
    captions_text_blip = "\n".join(f"- {c}" for c in captions_blip) if captions_blip else "- Not available."
    transcript_text    = transcript.strip()                           if transcript    else "Not available."
    ocr_text           = "\n".join(f"- {t}" for t in ocr_texts)      if ocr_texts    else "- Not available."

    try:
        response = ollama.chat(
            model='llama3',
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional video summarizer. "
                        "Produce ** bullet points**, each no more than one sentence long, "
                        "that capture the key scenes, actions, and participants. "
                        "Use fresh language (don’t copy captions verbatim). "
                        "Omit any mention of missing or unavailable data."
                        "Dont write the number of frames in the summary."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        # "**Visual Captions (GIT):**\n"
                        # f"{captions_text_git}\n\n"
                        "**Visual Captions (BLIP):**\n"
                        f"{captions_text_blip}\n\n"
                        "**Audio Transcript:**\n"
                        f"{transcript_text}\n\n"
                        "**OCR Text:**\n"
                        f"{ocr_text}\n\n"
                        "Now, write concise summarizing the video."
                    )
                }
            ]
        )
        return response['message']['content'].strip()

    except Exception as e:
        return f"Summarization error: {e}"
