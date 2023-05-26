import cv2
import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import Person_det_track


class App:
    def __init__(self, window, window_title, video_source=0):
        self.photo = None
        self.window = window
        self.window.title(window_title)

        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.canvas.bind("<ButtonPress-1>", self.SetFirstPoint)
        self.canvas.bind("<ButtonRelease-1>", self.SetSecondPoint)

        self.canvas.bind("<ButtonPress-2>", self.whell_click)

        self.canvas.bind("<Double-Button-3>", self.DeleteArea)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15

        self.btn4 = Button(self.window, width=10, text="Click")
        self.btn4.bind("<Button-1>", self.whell_click)
        self.btn4.pack(side=TOP, padx=5, pady=5, anchor=W)

        columns = ("id", "activeTime", "passiveTime")

        self.tree = ttk.Treeview(columns=columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1, padx=5)
        self.tree.anchor("w")
        self.tree.heading("id", text="ID")
        self.tree.heading("activeTime", text="Активное время")
        self.tree.heading("passiveTime", text="Пассивное время")

        self.btn = Button(self.window, width=10, text="Click")
        self.btn.bind("<Button-1>", self.reload_table)
        self.btn.pack(side=LEFT, padx=5, pady=5, anchor=W)

        self.btn2 = Button(self.window, width=10, text="Click too")
        self.btn2.pack(side=LEFT, padx=5, pady=5, anchor=W)

        self.btn3 = Button(self.window, width=10, text="Click too___")
        self.btn3.pack(side=TOP, padx=5, pady=5, anchor=W)

    def update(self, img=None):
        # Get a frame from the video source
        self.window.configure(bg='#%02x%02x%02x' % (64, 204, 208))
        ret, frame = Person_det_track.myfunc()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)
        # if img is not None:
        #     self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        #     self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        # self.window.after(self.delay, self.update)

    def SetFirstPoint(self, event):
        Person_det_track.SetFirstPoint(event.x, event.y)

    def SetSecondPoint(self, event):
        Person_det_track.SetSecondPoint(event.x, event.y)
        Person_det_track.AddArea()

    def DeleteArea(self, event):
        Person_det_track.DeleteArea(event.x, event.y)

    def whell_click(self, event):
        if self.tree.winfo_viewable():
            self.tree.pack_forget()
            self.btn.pack_forget()
            self.btn2.pack_forget()
            self.btn3.pack_forget()
        else:
            self.tree.delete(*self.tree.get_children())
            for area in Person_det_track.selectedAreasList:
                self.tree.insert("", END, values=(1, area.activeTime, area.passiveTime))

            self.tree.pack(fill=BOTH, expand=1, anchor=N, padx=5)
            self.btn.pack(side=LEFT, padx=5, pady=5, anchor=W)
            self.btn2.pack(side=LEFT, padx=5, pady=5, anchor=W)
            self.btn3.pack(side=TOP, padx=5, pady=5, anchor=W)

    def reload_table(self, event):
        self.tree.delete(*self.tree.get_children())
        for area in Person_det_track.selectedAreasList:
            self.tree.insert("", END, values=(1, area.activeTime, area.passiveTime))



class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        ret, frame = self.vid.read()
        if self.vid.isOpened():

            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None


if __name__ == "__main__":
    a = App(tkinter.Tk(), 'имя окна')
    a.update()
    a.window.mainloop()
# i=0
# while i<1000:
#     print(1)
#     a.update()
#     i+=1
#
# a.window.mainloop()
