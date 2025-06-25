import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

class TextFileChunker(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Chia nhỏ file TXT có sẵn từ thư mục con")
        master.geometry("650x450") # Increased height to accommodate new widgets
        self.pack(fill=tk.BOTH, expand=True)

        self.input_parent_dir = None # This will now be the parent directory
        self.output_base_dir = None # This will be the base output directory
        self.create_widgets()

    def create_widgets(self):
        # Frame for input parent directory selection
        input_frame = tk.LabelFrame(self, text="Thư mục CHA chứa các thư mục con có file .txt", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        self.input_dir_label = tk.Label(input_frame, text="Chưa chọn thư mục nào", wraplength=450, justify=tk.LEFT)
        self.input_dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.select_input_dir_button = tk.Button(input_frame, text="Chọn thư mục cha", command=self.choose_input_parent_dir)
        self.select_input_dir_button.pack(side=tk.RIGHT, padx=5)

        # Frame for output base directory selection
        output_frame = tk.LabelFrame(self, text="Thư mục GỐC để lưu các thư mục con đã chia nhỏ", padx=10, pady=10)
        output_frame.pack(pady=10, padx=10, fill=tk.X)

        self.output_dir_label = tk.Label(output_frame, text="Chưa chọn thư mục nào", wraplength=450, justify=tk.LEFT)
        self.output_dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.select_output_dir_button = tk.Button(output_frame, text="Chọn thư mục gốc xuất file", command=self.choose_output_base_dir)
        self.select_output_dir_button.pack(side=tk.RIGHT, padx=5)

        # Frame for max chunk length input
        length_frame = tk.LabelFrame(self, text="Cài đặt chia nhỏ", padx=10, pady=10)
        length_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(length_frame, text="Số ký tự tối đa cho mỗi phần:").pack(side=tk.LEFT, padx=5)
        self.max_chars_entry = tk.Entry(length_frame, width=10)
        self.max_chars_entry.insert(0, "6500") # Default value
        self.max_chars_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(length_frame, text="(Để câu hoàn chỉnh)").pack(side=tk.LEFT, padx=5)

        # Process button
        self.process_button = tk.Button(self, text="Bắt đầu chia nhỏ file", command=self.process_files, pady=10, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.process_button.pack(pady=20, padx=10, fill=tk.X)

        # Status label
        self.status_label = tk.Label(self, text="", fg="blue", font=("Arial", 10))
        self.status_label.pack(pady=10)

    def choose_input_parent_dir(self):
        """Cho phép người dùng chọn thư mục cha chứa các thư mục con có file .txt."""
        self.input_parent_dir = filedialog.askdirectory(title="Chọn thư mục cha chứa các thư mục con có file .txt")
        if self.input_parent_dir:
            self.input_dir_label.config(text=self.input_parent_dir)
            self.status_label.config(text=f"Đã chọn thư mục cha đầu vào: {self.input_parent_dir}")
        else:
            self.input_dir_label.config(text="Chưa chọn thư mục nào")
            self.status_label.config(text="Chưa chọn thư mục cha đầu vào.")

    def choose_output_base_dir(self):
        """Cho phép người dùng chọn thư mục gốc để lưu kết quả."""
        self.output_base_dir = filedialog.askdirectory(title="Chọn thư mục gốc để lưu các thư mục đã chia nhỏ")
        if self.output_base_dir:
            self.output_dir_label.config(text=self.output_base_dir)
            self.status_label.config(text=f"Đã chọn thư mục gốc xuất file: {self.output_base_dir}")
        else:
            self.output_dir_label.config(text="Chưa chọn thư mục nào")
            self.status_label.config(text="Chưa chọn thư mục gốc xuất file.")

    def split_text_to_chunks(self, text, max_length):
        """
        Splits text into chunks of maximum length, ending with a complete sentence.
        Each chunk will be less than or equal to max_length.
        """
        chunks = []
        current_chunk = ""
        # Split by common sentence endings (., ?, !) followed by whitespace.
        # The regex uses positive lookbehind to include the punctuation in the sentence.
        # It also handles abbreviations (e.g., Mr., U.S.A.) by using negative lookbehind.
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s+', text)

        for sentence in sentences:
            # Check if adding the next sentence (plus a space) exceeds max_length
            # If current_chunk is empty, we don't need to add a space before the first sentence
            if not current_chunk or (len(current_chunk) + len(sentence) + 1 <= max_length):
                current_chunk += sentence + " "
            else:
                # If adding the next sentence would exceed max_length,
                # save the current_chunk and start a new one.
                if current_chunk.strip(): # Ensure current_chunk is not just whitespace
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " " # Start the new chunk with the current sentence

        # Add the last chunk if it contains any content
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def process_files(self):
        """
        Xử lý các file .txt trong các thư mục con của thư mục cha đã chọn,
        chia nhỏ chúng và lưu vào thư mục xuất tương ứng.
        """
        if not self.input_parent_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục CHA chứa các file .txt cần chia nhỏ.")
            return

        if not self.output_base_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục GỐC để lưu các thư mục đã chia nhỏ.")
            return

        try:
            max_chars = int(self.max_chars_entry.get())
            if max_chars <= 0:
                messagebox.showerror("Lỗi", "Số ký tự tối đa phải là một số nguyên dương.")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Đầu vào không hợp lệ. Vui lòng nhập một số nguyên cho số ký tự tối đa.")
            return

        self.status_label.config(text=f"Đang xử lý các thư mục con trong: {self.input_parent_dir}")
        processed_file_count = 0
        error_files_list = []
        processed_folders_count = 0

        # Create the base output directory if it doesn't exist
        os.makedirs(self.output_base_dir, exist_ok=True)

        # Iterate through items in the chosen parent directory
        for item_name in os.listdir(self.input_parent_dir):
            item_path = os.path.join(self.input_parent_dir, item_name)

            # Check if the item is a directory (a subdirectory containing .txt files)
            if os.path.isdir(item_path):
                processed_folders_count += 1
                current_input_subdir = item_path
                current_output_subdir = os.path.join(self.output_base_dir, item_name)

                # Create the corresponding output subdirectory
                os.makedirs(current_output_subdir, exist_ok=True)
                self.status_label.config(text=f"Đang xử lý thư mục con: '{item_name}'")
                self.update_idletasks() # Update GUI immediately

                # Now, iterate through files within this subdirectory
                for filename in os.listdir(current_input_subdir):
                    if filename.lower().endswith(".txt"):
                        file_path = os.path.join(current_input_subdir, filename)
                        file_base_name = os.path.splitext(filename)[0] # Get name without .txt extension

                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()

                            chunks = self.split_text_to_chunks(content, max_chars)

                            # Save each chunk to a new file in the dedicated output subfolder
                            for i, chunk in enumerate(chunks):
                                # Modified line: Add original file_base_name as prefix to chunk filename
                                chunk_filename = os.path.join(current_output_subdir, f"{file_base_name}_chunk_{i+1}.txt")
                                with open(chunk_filename, 'w', encoding='utf-8') as f_chunk:
                                    f_chunk.write(chunk)

                            processed_file_count += 1
                            self.status_label.config(text=f"Đã xử lý file: '{filename}' trong '{item_name}'")
                            self.update_idletasks() # Update GUI immediately
                        except Exception as e:
                            error_message = f"Lỗi khi xử lý file '{filename}' trong thư mục '{item_name}': {e}"
                            messagebox.showerror("Lỗi", error_message)
                            self.status_label.config(text=error_message)
                            error_files_list.append(f"{item_name}/{filename}")
            else:
                self.status_label.config(text=f"Bỏ qua '{item_name}' vì không phải là thư mục.")
                self.update_idletasks()

        if processed_file_count > 0 and not error_files_list:
            messagebox.showinfo("Thông báo", f"Hoàn tất xử lý. Đã chia nhỏ {processed_file_count} file từ {processed_folders_count} thư mục con thành công!")
            self.status_label.config(text="Hoàn tất xử lý các file .txt.")
        elif processed_file_count > 0 and error_files_list:
            messagebox.warning("Cảnh báo", f"Hoàn tất xử lý {processed_file_count} file. Có lỗi xảy ra với các file: {', '.join(error_files_list)}")
            self.status_label.config(text=f"Hoàn tất với lỗi. Xem chi tiết trong hộp thoại cảnh báo.")
        else:
            messagebox.showinfo("Thông báo", "Không có file .txt nào được xử lý thành công trong bất kỳ thư mục con nào.")
            self.status_label.config(text="Không có file .txt nào được xử lý thành công.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TextFileChunker(root)
    root.mainloop()

