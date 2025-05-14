import tkinter as tk
from tkinter import filedialog, messagebox
import os

class TextFileJoiner(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Ghép File Văn Bản (.txt)")
        master.geometry("600x400")  # Set an appropriate window size
        self.pack(fill=tk.BOTH, expand=True)

        self.parent_dir = None
        self.output_dir = None
        self.create_widgets()

    def create_widgets(self):
        self.select_parent_dir_button = tk.Button(self, text="Chọn thư mục cha chứa các thư mục văn bản", command=self.choose_parent_dir, width=40, pady=10)
        self.select_parent_dir_button.pack(pady=20)

        self.output_dir_label = tk.Label(self, text="Thư mục lưu file văn bản đã ghép:")
        self.output_dir_label.pack(pady=5)
        self.output_dir_entry = tk.Entry(self, width=50)
        self.output_dir_entry.pack(pady=5)
        self.select_output_dir_button = tk.Button(self, text="Chọn thư mục lưu file văn bản", command=self.choose_output_dir, width=40, pady=10)
        self.select_output_dir_button.pack(pady=20)

        self.process_button = tk.Button(self, text="Bắt đầu ghép file văn bản", command=self.process_text_subdirs, width=40, pady=10)
        self.process_button.pack(pady=20)

        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=10)

    def choose_parent_dir(self):
        self.parent_dir = filedialog.askdirectory(title="Chọn thư mục cha chứa các thư mục văn bản")
        if self.parent_dir:
            self.status_label.config(text=f"Đã chọn thư mục cha: {self.parent_dir}")

    def choose_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Chọn thư mục để lưu file văn bản đã ghép")
        if self.output_dir:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, self.output_dir)
            self.status_label.config(text=f"Đã chọn thư mục lưu file văn bản: {self.output_dir}")

    def process_text_subdirs(self):
        if not self.parent_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục cha chứa các thư mục văn bản.")
            return
        if not self.output_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục để lưu file văn bản đã ghép.")
            return

        subdirectories = [d for d in os.listdir(self.parent_dir) if os.path.isdir(os.path.join(self.parent_dir, d))]

        if not subdirectories:
            messagebox.showinfo("Thông báo", "Không tìm thấy thư mục con nào.")
            return

        for subdir_name in subdirectories:
            subdir_path = os.path.join(self.parent_dir, subdir_name)
            text_files = sorted([f for f in os.listdir(subdir_path) if f.endswith(('.txt'))])

            if not text_files:
                self.status_label.config(text=f"Không tìm thấy file .txt nào trong thư mục: {subdir_name}")
                continue

            output_filename = f"{subdir_name}.txt"
            output_path = os.path.join(self.output_dir, output_filename)
            combined_text = ""

            try:
                for text_file in text_files:
                    text_file_path = os.path.join(subdir_path, text_file)
                    with open(text_file_path, 'r', encoding='utf-8') as f:
                        combined_text += f.read() + "\n\n"  # Add content and separator

                with open(output_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(combined_text)
                self.status_label.config(text=f"Đã ghép {len(text_files)} file văn bản từ thư mục '{subdir_name}' thành '{output_filename}'")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi ghép file văn bản từ thư mục '{subdir_name}': {e}")

        messagebox.showinfo("Thông báo", "Hoàn thành ghép file văn bản từ các thư mục con!")

root = tk.Tk()
app = TextFileJoiner(root)
root.mainloop()