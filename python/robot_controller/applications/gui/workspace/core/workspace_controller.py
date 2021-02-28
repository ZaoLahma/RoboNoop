from .....core.log.log import Log

class WorkspaceController:
    def __init__(self, ws_frame, ws_resolution):
        Log.log("WorkspaceController init")
        self.ws_frame = ws_frame
        self.ws_resolution = ws_resolution
        self.workspaces = {}
        self.curr_workspace = None

    def add_workspace(self, WS_CLASS):
        self.workspaces[WS_CLASS.get_id()] = WS_CLASS

    def activate_workspace(self, WS_CLASS):
        if None == self.curr_workspace or WS_CLASS.get_id() != self.curr_workspace.get_id():
            if None != self.curr_workspace:
                self.curr_workspace.deactivate()
                self.curr_workspace.destroy()
            self.curr_workspace = WS_CLASS(self.ws_frame, self, self.ws_resolution)
            self.curr_workspace.grid(row = 0, column = 0)
            self.curr_workspace.activate()
            self.curr_workspace.tkraise()
            Log.log("Activated workspace " + self.curr_workspace.get_id())

    def get_workspaces(self):
        return self.workspaces