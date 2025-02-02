import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from urllib.parse import urljoin
from tkinter import filedialog
import threading
import time
from tkinter import ttk
import sv_ttk
from collections import deque 


SUPPORTED_FORMATS = [
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'ts', 'webm', 'mpg', 'mov',
    'zip', 'rar', 'pdf', 'm4v', 'mkv', 'mp3', 'mpeg', 'avi', 'jfif', 'wmv',
    '7z', 'tar', 'flv', 'm4a'
]

LANGUAGES = {
    'tr': {
        'title': 'Bunkr Downloader Pro',
        'subtitle': 'Hızlı ve Güvenli İndirme Aracı',
        'url_label': 'İndirme Linki',
        'folder_label': 'Ana Klasör (Albüm alt klasörü otomatik oluşturulacak)',
        'browse_button': 'Gözat',
        'download_button': 'İndirmeyi Başlat',
        'progress_label': 'İndirme Durumu',
        'stats_label': 'İndirme İstatistikleri',
        'ready_status': 'Hazır',
        'theme_button': '🌓 Tema Değiştir',
        'language_button': '🌍 Dil Değiştir',
        'error_url': 'Lütfen bir URL girin.',
        'error_folder': 'Lütfen ana klasör seçin.',
        'collecting_links': "'{title}' albümü için linkler toplanıyor...",
        'no_files': 'İndirilecek dosya bulunamadı.',
        'downloading_image': 'Resim indiriliyor ({current}/{total})',
        'checking_videos': 'Video boyutları kontrol ediliyor...',
        'downloading_video': 'Video indiriliyor ({current}/{total}) - Boyut: {size:.1f} MB',
        'download_complete': 'İndirme tamamlandı!',
        'downloading_file': 'İndiriliyor: {filename} ({downloaded:.1f}/{total:.1f} MB)',
        'download_success': 'Tamamlandı: {filename}',
        'download_error': 'Hata: {error}',
        'result_message': (
            'İndirme tamamlandı.\n'
            'Toplam Resim: {images}\n'
            'Toplam Video: {videos}\n'
            'Başarılı: {success}\n'
            'Başarısız: {failed}'
        ),
        'info_title': 'Bilgi',
        'error_title': 'Hata',
        'clipboard_enabled': 'Otomatik indirme aktif',
        'clipboard_disabled': 'Otomatik indirme devre dışı',
        'clipboard_toggle': 'Otomatik İndirme',
        'download_cancelled': 'İndirme iptal edildi',
        'cancel_button': 'İptal Et',
        'queue_status': '📥 Kuyrukta bekleyen indirme: {count}',
        'queue_empty': '📥 İndirme kuyruğu boş',
        'current_download': '🔄 Şu anki indirme:\n{current}\n\n📑 Kuyrukta bekleyen: {queue} dosya',
    },
    'en': {
        'title': 'Bunkr Downloader Pro',
        'subtitle': 'Fast and Secure Download Tool',
        'url_label': 'Download Link',
        'folder_label': 'Main Folder (Album subfolder will be created automatically)',
        'browse_button': 'Browse',
        'download_button': 'Start Download',
        'progress_label': 'Download Progress',
        'stats_label': 'Download Statistics',
        'ready_status': 'Ready',
        'theme_button': '🌓 Toggle Theme',
        'language_button': '🌍 Change Language',
        'error_url': 'Please enter a URL.',
        'error_folder': 'Please select a main folder.',
        'collecting_links': "Collecting links for '{title}'...",
        'no_files': 'No files found to download.',
        'downloading_image': 'Downloading image ({current}/{total})',
        'checking_videos': 'Checking video sizes...',
        'downloading_video': 'Downloading video ({current}/{total}) - Size: {size:.1f} MB',
        'download_complete': 'Download completed!',
        'downloading_file': 'Downloading: {filename} ({downloaded:.1f}/{total:.1f} MB)',
        'download_success': 'Completed: {filename}',
        'download_error': 'Error: {error}',
        'result_message': (
            'Download completed.\n'
            'Total Images: {images}\n'
            'Total Videos: {videos}\n'
            'Successful: {success}\n'
            'Failed: {failed}'
        ),
        'info_title': 'Information',
        'error_title': 'Error',
        'clipboard_enabled': 'Auto-download active',
        'clipboard_disabled': 'Auto-download disabled',
        'clipboard_toggle': 'Auto Download',
        'download_cancelled': 'Download cancelled',
        'cancel_button': 'Cancel',
        'queue_status': '📥 Downloads in queue: {count}',
        'queue_empty': '📥 Download queue is empty',
        'current_download': '🔄 Current download:\n{current}\n\n📑 Queued downloads: {queue} files',
    }
}

current_language = 'tr'

root = None
title_label = None
subtitle_label = None
url_frame = None
folder_frame = None
progress_frame = None
stats_frame = None
folder_button = None
download_button = None
theme_button = None
language_button = None
status_label = None
stats_text = None
last_clipboard = ""
clipboard_var = None  


cancel_download = False
cancel_button = None
clipboard_status = None
clipboard_toggle = None
download_queue = deque()  
is_downloading = False  

def toggle_language():
    global current_language
    current_language = 'en' if current_language == 'tr' else 'tr'
    update_gui_language()

def get_text(key, **kwargs):
    text = LANGUAGES[current_language].get(key, LANGUAGES['en'][key])
    return text.format(**kwargs) if kwargs else text

def update_theme_colors(stats_text):
    current_theme = sv_ttk.get_theme()
    if current_theme == "dark":
        stats_text.configure(
            bg='#2b2b2b',  
            fg='#e0e0e0'   
        )
    else:
        stats_text.configure(
            bg='#ffffff',  
            fg='#000000'   
        )

def toggle_theme(stats_text):
    sv_ttk.toggle_theme()
    update_theme_colors(stats_text)

def update_gui_language():
    global root, title_label, subtitle_label, url_frame, folder_frame
    global progress_frame, stats_frame, folder_button, download_button
    global theme_button, language_button, status_label, stats_text, cancel_button
    global clipboard_status, clipboard_toggle  
    
    root.title(get_text('title'))
    if title_label:
        title_label.configure(text=get_text('title'))
    if subtitle_label:
        subtitle_label.configure(text=get_text('subtitle'))
    
    if url_frame:
        url_frame.configure(text=get_text('url_label'))
    if folder_frame:
        folder_frame.configure(text=get_text('folder_label'))
    if progress_frame:
        progress_frame.configure(text=get_text('progress_label'))
    if stats_frame:
        stats_frame.configure(text=get_text('stats_label'))
    
    if folder_button:
        folder_button.configure(text=get_text('browse_button'))
    if download_button:
        download_button.configure(text=get_text('download_button'))
    if cancel_button: 
        cancel_button.configure(text=get_text('cancel_button'))
    if theme_button:
        theme_button.configure(text=get_text('theme_button'))
    if language_button:
        language_button.configure(text=get_text('language_button'))
    
    if status_label:
        status_label.configure(text=get_text('ready_status'))
    
    if stats_text:
        update_theme_colors(stats_text)
        current_text = stats_text.get('1.0', tk.END).strip()
        if current_text:  
            lines = current_text.split('\n')
            if len(lines) >= 5:
                try:
                    images = int(lines[1].split(':')[1].strip())
                    videos = int(lines[2].split(':')[1].strip())
                    success = int(lines[3].split(':')[1].strip())
                    failed = int(lines[4].split(':')[1].strip())
                    
                    update_stats(stats_text, get_text('result_message').format(
                        images=images,
                        videos=videos,
                        success=success,
                        failed=failed
                    ))
                except:
                    pass

    if clipboard_status:
        if clipboard_var and clipboard_var.get():
            clipboard_status.configure(
                text="📋 " + get_text('clipboard_enabled'),
                foreground='#00aa00'
            )
        else:
            clipboard_status.configure(
                text="📋 " + get_text('clipboard_disabled'),
                foreground='#aa0000'
            )
    
    if clipboard_toggle:
        clipboard_toggle.configure(text=get_text('clipboard_toggle'))

def download_with_progress(url, folder, progress_var=None, status_label=None):
    try:
        global cancel_download 
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://bunkr.cr/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive'
        }

        response = requests.get(url, headers=headers, stream=True)
        
        if response.status_code == 200:
            file_name = url.split('/')[-1].split('?')[0]
            file_path = os.path.join(folder, file_name)
            
            total_size = int(response.headers.get('content-length', 0))
            
            if progress_var and status_label:
                if total_size > 0:
                    status_label.config(text=get_text('downloading_file', filename=file_name, downloaded=0, total=total_size/1024/1024))
                else:
                    status_label.config(text=get_text('downloading_file', filename=file_name, downloaded=0, total=0))
                progress_var.set(0)
                
            block_size = 8192
            downloaded = 0
            
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=block_size):
                    if cancel_download:  
                        file.close()
                        os.remove(file_path)  
                        return False
                        
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_var and status_label and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_var.set(progress)
                            status_label.config(text=get_text('downloading_file', 
                                filename=file_name, 
                                downloaded=downloaded/1024/1024, 
                                total=total_size/1024/1024))
                            
            if status_label:
                status_label.config(text=get_text('download_success', filename=file_name))
            return True
        else:
            if status_label:
                status_label.config(text=get_text('download_error', error=response.status_code))
            return False
            
    except Exception as e:
        if status_label:
            status_label.config(text=get_text('download_error', error=str(e)))
        return False

def extract_album_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        is_single_file = '/f/' in url
        
        if is_single_file:
            media_element = soup.find(['img', 'video'], class_='max-h-full')
            if media_element:
                if media_element.name == 'video':
                    source = media_element.find('source')
                    src = source['src'] if source else media_element.get('src')
                else:
                    src = media_element.get('src')
                
                if src:
                    file_name = src.split('/')[-1].split('.')[0]
                    return file_name
        else:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.text.split('|')[0].strip()
                title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_'))
                return title
                
        return "Bunkr_Download"
    except:
        return "Bunkr_Download"

def extract_links(url):
    try:
        is_single_file = '/f/' in url
        
        if is_single_file:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            all_links = []
            
            og_url = soup.find('meta', property='og:url')
            if og_url and og_url.get('content'):
                media_url = og_url['content']
                extension = media_url.split('.')[-1].lower()
                if extension in SUPPORTED_FORMATS:
                    all_links.append(media_url)
                    return all_links
            
            media_element = soup.find(['img', 'video'], class_='max-h-full')
            if media_element:
                if media_element.name == 'video':
                    source = media_element.find('source')
                    src = source['src'] if source else media_element.get('src')
                else:
                    src = media_element.get('src')
                
                if src:
                    media_url = urljoin(url, src)
                    extension = media_url.split('.')[-1].lower()
                    if extension in SUPPORTED_FORMATS:
                        all_links.append(media_url)
                        return all_links
            
            return []
            
        else:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            all_links = []
            
            file_pages = []
            for item in soup.find_all('div', class_='theItem'):
                a_tag = item.find('a', href=True)
                if a_tag and '/f/' in a_tag['href']:
                    file_url = urljoin(url, a_tag['href'])
                    file_pages.append(file_url)
            
            for file_page in file_pages:
                try:
                    page_response = requests.get(file_page)
                    page_soup = BeautifulSoup(page_response.text, 'html.parser')
                    
                    og_url = page_soup.find('meta', property='og:url')
                    if og_url and og_url.get('content'):
                        media_url = og_url['content']
                        extension = media_url.split('.')[-1].lower()
                        if extension in SUPPORTED_FORMATS:
                            all_links.append(media_url)
                            continue
                    
                    media_element = page_soup.find(['img', 'video'], class_='max-h-full')
                    if media_element:
                        if media_element.name == 'video':
                            source = media_element.find('source')
                            src = source['src'] if source else media_element.get('src')
                        else:
                            src = media_element.get('src')
                        
                        if src:
                            media_url = urljoin(file_page, src)
                            extension = media_url.split('.')[-1].lower()
                            if extension in SUPPORTED_FORMATS:
                                all_links.append(media_url)
                
                except Exception as e:
                    print(f"Error processing file page {file_page}: {e}")
                    continue
            
            return list(set(all_links)) 
    
    except Exception as e:
        print(f"Error extracting links: {e}")
        return []

def get_file_size(url, headers):
    try:
        response = requests.head(url, headers=headers)
        if response.status_code == 200:
            return int(response.headers.get('content-length', 0))
        return 0
    except:
        return 0

def start_download_thread():
    download_thread = threading.Thread(target=start_download)
    download_thread.daemon = True
    download_thread.start()

def cancel_download_process():
    global cancel_download
    cancel_download = True
    status_label.config(text=get_text('download_cancelled'))
    download_button.config(state='normal')
    cancel_button.config(state='disabled')

def process_download_queue():
    global is_downloading
    
    if is_downloading or not download_queue:
        return
        
    is_downloading = True
    url = download_queue.popleft()  
    
    url_entry.delete(0, tk.END)
    url_entry.insert(0, url)
    
    current_text = stats_text.get('1.0', tk.END).strip()
    if current_text:
        update_stats(stats_text, current_text)
    
    start_download_thread()

def download_complete_callback():
    global is_downloading
    is_downloading = False
    
    if download_queue:
        root.after(1000, process_download_queue)  

def start_download():
    global cancel_download
    cancel_download = False
    
    url = url_entry.get()
    if not url:
        messagebox.showerror(get_text('error_title'), get_text('error_url'))
        return

    album_title = extract_album_title(url)
    base_folder = folder_entry.get()
    
    if not base_folder:
        messagebox.showerror(get_text('error_title'), get_text('error_folder'))
        return

    folder = os.path.join(base_folder, album_title)
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    download_button.config(state='disabled')
    cancel_button.config(state='normal')  
    progress_var.set(0)
    status_label.config(text=get_text('collecting_links', title=album_title))

    links = extract_links(url)
    if not links:
        status_label.config(text=get_text('no_files'))
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        return

    image_links = []
    video_links = []
    
    for link in links:
        extension = link.split('.')[-1].lower()
        if extension in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'jfif']:
            image_links.append(link)
        elif extension in ['mp4', 'ts', 'webm', 'mpg', 'mov', 'm4v', 'mkv', 'mpeg', 'avi', 'wmv', 'flv']:
            video_links.append(link)

    total_files = len(image_links) + len(video_links)
    successful = 0
    failed = 0

    for i, link in enumerate(image_links, 1):
        if cancel_download:  
            status_label.config(text=get_text('download_cancelled'))
            break
        status_label.config(text=get_text('downloading_image', current=i, total=len(image_links)))
        if download_with_progress(link, folder, progress_var, status_label):
            successful += 1
        else:
            failed += 1
        time.sleep(0.5)

    if video_links and not cancel_download: 
        status_label.config(text="Video boyutları kontrol ediliyor...")
        
        video_sizes = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        for link in video_links:
            size = get_file_size(link, headers)
            video_sizes.append((link, size))
        
        video_sizes.sort(key=lambda x: x[1])
        
        for i, (link, size) in enumerate(video_sizes, 1):
            if cancel_download: 
                status_label.config(text=get_text('download_cancelled'))
                break
            size_mb = size / (1024 * 1024)
            status_label.config(text=get_text('downloading_video', current=i, total=len(video_links), size=size_mb))
            if download_with_progress(link, folder, progress_var, status_label):
                successful += 1
            else:
                failed += 1

    download_button.config(state='normal')
    cancel_button.config(state='disabled')
    
    if not cancel_download:
        status_label.config(text=get_text('download_complete'))
        update_stats(stats_text, get_text('result_message').format(
            images=len(image_links),
            videos=len(video_links),
            success=successful,
            failed=failed
        ))
        
        download_complete_callback()

def select_folder(folder_entry):
    folder = filedialog.askdirectory()
    if folder:  
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

def check_clipboard():
    try:
        global last_clipboard, clipboard_var
        
        try:
            if not root.winfo_exists():
                return
        except:
            return
            
        current_clipboard = root.clipboard_get()
        
        if (current_clipboard != last_clipboard and 
            ('bunkr.cr' in current_clipboard or 'bunkr.ru' in current_clipboard) and
            ('https://' in current_clipboard or 'http://' in current_clipboard)):
            
            print(f"Yeni Bunkr linki algılandı: {current_clipboard}")
            
            if folder_entry.get():
                download_queue.append(current_clipboard)
                
                update_queue_status()
                
                if not is_downloading:
                    process_download_queue()
            else:
                status_label.config(text=get_text('error_folder'))
            
            last_clipboard = current_clipboard
        
        if root.winfo_exists() and clipboard_var and clipboard_var.get():
            root.after(1000, check_clipboard)
        
    except tk.TclError:
        if root.winfo_exists() and clipboard_var and clipboard_var.get():
            root.after(1000, check_clipboard)
    except Exception as e:
        print(f"Clipboard kontrol hatası: {e}")
        if root.winfo_exists() and clipboard_var and clipboard_var.get():
            root.after(1000, check_clipboard)

def update_queue_status():
    if download_queue:
        queue_text = get_text('queue_status', count=len(download_queue))
        status_label.config(text=queue_text)
        current_text = stats_text.get('1.0', tk.END).strip()
        if current_text:
            update_stats(stats_text, current_text)
    else:
        status_label.config(text=get_text('queue_empty'))

def create_gui():
    global root, title_label, subtitle_label, url_frame, folder_frame
    global progress_frame, stats_frame, folder_button, download_button
    global theme_button, language_button, status_label, stats_text
    global last_clipboard, clipboard_var, cancel_button
    global clipboard_status, clipboard_toggle 
    
    root = tk.Tk()
    
    try:
        last_clipboard = root.clipboard_get()
    except:
        last_clipboard = ""
    
    root.title("Bunkr Downloader Pro")
    
    window_width = 1000
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.minsize(800, 500)  
    
    sv_ttk.set_theme("dark")
    
    container = ttk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    left_panel = ttk.Frame(container)
    left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    
    header_frame = ttk.Frame(left_panel)
    header_frame.pack(fill=tk.X, pady=(0, 20))
    
    logo_label = ttk.Label(
        header_frame,
        text="⚡",
        font=('Segoe UI Emoji', 32)
    )
    logo_label.pack(side=tk.LEFT, padx=(0, 10))
    
    title_frame = ttk.Frame(header_frame)
    title_frame.pack(side=tk.LEFT)
    
    title_label = ttk.Label(
        title_frame,
        text="Bunkr Downloader Pro",
        font=('Segoe UI', 24, 'bold')
    )
    title_label.pack(anchor='w')
    
    subtitle_label = ttk.Label(
        title_frame,
        text="Hızlı ve Güvenli İndirme Aracı",
        font=('Segoe UI', 10)
    )
    subtitle_label.pack(anchor='w')
    
    url_frame = ttk.LabelFrame(left_panel, text="İndirme Linki", padding=15)
    url_frame.pack(fill=tk.X, pady=(0, 15))
    
    url_entry = ttk.Entry(
        url_frame,
        font=('Segoe UI', 10)
    )
    url_entry.pack(fill=tk.X, pady=(5, 0))
    
    folder_frame = ttk.LabelFrame(left_panel, text="Ana Klasör (Albüm alt klasörü otomatik oluşturulacak)", padding=15)
    folder_frame.pack(fill=tk.X, pady=(0, 15))
    
    folder_entry = ttk.Entry(
        folder_frame,
        font=('Segoe UI', 10)
    )
    folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    
    folder_button = ttk.Button(
        folder_frame,
        text="Gözat",
        command=lambda: select_folder(folder_entry),
        style='Accent.TButton',
        width=15
    )
    folder_button.pack(side=tk.RIGHT)
    
    button_frame = ttk.Frame(left_panel)
    button_frame.pack(pady=(0, 20))
    
    download_button = ttk.Button(
        button_frame,
        text=get_text('download_button'),
        command=start_download_thread,
        style='Accent.TButton',
        width=25
    )
    download_button.pack(side=tk.LEFT, padx=5)
    
    cancel_button = ttk.Button(  
        button_frame,
        text=get_text('cancel_button'),
        command=cancel_download_process,
        style='Secondary.TButton',
        width=15,
        state='disabled' 
    )
    cancel_button.pack(side=tk.LEFT, padx=5)
    
    right_panel = ttk.Frame(container)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
    progress_frame = ttk.LabelFrame(right_panel, text="İndirme Durumu", padding=15)
    progress_frame.pack(fill=tk.X, pady=(0, 15))
    
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(
        progress_frame,
        variable=progress_var,
        maximum=100,
        mode='determinate',
        style='Accent.Horizontal.TProgressbar'
    )
    progress_bar.pack(fill=tk.X, pady=(5, 10))
    
    status_label = ttk.Label(
        progress_frame,
        text="Hazır",
        font=('Segoe UI', 10)
    )
    status_label.pack(anchor='w')
    
    stats_frame = ttk.LabelFrame(right_panel, text="İndirme İstatistikleri", padding=15)
    stats_frame.pack(fill=tk.BOTH, expand=True)
    
    stats_text = tk.Text(
        stats_frame,
        font=('Cascadia Code', 10),
        wrap=tk.WORD,
        state='disabled',
        bg='#2b2b2b',
        fg='#e0e0e0',
        relief='flat',
        height=10
    )
    stats_text.pack(fill=tk.BOTH, expand=True)
    
    footer_frame = ttk.Frame(root)
    footer_frame.pack(fill=tk.X, padx=20, pady=10)
    
    theme_button = ttk.Button(
        footer_frame,
        text="🌓 Tema Değiştir",
        command=lambda: toggle_theme(stats_text),
        style='Secondary.TButton',
        width=15
    )
    theme_button.pack(side=tk.RIGHT)
    
    version_label = ttk.Label(
        footer_frame,
        text="v1.0.0",
        font=('Segoe UI', 8)
    )
    version_label.pack(side=tk.LEFT)
    
    style = ttk.Style()
    style.configure('Accent.TButton', font=('Segoe UI', 10))
    style.configure('Secondary.TButton', font=('Segoe UI', 9))
    
    control_frame = ttk.Frame(footer_frame)
    control_frame.pack(side=tk.RIGHT)
    
    language_button = ttk.Button(
        control_frame,
        text=get_text('language_button'),
        command=toggle_language,
        style='Secondary.TButton',
        width=15
    )
    language_button.pack(side=tk.RIGHT, padx=5)
    
    theme_button.pack(side=tk.RIGHT, padx=5)
    
    clipboard_frame = ttk.Frame(right_panel)
    clipboard_frame.pack(fill=tk.X, pady=(0, 15))
    
    clipboard_status = ttk.Label(  
        clipboard_frame,
        text="📋 " + get_text('clipboard_enabled'),
        font=('Segoe UI', 9),
        foreground='#00aa00'
    )
    clipboard_status.pack(side=tk.LEFT)
    
    clipboard_var = tk.BooleanVar(value=True)  
    
    def toggle_clipboard():
        if clipboard_var.get():
            global last_clipboard
            try:
                last_clipboard = root.clipboard_get()  
            except:
                last_clipboard = ""
            root.after(1000, check_clipboard)
            clipboard_status.configure(
                text="📋 " + get_text('clipboard_enabled'),
                foreground='#00aa00'
            )
        else:
            clipboard_status.configure(
                text="📋 " + get_text('clipboard_disabled'),
                foreground='#aa0000'
            )
    
    clipboard_toggle = ttk.Checkbutton(  
        clipboard_frame,
        text=get_text('clipboard_toggle'),
        variable=clipboard_var,
        command=toggle_clipboard,
        style='Switch.TCheckbutton'
    )
    clipboard_toggle.pack(side=tk.RIGHT)
    
    if clipboard_var.get():
        root.after(1000, check_clipboard)
    
    return root, url_entry, folder_entry, progress_var, status_label, download_button, stats_text

def update_stats(stats_text, message):
    stats_text.config(state='normal')
    stats_text.delete(1.0, tk.END)
    
    stats_text.insert(tk.END, message)
    
    if download_queue:
        current_url = url_entry.get()  
        queue_message = (
            "\n\n" + "=" * 30 + "\n" +
            get_text('current_download').format(
                current=current_url,
                queue=len(download_queue)
            )
        )
        stats_text.insert(tk.END, queue_message)
    
    stats_text.config(state='disabled')

def update_queue_status():
    if download_queue:
        queue_text = get_text('queue_status', count=len(download_queue))
        status_label.config(text=queue_text)
        current_text = stats_text.get('1.0', tk.END).strip()
        if current_text:
            update_stats(stats_text, current_text)
    else:
        status_label.config(text=get_text('queue_empty'))

if __name__ == "__main__":
    root, url_entry, folder_entry, progress_var, status_label, download_button, stats_text = create_gui()
    root.mainloop() 