from flask import Flask, render_template, request, jsonify
import face_recognition
import pickle
import numpy as np
import cv2
import base64
import pandas as pd
import datetime
import os
import time

app = Flask(__name__)

# -------------------- LOAD ENCODINGS --------------------

with open("encodings.pickle", "rb") as f:
    data = pickle.load(f)

attendance_file = "attendance/attendance.xlsx"
os.makedirs("attendance", exist_ok=True)

# Create Excel file if not exists
if not os.path.exists(attendance_file):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    with pd.ExcelWriter(attendance_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Attendance")
        df.to_excel(writer, index=False, sheet_name="Summary")

# -------------------- FUNCTION --------------------

def mark_attendance(name):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")

    try:
        df = pd.read_excel(attendance_file, sheet_name="Attendance")
    except:
        df = pd.DataFrame(columns=["Name", "Date", "Time"])

    # Prevent duplicate within 30 sec
    recent = df[(df["Name"] == name) & (df["Date"] == date)]

    if not recent.empty:
        last_time = recent.iloc[-1]["Time"]
        last_time = datetime.datetime.strptime(last_time, "%H:%M:%S")
        if (now - last_time).seconds < 30:
            return "Already Marked"

    new_row = {"Name": name, "Date": date, "Time": time_now}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Create summary
    summary = df.groupby("Name")["Date"].nunique().reset_index()
    summary.columns = ["Name", "Days Present"]

    # Safe write (handles Excel open issue)
    while True:
        try:
            with pd.ExcelWriter(attendance_file, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, index=False, sheet_name="Attendance")
                summary.to_excel(writer, index=False, sheet_name="Summary")
            break
        except PermissionError:
            print("⚠️ Close Excel file to continue...")
            time.sleep(2)

    print(f"{name} marked at {time_now}")
    return "Marked"

# -------------------- ROUTES --------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recognize", methods=["POST"])
def recognize():
    data_img = request.json["image"]

    # Decode image
    img_data = base64.b64decode(data_img.split(",")[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    result = "Unknown"

    for face_encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], face_encoding)

        if True in matches:
            index = matches.index(True)
            result = data["names"][index]
            mark_attendance(result)

    return jsonify({"name": result})

# -------------------- SUMMARY ROUTE --------------------

@app.route("/summary")
def summary():
    try:
        df = pd.read_excel(attendance_file, sheet_name="Attendance")
    except:
        return jsonify([])

    if df.empty:
        return jsonify([])

    summary = df.groupby("Name")["Date"].nunique().reset_index()
    summary.columns = ["Name", "Days"]

    return summary.to_dict(orient="records")

# -------------------- RUN --------------------

if __name__ == "__main__":
    app.run(debug=True)