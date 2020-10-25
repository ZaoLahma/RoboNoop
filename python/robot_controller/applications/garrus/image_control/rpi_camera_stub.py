from ....core.log.log import Log
import random

class PiCamera:
  def __init__(self):
    Log.log("Creating an RPiCameraStub")
    self.resolution = (0, 0)
    self.rotation = 0

  def __getRandomColorVal(self):
    return random.randint(0, 255).to_bytes(1, byteorder='little')

  def capture(self, buffer, image_format, use_video_port):
    for _ in range(0, (self.resolution[0] * self.resolution[1])):
      if 'rgb' == image_format:
        buffer.write(self.__getRandomColorVal())
        buffer.write(self.__getRandomColorVal())
        buffer.write(self.__getRandomColorVal())
      else:
        raise NotImplementedError