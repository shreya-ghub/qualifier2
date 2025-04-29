from fastapi import FastAPI, UploadFile, File
from utils import preprocess_image, ocr_image
from parser import parse_lab_report
import uvicorn
import shutil
import os

app = FastAPI()

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        img = preprocess_image(temp_file_path)
        text = ocr_image(img)
        lab_data = parse_lab_report(text)

        os.remove(temp_file_path)

        return {
            "is_success": True,
            "data": lab_data
        }

    except Exception as e:
        return {
            "is_success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
