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
from datetime import timedelta

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Create a folder to store the uploaded and processed images
os.makedirs ("images", exist_ok=True)
os.makedirs ("images_tmp", exist_ok=True)
# Mount the folder as a static file directory
app.mount ("/images", StaticFiles (directory="images"), name="images")
app.mount ("/images_tmp", StaticFiles (directory="images_tmp"), name="images_tmp")

def deletetmp():
    folder = 'images'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def deletetmp2(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))



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

    os.makedirs ("images_tmp/"+substring[1]+"_FaceDetected", exist_ok=True)
    foldername = os.path.join(os.getcwd(), "images_tmp/"+substring[1]+"_FaceDetected")
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
                estimated_time_delta = timedelta(seconds=int(estimated_time))
                print(f"Processed {processed_files} out of {total_files} files. Estimated time left: {estimated_time_delta} seconds.")
                if result[0]:
                    cv2.imshow(" ",img)
                    #cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    
                    Face_folder = os.path.join ("images_tmp/"+substring[1]+"_FaceDetected")
                    print(f"File name: {file}, Location: {img_path}")
                    shutil.copy(img_path, Face_folder)
                if input() == 'q':
                    break
    deletetmp()  
    deletetmp2(pictures_folder) 
        #return templates.TemplateResponse("gallery.html", {"request":None , "image_files": pictures_folder})



# Add a conditional statement to run Uvicorn if the file is the main script
if __name__ == "__main__":
    set_port = 8000
    host_address = "0.0.0.0"
    webbrowser.open("http://localhost:8000/")
    uvicorn.run("main_linux:app", host=host_address, port=set_port, reload=True)
    
