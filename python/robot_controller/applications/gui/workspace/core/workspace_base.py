from tkinter import Frame

class WorkspaceBase():
    def __init__(self, parent_frame, ws_controller, ws_resolution):
        self.parent_frame = parent_frame
        self.ws_controller = ws_controller
        self.ws_resolution = ws_resolution
        self.ws_frame = None
        self.components = []

    def construct_frame(self):
        self.ws_frame = Frame(self.parent_frame)

    def tkraise(self):
        self.ws_frame.tkraise()

    def add_component(self, component):
        self.components.append(component)

    @staticmethod
    def get_id(self):
        raise NotImplementedError

    def activate(self):
        raise NotImplementedError

    def pause(self):
        raise NotImplementedError

    def deactivate(self):
        raise NotImplementedError

    def destroy(self):
        self.ws_frame.destroy()
