from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

client = genai.Client(api_key=os.getenv("GOOGLE_GEMENI_API"))
