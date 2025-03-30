# Image Generation with Google Gemini API

This project generates photorealistic, high-resolution images by combining product, model, and background descriptions using the Google Gemini API. The generated images are tailored for fashion advertisements, showcasing products in various contexts.

## Features

- **Product Description Extraction**: Automatically extracts detailed descriptions of products from images
- **Model and Background Description**: Generates descriptions for models and backgrounds using the Gemini API
- **Image Prompt Generation**: Creates detailed prompts for generating images based on the extracted descriptions
- **Image Generation**: Produces photorealistic images with high accuracy using the Google Gemini API

## Project Structure

```
├── .env.example         # Example environment file for API keys
├── .gitignore          # Git ignore file
├── config.py           # Configuration for the Google Gemini API client
├── main.py             # Main script to generate images
├── requirements.txt    # Python dependencies
├── utils.py           # Utility functions for prompt generation and description extraction
└── assets/            # Directory containing input images
    ├── background/    # Background images
    ├── models/        # Model images
    └── products/      # Product images
```

## Prerequisites

- Python 3.8 or higher
- A valid Google Gemini API key

// ...existing code until Installation section...

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/image_generation.git
cd image_generation
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Edit the `.env` file and add your Google Gemini API key:
```
GOOGLE_GEMENI_API=your_api_key_here
```

6. Create required directories:
```bash
mkdir -p assets/{products,models,background} out
```

## Usage

1. Prepare your images:
   - Place product images (JPG/PNG) in `assets/products/`
   - Place model images (JPG/PNG) in `assets/models/`
   - Place background images (JPG/PNG) in `assets/background/`

2. Ensure image requirements:
   - Recommended resolution: 1024x1024 pixels or higher
   - File formats: JPG or PNG
   - Clear, well-lit images for better results

3. Run the image generation:
```bash
python main.py
```

4. Check generated outputs:
   - Generated images will be saved in the `out/` directory
   - Each run creates a timestamped subfolder
   - JSON files with image descriptions are saved alongside the images

## Troubleshooting

Common issues and solutions:

1. API Key errors:
```bash
# Verify your API key is set correctly
echo $GOOGLE_GEMENI_API
# If empty, reload environment variables
source .env
```

2. Missing directories:
```bash
# Create any missing directories
mkdir -p assets/{products,models,background} out
```

3. Image processing errors:
   - Ensure images are in JPG/PNG format
   - Check image permissions: `chmod 644 assets/**/*`
   - Verify image files are not corrupted

## How It Works

1. The script uses the Google Gemini API to:
   - Extract product descriptions 
   - Generate model and background descriptions
   - Create detailed prompts combining all elements
   - Generate photorealistic images based on the prompts

2. The [`utils.py`](utils.py) contains key functions:
   - `generate_description_from_image()`: Extracts descriptions from images
   - `generate_image_prompt()`: Creates prompts for image generation
   - `extract_json_from_response()`: Parses API responses
