from fastapi import FastAPI, File, UploadFile, Request, WebSocket, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import io
import os
import uvicorn # Import Uvicorn
import cv2
import face_recognition
import os
import time
import sys
from pathlib import Path
import webbrowser
import zipfile
import shutil

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Create a folder to store the uploaded and processed images
os.makedirs ("images", exist_ok=True)
os.makedirs ("images_tmp", exist_ok=True)
# Mount the folder as a static file directory
app.mount ("/images", StaticFiles (directory="images"), name="images")
app.mount ("/images_tmp", StaticFiles (directory="images_tmp"), name="images_tmp")

app.mount("/static", StaticFiles(directory="static"), name="static")
# Define a route to display the web UI
@app.get ("/", response_class=HTMLResponse)
async def index(request:Request):
    # Return a simple HTML form to upload a file
    return templates.TemplateResponse("index.html", {"request": request, "message": None})


# Define a route to handle the file upload
@app.post ("/uploadfile/")
async def create_upload_file(img: UploadFile = File (...), files: list[UploadFile] = File (...)):
    # Save the uploaded file to the images folder
    
    file_path = os.path.join ("images", img.filename)
    image_path = file_path
    print(file_path)
    
    

    for file in files:
        # Save the uploaded file to the images folder
        pathdir = os.path.join ("images_tmp", file.filename)
        print(pathdir)
        substring=pathdir.split("/")
        os.makedirs ("images_tmp/"+substring[1], exist_ok=True)
        folder_files = os.path.join ("images_tmp", file.filename)
        #os.makedirs (folder_files, exist_ok=True)
        with open (folder_files, "wb") as f:
             f.write (file.file.read())
 

    with open (file_path, "wb") as f:
        f.write (img.file.read ())
            
    pictures_folder = os.path.join ("images_tmp/"+substring[1])
    total_files = len([name for name in os.listdir(pictures_folder) if os.path.isfile(os.path.join(pictures_folder, name))])
    processed_files = 0

    docs_img = cv2.imread(f"{image_path}")
    docs_rgb_img = cv2.cvtColor(docs_img, cv2.COLOR_BGR2RGB)
    docs_img_encoding = face_recognition.face_encodings(docs_rgb_img)[0]

    start_time = time.time()

    os.makedirs ("images_tmp/"+substring[1]+"FaceDetected", exist_ok=True)
    foldername = os.path.join(os.getcwd(), "images_tmp/"+substring[1]+"FaceDetected")
    #os.startfile(folder_path2)
    os.system('xdg-open "%s"' % foldername)

    for root, dirs, files in os.walk(pictures_folder):
        for file in files:
            if file.endswith(".jpeg") or file.endswith(".jpg") or file.endswith(".png"):
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                #img_encoding = face_recognition.face_encodings(rgb_img)[0]
                encodings = face_recognition.face_encodings(rgb_img)
                if len(encodings) > 0:
                    img_encoding = encodings[0]
                # do something with img_encoding
                else:
                    print("No faces found in the image")

                result = face_recognition.compare_faces([docs_img_encoding], img_encoding)
                processed_files += 1
                elapsed_time = time.time() - start_time
                estimated_time = (elapsed_time / processed_files) * (total_files - processed_files)
                print(f"Processed {processed_files} out of {total_files} files. Estimated time left: {estimated_time:.2f} seconds.")
                if result[0]:
                    cv2.imshow(" ",img)
                    #cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    
                    Face_folder = os.path.join ("images_tmp/"+substring[1]+"FaceDetected")
                    print(f"File name: {file}, Location: {img_path}")
                    shutil.copy(img_path, Face_folder)
        
        #return templates.TemplateResponse("gallery.html", {"request":None , "image_files": pictures_folder})


# Define a route for the download page that will allow the user to select and download images as a zip file
@app.post("/download", response_class=HTMLResponse)
async def download(request: Request):
    # Get the form data from the request
    form_data = await request.form()
    # Get the list of selected image filenames from the form data
    selected_images = form_data.getlist("images")
    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        # Loop through the selected images and add them to the zip file
        for image in selected_images:
            zip_file.write(f"images_tmp/{image}", image)
    # Return the zip file as a response with the appropriate headers
    return Response(
        zip_buffer.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=images.zip"
        }
    )

# Add a conditional statement to run Uvicorn if the file is the main script
if __name__ == "__main__":
    webbrowser.open("http://localhost:8000/")
    uvicorn.run("main_linux:app", host="0.0.0.0", port=8000, reload=True)
    
