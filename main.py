import cv2
import face_recognition
import pickle
import datetime
import os
import pandas as pd
import pyttsx3
import matplotlib.pyplot as plt

# -------------------- INIT --------------------

# Load encodings
with open("encodings.pickle", "rb") as f:
    data = pickle.load(f)

# Voice engine
engine = pyttsx3.init()

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
    time = now.strftime("%H:%M:%S")

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
            return

    new_row = {"Name": name, "Date": date, "Time": time}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Create summary (unique days per student)
    summary = df.groupby("Name")["Date"].nunique().reset_index()
    summary.columns = ["Name", "Days Present"]

    # Save both sheets
    with pd.ExcelWriter(attendance_file, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, index=False, sheet_name="Attendance")
        summary.to_excel(writer, index=False, sheet_name="Summary")

    print(f"{name} marked at {time}")

    # 🔊 Voice Alert
    engine.say(f"{name} marked present")
    engine.runAndWait()

# -------------------- CAMERA --------------------

print("[INFO] Starting camera... Press Q to exit")

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        print("Camera error")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    for (top, right, bottom, left), face_encoding in zip(faces, encodings):
        matches = face_recognition.compare_faces(data["encodings"], face_encoding)
        name = "Unknown"

        if True in matches:
            index = matches.index(True)
            name = data["names"][index]
            mark_attendance(name)
        else:
            cv2.putText(frame, "Unknown!", (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Face Attendance System", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

# -------------------- TERMINAL SUMMARY --------------------

def show_summary():
    try:
        df = pd.read_excel(attendance_file, sheet_name="Attendance")
    except:
        print("No attendance data")
        return

    if df.empty:
        print("No attendance data")
        return

    summary = df.groupby("Name")["Date"].nunique()

    print("\n===== ATTENDANCE SUMMARY =====")
    for name, count in summary.items():
        print(f"{name} → {count} days present")

show_summary()

# -------------------- GRAPH --------------------

def show_graph():
    df = pd.read_excel(attendance_file, sheet_name="Attendance")

    if df.empty:
        print("No data for graph")
        return

    count = df.groupby("Name")["Date"].nunique()

    plt.figure()
    count.plot(kind='bar')
    plt.title("Attendance Report")
    plt.xlabel("Name")
    plt.ylabel("Days Present")
    plt.show()

show_graph()