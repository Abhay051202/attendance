Face Recognition Attendance System
A comprehensive, production-ready face recognition attendance system using InsightFace, ByteTrack, and OpenCV.
🌟 Features

Real-time Face Detection & Recognition using InsightFace
Multi-person Tracking with ByteTrack
Automatic Attendance Marking (Arrival & Leaving)
Duplicate Prevention - No repeated attendance for the same day
SQLite Database for persistent storage
CSV Export functionality
Interactive CLI with menu-driven interface
Webcam Registration for new persons
Statistics & Reports

📁 Project Structure
attendance_system/
├── main.py                    # Main entry point
├── database.py                # Database operations
├── face_recognition.py        # Face recognition logic
├── attendance_tracker.py      # Attendance marking logic
├── video_processor.py         # Video processing & tracking
├── registration.py            # Person registration module
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
├── attendance.db              # SQLite database (auto-created)
├── face_encodings.pkl         # Face encodings (auto-created)
└── exports/                   # CSV export folder
🚀 Installation
Prerequisites

Python 3.8 or higher
Webcam
(Optional) CUDA-capable GPU for faster processing

Step 1: Clone or Download the Project
bashgit clone <your-repo-url>
cd attendance_system
Step 2: Create Virtual Environment (Recommended)
bash# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
bashpip install -r requirements.txt
Step 4: Download InsightFace Model
The first time you run the system, InsightFace will automatically download the required model (~300MB).
💻 Usage
Running the System
bashpython main.py
Main Menu Options
1. Start Attendance System (Webcam)   - Run live attendance tracking
2. Register New Person                - Add new person to system
3. View All Registered Persons        - List all registered users
4. View Today's Attendance            - Show today's records
5. View All Attendance Records        - Show complete history
6. Export Attendance to CSV           - Export data to CSV file
7. View Statistics                    - Display system statistics
8. Delete Person                      - Remove a person from system
9. Exit                               - Close application
📝 Step-by-Step Guide
1. Register a New Person

Select option 2 from main menu
Enter Person ID (unique identifier)
Enter Full Name
Enter Email (optional)
Enter Department (optional)
Position face in webcam frame
Press c to capture face
System will save the person with face encoding

2. Run Attendance System

Select option 1 from main menu
System will start webcam
When a registered face is detected:

First detection: Marks arrival time
Second detection: Marks leaving time
Further detections: Ignored (prevents duplicates)


Press q to quit
Press r to reset tracker
Press s to show statistics

3. View Attendance Records

Today's Attendance: Option 4 - Shows all attendance for current day
All Records: Option 5 - Shows complete attendance history
Export to CSV: Option 6 - Exports records to CSV file

⚙️ Configuration
Edit config.py to customize system behavior:
python# Face Recognition Settings
SIMILARITY_THRESHOLD = 0.6        # Lower = stricter matching

# Attendance Settings
ATTENDANCE_COOLDOWN_SECONDS = 5   # Cooldown between marks

# Video Settings
WEBCAM_INDEX = 0                  # Camera index
DISPLAY_LANDMARKS = True          # Show facial landmarks
🗄️ Database Schema
persons Table
sql- person_id (TEXT, PRIMARY KEY)
- name (TEXT)
- email (TEXT)
- department (TEXT)
- registered_date (TEXT)
- face_encoding (BLOB)
attendance Table
sql- id (INTEGER, PRIMARY KEY)
- person_id (TEXT, FOREIGN KEY)
- date (TEXT)
- arrival_time (TEXT)
- leaving_time (TEXT)
- status (TEXT)
- UNIQUE(person_id, date)  # Prevents duplicates
🎯 Key Features Explained
1. Duplicate Prevention

Uses UNIQUE(person_id, date) constraint in database
Tracks attendance status in memory
Cooldown period between detections

2. Face Recognition

Uses InsightFace's Buffalo_L model
Cosine similarity for face matching
Configurable similarity threshold

3. Person Tracking

ByteTrack algorithm for multi-person tracking
Maintains consistent IDs across frames
Color-coded bounding boxes

4. Attendance Logic
First Detection  → Mark Arrival Time
Second Detection → Mark Leaving Time
Third+ Detection → Ignored (Already marked)
📊 CSV Export Format
csvPerson ID,Name,Date,Arrival Time,Leaving Time,Status
EMP001,John Doe,2024-11-17,09:00:15,17:30:45,Present
EMP002,Jane Smith,2024-11-17,09:15:30,N/A,Present
🔧 Troubleshooting
Camera Not Working
python# Try different camera index in config.py
WEBCAM_INDEX = 1  # or 2, 3, etc.
Face Not Detected

Ensure good lighting
Face should be clearly visible
Look directly at camera
Remove glasses/masks if possible

Recognition Not Working

Lower similarity threshold in config.py
Re-register person with better quality image
Ensure consistent lighting

GPU Not Working
bash# Install GPU version
pip install onnxruntime-gpu
🎨 Integration with Web UI
The React UI artifact can be integrated by:

Creating a REST API (Flask/FastAPI)
Adding WebSocket support for real-time updates
Sharing the SQLite database
Using the same attendance logic

Example Flask integration:
pythonfrom flask import Flask, jsonify
from database import DatabaseManager

app = Flask(__name__)
db = DatabaseManager()

@app.route('/api/attendance/today')
def get_today_attendance():
    records = db.get_today_attendance()
    return jsonify(records)
📈 Performance Tips

Use GPU: Install onnxruntime-gpu for faster processing
Adjust Detection Size: Lower size = faster but less accurate
Optimize Cooldown: Increase cooldown to reduce processing
Frame Skip: Process every 2nd or 3rd frame for better performance

🔐 Security Considerations

Face encodings are stored as binary blobs in database
Consider encrypting the database in production
Implement user authentication for registration
Add audit logs for attendance modifications

📄 License
This project is provided as-is for educational and commercial use.
🤝 Contributing
Feel free to submit issues, fork the repository, and create pull requests.
📞 Support
For issues or questions, please create an issue in the repository.