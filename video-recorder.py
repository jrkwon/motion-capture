#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 17:30:58 2021

@author: jaerock
"""

# import the opencv library
import cv2
import datetime
import time
#import sys
import os
import argparse

class VideoRecoder():
    def __init__(self, target_dir, camera_id, time_zone):
        self.image_ext = '.jpg'
        self.camera_id = camera_id
        self.time_zone = time_zone
        self.video = cv2.VideoCapture(camera_id)
        
    def get_time_stamp(self):
        unix_time = time.time()
        if self.time_zone == "utc":
            time_stamp = datetime.datetime.utcfromtimestamp(unix_time).strftime("%Y-%m-%d-%H-%M-%S-%f")
        else:
            time_stamp = datetime.datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d-%H-%M-%S-%f")
        return "{:.6f}={}".format(unix_time, time_stamp)
    
    def create_directory(self, target_dir):
        directory = self.get_time_stamp()
        path = os.path.join(target_dir, directory)
        os.makedirs(path)
        print("Directory {} created.".format(path))
        return path
    
def main(target_dir, camera_id, time_zone):
    # define a video capture object
    vr = VideoRecoder(target_dir, camera_id, time_zone)

    path = vr.create_directory(target_dir)
        
    print("Press 'q' to stop.")
    while(True):
          
        # Capture the video frame
        # by frame
        ret, frame = vr.video.read()
      
        # Display the resulting frame
        filename = vr.get_time_stamp() + vr.image_ext
        
        cv2.imshow('Video', frame)
        file_path = os.path.join(path, filename)
        print(file_path)
        cv2.imwrite(file_path, frame)
          
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
      
    # After the loop release the cap object
    vr.video.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Video Recorder ver 0.1')
    parser.add_argument("-c", "--camera_id", default=0, choices=[0, 1, 2, 3], 
                        help="camera id number")
    parser.add_argument("-t", "--time_zone", default="utc", 
                        choices=["utc", "local"], 
                        help="time zone: default utc")
    parser.add_argument("target_dir", type=str, help="target directory name")
    args = parser.parse_args()
    
    main(args.target_dir, args.camera_id, args.time_zone)