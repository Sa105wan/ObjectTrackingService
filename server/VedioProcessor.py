import os
import requests
import time
import json
import csv
from ObjectProcessor import ObjectProcessor
from db.DatabaseConnection import DatabaseConnection
from db.LogDatabase import LogDatabase
from LogEntry import LogEntry
import subprocess

LOG_FILE = 'server_logs.csv'
ot_time=0
service_data = {}
model=""


class VedioProcessor:
    def __init__(self):
        self.object_processor = ObjectProcessor()
        self.db_connection = DatabaseConnection()  # Create an instance of DatabaseConnection
        self.log_database = LogDatabase(self.db_connection) 
        self.log_entry_csv={}
        self.log_entry_frontend={}
        # self.avg_power

    def process_video(self, video_stream, model_name):
        global ot_time
        global model

        try:
            global ot_time
            global model

            start_time=time.time()
            # initial_power = self.get_power_usage_nvidia()
            name = model_name.split("_")
            if(name[1]=="botsort" or name[1]=="bytetrack"):
                print("model name is ")
                print(model_name)
                self.object_processor.trackInbuild(model_name)
                # final_power = self.get_power_usage_nvidia()
                end_time=time.time()
                ot_time = round((end_time-start_time)*1000,2)
                model=model_name
                return 'video successfully processed'

            else:
                self.object_processor.load_model(model_name)
                detections = self.object_processor.detect_objects("received_video.mp4")
                self.object_processor.track_objects(detections, "received_video.mp4" )
                # final_power = self.get_power_usage_nvidia()
                end_time=time.time()
                ot_time = round((end_time-start_time)*1000,2)
                print(model_name)
                model=model_name
                # self.avg_power = (initial_power + final_power) / 2
                return 'Vedio Successfully processed'

        except FileNotFoundError as fnf_error:
            # Handle file not found errors
            return fnf_error

        except ValueError as val_error:
            # Handle specific value-related issues
            return val_error

        except AttributeError as attr_error:
            # Handle missing attributes or methods
            return attr_error

        except Exception as e:
            # Catch all other unexpected errors
            return e




    def LogEntrySetter(self, request):
        global ot_time
        self.LogEntryProcessor(request, 'service1', ot_time)
        log_entry_string = json.dumps(self.log_entry_frontend, indent=4)
        return log_entry_string


    def LogEntryProcessor(self, request, service_name, ot_time):
        print("ot time is")
        print(ot_time)
        self.log_entry_csv = {
            'service_name': model,
            'ip_address': request.ip_address,
            'location': self.get_location_from_ip(request.ip_address),
            'grpc_system_response_time': request.grpc_system_response_time,
            'grpc_system_latency': round(request.grpc_system_response_time - ot_time, 2),
            'total_response_time': request.total_response_time,
            'total_latency': round(request.total_response_time - ot_time, 2),
            'throughput':self.get_throughput(ot_time,"received_video.mp4")
        }

# Just to add units to the frontend
        self.log_entry_frontend = {
            'service_name': model,
            'ip_address': request.ip_address,
            'location': self.get_location_from_ip(request.ip_address),
            'grpc_system_response_time': str(request.grpc_system_response_time) + " ms",  # Convert to string
            'grpc_system_latency': str(round(request.grpc_system_response_time - ot_time, 2)) + " ms",  # Convert to string
            'total_response_time': str(request.total_response_time) + " ms",  # Convert to string
            'total_latency': str(round(request.total_response_time - ot_time, 2)) + " ms",  # Convert to string
            'throughput': str(self.get_throughput(ot_time, "received_video.mp4")) + " Mbps"  # Convert to string
        }

        # Check if the file already exists
        file_exists = os.path.isfile(LOG_FILE)

        # Define fieldnames to maintain the column order
        fieldnames = [
            'service_name', 'ip_address', 'location', 
            'grpc_system_response_time', 'grpc_system_latency', 
            'total_response_time', 'total_latency', 'throughput'
        ]

        # Open the CSV file in append mode
        with open(LOG_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header only if file does not exist
            if not file_exists:
                writer.writeheader()

            # Write the log entry as a new row
            writer.writerow(self.log_entry_csv)

        log_entry = LogEntry(
            service_name=model,
            ip_address=request.ip_address,
            location=self.get_location_from_ip(request.ip_address),
            grpc_system_response_time=request.grpc_system_response_time,
            grpc_system_latency=round(request.grpc_system_response_time - ot_time, 2),
            total_response_time=request.total_response_time,
            total_latency=round(request.total_response_time - ot_time, 2)
            # througput=self.get_throughput(ot_time, "received_video.mp4")
        )

        # Save the log entry to the database using LogDatabase
        self.log_database.save_log(log_entry)


    def get_location_from_ip(self, ip_address):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()
            if data['status'] == 'success':
                return {
                    'country': data['country'],
                    'region': data['regionName'],
                    'city': data['city']
                }
            else:
                return {"error": "Unable to retrieve location"}
        except Exception as e:
            return {"error": str(e)}
        
    def get_throughput(self,ot_time, video_path):
        file_size_bytes = os.path.getsize(video_path)

        file_size_mb = file_size_bytes / (1024 * 1024)
        if ot_time==0:
            return 'err process time is 0'
        return round((file_size_mb / (ot_time / 1000)) * 8, 4)    #throughput Mbps


    def get_power_usage_nvidia():
        try:
           
            output = subprocess.check_output(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'])
            power_watts = float(output.decode('utf-8').strip())
            return power_watts
        except Exception as e:
            print(f"Error fetching power consumption: {e}")
            return 0  