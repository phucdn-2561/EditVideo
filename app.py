import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from moviepy.editor import *
from tkvideo import tkvideo
import random
import os  # Để tạo thư mục

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

        self.mix_button = tk.Button(master, text="Trộn Video", command=self.mix_video)
        self.mix_button.pack()

        self.split_button = tk.Button(master, text="Chia Video", command=self.split_video)
        self.split_button.pack()

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
        self.video_player = tkvideo(self.video_path, self.video_label, loop=1, size=(400, 300))
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

    def mix_video(self):
        if not self.video_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn video trước!")
            return

        segment_duration = simpledialog.askinteger("Nhập thời gian", "Độ dài đoạn video (giây):")
        if segment_duration is None or segment_duration <= 0:
            messagebox.showerror("Lỗi", "Độ dài đoạn video không hợp lệ.")
            return

        video = VideoFileClip(self.video_path)
        video_duration = video.duration

        segments = []
        for start_time in range(0, int(video_duration), segment_duration):
            end_time = min(start_time + segment_duration, video_duration)
            segments.append((start_time, end_time))  # Lưu trữ (start, end)

        # Tạo danh sách các chỉ số và xáo trộn chúng
        indices = list(range(len(segments)))
        random.shuffle(indices)

        # Xây dựng danh sách các đoạn video đã xáo trộn
        mixed_segments = []
        for i in indices:
            start, end = segments[i]
            mixed_segments.append(video.subclip(start, end))

        mixed_video = concatenate_videoclips(mixed_segments)

        output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 file", "*.mp4")])
        if output_path:
            try:
                mixed_video.write_videofile(output_path, codec="libx264")
                messagebox.showinfo("Thông báo", "Đã trộn video thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi trộn video: {e}")

    def split_video(self):
        if not self.video_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn video trước!")
            return

        segment_duration = simpledialog.askinteger("Nhập thời gian", "Độ dài mỗi đoạn (giây):")
        if segment_duration is None or segment_duration <= 0:
            messagebox.showerror("Lỗi", "Độ dài đoạn video không hợp lệ.")
            return

        video = VideoFileClip(self.video_path)
        video_duration = video.duration

        # Tạo thư mục để lưu các đoạn video
        output_dir = filedialog.askdirectory(title="Chọn thư mục để lưu các đoạn video")
        if not output_dir:
            return  # Người dùng hủy chọn thư mục

        base_filename = os.path.splitext(os.path.basename(self.video_path))[0]  # Lấy tên file gốc

        start_time = 0
        segment_number = 1
        while start_time < video_duration:
            end_time = min(start_time + segment_duration, video_duration)
            segment = video.subclip(start_time, end_time)

            output_path = os.path.join(output_dir, f"{base_filename}_segment_{segment_number}.mp4")
            try:
                segment.write_videofile(output_path, codec="libx264")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi xuất đoạn video: {e}")
                return

            start_time = end_time
            segment_number += 1

        messagebox.showinfo("Thông báo", "Đã chia video thành công!")

root = tk.Tk()
app = VideoEditor(root)
root.mainloop()