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

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and add your Google Gemini API key:
```
GOOGLE_GEMENI_API=your_api_key_here
```

## Usage

1. Place your images in the appropriate directories under `assets/`:
   - Product images in `assets/products/`
   - Model images in `assets/models/` 
   - Background images in `assets/background/`

2. Run the main script:
```bash
python main.py
```

3. Generated images will be saved in the `out/` directory

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

## Dependencies

Main dependencies from [`requirements.txt`](requirements.txt):
- Pillow: Image processing
- google-generativeai: Google Gemini API client
- python-dotenv: Environment variable management
- pydantic-ai: AI model integration

## License

This project is open source and available under the MIT License.

## Notes

- Ensure input images are high quality for best results
- Currently processes one product, model, and multiple backgrounds in sequence
- Generated images maintain product accuracy while creating realistic fashion advertisements

Feel free to contribute to this project by submitting issues or pull requests.