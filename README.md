# Trình chỉnh sửa Video Tkinter

Ứng dụng này là một trình chỉnh sửa video đơn giản được xây dựng bằng Python và thư viện Tkinter. Nó cho phép bạn thực hiện các thao tác cơ bản như chọn video, cắt video, trộn video, chia video và xóa video đang phát.

## Yêu cầu hệ thống

- Python 3.x
- Tkinter (thường được cài đặt sẵn với Python)
- moviepy
- tkvideo

## Cài đặt

### Ubuntu

1.  **Cài đặt Python 3 và Tkinter:**

    ```bash
    sudo apt update
    sudo apt install python3 python3-tk
    ```

2.  **Cài đặt các gói Python cần thiết:**

    ```bash
    pip install moviepy tkvideo
    ```

### macOS

1.  **Cài đặt Python 3 (nếu chưa có):**

    Bạn có thể cài đặt Python 3 bằng Homebrew:

    ```bash
    /bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"
    brew install python3
    ```

2.  **Cài đặt các gói Python cần thiết:**

    ```bash
    pip3 install moviepy tkvideo
    ```

    - **Lưu ý về Tkinter trên macOS:** Tkinter thường được cài đặt sẵn, nhưng nếu bạn gặp vấn đề, hãy đảm bảo Python của bạn được cài đặt đúng cách (ví dụ, thông qua Homebrew).

### Windows

1.  **Cài đặt Python 3:**

    - Tải trình cài đặt Python 3 từ trang web chính thức của Python ([https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)).
    - Khi cài đặt, hãy đảm bảo chọn tùy chọn "Add Python 3.x to PATH".

2.  **Cài đặt các gói Python cần thiết:**

    - Mở Command Prompt hoặc PowerShell.
    - Chạy lệnh:

      ```bash
      pip install moviepy tkvideo
      ```

## Chạy chương trình

1.  Mở terminal hoặc Command Prompt.
2.  Di chuyển đến thư mục chứa file Python.
3.  Chạy lệnh:

    ```bash
    python app.py
    ```

## Hướng dẫn sử dụng

1.  **Chọn Video:** Nhấn nút "Chọn Video" để chọn một file video.
2.  **Cắt Video:** Nhấn nút "Cắt Video" để cắt video theo thời gian chỉ định.
3.  **Trộn Video:** Nhấn nút "Trộn Video" để trộn các đoạn video.
4.  **Chia Video:** Nhấn nút "Chia Video" để chia video thành nhiều đoạn nhỏ.
5.  **Clear:** Nhấn nút "Clear" để xóa video đang phát và reset ứng dụng.

## Lưu ý

- Đảm bảo bạn đã cài đặt `ffmpeg` trên hệ thống của mình để `moviepy` hoạt động.
  - **Ubuntu:** `sudo apt install ffmpeg`
  - **macOS:** `brew install ffmpeg` (nếu dùng Homebrew)
  - **Windows:** Tải từ trang web của ffmpeg và thêm vào PATH.
- Ứng dụng này có thể không phù hợp cho các tác vụ chỉnh sửa video chuyên nghiệp.

## Đóng góp

Mọi đóng góp đều được hoan nghênh!

## Giấy phép

[]
