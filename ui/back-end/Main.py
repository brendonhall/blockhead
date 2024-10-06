from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import os

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        file_location = f"{upload_dir}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        # Check if the file exists and can be opened
        if not os.path.exists(file_location):
            raise FileNotFoundError(f"File {file_location} not found after upload.")

        df = pd.read_csv(file_location)
        print(df.head())

        os.remove(file_location)

        return JSONResponse(content={"message": "File uploaded successfully"}, status_code=200)
    except FileNotFoundError as fnf_error:
        return JSONResponse(content={"message": f"File not found: {str(fnf_error)}"}, status_code=404)
    except pd.errors.EmptyDataError:
        return JSONResponse(content={"message": "File is empty or not a valid CSV"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"message": f"File upload failed: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)