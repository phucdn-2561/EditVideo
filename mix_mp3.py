import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import *
import os

class MP3Joiner(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Ghép File MP3 tu thu muc cha chua cac thu muc con")
        master.geometry("600x400")
        self.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

        self.parent_audio_dir = None
        self.output_dir = None

    def create_widgets(self):
        self.select_parent_dir_button = tk.Button(self, text="Chọn thư mục cha chứa audio", command=self.choose_parent_audio_dir, width=30, pady=10)
        self.select_parent_dir_button.pack(pady=20)

        self.output_dir_label = tk.Label(self, text="Thư mục lưu file MP3:")
        self.output_dir_label.pack(pady=5)
        self.output_dir_entry = tk.Entry(self, width=50)
        self.output_dir_entry.pack(pady=5)
        self.select_output_dir_button = tk.Button(self, text="Chọn thư mục lưu file MP3", command=self.choose_output_dir, width=30, pady=10)
        self.select_output_dir_button.pack(pady=20)

        self.process_button = tk.Button(self, text="Bắt đầu ghép file MP3", command=self.process_audio_subdirs, width=30, pady=10)
        self.process_button.pack(pady=20)

        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)

    def choose_parent_audio_dir(self):
        self.parent_audio_dir = filedialog.askdirectory(title="Chọn thư mục cha chứa các thư mục audio")
        if self.parent_audio_dir:
            self.status_label.config(text=f"Đã chọn thư mục cha audio: {self.parent_audio_dir}")

    def choose_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Chọn thư mục để lưu file MP3 đã ghép")
        if self.output_dir:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, self.output_dir)
            self.status_label.config(text=f"Đã chọn thư mục lưu file MP3: {self.output_dir}")

    def process_audio_subdirs(self):
        if not self.parent_audio_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục cha chứa audio.")
            return
        if not self.output_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục để lưu file MP3.")
            return

        subdirectories = [d for d in os.listdir(self.parent_audio_dir) if os.path.isdir(os.path.join(self.parent_audio_dir, d))]

        if not subdirectories:
            messagebox.showinfo("Thông báo", "Không tìm thấy thư mục con nào.")
            return

        for subdir_name in subdirectories:
            subdir_path = os.path.join(self.parent_audio_dir, subdir_name)
            audio_files = sorted([f for f in os.listdir(subdir_path) if f.endswith(('.mp3'))])

            if not audio_files:
                self.status_label.config(text=f"Không tìm thấy file .mp3 nào trong thư mục: {subdir_name}")
                continue

            audio_paths = [os.path.join(subdir_path, af) for af in audio_files]
            output_filename = f"{subdir_name}.mp3"
            output_path = os.path.join(self.output_dir, output_filename)

            try:
                audio_clips = [AudioFileClip(ap) for ap in audio_paths]
                final_audio_clip = concatenate_audioclips(audio_clips)
                final_audio_clip.write_audiofile(output_path)
                final_audio_clip.close()
                for clip in audio_clips:
                    clip.close()
                self.status_label.config(text=f"Đã ghép {len(audio_files)} audio từ thư mục '{subdir_name}' thành '{output_filename}'")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi ghép audio từ thư mục '{subdir_name}': {e}")

        messagebox.showinfo("Thông báo", "Hoàn thành ghép file MP3 từ các thư mục con!")

root = tk.Tk()
app = MP3Joiner(root)
root.mainloop()