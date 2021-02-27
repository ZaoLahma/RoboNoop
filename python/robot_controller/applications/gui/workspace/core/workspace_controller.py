from .....core.log.log import Log

class WorkspaceController:
    def __init__(self):
        Log.log("WorkspaceController init")
        self.workspaces = {}
        self.curr_workspace = None

    def add_workspace(self, workspace):
        self.workspaces[workspace.get_id()] = workspace

    def activate_workspace(self, WS_CLASS):
        ws_to_activate = self.workspaces[WS_CLASS.get_id()]
        if ws_to_activate != self.curr_workspace:
            if None != self.curr_workspace:
                self.curr_workspace.deactivate()
                self.curr_workspace.destroy()
            self.curr_workspace = ws_to_activate
            self.curr_workspace.construct_frame()
            self.curr_workspace.ws_frame.grid(row = 0, column = 0)
            self.curr_workspace.activate()
            self.curr_workspace.tkraise()
            Log.log("Activated workspace " + self.curr_workspace.get_id())

    def get_workspaces(self):
        return self.workspaces