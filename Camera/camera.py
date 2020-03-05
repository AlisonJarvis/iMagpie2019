#!/usr/bin/env python

import argparse
import os
import sys
import time
import zwoasi as asi
import numpy as np
from PIL import Image
import wx

__author__ = 'Steve Marple'
__version__ = '0.1.0'
__license__ = 'MIT'

SIZE = (640, 480)
WIDTH = 4656
HEIGHT = 3520

# ASI_IMGTYPE
ASI_IMG_RAW8 = 0
ASI_IMG_RGB24 = 1
ASI_IMG_RAW16 = 2
ASI_IMG_Y8 = 3
ASI_IMG_END = -1


def save_control_values(filename, settings):
    filename += '.txt'
    with open(filename, 'w') as f:
        for k in sorted(settings.keys()):
            f.write('%s: %s\n' % (k, str(settings[k])))
    print('Camera settings saved to %s' % filename)

def get_bitmap(camera):
    data = camera.get_video_data()
    buffer = np.repeat(bytes(data),3)
    bitmap = wx.Bitmap.FromBuffer(WIDTH, HEIGHT, buffer)
    return bitmap

class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent, -1)
        self.camera = parent.camera
        self.SetSize(SIZE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.update()
    def update(self):
        self.Refresh()
        self.Update()
        wx.CallLater(15, self.update)
    def create_bitmap(self):
        bitmap = get_bitmap(self.camera)
        return bitmap
    def on_paint(self, event):
        bitmap = self.create_bitmap()
        dc = wx.AutoBufferedPaintDC(self)
        dc.DrawBitmap(bitmap, 0, 0)

class Frame(wx.Frame):
    def __init__(self,camera):
        style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX
        super(Frame, self).__init__(None, -1, 'Camera Viewer', style=style)
        self.camera = camera
        panel = Panel(self)
        self.Fit()


class ImageSensor():
    def __init__(self):
        env_filename = os.getenv('ZWO_ASI_LIB')
        parser = argparse.ArgumentParser(description='Process and save images from a camera')
        parser.add_argument('filename',
                            nargs='?',
                            help='SDK library filename')
        args = parser.parse_args()
        args.filename = '../ZWO_ASI_Library/lib/armv7/libASICamera2.so';
        #args.filename = '../ZWO_ASI_Library/lib/mac/libASICamera2.dylib';
        # Initialize zwoasi with the name of the SDK library
        if args.filename:
            asi.init(args.filename)
        elif env_filename:
            asi.init(env_filename)
        else:
            print('The filename of the SDK library is required (or set ZWO_ASI_LIB environment variable with the filename)')
            sys.exit(1)
        num_cameras = asi.get_num_cameras()
        if num_cameras == 0:
            print('No cameras found')
            sys.exit(0)
        cameras_found = asi.list_cameras()  # Models names of the connected cameras
        if num_cameras == 1:
            camera_id = 0
            print('Found one camera: %s' % cameras_found[0])
        else:
            print('Found %d cameras' % num_cameras)
            for n in range(num_cameras):
                print('    %d: %s' % (n, cameras_found[n]))
            # TO DO: allow user to select a camera
            camera_id = 0
            print('Using #%d: %s' % (camera_id, cameras_found[camera_id]))

        camera = asi.Camera(camera_id)
        camera_info = camera.get_camera_property()
        # Get all of the camera controls
        print('')
        print('Camera controls:')
        controls = camera.get_controls()
        for cn in sorted(controls.keys()):
            print('    %s:' % cn)
            for k in sorted(controls[cn].keys()):
                print('        %s: %s' % (k, repr(controls[cn][k])))
        # Use maximum USB bandwidth permitted
        camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MaxValue'])
        # Set some sensible defaults. They will need adjusting depending upon
        # the sensitivity, lens and lighting conditions used.
        camera.disable_dark_subtract()
        camera.set_control_value(asi.ASI_GAIN, 0)
        camera.set_control_value(asi.ASI_EXPOSURE, 10000)
        camera.set_control_value(asi.ASI_WB_B, 99)
        camera.set_control_value(asi.ASI_WB_R, 75)
        camera.set_control_value(asi.ASI_GAMMA, 50)
        camera.set_control_value(asi.ASI_BRIGHTNESS, 50)
        camera.set_control_value(asi.ASI_FLIP, 0)
        self.camera = camera
    def save_image(self):
        print('Enabling stills mode')
        try:
            # Force any single exposure to be halted
            self.camera.stop_video_capture()
            self.camera.stop_exposure()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pass
        print('Capturing a single 8-bit mono image')
        filename = 'image_mono.jpg'
        self.camera.set_image_type(asi.ASI_IMG_RAW8)
        self.camera.capture(filename=filename)
        print('Saved to %s' % filename)
        save_control_values(filename, self.camera.get_control_values())
    def start_video_feed(self):
        # Enable video mode
        try:
            # Force any single exposure to be halted
            camera.stop_exposure()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pass
        print('Enabling video mode')
        self.camera.start_video_capture()
        # Set the timeout, units are ms
        timeout = (self.camera.get_control_value(asi.ASI_EXPOSURE)[0] / 1000) * 2 + 500
        self.camera.default_timeout = timeout
        # Set up window and display images
        app = wx.App()
        frame = Frame(self.camera)
        frame.Center()
        frame.Show()
        app.MainLoop()

# Initialize object
imageSensor = ImageSensor()

# 8-BIT MONO IMAGE CAPTURE
imageSensor.save_image()

# LIVE VIDEO FEED
imageSensor.start_video_feed()

## 16-BIT MONO IMAGE CAPTURE
# print('Capturing a single 16-bit mono image')
# filename = 'image_mono16.tiff'
# camera.set_image_type(asi.ASI_IMG_RAW16)
# camera.capture(filename=filename)
# print('Saved to %s' % filename)
# save_control_values(filename, camera.get_control_values())
# 
# img1 = Image.open('image_mono16.tiff')
# img1.point(lambda i:i*(1./256)).convert('L').save('my.png')

## DEMO VIDEO CODE
# # Enable video mode
# try:
#     # Force any single exposure to be halted
#     camera.stop_exposure()
# except (KeyboardInterrupt, SystemExit):
#     raise
# except:
#     pass
# 
# print('Enabling video mode')
# camera.start_video_capture()
# 
# #Restore all controls to default values except USB bandwidth
# for c in controls:
#     if controls[c]['ControlType'] == asi.ASI_BANDWIDTHOVERLOAD:
#         continue
#     camera.set_control_value(controls[c]['ControlType'], controls[c]['DefaultValue'])
# 
# # Set the timeout, units are ms
# timeout = (camera.get_control_value(asi.ASI_EXPOSURE)[0] / 1000) * 2 + 500
# print(timeout)
# camera.default_timeout = timeout
# 
# if camera_info['IsColorCam']:
#     print('Capturing a single color frame')
#     filename = 'image_video_color.jpg'
#     camera.set_image_type(asi.ASI_IMG_RGB24)
#     camera.capture_video_frame(filename=filename)
# else:
#     print('Capturing a single 8-bit mono frame')
#     filename = 'image_video_mono.jpg'
#     camera.set_image_type(asi.ASI_IMG_RAW8)
#     camera.capture_video_frame(filename=filename)
# 
# print('Saved to %s' % filename)
# save_control_values(filename, camera.get_control_values())