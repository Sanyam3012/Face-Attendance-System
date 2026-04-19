import face_recognition
import os
import pickle

dataset_path = "dataset"
encodings = []
names = []

print("[INFO] Encoding faces...")

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)
        image = face_recognition.load_image_file(image_path)

        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            encodings.append(encoding)
            names.append(person_name)

data = {"encodings": encodings, "names": names}

with open("encodings.pickle", "wb") as f:
    pickle.dump(data, f)

print("[INFO] Done encoding!")