from ast import parse
import yolo_pb2_grpc
import yolo_pb2

import logging
import grpc
from PIL import Image
import sys
import io
import ast
import os

def run():

    image = Image.open(sys.argv[2])
    image_bytes = io.BytesIO()
    if image.mode == 'RGB':
        image.save(image_bytes, format='JPEG')
    else:
        image.save(image_bytes, format='PNG')
    bytes_array = image_bytes.getvalue()


    with grpc.insecure_channel(sys.argv[1]) as channel:
        stub = yolo_pb2_grpc.YoloServiceStub(channel)
        response = stub.Detection(yolo_pb2.RequestDetction(img=bytes_array))        
        print('Received a response from the server!')
        
        response = response.detections.decode("utf-8")
        #response = ast.literal_eval(response)       
         
        print("The response from the server is:", response) 




if __name__ == '__main__':
    logging.basicConfig()
    run()
