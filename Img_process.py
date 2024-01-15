import cv2
import face_recognition
import os
import time
from beflask import base
import sys

#folder_path = sys.argv[1]
docs_folder = "/mnt/DATA/Pictures/David Photos/DP"
#pictures_folder = folder_path 
pictures_folder = "/mnt/DATA/Pictures/Friends/Church"
total_files = len([name for name in os.listdir(pictures_folder) if os.path.isfile(os.path.join(pictures_folder, name))])
processed_files = 0

docs_img = cv2.imread(f"{docs_folder}/IMG_20211028_170616707.jpg")
docs_rgb_img = cv2.cvtColor(docs_img, cv2.COLOR_BGR2RGB)
docs_img_encoding = face_recognition.face_encodings(docs_rgb_img)[0]



start_time = time.time()


for root, dirs, files in os.walk(pictures_folder):
    for file in files:
        if file.endswith(".jpeg") or file.endswith(".jpg") or file.endswith(".png"):
            img_path = os.path.join(root, file)
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_encoding = face_recognition.face_encodings(rgb_img)[0]
            result = face_recognition.compare_faces([docs_img_encoding], img_encoding)
            processed_files += 1
            elapsed_time = time.time() - start_time
            estimated_time = (elapsed_time / processed_files) * (total_files - processed_files)
            print(f"Processed {processed_files} out of {total_files} files. Estimated time left: {estimated_time:.2f} seconds.")
            if result[0]:
                cv2.imshow(" ",img)
                #cv2.waitKey(0)
                cv2.destroyAllWindows()
                print(f"File name: {file}, Location: {img_path}")

