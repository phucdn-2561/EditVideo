import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from moviepy.editor import *
from tkvideo import tkvideo

class VideoEditor:
    def __init__(self, master):
        self.master = master
        master.title("Trình chỉnh sửa Video")

        # Các thành phần giao diện
        self.load_button = tk.Button(master, text="Chọn Video", command=self.load_video)
        self.load_button.pack()

        self.trim_button = tk.Button(master, text="Cắt Video", command=self.trim_video)
        self.trim_button.pack()

        self.output_button = tk.Button(master, text="Xuất Video", command=self.output_video)
        self.output_button.pack()

        self.video_label = tk.Label(master)
        self.video_label.pack()

        self.video_path = None
        self.video_player = None

    def load_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if self.video_path:
            messagebox.showinfo("Thông báo", "Đã tải video thành công!")
            self.play_video()

    def play_video(self):
      if self.video_player:
          self.video_player.stop()
      self.video_player = tkvideo(self.video_path, self.video_label, loop = 1, size = (400,300))
      self.video_player.play()

    def trim_video(self):
        if not self.video_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn video trước!")
            return

        start_time = simpledialog.askstring("Nhập thời gian", "Thời gian bắt đầu (giây):")
        end_time = simpledialog.askstring("Nhập thời gian", "Thời gian kết thúc (giây):")

        if start_time and end_time:
            try:
                start_time = float(start_time)
                end_time = float(end_time)
                video = VideoFileClip(self.video_path)
                trimmed_video = video.subclip(start_time, end_time)
                self.trimmed_video = trimmed_video
                messagebox.showinfo("Thông báo", "Đã cắt video thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi cắt video: {e}")

    def output_video(self):
        if hasattr(self, "trimmed_video"):
            output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 file", "*.mp4")])
            if output_path:
                try:
                    self.trimmed_video.write_videofile(output_path, codec="libx264")
                    messagebox.showinfo("Thông báo", "Đã xuất video thành công!")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Lỗi xuất video: {e}")
        else:
            messagebox.showerror("Lỗi", "Chưa cắt video!")

root = tk.Tk()
app = VideoEditor(root)
root.mainloop()