from google.genai import types
from PIL import Image
from io import BytesIO
import os
from utils import generate_description_from_image,generate_image_prompt
from config import client

output_dir = "out/"

product_image = Image.open(f'assets/products/product11.jpg')

product_description = generate_description_from_image(product_image, description_type="product")
product_name = product_image.filename.split('/')[-1]

# Model and background image handling
model = Image.open(f'assets/models/model-2.jpg')
model_name = model.filename.split('/')[-1]

# Generate Gemini description for the model
model_description_gemini = generate_description_from_image(model, description_type="model")


# Loop through background images
for i in range(6,7):  # Assuming you want to work with 10 background images
    background_image = Image.open(f'assets/background/bg{i}.png')
    bg_name = background_image.filename.split('/')[-1]

    # Generate Gemini description for the background
    background_description_gemini = generate_description_from_image(background_image, description_type="background")
   
    prompt_text = generate_image_prompt(product_name,product_description,model_name, model_description_gemini,bg_name,background_description_gemini)
    print(f"Generating image for Model: {model_name}, Background: {bg_name}, Product: {product_name}")
    
    print(f"Prompt: {prompt_text}")
    # Image generation request to Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[prompt_text, product_image,model,background_image],
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image'],
            temperature=0.5,
        )
    )


    try:
        parts = response.candidates[0].content.parts
        print(f"Number of parts: {len(parts)}")

        for i, part in enumerate(parts):
            print(f"Part {i+1}:")
            image = Image.open(BytesIO((part.inline_data.data)))
            output_filename = f"{model_name}_view_{i}_{bg_name}_{product_name.replace(' ', '_')}"
            output_path = os.path.join(output_dir, output_filename)
            image.save(output_path)
            print(f"Image saved to: {output_path}")
            print("-" * 30)
    except Exception as e:
        print("Error in response", e)
        continue
