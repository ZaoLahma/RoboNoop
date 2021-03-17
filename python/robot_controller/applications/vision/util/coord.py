import math

#
# Alright, some definitions
# cam-centre coordinate system has its origin
# in the middle of the image, where -1 <= x <= 1
# increasing left to right and -1 <= y <= 1 incresing
# down to up
#          1
#          |
# -1 ------|----- -1
#          |
#         -1

class Coord():
    X_OFFSET = -1
    Y_OFFSET = -1

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

        rndfloat = Coord.round_to_float

        return [rndfloat(rect[0] / x_res) + Coord.X_OFFSET, (rndfloat(rect[1] / y_res) + Coord.Y_OFFSET) * -1, rndfloat(rect[2] / x_res) + Coord.X_OFFSET, rndfloat(rect[3] / y_res) + Coord.Y_OFFSET]

    @staticmethod
    def cam_centre_to_image(rect, image_res):
        raise NotImplementedError