from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch

blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption_blip(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = blip_processor(images=image, return_tensors="pt")
    out = blip_model.generate(**inputs)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)
    return caption

git_processor = AutoProcessor.from_pretrained("microsoft/git-base")
git_model = AutoModelForCausalLM.from_pretrained("microsoft/git-base")

def generate_caption_git(image_path):
    image = Image.open(image_path).convert("RGB")
    pixel_values = git_processor(images=image, return_tensors="pt").pixel_values
    generated_ids = git_model.generate(pixel_values=pixel_values, max_length=50)
    caption = git_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return caption