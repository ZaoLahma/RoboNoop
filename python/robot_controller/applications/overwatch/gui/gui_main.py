from tkinter import Tk


class GuiMain():
    def __init__(self, dimensions, scheduler, comm_if):
        self.dimensions = dimensions
        self.scheduler = scheduler
        self.comm_if = comm_if
        self.window = Tk()
        self.window.title("Overwatch")
        self.window.size
        self.active = False

    def update(self):
        if self.active:
            self.window.after(200, self.update)

    def run(self):
        self.active = True
        self.update()
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()

    def stop(self):
        self.scheduler.stop()
        self.active = False
        self.window.destroy()
