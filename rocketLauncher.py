#!/usr/bin/python3

import os
import sys
import time
import usb.core
import cv2

class startRocket():
   
   def __init__(self):
   
      self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
   
      if self.dev is None:
         raise ValueError('Launcher not found.')
   
      if self.dev.is_kernel_driver_active(0) is True:
         self.dev.detach_kernel_driver(0)
      self.dev.set_configuration()

      self.captureVideo()

   def captureVideo(self):
   	  # Enter Camera Index here:
      cap = cv2.VideoCapture(2)
      
      if (cap.isOpened() == False): 
         print("Unable to read camera feed")
      
      frame_width = int(cap.get(3))
      frame_height = int(cap.get(4))
      
      out = cv2.VideoWriter('rocketLauncher.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
      
      while(True):
         ret, frame = cap.read()
         
         if ret == True: 
            
            out.write(frame)
            cv2.imshow('frame', frame)
         
            key = cv2.waitKey(50)

            if (key == 81):
               self.left()
            elif (key == 82):
               self.up()
            elif (key == 83):
               self.right()
            elif (key == 84):
               self.down()
            elif (key == ord(' ')):
               self.fire()
            elif (key == 27):
               break
            else:
               self.stop()
         
         else:
            break 
      
      cap.release()
      out.release()
      
      cv2.destroyAllWindows()

   def up(self):
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00]) 

   def down(self):
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00])

   def left(self):
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00])

   def right(self):
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00])

   def stop(self):
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00])

   def fire(self):
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00])
      time.sleep(2)


if __name__ == '__main__':
   startRocket()
