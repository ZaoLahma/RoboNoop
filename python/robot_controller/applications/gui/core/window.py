from tkinter import Tk
from tkinter import ttk
from tkinter import Frame
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import TOP
from tkinter import NW
from ....core.log.log import Log
from ..workspace.core.workspace_controller import WorkspaceController

class Window(Tk):
    def __init__(self, resolution):
        Log.log("Window init")
        Tk.__init__(self)

        self.resolution = resolution

        self.rowconfigure(0, minsize = resolution[1], weight = 1)
        self.columnconfigure(1, minsize = resolution[0], weight = 1)

        self.protocol("WM_DELETE_WINDOW", self.execute_shutdown_hooks)

        self.ws_controller = WorkspaceController()
        self.shutdown_hooks = []

        self.btn_frame = Frame(self)
        self.ws_frame = Frame(self)

        self.btn_frame.grid(row = 0, column = 0, sticky="ns")
        self.ws_frame.grid(row = 0, column = 1, sticky="nsew")

    def add_shutdown_hook(self, hook):
        self.shutdown_hooks.append(hook)

    def execute_shutdown_hooks(self):
        for hook in self.shutdown_hooks:
            hook()
        self.destroy()

    def get_ws_frame(self):
        return self.ws_frame

    def get_ws_controller(self):
        return self.ws_controller

    def add_workspace(self, WS_CLASS):
        workspace = WS_CLASS(self.ws_frame, self.ws_controller, self.resolution)
        self.ws_controller.add_workspace(workspace)
        ws_button = ttk.Button(self.btn_frame, text = workspace.get_id(), command = lambda : self.activate_workspace(WS_CLASS))
        ws_button.grid(row = len(self.ws_controller.get_workspaces()), column=0, sticky="ew", padx=5, pady=5)

    def activate_workspace(self, WS_CLASS):
        self.ws_controller.activate_workspace(WS_CLASS)

    def run(self):
        self.mainloop()