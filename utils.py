import json
from config import client
from google.genai import types
import re

def generate_image_prompt(product_name, product_descriptions,model_name, model_description_gemini, background_name,background_description_gemini):
    product_text = " ".join(f"{key}: {value}" for key, value in product_descriptions.items())
    model_text = " ".join(f"{key}: {value}" for key, value in model_description_gemini.items())
    background_text = " ".join(f"{key}: {value}" for key, value in background_description_gemini.items())
    
    prompt = f"""
    Generate a photorealistic, high-resolution image.
    Product: {product_name} - {product_text}
    Model: {model_name} - {model_text}
    Background:{background_name} - {background_text}
    Model pose: Pose the model to best showcase the product. Consider the product's function and style.
    Examples: standing confidently, walking, interacting with the environment.and make sure that the product is wore by the model according to the product type and subtype.
    Generate 3 views of the model showcasing the product  (e.g., front, back, side).
    pick the product model and background from the context provided in the same order. make sure that the generated images has the product accuracy upto 99%.
    Lighting: Natural, soft lighting.
    Image style: Fashion advertisement.
    """
    return prompt.strip()

def extract_json_from_response(response_text):
    """
    Extracts the JSON string from the model's response, handling markdown code block formatting.
    
    Args:
        response_text (str): The raw text response from the model.
    
    Returns:
        str: The extracted JSON string, or None if no JSON is found.
    """
    lines = response_text.split('\n')
    if lines[0].strip() == '```json' and lines[-1].strip() == '```':
        # Extract lines between the code block markers
        json_lines = lines[1:-1]
        json_str = '\n'.join(json_lines).strip()
        return json_str
    else:
        # Fallback: use regex to find the JSON object
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json_match.group().strip()
        return None

def generate_description_from_image(image, description_type="product"):
    """
    Generates a dictionary description of an image using the Gemini model.

    Args:
        image: PIL Image object to be described.
        description_type (str): Type of description ("product", "model", "background", or other).
    
    Returns:
        dict: Description as a dictionary, or a default dictionary if generation or parsing fails.
    """
    try:
        # Define prompts that request JSON output based on description_type
        if description_type == "product":
            prompt = """
            Describe the product in the image and provide the description in JSON format with the following keys:
            - "type": the type of the product 
            - "subtype": the subtype e.g. upper, lower, footwear, full body etc.
            - "color": the color of the product
            - "Brand": the brand of the product
            - "pattern": the pattern or design of the product
            - "material": the material of the product
            - "Button": the button type of the product
            - "sleeve": the sleeve type of the product
            - "neck": the neck type of the product
            - "fit": the fit of the product
            - "occasion": the occasion or style of the product
            - "texture": the texture or material of the product
            - "size": the size or dimensions of the product
            - "features": main features of the product
            - "style": the style of the product
            Be concise and descriptive.
            """
        elif description_type == "model":
            prompt = """
            Describe the model in the image and provide the description in JSON format with the following keys:
            - "gender": the gender of the model
            - "appearance": brief description of appearance
            - "hair": description of hair color and style
            - "snintone": description of skin tone
            - "body_type": description of body type
            - "height": height of the model
            - "age": approximate age of the model
            - "expression": description of the model's expression
            - "pose": description of the pose
            Be succinct yet descriptive.
            """
        elif description_type == "background":
            prompt = """
            Describe the background in the image and provide the description in JSON format with the following keys:
            - "setting": the setting or location
            - "elements": key elements present
            - "mood": the overall mood or atmosphere
            - "time_of_day": the time of day
            - "weather": the weather conditions
            - "items": any notable items or objects
            Keep it brief but vivid.
            """
        else:
            prompt = f"""
            Provide a brief description of the {description_type} in the image, emphasizing its most notable characteristics.
            Return the description in JSON format with a single key "description".
            """

        # Generate content from the Gemini model
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=[prompt, image],
            config=types.GenerateContentConfig(
                response_modalities=['Text'],
                max_output_tokens=2048
            )
        )

        # Extract the response text
        response_text = response.candidates[0].content.parts[0].text.strip()

        # Extract the JSON string from the response
        json_str = extract_json_from_response(response_text)

        if json_str:
            try:
                # Parse the JSON string into a dictionary
                description_dict = json.loads(json_str)
                if isinstance(description_dict, dict):
                    return description_dict
                else:
                    raise ValueError("Response is not a dictionary")
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}. Extracted JSON string was: {json_str}")

        # Fallback if extraction or parsing fails
        defaults = {
            "product": {"type": "unknown", "features": "generic", "style": "standard"},
            "model": {"gender": "unknown", "appearance": "average", "pose": "standing"},
            "background": {"setting": "generic", "elements": "none", "mood": "neutral"}
        }
        return defaults.get(description_type, {"description": "generic description"})

    except Exception as e:
        print(f"Error generating {description_type} description: {e}")
        # Return fallback dictionary
        defaults = {
            "product": {"type": "unknown", "features": "generic", "style": "standard"},
            "model": {"gender": "unknown", "appearance": "average", "pose": "standing"},
            "background": {"setting": "generic", "elements": "none", "mood": "neutral"}
        }
        return defaults.get(description_type, {"description": "generic description"})



