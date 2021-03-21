from ....core.log.log import Log

import math

#
# Alright, some definitions
# cam-centre coordinate system has its origin
# in the middle of the image, where -0.5 <= x <= 0.5
# increasing left to right and -0.5 <= y <= 0.5 incresing
# down to up
#           0.5
#            |
# -0.5 ------|----- 0.5
#            |
#          -0.5

#
# 320 / 640 = 0.5 - 1 = -0.5 
# 320 / 640 = 0.5 - 0.5 = 0
# 160 / 640 = 0.25 - 0.5 = -0.25
# 480 / 640 = 0.75 - 0.5 = 0.25
#
class Coord():
    X_OFFSET = -0.5
    Y_OFFSET = -0.5

    @staticmethod
    def round_to_float(value):
        return math.ceil(value * 100) / 100

    @staticmethod
    def round_to_int(value):
        return math.floor(value + 0.5)

    @staticmethod
    def image_to_cam_centre(rect, image_res):
        x_res = image_res[0]
        y_res = image_res[1]

        Log.log("Transforming: " + str(rect))

        rndfloat = Coord.round_to_float

        return [rndfloat(rect[0] / x_res) + Coord.X_OFFSET, (rndfloat(rect[1] / y_res) + Coord.Y_OFFSET) * -1, rndfloat(rect[2] / x_res), rndfloat(rect[3] / y_res)]

    @staticmethod
    def cam_centre_to_image(rect, image_res):
        x_res = image_res[0]
        y_res = image_res[1]

        rndint = Coord.round_to_int

        x = ((rect[0] - Coord.X_OFFSET) * x_res)
        y = (((rect[1] * -1) - Coord.Y_OFFSET) * y_res)
        w = (rect[2] * x_res)
        h = (rect[3] * y_res)

        return [rndint(x), rndint(y), rndint(w), rndint(h)]

# -0.45 * -1 = 0.45 -0.5 = 0.05 * 480

#2021-03-21 18:54:38.299937 vision coord.py:40 - Transforming: [200  22  87 174]
#2021-03-21 18:54:38.321033 vision coord.py:40 - Transforming: [287   0 115 216]
#2021-03-21 18:54:38.346426 vision vision_task.py:68 - Detected these humans: [[-0.18  0.45  0.14  0.37]
# [-0.05  0.5   0.18  0.45]] []
#2021-03-21 19:54:40.280929 ws_vision.py:114 - Detected orig coords: [-0.18, 0.44999999999999996, 0.14, 0.37] transformed: [205, 240, 90, 178]
#2021-03-21 19:54:40.281373 ws_vision.py:114 - Detected orig coords: [-0.04999999999999999, 0.5, 0.18, 0.45] transformed: [288, 240, 115, 216]