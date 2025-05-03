import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from urllib.parse import urljoin, unquote
from tkinter import filedialog
import threading
import time
from tkinter import ttk
import sv_ttk
from collections import deque 
import re
from urllib.parse import urlparse
from base64 import b64decode
from math import floor
import sys
import io
import codecs
import random
import string
from hashlib import sha256  # Added for GoFile password hashing
from concurrent.futures import ThreadPoolExecutor  # Added for parallel downloads
import socket
import concurrent.futures
import tempfile
import math
import subprocess
import importlib.util
import json

# Ensure correct encoding for console output
if sys.stdout is not None and getattr(sys.stdout, "encoding", None) != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SUPPORTED_FORMATS = [
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'ts', 'webm', 'mpg', 'mov',
    'zip', 'rar', 'pdf', 'm4v', 'mkv', 'mp3', 'mpeg', 'avi', 'jfif', 'wmv',
    '7z', 'tar', 'flv', 'm4a'
]

# Bunkr API settings
BUNKR_VS_API_URL = "https://bunkr.cr/api/vs"
SECRET_KEY_BASE = "SECRET_KEY_"

# Supported sites
SUPPORTED_SITES = {
    'bunkr': ['bunkr.cr', 'bunkr.ru', 'bunkr.red', 'bunkr.black', 'bunkr.sk', 'bunkr.media', 
              'bunkr.ws', 'bunkr.fi', 'bunkr.ac', 'bunkr.site', 'bunkr.ph', 'bunkr.pk', 'bunkr.si'],
    'videzz': ['videzz.net', 'vidoza.net'],
    'gofile': ['gofile.io'],
    'pixeldrain': ['pixeldrain.com'],
    'streamtape': ['streamtape.com'],
    'vtube': ['vtube.network', 'vtbe.to'],
    'rubyvid': ['rubyvid.com', 'stmruby.com', 'rubystm.com']
}

LANGUAGES = {
    'tr': {
        'title': 'Bunkr & GoFile Downloader Pro',
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
        
        # GoFile specific translations
        'gofile_collecting': 'GoFile için linkler toplanıyor...',
        'gofile_token_error': 'GoFile erişim anahtarı alınamadı',
        'gofile_no_files': 'GoFile\'dan indirilecek dosya bulunamadı',
        'gofile_password_required': 'Şifre korumalı GoFile linki. Lütfen şifre girin.',
        'gofile_invalid_url': 'Geçersiz GoFile URL formatı',
        'gofile_downloading': 'GoFile dosyası indiriliyor ({current}/{total}): {filename}',
        'gofile_result': (
            'İndirme tamamlandı.\n'
            'Toplam Dosya: {total}\n'
            'Başarılı: {success}\n'
            'Başarısız: {failed}'
        ),
    },
    'en': {
        'title': 'Bunkr & GoFile Downloader Pro',
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
        
        # GoFile specific translations
        'gofile_collecting': 'Collecting links from GoFile...',
        'gofile_token_error': 'Failed to get GoFile access token',
        'gofile_no_files': 'No files found to download from GoFile',
        'gofile_password_required': 'Password protected GoFile link. Please provide password.',
        'gofile_invalid_url': 'Invalid GoFile URL format',
        'gofile_downloading': 'Downloading GoFile file ({current}/{total}): {filename}',
        'gofile_result': (
            'Download completed.\n'
            'Total Files: {total}\n'
            'Successful: {success}\n'
            'Failed: {failed}'
        ),
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
prev_url_type = None  # Track previous URL type for queue delay

def toggle_language():
    global current_language
    current_language = 'en' if current_language == 'tr' else 'tr'
    update_gui_language()

def get_text(key, **kwargs):
    text = LANGUAGES[current_language].get(key, LANGUAGES['en'][key])
    formatted_text = text.format(**kwargs) if kwargs else text
    # Fix any potential Turkish encoding issues
    return fix_turkish_encoding(formatted_text)

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

def download_with_progress(url, folder, progress_var=None, status_label=None, custom_filename=None, token=None):
    try:
        global cancel_download 
        
        # Ensure the folder path has no trailing spaces
        folder = folder.strip() if isinstance(folder, str) else folder
        
        # Special handling for GoFile URLs
        if "gofile.io" in url or "gofilecdn.com" in url or "store" in url and "gofile.io" in url:
            try:
                if custom_filename:
                    file_name = custom_filename
                else:
                    file_name = url.split('/')[-1].split('?')[0]
                    # Ensure filename is properly decoded
                    file_name = unquote(file_name)
                    
                file_path = os.path.join(folder, file_name)
                tmp_file = f"{file_path}.part"
                
                # Ensure the directory exists before trying to write to it
                os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
                
                if status_label:
                    status_label.config(text=f"GoFile: Downloading {file_name}")
                if progress_var:
                    progress_var.set(0)
                
                print(f"Starting GoFile download for: {url}")
                
                # Setup headers for GoFile with token in cookie
                headers = {
                    "Cookie": f"accountToken={token}" if token else "",
                    "Accept-Encoding": "gzip, deflate, br",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                    "Accept": "*/*",
                    "Referer": "https://gofile.io/",
                    "Origin": "https://gofile.io",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "Range": "bytes=0-"  # Request full file
                }
                
                # Check for partial download to resume
                part_size = 0
                if os.path.isfile(tmp_file):
                    part_size = os.path.getsize(tmp_file)
                    headers["Range"] = f"bytes={part_size}-"
                
                # Longer timeout (60 seconds connect, 1 hour read)
                response = requests.get(url, headers=headers, stream=True, timeout=(60, 3600))
                
                if response.status_code not in [200, 206]:  # 200 for full download, 206 for partial
                    print(f"Error: Server returned status code {response.status_code}")
                    if status_label:
                        status_label.config(text=f"Error: Server returned status code {response.status_code}")
                    return False
                
                # Get total file size
                content_length = response.headers.get('content-length')
                content_range = response.headers.get('content-range')
                
                if content_range and '/' in content_range:
                    total_size = int(content_range.split('/')[-1])
                elif content_length:
                    total_size = int(content_length) + part_size
                else:
                    total_size = 0
                    
                # Print headers for debugging
                print(f"Response headers: {response.headers}")
                print(f"Total size: {total_size}, Part size: {part_size}")
                    
                # Initialize counters
                start_time = time.time()
                downloaded = part_size
                last_update_time = start_time
                
                # Open file in append mode if resuming, otherwise write mode
                with open(tmp_file, 'ab' if part_size > 0 else 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if cancel_download:
                            f.close()
                            return False
                        
                        if chunk:  # Filter out keep-alive chunks
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Update progress every 0.5 seconds
                            current_time = time.time()
                            if current_time - last_update_time > 0.5:
                                last_update_time = current_time
                                elapsed = current_time - start_time
                                
                                if elapsed > 0:
                                    # Calculate download speed
                                    speed = (downloaded - part_size) / (1024 * 1024 * elapsed)  # MB/s
                                    
                                    # Update progress bar if total size is known
                                    if total_size > 0 and progress_var:
                                        percent = min(100, (downloaded / total_size) * 100)
                                        progress_var.set(percent)
                                    
                                    # Update status with detailed info
                                    if status_label:
                                        if total_size > 0:
                                            status_label.config(text=f"GoFile: {file_name} - {downloaded/(1024*1024):.2f}/{total_size/(1024*1024):.2f} MB ({speed:.2f} MB/s)")
                                        else:
                                            status_label.config(text=f"GoFile: {file_name} - {downloaded/(1024*1024):.2f} MB ({speed:.2f} MB/s)")
                
                # Check if download completed successfully
                if os.path.exists(tmp_file):
                    actual_size = os.path.getsize(tmp_file)
                    print(f"Download completed. File size: {actual_size} bytes")
                    
                    # Rename temp file to final name
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    os.rename(tmp_file, file_path)
                    
                    if status_label:
                        status_label.config(text=get_text('download_success', filename=file_name))
                    
                    # Verify file is not HTML
                    if actual_size < 100000:  # Small file, might be HTML error
                        try:
                            with open(file_path, 'rb') as f:
                                first_bytes = f.read(1024).decode('utf-8', errors='ignore')
                                if '<!DOCTYPE html>' in first_bytes or '<html' in first_bytes:
                                    print(f"Error: Downloaded file is HTML, not a video file")
                                    if status_label:
                                        status_label.config(text="Error: Downloaded file is HTML, not the actual video")
                                    os.remove(file_path)
                                    return False
                        except:
                            pass  # Continue if we can't check
                    
                    print(f"GoFile download successful: {file_name} - Size: {actual_size/1024/1024:.2f} MB")
                    return True
                    
                return False
                
            except Exception as e:
                print(f"GoFile download error: {e}")
                if status_label:
                    status_label.config(text=f"Error: {str(e)}")
                return False
        
        # Regular download method for non-GoFile URLs
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',  # Add Turkish language preference
            'Accept-Encoding': 'identity',  # Request uncompressed content
            'Connection': 'keep-alive'
        }
        
        # Set Referer based on URL
        if any(domain in url for domain in SUPPORTED_SITES['bunkr']):
            headers['Referer'] = 'https://bunkr.cr/'
        elif "gofile.io" in url or "gofilecdn.com" in url:
            headers['Referer'] = 'https://gofile.io/'
        elif "videzz.net" in url or "vidoza.net" in url:
            headers['Referer'] = 'https://videzz.net/'

        # Increase timeout for larger files (60 seconds connect, 1 hour read)
        response = requests.get(url, headers=headers, stream=True, timeout=(60, 3600))
        
        if response.status_code == 200:
            if custom_filename:
                file_name = custom_filename
            else:
                file_name = url.split('/')[-1].split('?')[0]
                # Ensure filename is properly decoded
                file_name = unquote(file_name)
                
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
            start_time = time.time()
            last_update_time = start_time
            
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=block_size):
                    if cancel_download:  
                        file.close()
                        os.remove(file_path)  
                        return False
                        
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        
                        # Update progress every 0.5 seconds to prevent UI slowdown
                        current_time = time.time()
                        if current_time - last_update_time > 0.5 and progress_var and status_label and total_size > 0:
                            last_update_time = current_time
                            progress = (downloaded / total_size) * 100
                            progress_var.set(progress)
                            
                            elapsed = current_time - start_time
                            if elapsed > 0:
                                download_speed = downloaded / (1024 * 1024 * elapsed)  # MB/s
                                status_label.config(text=f"{file_name}: {downloaded/(1024*1024):.2f}/{total_size/(1024*1024):.2f} MB - {download_speed:.2f} MB/s")
            
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
        print(f"Download error: {e}")
        return False

def normalize_text(text):
    """Normalize text to ensure proper encoding of Turkish characters"""
    try:
        # First try to detect if text is already UTF-8 encoded
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        
        # Handle common encoding issues
        encodings = ['utf-8', 'latin-1', 'iso-8859-9', 'windows-1254']  # Add Turkish-specific encodings
        
        for encoding in encodings:
            try:
                # Try encoding and decoding to fix potential issues
                normalized = text.encode(encoding).decode('utf-8')
                
                # Check if normalized text has the expected characters
                if 'Ã¼' in normalized:  # This indicates wrong encoding
                    continue
                    
                # Replace common problematic sequences for Turkish characters
                normalized = normalized.replace('Ã¼', 'ü')
                normalized = normalized.replace('Ä±', 'ı')
                normalized = normalized.replace('Ã¶', 'ö')
                normalized = normalized.replace('Ã§', 'ç')
                normalized = normalized.replace('ÄŸ', 'ğ')
                normalized = normalized.replace('ÅŸ', 'ş')
                
                return normalized
            except:
                continue
                
        # If all attempts fail, use unidecode as last resort
        return text
    except Exception as e:
        print(f"Error normalizing text: {e}")
        return text

def remove_illegal_chars(string):
    """Remove illegal filename characters while preserving Turkish characters"""
    try:
        # Normalize the string first to handle encoding issues
        string = normalize_text(string)
        
        # Remove illegal characters for filenames
        sanitized = re.sub(r'[<>:"/\\|?*\']|[\0-\31]', "-", string).strip()
        return sanitized
    except Exception as e:
        print(f"Error sanitizing filename: {e}")
        return string.encode('ascii', 'ignore').decode('ascii')

def extract_album_title(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',  # Set Turkish as preferred language
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://bunkr.cr/',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(url, headers=headers)
        
        # Ensure the content is decoded properly
        if response.encoding.lower() != 'utf-8':
            response.encoding = 'utf-8'
            
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
                    return remove_illegal_chars(unquote(file_name))
        else:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.text.split('|')[0].strip()
                # Ensure proper decoding of title
                title = unquote(title)
                return remove_illegal_chars(title)
                
        return "Video"
    except Exception as e:
        print(f"Error extracting album title: {e}")
        return "Video"

def get_url_data(url):
    parsed_url = urlparse(url)
    return {
        'file_name': os.path.basename(parsed_url.path), 
        'extension': os.path.splitext(parsed_url.path)[1].lower().lstrip('.'), 
        'hostname': parsed_url.hostname
    }

def get_encryption_data(slug, session):
    try:
        response = session.post(BUNKR_VS_API_URL, json={'slug': slug})
        if response.status_code != 200:
            print(f"HTTP error {response.status_code} getting encryption data")
            return None
        
        return response.json()
    except Exception as e:
        print(f"Error getting encryption data: {e}")
        return None

def decrypt_encrypted_url(encryption_data):
    if not encryption_data:
        return None
        
    try:
        secret_key = f"{SECRET_KEY_BASE}{floor(encryption_data['timestamp'] / 3600)}"
        encrypted_url_bytearray = list(b64decode(encryption_data['url']))
        secret_key_byte_array = list(secret_key.encode('utf-8'))

        decrypted_url = ""

        for i in range(len(encrypted_url_bytearray)):
            decrypted_url += chr(encrypted_url_bytearray[i] ^ secret_key_byte_array[i % len(secret_key_byte_array)])

        return decrypted_url
    except Exception as e:
        print(f"Error decrypting URL: {e}")
        return None

def get_real_download_url(url, session):
    try:
        if not url.startswith('http'):
            url = f'https://bunkr.cr{url}'
            
        # Handle API-based URL decryption for videos
        if '/f/' in url:
            response = session.get(url)
            if response.status_code != 200:
                print(f"HTTP error {response.status_code} getting URL {url}")
                return None
                
            # Try to get the slug from the URL
            slug_match = re.search(r'\/f\/(.*?)(?:\?|$)', url)
            if slug_match:
                slug = slug_match.group(1)
                encryption_data = get_encryption_data(slug, session)
                if encryption_data:
                    decrypted_url = decrypt_encrypted_url(encryption_data)
                    if decrypted_url:
                        return decrypted_url
            
            # Fallback to parsing the page directly
            soup = BeautifulSoup(response.text, 'html.parser')
            
            og_url = soup.find('meta', property='og:url')
            if og_url and og_url.get('content'):
                return og_url['content']
            
            media_element = soup.find(['img', 'video'], class_='max-h-full')
            if media_element:
                if media_element.name == 'video':
                    source = media_element.find('source')
                    src = source['src'] if source else media_element.get('src')
                else:
                    src = media_element.get('src')
                
                if src:
                    return urljoin(url, src)
                    
        return url
    except Exception as e:
        print(f"Error getting real download URL: {e}")
        return None

def extract_links(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://bunkr.cr/',
            'Connection': 'keep-alive'
        }
        
        session = requests.Session()
        session.headers.update(headers)
        
        is_single_file = '/f/' in url
        
        if is_single_file:
            media_url = get_real_download_url(url, session)
            if media_url:
                extension = get_url_data(media_url)['extension']
                if extension in SUPPORTED_FORMATS:
                    return [media_url]
            return []
            
        else:
            response = session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            all_links = []
            
            # Check if we're on a gallery page with direct videos
            direct_link = soup.find('span', {'class': 'ic-videos'}) is not None or soup.find('div', {'class': 'lightgallery'}) is not None
            if direct_link:
                media_url = get_real_download_url(url, session)
                if media_url:
                    extension = get_url_data(media_url)['extension'] 
                    if extension in SUPPORTED_FORMATS:
                        all_links.append(media_url)
                    return all_links
            
            # Standard album page with multiple files
            file_pages = []
            
            # First try the new Bunkr interface
            boxes = soup.find_all('a', {'class': 'after:absolute'})
            if boxes:
                for box in boxes:
                    if box.get('href'):
                        file_url = urljoin(url, box['href'])
                        file_pages.append(file_url)
            
            # Fallback to older interface
            if not file_pages:
                for item in soup.find_all('div', class_='theItem'):
                    a_tag = item.find('a', href=True)
                    if a_tag and '/f/' in a_tag['href']:
                        file_url = urljoin(url, a_tag['href'])
                        file_pages.append(file_url)
            
            for file_page in file_pages:
                try:
                    media_url = get_real_download_url(file_page, session)
                    if media_url:
                        extension = get_url_data(media_url)['extension']
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
    global is_downloading, prev_url_type
    
    if is_downloading or not download_queue:
        return
        
    is_downloading = True
    url = download_queue.popleft()  

    # Determine current url type
    if is_gofile_url(url):
        curr_type = 'gofile'
    elif is_bunkr_url(url):
        curr_type = 'bunkr'
    elif is_videzz_url(url):
        curr_type = 'videzz'
    elif is_pixeldrain_url(url):
        curr_type = 'pixeldrain'
    else:
        curr_type = 'other'

    # If previous was gofile and current is gofile, wait 2 seconds
    if prev_url_type == 'gofile' and curr_type == 'gofile':
        for remaining in range(2, 0, -1):
            msg = f"Waiting {remaining} seconds before next GoFile download..."
            status_label.config(text=msg)
            stats_text.config(state='normal')
            stats_text.delete(1.0, tk.END)
            stats_text.insert(tk.END, msg)
            stats_text.config(state='disabled')
            root.update_idletasks()
            time.sleep(1)

    prev_url_type = curr_type

    url_entry.delete(0, tk.END)
    url_entry.insert(0, url)
    
    current_text = stats_text.get('1.0', tk.END).strip()
    if current_text:
        update_stats(stats_text, current_text)
    
    # Start download in a new thread
    download_thread = threading.Thread(target=start_download)
    download_thread.daemon = True
    download_thread.start()

def download_complete_callback():
    global is_downloading
    is_downloading = False
    
    # Update UI
    download_button.config(state='normal')
    cancel_button.config(state='disabled')
    
    # Process next URL in queue if available
    if download_queue:
        # Use after to schedule the next download
        root.after(1000, process_download_queue)
    else:
        # Update status if queue is empty
        status_label.config(text=get_text('queue_empty'))
        update_stats(stats_text, get_text('queue_empty'))

def sanitize_url(url):
    """Sanitize URL to handle special characters"""
    try:
        # Remove any whitespace
        url = url.strip()
        
        # Ensure URL has a scheme
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Make sure URL is properly encoded
        parsed = urlparse(url)
        path = parsed.path
        
        # Keep the query string if it exists
        query = f"?{parsed.query}" if parsed.query else ""
        
        # Reconstruct the URL with proper components
        sanitized_url = f"{parsed.scheme}://{parsed.netloc}{path}{query}"
        return sanitized_url
    except Exception as e:
        print(f"URL sanitization error: {e}")
        return url

def fix_turkish_encoding(text):
    """Specifically fix Turkish encoding issues in displayed text"""
    mapping = {
        'Ã¼': 'ü', 'ÃœÌ': 'Ü', 'Ã¶': 'ö', 'Ã–': 'Ö', 
        'Ã§': 'ç', 'Ã‡': 'Ç', 'Ä±': 'ı', 'Ä°': 'İ',
        'ÄŸ': 'ğ', 'Äž': 'Ğ', 'ÅŸ': 'ş', 'Åž': 'Ş',
        'â€™': "'", 'â€"': "–", 'â€"': "—",
        'Ã¢': 'â', 'Ã®': 'î'
    }
    
    for wrong, correct in mapping.items():
        text = text.replace(wrong, correct)
    
    return text

def generate_random_filename(extension):
    """Generate a random filename with the given extension"""
    letters = string.ascii_lowercase + string.digits
    random_name = ''.join(random.choice(letters) for i in range(12))
    return f"{random_name}.{extension}"

def extract_videzz_video(url, headers=None):
    """Extract video URL from videzz.net pages"""
    if not headers:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching videzz URL: {response.status_code}")
            return None
        
        # Look for the sourcesCode pattern in the HTML
        video_pattern = r'sourcesCode:\s*\[\{\s*src:\s*"([^"]+)",\s*type:'
        match = re.search(video_pattern, response.text)
        
        if match:
            video_url = match.group(1)
            return video_url
        
        # Alternative method using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        
        for script in scripts:
            if script.string and 'sourcesCode' in script.string:
                video_pattern = r'sourcesCode:\s*\[\{\s*src:\s*"([^"]+)",\s*type:'
                match = re.search(video_pattern, script.string)
                if match:
                    video_url = match.group(1)
                    return video_url
        
        return None
    except Exception as e:
        print(f"Error extracting videzz video: {e}")
        return None

def is_videzz_url(url):
    """Check if URL is from videzz.net or vidoza.net"""
    parsed_url = urlparse(url)
    return any(domain in parsed_url.netloc for domain in SUPPORTED_SITES['videzz'])

def is_bunkr_url(url):
    """Check if URL is from bunkr.cr or bunkr.ru"""
    parsed_url = urlparse(url)
    return any(domain in parsed_url.netloc for domain in SUPPORTED_SITES['bunkr'])

def is_gofile_url(url):
    """Check if URL is from GoFile.io"""
    parsed_url = urlparse(url)
    return any(domain in parsed_url.netloc for domain in SUPPORTED_SITES['gofile'])

def get_gofile_token():
    """Get GoFile API token"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
        "Connection": "keep-alive",
    }

    try:
        response = requests.post("https://api.gofile.io/accounts", headers=headers).json()
        if response["status"] == "ok":
            print(f"Successfully obtained GoFile token")
            return response["data"]["token"]
        else:
            print(f"Error getting GoFile token: {response}")
            return None
    except Exception as e:
        print(f"Error getting GoFile token: {e}")
        return None

def recursive_extract_gofile_links(url, token, password=None, status_label=None, recursive_depth=0, parent_path=""):
    """Recursively extract all links from GoFile folders"""
    if recursive_depth > 10:  # Prevent too deep recursion
        return None, []

    try:
        if status_label and recursive_depth == 0:
            status_label.config(text=get_text('gofile_collecting'))
        
        # Parse URL to get content ID
        if recursive_depth == 0:  # Only parse URL at top level, deeper levels get direct IDs
            try:
                parsed_url = urlparse(url)
                path_parts = parsed_url.path.split('/')
                
                # Look for /d/ in the URL path
                if '/d/' in parsed_url.path:
                    for i, part in enumerate(path_parts):
                        if part == 'd' and i+1 < len(path_parts):
                            content_id = path_parts[i+1]
                            break
                    else:  # If no content ID found after /d/
                        if status_label:
                            status_label.config(text=get_text('gofile_invalid_url'))
                        return None, []
                else:
                    # Direct ID was provided
                    content_id = url
            except Exception:
                if status_label:
                    status_label.config(text=get_text('gofile_invalid_url'))
                return None, []
        else:
            # For recursive calls, the URL parameter already contains the content ID
            content_id = url
        
        # Hash password if provided
        hashed_password = sha256(password.encode()).hexdigest() if password else None
        
        # Build API URL with updated parameters
        api_url = f"https://api.gofile.io/contents/{content_id}?wt=4fd6sg89d7s6&cache=true&sortField=createTime&sortDirection=1"
        if hashed_password:
            api_url = f"{api_url}&password={hashed_password}"
        
        print(f"Requesting GoFile API: {api_url}")
        
        # Request API with improved headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Authorization": f"Bearer {token}",
            "Referer": "https://gofile.io/",
            "Origin": "https://gofile.io"
        }
        
        # Increase timeout for API response
        response = requests.get(api_url, headers=headers, timeout=30).json()
        
        print(f"API response status: {response['status']}")
        
        if response["status"] != "ok":
            if status_label and recursive_depth == 0:
                status_label.config(text=get_text('gofile_no_files'))
            return None, []
        
        # Continue with the rest of the function as is
        data = response["data"]
        
        # Check if password protected
        if "password" in data and "passwordStatus" in data and data["passwordStatus"] != "passwordOk":
            if status_label:
                status_label.config(text=get_text('gofile_password_required'))
            return None, []
        
        # Get folder name for the album title
        folder_name = data["name"]
        
        # Main folder only when at root level
        if recursive_depth == 0:
            main_folder_name = folder_name
        else:
            main_folder_name = parent_path
        
        # Current path including this folder
        current_path = parent_path
        if recursive_depth > 0:
            current_path = os.path.join(parent_path, folder_name)
        
        # Extract file links
        all_links = []
        
        # Process single file if content is a file
        if data["type"] != "folder":
            all_links.append({
                "filename": data["name"],
                "link": data["link"],
                "path": current_path
            })
            return main_folder_name, all_links
        
        # Process all items in folder
        for child_id in data["children"]:
            child = data["children"][child_id]
            
            if child["type"] == "folder":
                # Recursively get links from subfolder
                _, subfolder_links = recursive_extract_gofile_links(
                    child["id"], 
                    token, 
                    password, 
                    status_label, 
                    recursive_depth + 1,
                    current_path
                )
                all_links.extend(subfolder_links)
            else:
                all_links.append({
                    "filename": child["name"],
                    "link": child["link"],
                    "path": current_path
                })
        
        return main_folder_name, all_links
    
    except Exception as e:
        print(f"Error extracting GoFile links: {e}")
        if status_label and recursive_depth == 0:
            status_label.config(text=get_text('download_error', error=str(e)))
        return None, []

def show_password_dialog():
    """Show a dialog to request password for protected links"""
    password_window = tk.Toplevel(root)
    password_window.title(get_text('gofile_password_required'))
    
    window_width = 400
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    password_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    password_window.resizable(False, False)
    
    password_window.grab_set()  # Make the dialog modal
    
    # Apply theme
    sv_ttk.set_theme(sv_ttk.get_theme())
    
    # Container
    container = ttk.Frame(password_window, padding=20)
    container.pack(fill=tk.BOTH, expand=True)
    
    # Password label
    password_label = ttk.Label(
        container,
        text=get_text('gofile_password_required'),
        font=('Segoe UI', 10)
    )
    password_label.pack(pady=(0, 10))
    
    # Password entry
    password_var = tk.StringVar()
    password_entry = ttk.Entry(
        container,
        font=('Segoe UI', 10),
        show="•",  # Show bullets instead of actual characters
        textvariable=password_var
    )
    password_entry.pack(fill=tk.X, pady=(0, 20))
    password_entry.focus_set()
    
    # Buttons frame
    button_frame = ttk.Frame(container)
    button_frame.pack(fill=tk.X)
    
    result = [None]  # Use a list to store the result since nonlocal is not needed for lists
    
    def on_ok():
        result[0] = password_var.get()
        password_window.destroy()
    
    def on_cancel():
        password_window.destroy()
    
    # OK button
    ok_button = ttk.Button(
        button_frame,
        text="OK",
        command=on_ok,
        style='Accent.TButton',
        width=15
    )
    ok_button.pack(side=tk.RIGHT, padx=5)
    
    # Cancel button
    cancel_button = ttk.Button(
        button_frame,
        text=get_text('cancel_button'),
        command=on_cancel,
        style='Secondary.TButton',
        width=15
    )
    cancel_button.pack(side=tk.RIGHT, padx=5)
    
    # Bind Enter key to OK button
    password_entry.bind("<Return>", lambda event: on_ok())
    
    # Wait until the window is destroyed
    password_window.wait_window()
    
    return result[0]

def download_from_gofile(url, base_folder, status_label=None, progress_var=None):
    """Handle downloading from GoFile.io"""
    # Get GoFile token
    token = get_gofile_token()
    if not token:
        status_label.config(text=get_text('gofile_token_error'))
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        return
    
    # First try without password
    album_title, file_links = recursive_extract_gofile_links(url, token, None, status_label)
    
    # If no links found, it might be password protected
    if not album_title or not file_links:
        # Check if API response indicates password protection
        try:
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.split('/')
            
            # Extract content ID
            content_id = None
            if '/d/' in parsed_url.path:
                for i, part in enumerate(path_parts):
                    if part == 'd' and i+1 < len(path_parts):
                        content_id = path_parts[i+1]
                        break
            else:
                content_id = url
                
            if content_id:
                check_api_url = f"https://api.gofile.io/contents/{content_id}?wt=4fd6sg89d7s6"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                    "Accept": "*/*",
                    "Authorization": f"Bearer {token}",
                    "Referer": "https://gofile.io/",
                    "Origin": "https://gofile.io"
                }
                
                check_response = requests.get(check_api_url, headers=headers, timeout=30).json()
                
                # If password protected, show password dialog
                if (check_response["status"] == "ok" and 
                    "data" in check_response and 
                    "password" in check_response["data"] and 
                    check_response["data"]["password"]):
                    
                    password = show_password_dialog()
                    
                    if password:
                        # Try again with password
                        album_title, file_links = recursive_extract_gofile_links(url, token, password, status_label)
        except Exception as e:
            print(f"Error checking password protection: {e}")
    
    if not album_title or not file_links:
        status_label.config(text=get_text('gofile_no_files'))
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        return
    
    # Clean up album title and ensure no trailing spaces
    album_title = fix_turkish_encoding(album_title).strip()
    
    # Create main GoFile folder if it doesn't exist
    main_gofile_folder = os.path.join(base_folder, "GoFile")
    if not os.path.exists(main_gofile_folder):
        os.makedirs(main_gofile_folder)
    
    # If only 1-2 files, download directly to GoFile folder
    # Otherwise create a subfolder with album name
    if len(file_links) <= 2:
        target_folder = main_gofile_folder
        print(f"Downloading {len(file_links)} files directly to GoFile folder")
    else:
        # Create album-specific subfolder with the clean title
        target_folder = os.path.join(main_gofile_folder, album_title)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        print(f"Downloading {len(file_links)} files to album folder: {album_title}")
    
    # Print diagnostic info
    print(f"Found {len(file_links)} files to download from GoFile")
    for i, file_info in enumerate(file_links):
        print(f"{i+1}. {file_info['filename']} - {file_info['link']}")
    
    # Download files
    total_files = len(file_links)
    successful = 0
    failed = 0
    
    for i, file_info in enumerate(file_links, 1):
        if cancel_download:
            status_label.config(text=get_text('download_cancelled'))
            break
            
        filename = file_info["filename"]
        link = file_info["link"]
        path = file_info["path"].strip() if file_info["path"] else ""  # Ensure no trailing spaces
        
        # Create subfolder structure if needed (and if we have more than 2 files)
        if path and len(file_links) > 2:
            full_path = os.path.join(target_folder, path)
            if not os.path.exists(full_path):
                try:
                    os.makedirs(full_path)
                except Exception as e:
                    print(f"Error creating directory {full_path}: {e}")
                    full_path = target_folder  # Fallback to target folder
        else:
            full_path = target_folder
        
        status_label.config(text=get_text('gofile_downloading', current=i, total=total_files, filename=filename))
        
        # Pass token to download function
        if download_with_progress(link, full_path, progress_var, status_label, custom_filename=filename, token=token):
            successful += 1
        else:
            failed += 1
            
        # Add 2-second delay between downloads if there are more files in the queue
        if i < total_files and download_queue:
            status_label.config(text=f"Waiting 2 seconds before next download... ({i}/{total_files})")
            for remaining in range(2, 0, -1):
                if cancel_download:
                    break
                status_label.config(text=f"Waiting {remaining} seconds before next download... ({i}/{total_files})")
                time.sleep(1)
    
    download_button.config(state='normal')
    cancel_button.config(state='disabled')
    
    if not cancel_download:
        status_label.config(text=get_text('download_complete'))
        update_stats(stats_text, get_text('gofile_result', total=total_files, success=successful, failed=failed))
        
        download_complete_callback()

def is_pixeldrain_url(url):
    """Check if URL is from pixeldrain.com"""
    parsed_url = urlparse(url)
    return 'pixeldrain.com' in parsed_url.netloc

def extract_pixeldrain_info(url):
    """Extract information from pixeldrain.com URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://pixeldrain.com/',
        'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        # Extract the ID from the URL
        url_id = url.split('/')[-1]
        
        # Make the request to get the page content
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Find the viewer_data JSON in the page content
        pattern = r'window\.viewer_data\s*=\s*({.*?});'
        match = re.search(pattern, response.text, re.DOTALL)
        
        if match:
            viewer_data = json.loads(match.group(1))
            api_response = viewer_data.get('api_response', {})
            
            # Check if it's a single file or an album
            if 'files' in api_response:
                # It's an album
                album_id = api_response.get('id')
                album_title = api_response.get('title', 'Untitled Album')
                
                # Extract file information
                files = api_response.get('files', [])
                file_urls = []
                
                for file in files:
                    file_id = file.get('id')
                    file_name = file.get('name')
                    if file_id:
                        file_url = f'https://pixeldrain.com/api/file/{file_id}'
                        # Replace + with space in file name
                        file_name = file_name.replace('+', ' ')
                        file_urls.append({
                            'url': file_url,
                            'name': file_name
                        })
                
                return {
                    'type': 'album',
                    'album_id': album_id,
                    'album_title': album_title,
                    'file_urls': file_urls
                }
            else:
                # It's a single file
                file_id = api_response.get('id')
                file_name = api_response.get('name', 'Untitled File')
                if file_id:
                    file_url = f'https://pixeldrain.com/api/file/{file_id}'
                    # Replace + with space in file name
                    file_name = file_name.replace('+', ' ')
                    return {
                        'type': 'file',
                        'file_id': file_id,
                        'file_name': file_name,
                        'file_url': file_url
                    }
        else:
            # Try alternative method using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.text.split('|')[0].strip()
                return {
                    'type': 'file',
                    'file_id': url_id,
                    'file_name': title,
                    'file_url': f'https://pixeldrain.com/api/file/{url_id}'
                }
            return None
            
    except Exception as e:
        print(f"Error extracting PixelDrain info: {e}")
        return None

def download_from_pixeldrain(url, base_folder, status_label=None, progress_var=None):
    """Handle downloading from pixeldrain.com"""
    try:
        # Create Pixeldrain folder if it doesn't exist
        pixeldrain_folder = os.path.join(base_folder, "Pixeldrain")
        if not os.path.exists(pixeldrain_folder):
            os.makedirs(pixeldrain_folder)
        
        # Extract information from URL
        result = extract_pixeldrain_info(url)
        
        if not result:
            if status_label:
                status_label.config(text="Could not extract information from PixelDrain URL")
            download_button.config(state='normal')
            cancel_button.config(state='disabled')
            return
        
        if result['type'] == 'album':
            # Create album folder
            album_folder = os.path.join(pixeldrain_folder, result['album_title'])
            os.makedirs(album_folder, exist_ok=True)
            
            total_files = len(result['file_urls'])
            successful = 0
            failed = 0
            
            for i, file_info in enumerate(result['file_urls'], 1):
                if cancel_download:
                    if status_label:
                        status_label.config(text=get_text('download_cancelled'))
                    break
                    
                if status_label:
                    status_label.config(text=f"Downloading from PixelDrain ({i}/{total_files}): {file_info['name']}")
                
                # Reset progress for each file
                if progress_var:
                    progress_var.set(0)
                
                if download_with_progress(file_info['url'], album_folder, progress_var, status_label, custom_filename=file_info['name']):
                    successful += 1
                else:
                    failed += 1
                    
                if progress_var:
                    progress = (i / total_files) * 100
                    progress_var.set(progress)
            
            if status_label:
                status_label.config(text=get_text('download_complete'))
            update_stats(stats_text, f"Download completed.\nTotal Files: {total_files}\nSuccessful: {successful}\nFailed: {failed}")
            
        else:  # Single file
            if status_label:
                status_label.config(text=f"Downloading from PixelDrain: {result['file_name']}")
            
            # Reset progress for single file
            if progress_var:
                progress_var.set(0)
            
            if download_with_progress(result['file_url'], pixeldrain_folder, progress_var, status_label, custom_filename=result['file_name']):
                if status_label:
                    status_label.config(text=get_text('download_complete'))
                update_stats(stats_text, f"Download completed.\nFile: {result['file_name']}")
            else:
                if status_label:
                    status_label.config(text="Error downloading file")
        
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        download_complete_callback()
        
    except Exception as e:
        print(f"Error downloading from PixelDrain: {e}")
        if status_label:
            status_label.config(text=f"Error: {str(e)}")
        download_button.config(state='normal')
        cancel_button.config(state='disabled')

def is_streamtape_url(url):
    """Check if URL is from streamtape.com"""
    parsed_url = urlparse(url)
    return any(domain in parsed_url.netloc for domain in SUPPORTED_SITES['streamtape'])

def download_from_streamtape(url, base_folder, status_label=None, progress_var=None, retry_count=0):
    """Handle downloading from streamtape.com with retry mechanism"""
    try:
        # Create Streamtape folder if it doesn't exist
        streamtape_folder = os.path.join(base_folder, "Streamtape")
        if not os.path.exists(streamtape_folder):
            os.makedirs(streamtape_folder)

        # Headers for the request
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.6",
            "Connection": "keep-alive",
            "Host": "streamtape.com",
            "sec-ch-ua": '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }

        status_label.config(text="Extracting video from Streamtape...")
        
        # Try with original URL first
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Extract video ID from URL
        video_id = url.split('/')[-1]
        
        # Try to extract video URL
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        
        video_url_part = None
        for script in scripts:
            if script.string and 'get_video' in script.string:
                match = re.search(r"get_video\?id=([^&']+)&expires=([^&']+)&ip=([^&']+)&token=([^&']+)", script.string)
                if match:
                    video_id, expires, ip, token = match.groups()
                    video_id = video_id.replace('" + \'\'+ (\'xcd', '').replace('\')', '')
                    video_url_part = f"/get_video?id={video_id}&expires={expires}&ip={ip}&token={token}"
                    break
        
        # If not found, try alternative URL format
        if not video_url_part:
            alt_url = url.replace('/e/', '/v/') if '/e/' in url else url.replace('/v/', '/e/')
            alt_response = requests.get(alt_url, headers=headers)
            alt_response.raise_for_status()
            soup = BeautifulSoup(alt_response.text, 'html.parser')
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and 'get_video' in script.string:
                    match = re.search(r"get_video\?id=([^&']+)&expires=([^&']+)&ip=([^&']+)&token=([^&']+)", script.string)
                    if match:
                        video_id, expires, ip, token = match.groups()
                        video_id = video_id.replace('" + \'\'+ (\'xcd', '').replace('\')', '')
                        video_url_part = f"/get_video?id={video_id}&expires={expires}&ip={ip}&token={token}"
                        break
        
        if not video_url_part:
            if retry_count < 1:  # If we haven't retried yet
                status_label.config(text="Could not extract video URL, retrying...")
                time.sleep(2)  # Wait 2 seconds before retry
                return download_from_streamtape(url, base_folder, status_label, progress_var, retry_count + 1)
            else:
                status_label.config(text="Could not extract video URL from Streamtape after retry")
                download_button.config(state='normal')
                cancel_button.config(state='disabled')
                return
        
        # Construct the full video URL
        video_url = f"https://streamtape.com{video_url_part}&stream=1"
        
        # Extract video title
        title_meta = soup.find('meta', {'name': 'og:title'})
        if title_meta:
            filename = title_meta['content']
        else:
            filename = "video.mp4"  # Default filename if title not found
        
        status_label.config(text=f"Downloading: {filename}")
        
        # First, get the total size of the video
        head_response = requests.head(video_url, headers=headers)
        total_size = int(head_response.headers.get('content-length', 0))
        
        if total_size == 0:
            if retry_count < 1:  # If we haven't retried yet
                status_label.config(text="Could not determine video size, retrying...")
                time.sleep(2)  # Wait 2 seconds before retry
                return download_from_streamtape(url, base_folder, status_label, progress_var, retry_count + 1)
            else:
                status_label.config(text="Could not determine video size, falling back to single download")
                # Fallback to single download
                video_response = requests.get(video_url, headers=headers, stream=True)
                video_response.raise_for_status()
                
                file_path = os.path.join(streamtape_folder, filename)
                downloaded = 0
                start_time = time.time()
                last_update_time = start_time
                with open(file_path, 'wb') as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            current_time = time.time()
                            if current_time - last_update_time > 0.5:
                                last_update_time = current_time
                                mb = downloaded / (1024 * 1024)
                                elapsed = current_time - start_time
                                speed = mb / elapsed if elapsed > 0 else 0
                                status_label.config(text=f"Downloading: {filename} - {mb:.2f} MB ({speed:.2f} MB/s)")
                status_label.config(text=f"Download completed! File saved as: {filename}")
                return
        
        # Use 8 parallel connections with dynamic chunk size
        num_chunks = 8
        chunk_size = math.ceil(total_size / num_chunks)
        
        status_label.config(text=f"Downloading {filename} ({total_size / (1024*1024):.2f} MB) using {num_chunks} parallel connections")
        
        # Create temporary files for each chunk
        temp_files = []
        for i in range(num_chunks):
            start_byte = i * chunk_size
            end_byte = min(start_byte + chunk_size - 1, total_size - 1)
            temp_files.append((start_byte, end_byte, tempfile.NamedTemporaryFile(delete=False)))
        
        try:
            # Download chunks in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_chunks) as executor:
                # Submit all chunk downloads
                future_to_chunk = {
                    executor.submit(download_chunk, video_url, start, end, i, headers): i 
                    for i, (start, end, _) in enumerate(temp_files)
                }
                
                # Process completed chunks
                for future in concurrent.futures.as_completed(future_to_chunk):
                    chunk_num, chunk_data = future.result()
                    # Write chunk to temporary file
                    with open(temp_files[chunk_num][2].name, 'wb') as f:
                        f.write(chunk_data)
                    
                    # Update progress
                    if progress_var:
                        progress = ((chunk_num + 1) / num_chunks) * 100
                        progress_var.set(progress)
            
            # Merge chunks in order
            status_label.config(text="Merging chunks...")
            file_path = os.path.join(streamtape_folder, filename)
            with open(file_path, 'wb') as f:
                for _, _, temp_file in temp_files:
                    with open(temp_file.name, 'rb') as chunk_file:
                        f.write(chunk_file.read())
            
            status_label.config(text=f"Download completed! File saved as: {filename}")
            
        except Exception as e:
            if retry_count < 1:  # If we haven't retried yet
                status_label.config(text=f"Error during download, retrying... ({str(e)})")
                time.sleep(2)  # Wait 2 seconds before retry
                return download_from_streamtape(url, base_folder, status_label, progress_var, retry_count + 1)
            else:
                raise e  # Re-raise the exception if we've already retried
            
        finally:
            # Clean up temporary files
            for _, _, temp_file in temp_files:
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
        
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        download_complete_callback()
        
    except Exception as e:
        if retry_count < 1:  # If we haven't retried yet
            status_label.config(text=f"Error downloading from Streamtape, retrying... ({str(e)})")
            time.sleep(2)  # Wait 2 seconds before retry
            return download_from_streamtape(url, base_folder, status_label, progress_var, retry_count + 1)
        else:
            print(f"Error downloading from Streamtape: {e}")
            status_label.config(text=f"Error: {str(e)}")
            download_button.config(state='normal')
            cancel_button.config(state='disabled')

def start_download():
    global cancel_download
    cancel_download = False
    
    url = sanitize_url(url_entry.get())
    if not url:
        messagebox.showerror(get_text('error_title'), get_text('error_url'))
        return

    base_folder = folder_entry.get()
    
    if not base_folder:
        messagebox.showerror(get_text('error_title'), get_text('error_folder'))
        return
    
    download_button.config(state='disabled')
    cancel_button.config(state='normal')  
    progress_var.set(0)
    
    # Handle different URL types
    if is_bunkr_url(url):
        download_from_bunkr(url, base_folder)
    elif is_videzz_url(url):
        download_from_videzz(url, base_folder)
    elif is_gofile_url(url):
        download_from_gofile(url, base_folder, status_label, progress_var)
    elif is_pixeldrain_url(url):
        download_from_pixeldrain(url, base_folder, status_label, progress_var)
    elif is_streamtape_url(url):
        download_from_streamtape(url, base_folder, status_label, progress_var)
    elif is_vtube_url(url):  # Add vtube.network handling
        download_from_vtube(url, base_folder, status_label, progress_var)
    elif is_rubyvid_url(url):
        download_from_rubyvid(url, base_folder, status_label, progress_var)
    else:
        status_label.config(text="Unsupported URL type")
        download_button.config(state='normal')
        cancel_button.config(state='disabled')

def download_from_videzz(url, base_folder):
    """Handle downloading from videzz.net"""
    status_label.config(text="Extracting video from videzz.net...")
    
    # Create vidoza folder if it doesn't exist
    vidoza_folder = os.path.join(base_folder, "Vidoza")
    if not os.path.exists(vidoza_folder):
        os.makedirs(vidoza_folder)
    
    # Extract video URL
    video_url = extract_videzz_video(url)
    
    if not video_url:
        status_label.config(text="Could not extract video URL")
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        # Skip to next in queue if available
        download_complete_callback()
        return
    
    # Generate random filename
    original_extension = video_url.split('/')[-1].split('.')[-1]
    random_filename = generate_random_filename(original_extension)
    
    # Download the video
    status_label.config(text=f"Downloading video to {random_filename}")
    if download_with_progress(video_url, vidoza_folder, progress_var, status_label, custom_filename=random_filename):
        status_label.config(text="Video downloaded successfully")
        update_stats(stats_text, f"Download completed.\nVideo: {random_filename}\nSaved to: vidoza folder")
    else:
        status_label.config(text="Error downloading video")
    
    download_button.config(state='normal')
    cancel_button.config(state='disabled')
    download_complete_callback()

def download_from_bunkr(url, base_folder):
    """Handle downloading from bunkr.cr"""
    album_title = extract_album_title(url)
    # Fix potential encoding issues with Turkish characters
    album_title = fix_turkish_encoding(album_title)
    
    # Always download into a Bunkr folder inside the selected base folder
    bunkr_folder = os.path.join(base_folder, "Bunkr")
    if not os.path.exists(bunkr_folder):
        os.makedirs(bunkr_folder)
    folder = os.path.join(bunkr_folder, album_title)
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    status_label.config(text=get_text('collecting_links', title=album_title))

    links = extract_links(url)
    if not links:
        status_label.config(text=get_text('no_files'))
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        return

    image_links = []
    video_links = []
    other_links = []
    
    for link in links:
        extension = get_url_data(link)['extension'].lower()
        if extension in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'jfif']:
            image_links.append(link)
        elif extension in ['mp4', 'ts', 'webm', 'mpg', 'mov', 'm4v', 'mkv', 'mpeg', 'avi', 'wmv', 'flv']:
            video_links.append(link)
        else:
            other_links.append(link)

    total_files = len(image_links) + len(video_links) + len(other_links)
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
        status_label.config(text=get_text('checking_videos'))
        
        video_sizes = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://bunkr.cr/',
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

    if other_links and not cancel_download:
        for i, link in enumerate(other_links, 1):
            if cancel_download:
                status_label.config(text=get_text('download_cancelled'))
                break
            filename = get_url_data(link)['file_name']
            status_label.config(text=f"Diğer dosya indiriliyor: {filename} ({i}/{len(other_links)})")
            if download_with_progress(link, folder, progress_var, status_label):
                successful += 1
            else:
                failed += 1
            time.sleep(0.5)

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
        
        if current_clipboard != last_clipboard:
            # Check for multiple URLs (one per line)
            lines = current_clipboard.strip().split('\n')
            
            valid_urls = []
            for line in lines:
                line = line.strip()
                # Check if it's a valid URL from supported sites
                supported_url = False
                
                # Check if it's a Bunkr URL
                if any(domain in line for domain in SUPPORTED_SITES['bunkr']) and ('https://' in line or 'http://' in line):
                    supported_url = True
                    
                # Check if it's a Videzz URL
                elif any(domain in line for domain in SUPPORTED_SITES['videzz']) and ('https://' in line or 'http://' in line):
                    supported_url = True
                
                # Check if it's a GoFile URL
                elif any(domain in line for domain in SUPPORTED_SITES['gofile']) and ('https://' in line or 'http://' in line):
                    supported_url = True
                
                # Check if it's a PixelDrain URL
                elif 'pixeldrain.com' in line and ('https://' in line or 'http://' in line):
                    supported_url = True
                
                # Check if it's a Streamtape URL
                elif any(domain in line for domain in SUPPORTED_SITES['streamtape']) and ('https://' in line or 'http://' in line):
                    supported_url = True
                
                # Check if it's a vTube URL
                elif any(domain in line for domain in SUPPORTED_SITES['vtube']) and ('https://' in line or 'http://' in line):
                    supported_url = True
                
                # Check if it's a RubyVid URL
                elif any(domain in line for domain in SUPPORTED_SITES['rubyvid']) and ('https://' in line or 'http://' in line):
                    supported_url = True
                
                if supported_url:
                    valid_urls.append(line)
            
            if valid_urls:
                print(f"Found {len(valid_urls)} valid URLs in clipboard")
                
                if folder_entry.get():
                    for url in valid_urls:
                        download_queue.append(url)
                    
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
    global clipboard_status, clipboard_toggle, url_entry, folder_entry
    
    # Set default encoding to UTF-8
    import locale
    locale.setlocale(locale.LC_ALL, '')
    
    root = tk.Tk()
    
    # Force UTF-8 encoding for all text handling
    try:
        root.tk.eval('encoding system utf-8')
        root.option_add('*Font', 'TkDefaultFont')
    except Exception as e:
        print(f"Encoding setup error: {e}")
    
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
    
    # Marquee frame and label for supported sites
    marquee_frame = ttk.Frame(footer_frame)
    marquee_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    supported_sites_text = "    Desteklenen Siteler: Bunkr • Vidoza • GoFile • Pixeldrain • RubyVid • vTube • Streamtape"
    marquee_label = ttk.Label(
        marquee_frame,
        text=supported_sites_text,
        font=('Segoe UI', 8),
        foreground='gray'
    )
    marquee_label.pack(side=tk.LEFT)
    
    # Marquee animation function
    def animate_marquee():
        text = marquee_label.cget('text')
        text = text[1:] + text[0]
        marquee_label.config(text=text)
        root.after(100, animate_marquee)  # Update every 100ms
    
    # Start marquee animation
    root.after(100, animate_marquee)
    
    theme_button = ttk.Button(
        footer_frame,
        text="🌓 Tema Değiştir",
        command=lambda: toggle_theme(stats_text),
        style='Secondary.TButton',
        width=15
    )
    theme_button.pack(side=tk.RIGHT)
    
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
    # Fix Turkish character encoding issues in stats display
    message = fix_turkish_encoding(message)
    
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

def is_vtube_url(url):
    """Check if URL is from vtube.network or vtbe.to"""
    parsed_url = urlparse(url)
    return any(domain in parsed_url.netloc for domain in SUPPORTED_SITES['vtube'])

def download_from_vtube(url, base_folder, status_label=None, progress_var=None):
    """Handle downloading from vtube.network"""
    try:
        # Create vTube folder if it doesn't exist
        vtube_folder = os.path.join(base_folder, "vTube")
        if not os.path.exists(vtube_folder):
            os.makedirs(vtube_folder)
        
        status_label.config(text="Extracting video from vtube.network...")
        
        # Extract m3u8 URL
        m3u8_url = extract_video_url(url)
        
        if not m3u8_url:
            status_label.config(text="Could not extract video URL")
            download_button.config(state='normal')
            cancel_button.config(state='disabled')
            download_complete_callback()  # Add this line to move to next in queue
            return
        
        # Generate random filename
        output_filename = create_random_filename()
        output_path = os.path.join(vtube_folder, output_filename)
        
        # Check if FFmpeg is installed
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            status_label.config(text="FFmpeg not found. Please install FFmpeg and add it to PATH")
            download_button.config(state='normal')
            cancel_button.config(state='disabled')
            download_complete_callback()  # Add this line to move to next in queue
            return
        
        status_label.config(text=f"Downloading: {output_filename}")
        
        # FFmpeg command
        command = [
            "ffmpeg",
            "-i", m3u8_url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            "-movflags", "faststart",
            output_path
        ]
        
        # Run FFmpeg
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Update progress
        for line in process.stdout:
            if cancel_download:
                process.terminate()
                status_label.config(text=get_text('download_cancelled'))
                break
                
            line = line.strip()
            if "time=" in line:
                status_label.config(text=f"Downloading: {output_filename} - {line}")
                if progress_var:
                    # Try to extract progress percentage
                    match = re.search(r'time=(\d+:\d+:\d+\.\d+)', line)
                    if match:
                        time_str = match.group(1)
                        h, m, s = map(float, time_str.split(':'))
                        total_seconds = h * 3600 + m * 60 + s
                        # Estimate progress (assuming 10 minute video)
                        progress = min(100, (total_seconds / 600) * 100)
                        progress_var.set(progress)
        
        process.wait()
        
        if process.returncode == 0 and not cancel_download:
            status_label.config(text=get_text('download_complete'))
            update_stats(stats_text, f"Download completed.\nVideo: {output_filename}")
        else:
            status_label.config(text="Error downloading video")
        
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        download_complete_callback()
        
    except Exception as e:
        print(f"Error downloading from vtube.network: {e}")
        status_label.config(text=f"Error: {str(e)}")
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        download_complete_callback()  # Add this line to move to next in queue

def create_random_filename(prefix="video_", extension=".mp4"):
    """Generate a random filename"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}{random_string}{extension}"

def extract_video_url(url):
    """Extract video ID from vtube.network and create m3u8 URL"""
    # Different User-Agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    ]
    
    # Select a random User-Agent
    user_agent = random.choice(user_agents)
    
    # Request headers
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "tr-TR,tr;q=0.9",
        "Connection": "keep-alive",
        "Host": url.split('/')[2],
        "User-Agent": user_agent,
        "Referer": "https://www.google.com/",
        "sec-ch-ua": '"Chromium";v="135", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }
    
    session = requests.Session()
    
    try:
        # Send request
        response = session.get(url, headers=headers, timeout=30)
        
        # Check if request was successful
        if response.status_code == 200:
            # Get HTML content
            html_content = response.text
            
            # Search for the pattern
            pattern = r"\|urlset\|(.*?)\|hls\|"
            matches = re.findall(pattern, html_content)
            
            if matches:
                video_id = matches[0]
                # Create URL
                m3u8_url = f"https://str12.vtube.network/hls/{video_id}/master.m3u8"
                return m3u8_url
            else:
                # Save output to file for debugging
                with open("vtube_response.html", "w", encoding="utf-8") as f:
                    f.write(html_content)
                return None
        else:
            return None

    except Exception as e:
        return None

def is_rubyvid_url(url):
    """Check if URL is from rubyvid.com"""
    parsed_url = urlparse(url)
    return any(domain in parsed_url.netloc for domain in SUPPORTED_SITES['rubyvid'])

def extract_rubyvid_m3u8(html_content):
    """Extract m3u8 URLs from RubyVid HTML content"""
    pattern = r"eval\(function\(p,a,c,k,e,d\){while\(c--\)if\(k\[c\]\)p=p\.replace\(new RegExp\(\'\\\\b\'\+c\.toString\(a\)\+\'\\\\b\',\'g\'\),k\[c\]\);return p}\(\'(.*?)\',(\d+),(\d+),\'(.*?)\'.split\(\'\|\'\)\)\)"
    match = re.search(pattern, html_content, re.DOTALL)

    if not match:
        return []

    p = match.group(1)
    a = int(match.group(2))
    k = match.group(4).split('|')

    def replace(match):
        num = int(match.group(0), a)
        return k[num] if 0 <= num < len(k) and k[num] else match.group(0)

    decoded = re.sub(r'\b\w+\b', replace, p)

    url_patterns = [
        r'https?://[^"\']*?\.m3u8[^"\']*',
    ]

    for pattern in url_patterns:
        url_matches = re.findall(pattern, decoded)
        clean_urls = []
        for url in url_matches:
            # Sadece kalite belirten kısmı düzelt
            url = re.sub(r'([/_])([a-z,]*h[a-z,]*)[,.]', r'\1h,.', url)  # örn: _l,n,h,  -> _h.
            clean_urls.append(url)

        if clean_urls:
            return clean_urls

    return []

def fetch_rubyvid_html(url):
    """Fetch HTML content from RubyVid URL"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "sec-ch-ua": '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching RubyVid URL: {e}")
        return None

def download_from_rubyvid(url, base_folder, status_label=None, progress_var=None):
    """Handle downloading from rubyvid.com"""
    try:
        # RubyVid klasörü oluştur
        rubyvid_folder = os.path.join(base_folder, "RubyVid")
        if not os.path.exists(rubyvid_folder):
            os.makedirs(rubyvid_folder)
            
        status_label.config(text="Extracting video from rubyvid.com...")
        
        # HTML içeriğini çek
        html = fetch_rubyvid_html(url)
        if not html:
            status_label.config(text="Could not fetch RubyVid page")
            download_button.config(state='normal')
            cancel_button.config(state='disabled')
            download_complete_callback()
            return
            
        # m3u8 URL'lerini çıkar
        m3u8_urls = extract_rubyvid_m3u8(html)
        if not m3u8_urls:
            # Fallback: Doğrudan HTML'den m3u8 URL'lerini ara
            m3u8_urls = re.findall(r'https?://[^"\']*?\.m3u8[^"\']*', html)
            if m3u8_urls:
                m3u8_urls = [re.sub(r'([/_])([a-z,]*h[a-z,]*)[,.]', r'\1h.', url) for url in m3u8_urls]
                
        if not m3u8_urls:
            status_label.config(text="Could not extract video URL")
            download_button.config(state='normal')
            cancel_button.config(state='disabled')
            download_complete_callback()
            return
            
        # İlk m3u8 URL'sini kullan
        m3u8_url = m3u8_urls[0]
        
        # Rastgele dosya adı
        output_filename = create_random_filename()
        output_path = os.path.join(rubyvid_folder, output_filename)
        
        # FFmpeg kontrolü
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            status_label.config(text="FFmpeg not found. Please install FFmpeg and add it to PATH")
            download_button.config(state='normal')
            cancel_button.config(state='disabled')
            return
            
        status_label.config(text=f"Downloading: {output_filename}")
        
        # FFmpeg komutu
        command = [
            "ffmpeg",
            "-i", m3u8_url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            "-movflags", "faststart",
            output_path
        ]
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        for line in process.stdout:
            if cancel_download:
                process.terminate()
                status_label.config(text=get_text('download_cancelled'))
                break
                
            line = line.strip()
            if "time=" in line:
                status_label.config(text=f"Downloading: {output_filename} - {line}")
                if progress_var:
                    match = re.search(r'time=(\d+:\d+:\d+\.\d+)', line)
                    if match:
                        time_str = match.group(1)
                        h, m, s = map(float, time_str.split(':'))
                        total_seconds = h * 3600 + m * 60 + s
                        progress = min(100, (total_seconds / 600) * 100)  # 10 dakika varsayılan süre
                        progress_var.set(progress)
                        
        process.wait()
        
        if process.returncode == 0 and not cancel_download:
            status_label.config(text=get_text('download_complete'))
            update_stats(stats_text, f"Download completed.\nVideo: {output_filename}")
        else:
            status_label.config(text="Error downloading video")
            
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        download_complete_callback()
        
    except Exception as e:
        print(f"Error downloading from rubyvid.com: {e}")
        status_label.config(text=f"Error: {str(e)}")
        download_button.config(state='normal')
        cancel_button.config(state='disabled')
        download_complete_callback()

if __name__ == "__main__":
    # Ensure the script is running with UTF-8 encoding
    if sys.stdout is not None and getattr(sys.stdout, "encoding", None) and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Force file operations to use UTF-8
    try:
        # Patch the built-in open function to use UTF-8 by default
        builtin_open = open
        def utf8_open(*args, **kwargs):
            if 'encoding' not in kwargs and 'b' not in args[1]:
                kwargs['encoding'] = 'utf-8'
            return builtin_open(*args, **kwargs)
        
        # Replace the built-in open with our UTF-8 version
        import builtins
        builtins.open = utf8_open
    except Exception as e:
        print(f"Error setting UTF-8 for file operations: {e}")
    
    root, url_entry, folder_entry, progress_var, status_label, download_button, stats_text = create_gui()
    root.mainloop() 