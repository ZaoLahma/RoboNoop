from tkinter import Frame

class WorkspaceBase(Frame):
    def __init__(self, parent_frame, ws_controller):
        Frame.__init__(self, parent_frame)
        self.parent_frame = parent_frame
        self.ws_controller = ws_controller

    @staticmethod
    def get_id(self):
        raise NotImplementedError

    def activate(self):
        raise NotImplementedError

    def pause(self):
        raise NotImplementedError

    def deactivate(self):
        raise NotImplementedError