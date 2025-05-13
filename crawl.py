import requests
from bs4 import BeautifulSoup
import time
import re
import os

def crawl_chapter_text(url):
    """Crawls text content, handling potential issues."""
    try:
        response = requests.get(url, timeout=10)  # Add timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        chapter_div = soup.find('div', id='chapter-c', class_='chapter-c', itemprop='articleBody')
        if chapter_div:
            text_elements = chapter_div.find_all(['p', 'br'])
            chapter_text = []
            for element in text_elements:
                if element.name == 'p':
                    text = element.get_text(separator='\n', strip=True)
                    if text:
                        chapter_text.append(text)
                elif element.name == 'br':
                    chapter_text.append('\n')
            return '\n'.join(chapter_text).strip()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi tải trang {url}: {e}")
        return None
    except Exception as e:
        print(f"Lỗi xử lý trang {url}: {e}")
        return None

def crawl_chapter_text_v2(url):
    """Crawls text content, handling potential issues."""
    try:
        response = requests.get(url, timeout=10)  # Add timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        chapter_div = soup.find('div', id='chapter-c', class_='chapter-c', itemprop='articleBody')
        if chapter_div:
            content_parts = chapter_div.contents
            chapter_text = []
            for part in content_parts:
                if part.name == 'br':
                    chapter_text.append('\n')
                elif part.name == 'div' and 'ads-' not in part.get('class', []):
                    text = part.get_text(separator='\n', strip=True)
                    if text:
                        chapter_text.append(text)
                elif isinstance(part, str) and part.strip():
                    chapter_text.append(part.strip())
            cleaned_text = [line for line in '\n'.join(chapter_text).splitlines() if line.strip()]
            return '\n'.join(cleaned_text)
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi tải trang {url}: {e}")
        return None
    except Exception as e:
        print(f"Lỗi xử lý trang {url}: {e}")
        return None


def generate_chapter_urls(base_url, start_chapter, end_chapter):
    """Generates chapter URLs."""
    urls = []
    parts = base_url.split('/')
    base = '/'.join(parts[:-1]) + '/chuong-'
    for i in range(start_chapter, end_chapter + 1):
        urls.append(f"{base}{i}/")
    return urls

def split_text_to_chunks(text, max_length=6500):
    """Splits text into chunks, ending with a sentence."""
    chunks = []
    current_chunk = ""
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s+', text)
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + " "
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

def save_chapter_to_txt(folder_name, chapter_number, text):
    """Saves chapter text to chunked files."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    chunks = split_text_to_chunks(text)
    for i, chunk in enumerate(chunks):
        filename = os.path.join(folder_name, f"chuong_{chapter_number}_chunk_{i+1}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(chunk)
    print(f"Đã lưu chương {chapter_number} vào {folder_name}")

def create_error_folder():
    """Creates a folder to store information about failed crawls."""
    error_folder = "Not_Crawled"
    if not os.path.exists(error_folder):
        os.makedirs(error_folder)
    return error_folder

def create_error_file(folder_path, errors):
    """Creates a text file to log chapters that failed to crawl."""
    filename = os.path.join(folder_path, "chapters_not_crawled.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Các chương không thể crawl:\n")
        for chapter, error_message in errors.items():
            f.write(f"Chương {chapter}: {error_message}\n")

def create_tap_summary_file(folder_name, tap_chapters_data):
    """Creates a summary file for all chapters in a tap."""
    summary_filename = os.path.join(folder_name, "tong_hop.txt")
    with open(summary_filename, 'w', encoding='utf-8') as f:
        for chapter_number, text in sorted(tap_chapters_data.items()):
            f.write(text)
            f.write("\n\n")
    print(f"Đã tạo file tổng hợp cho {folder_name}")

if __name__ == "__main__":
    base_url = input("Nhập URL gốc của truyện (ví dụ: https://truyenfull.vision/ten-truyen/): ")
    start_chapter = int(input("Nhập chương bắt đầu: "))
    end_chapter = int(input("Nhập chương kết thúc: "))
    chapters_per_tap = int(input("Nhập số chương mỗi tập: "))

    chapter_urls = generate_chapter_urls(base_url, start_chapter, end_chapter)
    errors = {}  # Store chapters that failed
    all_data = {}

    for i, url in enumerate(chapter_urls):
        chapter_number = start_chapter + i
        print(f"Đang crawl chương {chapter_number}: {url}")
        chapter_text = crawl_chapter_text(url)
        if not chapter_text:
            chapter_text = crawl_chapter_text_v2(url) # Fallback
            if not chapter_text:
                errors[chapter_number] = f"Không thể crawl chương {chapter_number} từ {url}"
                continue

        all_data[chapter_number] = chapter_text
        time.sleep(1)

    # Process and save data into taps
    taps_data = {}
    for chapter_number in range(start_chapter, end_chapter + 1):
        if chapter_number in all_data:
            tap_number = (chapter_number - start_chapter) // chapters_per_tap + 1
            folder_name = f"Esp_{tap_number}"
            save_chapter_to_txt(folder_name, chapter_number, all_data[chapter_number])
            if tap_number not in taps_data:
                taps_data[tap_number] = {}
            taps_data[tap_number][chapter_number] = all_data[chapter_number]

    # Create summary file for each tap
    for tap_number, tap_chapters in taps_data.items():
        folder_name = f"Esp_{tap_number}"
        create_tap_summary_file(folder_name, tap_chapters)

    # Print Tap information
    print("\nCác chương đã được crawl và lưu theo tập:")
    for tap, chapters_data in taps_data.items():
        print(f"Tập {tap}: Các chương {sorted(chapters_data.keys())}")

    if errors:
        error_folder = create_error_folder()
        create_error_file(error_folder, errors)
        print(f"\nCác chương không thể crawl đã được lưu thông tin vào thư mục: {error_folder}")
    else:
        print("\nKhông có chương nào không thể crawl.")

    print("Hoàn tất quá trình.")
