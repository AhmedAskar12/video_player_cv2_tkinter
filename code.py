import customtkinter
from PIL import Image, ImageTk
import tkinter as tk
import cv2
import time


# Configuring tkinter frame.
tframe = tk.Tk()
tframe.configure(bg='#212325')
tframe.geometry("700x400")
APP_NAME = "tframe"
tframe.title(APP_NAME)

# Building the frame.
VideoFrame = customtkinter.CTkFrame(master=tframe, corner_radius=0)
VideoFrame.place(relx=0.005, y=0, relwidth=1, relheight=1)

VFrame = tk.Label(VideoFrame, bg="#2a2d2e")
VFrame.place(relx=0, rely=0, relheight=.9, relwidth=1)

FilefpsD = tk.Label(VideoFrame, text="fps: 0", bg='#2a2d2e', foreground="white", font=("Roboto Medium", -14))
FilefpsD.place(relx=0.9, rely=0, relwidth=0.1, relheight=0.1)

Registratyion = tk.Label(VFrame, text="Add Media", bg="#2a2d2e", fg="gray29", font=("Roboto Medium", -20))
Registratyion.place(relx=0.0, rely=0, relheight=1, relwidth=1)

VideoBar = tk.Frame(master=tframe, bg='#212325')
VideoBar.place(relx=0.005, rely=0.9, relwidth=1, relheight=0.1)

PlayButton = customtkinter.CTkButton(master=VideoBar, text="Play", command=lambda: VideoPlay.source(),
                                     hover_color="#8B4000" ,fg_color="#EE7600",
                                     corner_radius=0)
PlayButton.place(relx=0.01, rely=0.15, relwidth=0.07, relheight=0.7)
PauseButton = customtkinter.CTkButton(master=VideoBar, text="Pause", command=lambda: VideoPlay.freeze(),
                                      hover_color="#8B4000" ,fg_color="#EE7600",
                                      corner_radius=0)
PauseButton.place(relx=0.1, rely=0.15, relwidth=0.07, relheight=0.7)
slider = customtkinter.CTkSlider(master=VideoBar, width=600 ,fg_color="#EE7600",
                                 button_color="#8B4000" ,button_hover_color="#8B4000")
slider.place(relx=0.2, rely=0.2, relheight=0.7, relwidth=0.65)
slider.set(0)
timeload = tk.Label(VideoBar, text="0:00 / 0:00", bg='#212325', foreground="white", font=("Roboto Medium", -14))
timeload.place(relx=0.85, rely=0.05, relwidth=0.15, relheight=0.9)


# Defining Video class.
class VideoPlay():

    Not_Running = 0 # Used to check if the same video is running.
    LastPercent = 0
    Continue = 1 # Used to check the Pause/Continue functions.
    file_name=""

    def source(self):

        if self.Continue == 0:
            # The video was pasued.
            self.Continue = 1
            self.show_frame()

        elif self.Not_Running == 0:
            # There is no video or the vide is done.
            self.importfile()
            self.cap = cv2.VideoCapture(self.file_name)
            self.tframes = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.start = 0
            self.Continue = 1
            self.show_frame()

    def show_frame(self):
        # Displaying the video
        self.Not_Running = 1
        self.start = self.start + 1

        # Calculating the percent of the frames spent.
        d = int((1000 / self.fps)) - 7
        t = time.time()
        percent = (self.start / self.tframes)

        _, frame = self.cap.read()

        tframe.update()

        try:
            x = frame.shape[0]  # height
            y = frame.shape[1]  # width
            frameWidth = VFrame.winfo_width()
            if y > x:
                framewidth = ((frameWidth - 10) * (frame.shape[0])) / (frame.shape[1])
                frame = cv2.resize(frame, ((frameWidth - 10), int(framewidth)))

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            VFrame.imgtk = imgtk
            VFrame.configure(image=imgtk)
            tframe.update()

            fps = (time.time() - t) + d / 1000
            fps = round(1 / fps)
            fps = str(fps)

            # Displaying the fps counter.
            FilefpsD["text"] = "fps: " + fps

            self.LastPercent = percent
            slider.set(self.LastPercent)
            time_spent = percent * (self.tframes / self.fps)

            # Displaying the time counter.
            if round(time_spent) < 10:

                if round(self.tframes / self.fps) > 10:
                    timeload["text"] = "{}:{}{} / {}:{} ".format(0, 0, round(time_spent), 0, round(self.tframes / self.fps))
                else:
                    timeload["text"] = "{}:{}{} / {}:{}{} ".format(0, 0, round(time_spent), 0, 0,
                                                                   round(self.tframes / self.fps))

            else:
                timeload["text"] = "{}:{} / {}:{}".format(0, round(time_spent), 0, round(self.tframes / self.fps))

            # Check if the video was paused or not.
            if self.Continue == 1:
                try:
                    VFrame.after(d, self.show_frame)
                except Exception:
                    # The video is done.
                    self.Not_Running = 0

        except Exception:
        # The video is done.
          self.Not_Running = 0
          self.Continue = 1


    def freeze(self):
        # Pause the video.
        self.Continue = 0


    def importfile(self):
        # Add video file function.
        self.file_name = tk.filedialog.askopenfilename(initialdir="{}".format(self.file_name),
                                                 title="Select a File",
                                                 filetypes=((".mp4", "*.mp4*"), ("all files", "*.*")))


VideoPlay=VideoPlay()
tframe.mainloop()