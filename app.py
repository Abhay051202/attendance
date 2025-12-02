from flask import Flask, render_template, Response, jsonify, request
from flask_cors import CORS
import cv2
import time
import json
from datetime import datetime

# Import your existing modules
from database import DatabaseManager
from face_recognition import FaceRecognitionHandler
from attendance_tracker import AttendanceTracker
from video_processor import VideoProcessor
from smtp_handler import SMTPHandler
from config import MYSQL_CONFIG, SMTP_CONFIG, EMAIL_NOTIFICATIONS_ENABLED

app = Flask(__name__)
CORS(app)  # Allow React to communicate with this server

# --- INITIALIZATION ---
print("Initializing Backend Systems...")
db = DatabaseManager()
face_handler = FaceRecognitionHandler('face_encodings.pkl')
tracker = AttendanceTracker(db, face_handler)
processor = VideoProcessor(face_handler)

# Initialize SMTP Handler
smtp_handler = None
if EMAIL_NOTIFICATIONS_ENABLED:
    try:
        smtp_handler = SMTPHandler(
            smtp_server=SMTP_CONFIG['smtp_server'],
            smtp_port=SMTP_CONFIG['smtp_port'],
            sender_email=SMTP_CONFIG['sender_email'],
            sender_password=SMTP_CONFIG['sender_password'],
            use_tls=SMTP_CONFIG['use_tls']
        )
        print("SMTP Handler initialized successfully")
    except Exception as e:
        print(f"Failed to initialize SMTP Handler: {e}")
        smtp_handler = None

# Global State
camera = None
is_running = False
current_camera_index = 0  # <--- New Variable to track the active ID

def get_camera():
    global camera, current_camera_index
    # Only initialize if it doesn't exist or is closed
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(current_camera_index)
    return camera

def generate_frames(mode='dashboard'):
    global camera, is_running
    
    while True:
        if not is_running and mode == 'dashboard':
            time.sleep(0.1)
            continue
            
        # Always get the current camera instance inside the loop
        cam = get_camera()
        
        success, frame = cam.read()
        if not success:
            # If read fails, try to reconnect or wait
            time.sleep(0.1)
            continue
            
        # ... (Rest of the processing logic remains the same) ...
        if mode == 'dashboard':
             annotated_frame, _, _, _ = processor.process_frame(frame, mark_attendance_callback=tracker.process_recognized_face)
        else:
             annotated_frame = frame
             # ... (Registration logic) ...

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames('dashboard'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_reg')
def video_feed_reg():
    return Response(generate_frames('registration'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/toggle_camera', methods=['POST'])
def toggle_camera():
    global is_running, camera, current_camera_index
    data = request.json
    
    req_status = data.get('status', False)
    req_index = int(data.get('camera_index', 0))

    # If we are switching cameras (e.g., from 0 to 1)
    if req_index != current_camera_index:
        if camera is not None:
            camera.release() # Close old camera
            camera = None    # Force get_camera to create a new one
        current_camera_index = req_index

    is_running = req_status
    return jsonify({"status": "success", "running": is_running, "camera_index": current_camera_index})

@app.route('/api/stats')
def get_stats():
    stats = db.get_statistics()
    # Get recent logs (last 5)
    logs_raw = db.get_recent_logs()
    # Format logs for frontend
    formatted_logs = [f"{l[3]} - {l[1]} ({l[0]})" for l in logs_raw[:10]]
    
    return jsonify({
        "total_registered": stats['total_persons'],
        "present_today": stats['present_today'],
        "logs": formatted_logs
    })

@app.route('/api/register', methods=['POST'])
def register_person():
    data = request.json
    pid = data.get('pid')
    name = data.get('name')
    email = data.get('email')
    dept = data.get('department')
    s_start = data.get('shiftStart')
    s_end = data.get('shiftEnd')

    # Capture a single frame from the camera for encoding
    cam = get_camera()
    ret, frame = cam.read()
    
    if not ret:
        return jsonify({"success": False, "message": "Camera failed"})

    encoding, msg = face_handler.extract_face_encoding(frame)
    
    if encoding is None:
        return jsonify({"success": False, "message": msg})

    # Check duplicate
    exist_id, exist_name, sim = face_handler.recognize_face(encoding)
    if exist_id and sim > 0.6:
        return jsonify({"success": False, "message": f"Face already registered as {exist_name}"})

    success, db_msg = db.add_person(pid, name, encoding, email, dept, s_start, s_end)
    
    if success:
        face_handler.add_face_encoding(pid, name, encoding)
        return jsonify({"success": True, "message": "Registration Successful"})
    else:
        return jsonify({"success": False, "message": db_msg})

@app.route('/api/records')
def get_records():
    # Default to today's summary
    records = db.get_today_attendance()
    # Convert for JSON (handle None types)
    clean_records = []
    for r in records:
        clean_records.append({
            "id": r[0],
            "name": r[1],
            "login": r[2] or "N/A",
            "logout": r[3] or "N/A",
            "status": r[4]
        })
    return jsonify(clean_records)

# --- SMTP EMAIL API ENDPOINTS ---

@app.route('/api/smtp/test', methods=['POST'])
def test_smtp():
    """Test SMTP connection"""
    if not smtp_handler:
        return jsonify({"success": False, "message": "SMTP not configured"})
    
    success, message = smtp_handler.test_connection()
    return jsonify({"success": success, "message": message})

@app.route('/api/smtp/send_notification', methods=['POST'])
def send_notification():
    """Send attendance notification email"""
    if not smtp_handler:
        return jsonify({"success": False, "message": "SMTP not configured"})
    
    data = request.json
    person_name = data.get('person_name')
    person_id = data.get('person_id')
    recipient_email = data.get('recipient_email')
    event_type = data.get('event_type', 'arrival')
    timestamp = data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    if not all([person_name, person_id, recipient_email]):
        return jsonify({"success": False, "message": "Missing required fields"})
    
    success, message = smtp_handler.send_attendance_notification(
        person_name, person_id, recipient_email, event_type, timestamp
    )
    return jsonify({"success": success, "message": message})

@app.route('/api/smtp/send_summary', methods=['POST'])
def send_summary():
    """Send daily attendance summary"""
    if not smtp_handler:
        return jsonify({"success": False, "message": "SMTP not configured"})
    
    data = request.json
    recipient_email = data.get('recipient_email', SMTP_CONFIG.get('admin_email'))
    
    if not recipient_email:
        return jsonify({"success": False, "message": "No recipient email provided"})
    
    # Get statistics
    stats = db.get_statistics()
    summary_data = {
        'total_registered': stats['total_persons'],
        'present_today': stats['present_today']
    }
    
    success, message = smtp_handler.send_daily_summary(recipient_email, summary_data)
    return jsonify({"success": success, "message": message})

@app.route('/api/smtp/send_late_alert', methods=['POST'])
def send_late_alert():
    """Send late arrival alert"""
    if not smtp_handler:
        return jsonify({"success": False, "message": "SMTP not configured"})
    
    data = request.json
    person_name = data.get('person_name')
    person_id = data.get('person_id')
    recipient_email = data.get('recipient_email')
    arrival_time = data.get('arrival_time')
    expected_time = data.get('expected_time')
    
    if not all([person_name, person_id, recipient_email, arrival_time, expected_time]):
        return jsonify({"success": False, "message": "Missing required fields"})
    
    success, message = smtp_handler.send_late_arrival_alert(
        person_name, person_id, recipient_email, arrival_time, expected_time
    )
    return jsonify({"success": success, "message": message})

@app.route('/api/smtp/send_absence_alert', methods=['POST'])
def send_absence_alert():
    """Send absence alert for employees who didn't show up"""
    if not smtp_handler:
        return jsonify({"success": False, "message": "SMTP not configured"})
    
    data = request.json
    person_name = data.get('person_name')
    person_id = data.get('person_id')
    recipient_email = data.get('recipient_email')
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    department = data.get('department')
    
    if not all([person_name, person_id, recipient_email]):
        return jsonify({"success": False, "message": "Missing required fields"})
    
    success, message = smtp_handler.send_absence_alert(
        person_name, person_id, recipient_email, date, department
    )
    return jsonify({"success": success, "message": message})

@app.route('/api/smtp/config', methods=['GET'])
def get_smtp_config():
    """Get SMTP configuration status"""
    return jsonify({
        "enabled": EMAIL_NOTIFICATIONS_ENABLED,
        "configured": smtp_handler is not None,
        "smtp_server": SMTP_CONFIG.get('smtp_server', 'Not configured'),
        "sender_email": SMTP_CONFIG.get('sender_email', 'Not configured')
    })

if __name__ == '__main__':
    # Threaded is required for streaming + API calls simultaneously
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)