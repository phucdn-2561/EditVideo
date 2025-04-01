import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from moviepy.editor import *
from tkvideo import tkvideo
import random
import os  # Để tạo thư mục

# Định nghĩa các hằng số cho định dạng video
VIDEO_FORMATS = [
    ("MP4 files", "*.mp4"),
    ("AVI files", "*.avi"),
    ("MOV files", "*.mov"),
    ("All video files", "*.mp4 *.avi *.mov")
]

class VideoEditor(tk.Frame):  # Kế thừa từ tk.Frame
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Trình chỉnh sửa Video")
        master.geometry("500x600")  # Đặt kích thước cửa sổ
        self.pack(fill=tk.BOTH, expand=True)  # Mở rộng Frame để lấp đầy cửa sổ

        self.create_widgets()

        self.video_path = None
        self.video_player = None

    def create_widgets(self):
        # Các thành phần giao diện
        self.load_button = tk.Button(self, text="Chọn Video", command=self.load_video, width=20, pady=5)
        self.load_button.pack(pady=10)  # Thêm khoảng cách theo chiều dọc

        self.trim_button = tk.Button(self, text="Cắt Video", command=self.trim_video, width=20, pady=5)
        self.trim_button.pack(pady=10)

        self.mix_button = tk.Button(self, text="Trộn Video", command=self.mix_video, width=20, pady=5)
        self.mix_button.pack(pady=10)

        self.split_button = tk.Button(self, text="Chia Video", command=self.split_video, width=20, pady=5)
        self.split_button.pack(pady=10)

        self.clear_button = tk.Button(self, text="Clear", command=self.clear_all, width=20, pady=5)

        self.create_video_label()  # Tạo video_label ban đầu

        # Ẩn nút Clear ban đầu
        self.clear_button.pack_forget()

    def create_video_label(self):
        # Tạo mới video_label
        self.video_label = tk.Label(self)
        self.video_label.pack(pady=10)  # Khoảng cách cho label

    def load_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=VIDEO_FORMATS)
        if self.video_path:
            messagebox.showinfo("Thông báo", "Đã tải video thành công!")
            self.play_video()  # Gọi play_video ngay sau khi tải
            # Hiển thị nút Clear sau khi tải video thành công
            self.clear_button.pack(pady=10)

    def play_video(self):
        # Kiểm tra xem có video player cũ không và dừng nó (gián tiếp)
        if self.video_player:
            self.video_player = None  # Đặt thành None để "dừng" phát video
            self.video_label.destroy() # Destroy the old video_label
            self.create_video_label() # Create a new video_label

        # Tạo video player mới và phát
        try:
            self.video_player = tkvideo(self.video_path, self.video_label, loop=1, size=(400, 300))
            self.video_player.play()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi phát video: {e}")
            self.video_path = None  # Reset đường dẫn nếu có lỗi
            self.video_player = None

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

                output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 file", "*.mp4")])
                if output_path:
                    try:
                        trimmed_video.write_videofile(output_path, codec="libx264")
                        messagebox.showinfo("Thông báo", "Đã cắt và xuất video thành công!")
                    except Exception as e:
                        messagebox.showerror("Lỗi", f"Lỗi xuất video: {e}")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi cắt video: {e}")

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

    def clear_all(self):
        # Dừng video đang phát (gián tiếp)
        self.video_player = None
        self.video_label.destroy() # Destroy the old video_label
        self.create_video_label() # Create a new video_label

        # Xóa đường dẫn video
        self.video_path = None

        # Ẩn nút Clear
        self.clear_button.pack_forget()

        # Hiển thị thông báo
        messagebox.showinfo("Thông báo", "Đã reset tất cả!")

root = tk.Tk()
app = VideoEditor(root)
root.mainloop()