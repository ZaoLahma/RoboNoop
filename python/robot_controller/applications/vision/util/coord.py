import math

class Coord():
    @staticmethod
    def round_up(value):
        return math.ceil(value * 100) / 100

    @staticmethod
    def image_to_cam_centre(rect, image_res):
        x_res = image_res[0]
        y_res = image_res[1]

        rndup = Coord.round_up

        return [rndup(rect[0] / x_res), rndup(rect[1] / y_res), rndup(rect[2] / x_res), rndup(rect[3] / y_res)]