import grpc
import otservice_pb2
import otservice_pb2_grpc

def video_file_generator(file_path):
    with open(file_path, 'rb') as f:
        chunk_size = 1024 * 1024  # 1MB chunks
        while chunk := f.read(chunk_size):
            yield otservice_pb2.VideoRequest(video_file=chunk)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = otservice_pb2_grpc.OtServiceStub(channel)
        response = stub.UploadVideo(video_file_generator('C:\\Users\\12514\\Desktop\\ObjectTrackingGRPCService\\client\\data\\input.mp4'))
        print(f"Response: {response.message}, Success: {response.success}")

if __name__ == '__main__':
    run()
