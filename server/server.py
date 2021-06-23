import yolo_pb2_grpc
import yolo_pb2 

import logging
import grpc
from PIL import Image
import sys
import os
import io
from concurrent import futures
import time
from subprocess import check_output

from detect import detect

class BaseLine(yolo_pb2_grpc.YoloServiceServicer):
    def Detection(self, request, context):
        print('Received an image!')

        stream = io.BytesIO(request.img)
        img = Image.open(stream)
        img_to_save = './infer_image.jpg'
        img.save(img_to_save)
        #         
        #print('Image size received:',img.size)

        detect(weights='./runs/training/weights/best.pt', source='server/' + img_to_save, project='server/detections/', )

        return yolo_pb2.ResponseDetection(detections=str.encode('Testando isso aqui meeu'))


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    yolo_pb2_grpc.add_YoloServiceServicer_to_server(BaseLine(), server)

    print(f'Starting server at port: {sys.argv[1]}')

    if not os.path.exists('temp/'):
            os.mkdir('temp')

    server.add_insecure_port(sys.argv[1])
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    run()
