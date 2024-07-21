import transformers
import torch
from transformers import AutoImageProcessor, ResNetForImageClassification
from diffusers import StableDiffusionPipeline

def generate_images(text):
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
    prompt = text
    image = pipe(prompt).images[0] 
    return image

def recognition_images(image):
    processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
    model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")

    inputs = processor(image, return_tensors="pt")

    with torch.no_grad():
        logits = model(**inputs).logits

    # model predicts 1 de las 1000 clases de ImageNet 
    predicted_label = logits.argmax(-1).item()
    
    return model.config.id2label[predicted_label]