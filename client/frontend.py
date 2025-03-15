# flask_app.py (Flask web interface)
import os
import io
from flask import Flask, request, render_template, jsonify
from app import upload_video_to_grpc, send_log_entry_to_grpc  # Import the existing function
import json
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
LOG_FILE = 'response_logs.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

log_entry = {}


def log_response_data(log_entry):    
    # Load existing logs if available
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    # Append new log entry
    logs.append(log_entry)

    # Write updated logs back to the file
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file part in the request"}), 400
    
    file = request.files['video']
    model_name = request.form['model']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        #file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        #file.save(file_path)
        ip_address = request.remote_addr
        log_entry['ip_address'] = ip_address
        start_time = time.time()
        in_memory_file = io.BytesIO(file.read())

        # Use the video_file_generator directly from app.py grpc 
        response = upload_video_to_grpc(in_memory_file, model_name)
        

        end_time = time.time()

        grpc_system_response_time = round((end_time-start_time)*1000, 2)
        log_entry['grpc_system_response_time'] = grpc_system_response_time

        # log_entry['message'] = response.message  # Assuming these attributes exist
        # log_entry['success'] = response.success

        # Return the gRPC response
        return jsonify({
            "message": response.message,  # Assuming these attributes exist
            "success": response.success
        })
    


@app.route('/log_round_trip_time', methods=['POST'])
def log_round_trip_time():
    round_trip_time = request.form.get('round_trip_time')
    if round_trip_time:

        # Log round-trip time to the JSON log file
        log_entry['total_response_time'] = round(float(round_trip_time),2)

        response = send_log_entry_to_grpc(log_entry)

        log_response_data(log_entry)

        return jsonify({
            "message": response.message,  # Assuming these attributes exist
            "success": response.success
        })
    else:
        return jsonify({"error": "Round-trip time not provided"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)  