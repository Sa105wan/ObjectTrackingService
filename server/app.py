import asyncio
import logging
import io
import grpc
import otservice_pb2, otservice_pb2_grpc
from VedioProcessor import VedioProcessor
import requests
import time

LOG_FILE = 'server_logs.json'
ot_time=0



class OtService(otservice_pb2_grpc.OtServiceServicer):

    def __init__(self):
        # Initialize the object tracker once in the service class
        self.vedio_processor = VedioProcessor()
        self.video_processed_flag = True
    
    async def UploadVideo(self, request_iterator, context):
        global ot_time
        total_data = b""
        self.video_processed_flag=True
        async for video_request in request_iterator:
            total_data += video_request.video_file
            if video_request.model:
                model_name = video_request.model  # Capture model name from request
        
        # Save the received video to a file (optional)
        with open('received_video.mp4', 'wb') as f:
            f.write(total_data)
        
        video_stream = io.BytesIO(total_data)

        result = self.vedio_processor.process_video(video_stream, model_name)

        if isinstance(result, Exception):
            self.video_processed_flag=False
            print(f"Error occurred while processing video: {str(result)}")
            # Respond to client with failure message
            return otservice_pb2.VideoResponse(
                success=False,
                message=f"Failed to process video: {str(result)}"
            )

        # Respond to client
        return otservice_pb2.VideoResponse(
            success=True,
            message=str(result)
        )
    
    
    
    def SendLogEntry(self, request, context):
        try:
        # Retrieve log entry data from request
            if not self.video_processed_flag:
                raise Exception("No logs generated as the video was not processed successfully.")

            global ot_time
            log_entry_string = self.vedio_processor.LogEntrySetter(request)

        # Return a success response
            return otservice_pb2.LogResponse(success=True, message=log_entry_string)
    
        except Exception as e:
        # Handle any unexpected errors
            error_message = f"Error processing log entry: {str(e)}"
            print(error_message)  # Log the error on the server side
            # return otservice_pb2.LogResponse(success=False, message=error_message)
            return otservice_pb2.LogResponse(
                success=False,
                message=f"Failed to process video: {str(e)}"
            )



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

async def serve() -> None:
    server = grpc.aio.server()
    otservice_pb2_grpc.add_OtServiceServicer_to_server(OtService(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
