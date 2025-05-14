import requests
from bs4 import BeautifulSoup
import time
import os

def crawl_chapter_text(url):
    """
    Cào nội dung chương, xử lý các vấn đề tiềm ẩn và loại bỏ trùng lặp.
    """
    try:
        response = requests.get(url, timeout=10)
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
            full_text = '\n'.join(chapter_text).strip()
            # Loại bỏ các đoạn văn bản trùng lặp
            unique_text = []
            seen_sentences = set()
            for sentence in full_text.splitlines():
                sentence = sentence.strip()
                if sentence and sentence not in seen_sentences:
                    unique_text.append(sentence)
                    seen_sentences.add(sentence)
            return '\n'.join(unique_text)
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi tải trang {url}: {e}")
        return None
    except Exception as e:
        print(f"Lỗi xử lý trang {url}: {e}")
        return None


def crawl_chapter_text_br(url):
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
             # Loại bỏ các đoạn văn bản trùng lặp
            unique_text = []
            seen_sentences = set()
            for sentence in cleaned_text:
                sentence = sentence.strip()
                if sentence and sentence not in seen_sentences:
                    unique_text.append(sentence)
                    seen_sentences.add(sentence)
            return '\n'.join(unique_text).strip()
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

def save_chapter_to_txt(folder_name, chapter_number, text):
    """Saves chapter text to a single file."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filename = os.path.join(folder_name, f"chuong_{chapter_number}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
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
    chapters_body = input("Nhập body (p hoặc br): ")

    chapter_urls = generate_chapter_urls(base_url, start_chapter, end_chapter)
    errors = {}
    all_data = {}

    for i, url in enumerate(chapter_urls):
        chapter_number = start_chapter + i
        print(f"Đang crawl chương {chapter_number}: {url}")
        if chapters_body == "br":
            chapter_text = crawl_chapter_text_br(url)
        else:
            chapter_text = crawl_chapter_text(url)

        if not chapter_text:
            errors[chapter_number] = f"Không thể crawl chương {chapter_number} từ {url}"
            continue

        all_data[chapter_number] = chapter_text
        time.sleep(1)

    taps_data = {}
    for chapter_number, text in all_data.items():
        tap_number = (chapter_number - start_chapter) // chapters_per_tap + 1
        folder_name = f"Esp_{tap_number}"
        save_chapter_to_txt(folder_name, chapter_number, text)
        if tap_number not in taps_data:
            taps_data[tap_number] = {}
        taps_data[tap_number][chapter_number] = all_data[chapter_number]

    for tap_number, tap_chapters in taps_data.items():
        folder_name = f"Esp_{tap_number}"
        create_tap_summary_file(folder_name, tap_chapters)

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
