import json
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel
 
MODEL = "gemini-3.5-flash-lite"
 
PROMPT = """
Look at the main object in the photo and identify what it is.

Return:
- name: a short name for the object
- description: one sentence describing the object
- tags: 5 to 8 lowercase keywords related to the object

Only use details that are clearly visible.
Do not describe the background or surroundings.
"""

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
 
 
class PhotoDetails(BaseModel):
    name: str
    description: str
    tags: list[str]


def get_photo_details(photo_file):
    picture = Image.open(photo_file)
    picture.thumbnail((1024, 1024))

    answer = client.models.generate_content(
        model=MODEL,
        contents=[PROMPT, picture],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=PhotoDetails
        )
    )

    return PhotoDetails.model_validate_json(answer.text)

def main():
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else "photos")
    photos = sorted(pic for pic in folder.iterdir() if pic.suffix.lower() in {".jpg", ".jpeg", ".png"})
    results = {}

    for pic in photos:
        print(f"{pic.name}")
        try:
            details = get_photo_details(pic)
            info = details.model_dump()
            print(json.dumps(info, indent=2))
            results[pic.name] = info
        except Exception as error:
            print(f"Error: {error}")

        time.sleep(4)

    with open("results.json", "w", encoding="utf-8") as output:
        json.dump(results, output, indent=2)

    print(f"\nFinished: {len(results)}/{len(photos)} images processed.")
    print("Results saved to results.json")

 
 
if __name__ == "__main__":
    main()