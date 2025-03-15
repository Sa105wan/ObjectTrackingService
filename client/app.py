import grpc
import otservice_pb2_grpc, otservice_pb2

# when video is comming from the client and stored at client server
def video_file_generator(file_path):
    with open(file_path, 'rb') as f:
        chunk_size = 1024 * 1024  # 1MB chunks
        while chunk := f.read(chunk_size):
            yield otservice_pb2.VideoRequest(video_file=chunk)

# when video is comming from user from the flask app
def in_memory_video_file_generator(in_memory_file, model_name):
    chunk_size = 1024 * 1024  
    in_memory_file.seek(0)  
    while chunk := in_memory_file.read(chunk_size):
        yield otservice_pb2.VideoRequest(video_file=chunk, model=model_name)

def upload_video_to_grpc(in_memory_file, model_name):
    """
    Handles the gRPC communication and uploads the video using the provided generator.
    """
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = otservice_pb2_grpc.OtServiceStub(channel)
            #response = stub.UploadVideo(video_file_generator(file_path))  # Call generator directly
        response = stub.UploadVideo(in_memory_video_file_generator(in_memory_file, model_name))
    return response


def send_log_entry_to_grpc(log_entry):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = otservice_pb2_grpc.OtServiceStub(channel)

        # Create a LogEntry message
        log_message = otservice_pb2.LogEntry(
            ip_address=log_entry['ip_address'],
            grpc_system_response_time=log_entry['grpc_system_response_time'],
            total_response_time=log_entry['total_response_time']
        )

        # Send the log entry to the server
        response = stub.SendLogEntry(log_message)

        # Check for a successful response
        if response.success:
            print("Log entry successfully sent to the server.")
        else:
            print(f"Failed to send log entry: ")
            print(response.message)
            return response
        
        return response



def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = otservice_pb2_grpc.OtServiceStub(channel)
        response = stub.UploadVideo(video_file_generator('C:\\Users\\12514\\Desktop\\ObjectTrackingGRPCService\\client\\data\\input.mp4'))
        print(f"Response: {response.message}, Success: {response.success}")

if __name__ == '__main__':
    run()
