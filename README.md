# 🎯 Face Recognition Attendance System

A complete AI-based attendance system using **Face Recognition**, built with both **Desktop (OpenCV)** and **Web (Flask)** versions.

---

## 🚀 Features

✅ Face Detection using OpenCV  
✅ Face Recognition using face_recognition library  
✅ Automatic Attendance Marking  
✅ Excel Storage (Attendance + Summary Sheets)  
✅ Duplicate Entry Prevention  
✅ Voice Alerts 🔊  
✅ Attendance Summary (Days Present)  
✅ Graph Visualization 📊  
✅ Web Version (Runs in Browser) 🌐  
✅ Stylish Frontend (HTML, CSS, JavaScript)  

---

## 🧠 Tech Stack

- Python 🐍
- OpenCV
- face_recognition
- Flask
- Pandas
- Matplotlib
- JavaScript
- HTML/CSS

---

## 📁 Project Structure


Face_Attendance_System/
│── dataset/
│ ├── person1/
│ ├── person2/
│
│── attendance/
│ └── attendance.xlsx
│
│── templates/
│ └── index.html
│
│── encode_faces.py
│── main.py
│── app.py
│── encodings.pickle


---

## ⚙️ Installation

### 1️⃣ Install dependencies

pip install opencv-python face-recognition pandas flask pyttsx3 matplotlib

---

## ▶️ How to Run

### 🔹 Step 1: Encode Faces

python encode_faces.py


---

### 🔹 Step 2: Run Desktop Version

python main.py


👉 Press **Q** to exit

---

### 🔹 Step 3: Run Web Version

python app.py

👉 Open browser:
http://127.0.0.1:5000


---

## 📊 Excel Output

### Sheet 1: Attendance
| Name | Date | Time |
|------|------|------|

### Sheet 2: Summary
| Name | Days Present |
|------|-------------|

---

## 🖼️ Screenshots

### 📸 Web Interface
![Web UI](images/web_ui.png)

### 📸 Face Detection
![Detection](images/detection.png)

### 📸 Excel Output
![Excel](images/excel.png)

### 📸 Graph Output
![Graph](images/graph.png)

---

## 🎓 Key Concepts Used

- Face Encoding & Matching
- Image Processing
- Flask API Integration
- Data Analysis using Pandas
- Excel Automation
- Real-time Video Processing

---

## 🔐 Error Handling

✔ Handles camera errors  
✔ Handles unknown faces  
✔ Prevents duplicate attendance  
✔ Handles Excel file lock (PermissionError)  

---

## 📈 Future Improvements

- Attendance Percentage Calculation  
- Monthly Reports  
- Cloud Database Integration  
- Mobile App Version  
- Live Face Detection (Auto Capture)  

---

## 👨‍💻 Author

**Your Name**

---

## ⭐ Conclusion

This project demonstrates how AI and Computer Vision can be used to automate real-world tasks like attendance management efficiently.

---

⭐ If you like this project, give it a star!
