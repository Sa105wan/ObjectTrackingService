import asyncio
import logging
import io
import grpc
import otservice_pb2
import otservice_pb2_grpc
from objectTracking import ObjectTracker

class OtService(otservice_pb2_grpc.OtServiceServicer):

    def __init__(self):
        # Initialize the object tracker once in the service class
        self.tracker = ObjectTracker()
    
    async def UploadVideo(self, request_iterator, context):
        total_data = b""
        async for video_request in request_iterator:
            total_data += video_request.video_file
        
        # Save the received video to a file (optional)
        with open('received_video.mp4', 'wb') as f:
            f.write(total_data)
        
        video_stream = io.BytesIO(total_data)

        # Pass the video stream to the object tracker
        tracking_results = self.tracker.track_objects(video_stream)
        
        # Respond to client
        return otservice_pb2.VideoResponse(
            success=True,
            message=tracking_results
        )

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
