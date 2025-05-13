import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import *
import random
import os

class VideoAudioMixer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Video Audio Mixer")
        master.geometry("600x400")
        self.pack(fill=tk.BOTH, expand=True)

        self.video_dir = None
        self.audio_dir = None
        self.create_widgets()

    def create_widgets(self):
        self.video_label = tk.Label(self, text="Thư mục Video:")
        self.video_label.pack(pady=5)
        self.video_entry = tk.Entry(self, width=50)
        self.video_entry.pack(pady=5)
        self.video_button = tk.Button(self, text="Chọn thư mục Video", command=self.choose_video_dir)
        self.video_button.pack(pady=5)

        self.audio_label = tk.Label(self, text="Thư mục Audio:")
        self.audio_label.pack(pady=5)
        self.audio_entry = tk.Entry(self, width=50)
        self.audio_entry.pack(pady=5)
        self.audio_button = tk.Button(self, text="Chọn thư mục Audio", command=self.choose_audio_dir)
        self.audio_button.pack(pady=5)

        self.mix_button = tk.Button(self, text="Trộn Audio với Video", command=self.mix_audio_with_video)
        self.mix_button.pack(pady=10)

        self.output_label = tk.Label(self, text="")
        self.output_label.pack(pady=10)

    def choose_video_dir(self):
        self.video_dir = filedialog.askdirectory(title="Chọn thư mục chứa video")
        if self.video_dir:
            self.video_entry.delete(0, tk.END)
            self.video_entry.insert(0, self.video_dir)

    def choose_audio_dir(self):
        self.audio_dir = filedialog.askdirectory(title="Chọn thư mục chứa audio")
        if self.audio_dir:
            self.audio_entry.delete(0, tk.END)
            self.audio_entry.insert(0, self.audio_dir)

    def mix_audio_with_video(self):
        if not self.video_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục video.")
            return
        if not self.audio_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục audio.")
            return

        video_files = [f for f in os.listdir(self.video_dir) if f.endswith(('.mp4', '.avi', '.mov'))]
        audio_files = [f for f in os.listdir(self.audio_dir) if f.endswith(('.mp3', '.wav'))]

        if not video_files:
            messagebox.showerror("Lỗi", "Không tìm thấy file video nào trong thư mục đã chọn.")
            return
        if not audio_files:
            messagebox.showerror("Lỗi", "Không tìm thấy file audio nào trong thư mục đã chọn.")
            return

        num_videos = len(video_files)
        num_audios = len(audio_files)

        output_dir = filedialog.askdirectory(title="Chọn thư mục để lưu video đã trộn audio")
        if not output_dir:
            return

        for i, audio_file in enumerate(audio_files):
            video_file = random.choice(video_files)
            video_path = os.path.join(self.video_dir, video_file)
            audio_path = os.path.join(self.audio_dir, audio_file)

            audio_base_name = os.path.splitext(audio_file)[0]
            video_base_name, video_ext = os.path.splitext(video_file)
            output_path = os.path.join(output_dir, f"{audio_base_name}__{video_base_name}{video_ext}")

            try:
                video_clip = VideoFileClip(video_path)
                audio_clip = AudioFileClip(audio_path)

                # Use audio duration for the final clip
                final_clip_duration = audio_clip.duration

                # Resize video to match audio duration
                if video_clip.duration > final_clip_duration:
                    video_clip = video_clip.subclip(0, final_clip_duration)
                elif video_clip.duration < final_clip_duration:
                    # Extend video with loop
                    video_clip = video_clip.loop(duration=final_clip_duration)

                final_clip = video_clip.set_audio(audio_clip)
                final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

                video_clip.close()
                audio_clip.close()
                self.output_label.config(text=f"Đã trộn audio {i+1}/{num_audios} với video {video_file}")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi trộn {audio_file} với {video_file}: {e}")

        messagebox.showinfo("Thông báo", "Hoàn thành trộn audio với video!")

root = tk.Tk()
app = VideoAudioMixer(root)
root.mainloop()