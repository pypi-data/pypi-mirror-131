# ---------------------------------- MATCH TEMPLATE

# from time import time, sleep
# import cv2 as cv
#
# from AlPyVision import Vision
#
# # Create new vision instance
# vision = Vision.Vision()
#
# # Grab window information once - outside of the loop
# window_information = vision.getWindowInfo(window_name='Albion Online Client')
#
# needle_img = cv.imread('tree_trunk_3.png')
#
# # Capture screen and show output, capture FPS while doing so
# loop_time = time()
# run = True
# while True:
#
#     screen_cap = vision.captureWindow(window_handle=None,
#                                       window_width=window_information[1],
#                                       window_height=window_information[2])
#
#     vision.findClickPositions(haystack_img=screen_cap, needle_img=needle_img,
#                               debug_mode=vision.debug_modes[1], threshold=0.3)
#
#     # cv.imshow('Bot Vision', screen_cap)
#     if cv.waitKey(1) == ord('y'):
#         cv.destroyAllWindows()
#         break

from AlPyVision import Data
gatherer = Data.Data()
root_filepath = 'D:/AlbionScreenshots'
resource = 'trees'
gatherer.gatherScreenshots(root_filepath)

