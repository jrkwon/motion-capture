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
    RES_480P  = 0
    RES_720P  = 1
    RES_1080P = 2
    
    
    def __init__(self, target_dir, camera_id, time_zone):
        self.image_ext = '.jpg'
        self.camera_id = camera_id
        self.time_zone = time_zone
        self.video = cv2.VideoCapture(camera_id)
        if self.video is None or not self.video.isOpened():
            print('Error: unable to open video source: ', camera_id)
            self.video = None   # to indicate video is not available


    def _change_resolution(self, width, height):
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


    def _make_1080p(self):
        self._change_resolution(1920, 1080)


    def _make_720p(self):
        self._change_resolution(1280, 720)


    def _make_480p(self):
        self._change_resolution(640, 480)


    def set_resolution(self, res_id):
        if res_id == self.RES_1080P:
            self._make_1080p()
        elif res_id == self.RES_720P:
            self._make_720p()
        elif res_id == self.RES_480P:
            self._make_480p()

    
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
    

def main(resolution, verbose, target_dir, camera_id, time_zone):
    # define a video capture object
    vr = VideoRecoder(target_dir, camera_id, time_zone)
    if vr.video is None:
        return

    path = vr.create_directory(target_dir)
    vr.set_resolution(resolution)
        
    print("Start recording... Press 'q' to stop.")
    while(True):
          
        # Capture the video frame
        # by frame
        ret, frame = vr.video.read()
      
        # Display the resulting frame
        filename = vr.get_time_stamp() + vr.image_ext
        
        cv2.imshow('Camera ' + str(camera_id), frame)
        file_path = os.path.join(path, filename)
        if verbose:
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
    print("Done recording.")
    print("Directory {} has all captured images.".format(path))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Video Recorder ver 0.3 by Jaerock Kwon, 2021')
    parser.add_argument("-r", "--resolution", type=int, default=0, choices=(0, 1, 2), 
                    help="resolution id number: 0:640x480, 1:1280x720, 2:1920x1080")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="print filenames")
    parser.add_argument("-c", "--camera_id", type=int, default=0, choices=(0, 1, 2, 3), 
                        help="camera id number")
    parser.add_argument("-t", "--time_zone", default="utc", 
                        choices=("utc", "local"), 
                        help="time zone: default utc")
    parser.add_argument("target_dir", type=str, help="target directory name")
    args = parser.parse_args()
    
    main(args.resolution, args.verbose, args.target_dir, args.camera_id, args.time_zone)
