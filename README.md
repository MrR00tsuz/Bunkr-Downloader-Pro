# Bunkr Downloader Pro

Bunkr Downloader Pro is a powerful and user-friendly application that allows you to download content from various file hosting services including Bunkr, GoFile, Pixeldrain, Streamtape, vTube, and RubyVid. The application features a modern GUI with support for multiple languages and themes.

![Bunkr Downloader Pro](https://github.com/user-attachments/assets/81237149-3441-4442-bfaf-7df0d524703e)


## Features

- **Multi-Platform Support**: Works on Windows, macOS, and Linux
- **Multiple Service Support**:
  - Bunkr (bunkr.cr, bunkr.ru, bunkr.red, etc.)
  - GoFile (gofile.io)
  - Pixeldrain (pixeldrain.com)
  - Streamtape (streamtape.com)
  - vTube (vtube.network, vtbe.to)
  - RubyVid (rubyvid.com, stmruby.com, rubystm.com)
- **User-Friendly Interface**:
  - Dark/Light theme support
  - Bilingual support (English/Turkish)
  - Progress tracking
  - Download statistics
  - Clipboard monitoring for automatic downloads
- **Advanced Features**:
  - Parallel downloads
  - Automatic folder creation
  - Support for password-protected GoFile links
  - Video quality selection
  - Download queue management

## Requirements

- Python 3.7 or higher
- Required Python packages:
  ```
  requests
  beautifulsoup4
  tkinter
  sv_ttk
  ```
- FFmpeg (required for video downloads from vTube and RubyVid)

## Installation

### Windows
1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install FFmpeg:
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Add FFmpeg to your system PATH
3. Install required packages:
   ```bash
   pip install requests beautifulsoup4 sv_ttk
   ```

### macOS
1. Install Python using Homebrew:
   ```bash
   brew install python
   ```
2. Install FFmpeg:
   ```bash
   brew install ffmpeg
   ```
3. Install required packages:
   ```bash
   pip3 install requests beautifulsoup4 sv_ttk
   ```

### Linux
1. Install Python and FFmpeg:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip ffmpeg

   # Fedora
   sudo dnf install python3 python3-pip ffmpeg
   ```
2. Install required packages:
   ```bash
   pip3 install requests beautifulsoup4 sv_ttk
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Basic Usage:
   - Enter the download URL in the "Download Link" field
   - Select the destination folder using the "Browse" button
   - Click "Start Download" to begin
   - Monitor progress in the "Download Progress" section
   - View statistics in the "Download Statistics" section

3. Advanced Features:
   - **Clipboard Monitoring**: Enable/disable automatic download of copied URLs
   - **Theme Switching**: Toggle between dark and light themes
   - **Language Switching**: Switch between English and Turkish
   - **Download Queue**: Multiple URLs can be queued for sequential downloading

## Supported File Types

- Images: JPG, JPEG, PNG, GIF, WEBP, JFIF
- Videos: MP4, TS, WEBM, MPG, MOV, M4V, MKV, MPEG, AVI, WMV, FLV
- Archives: ZIP, RAR, 7Z, TAR
- Documents: PDF
- Audio: MP3, M4A

## Troubleshooting

1. **FFmpeg Not Found**:
   - Ensure FFmpeg is installed and added to your system PATH
   - Restart the application after installation

2. **Download Failures**:
   - Check your internet connection
   - Verify the URL is valid and accessible
   - Try using a different service if available

3. **Encoding Issues**:
   - The application automatically handles Turkish character encoding
   - If issues persist, ensure your system locale is set correctly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request..

## Disclaimer

This application is intended for downloading content that you have the right to access. Please respect copyright laws and terms of service of the supported platforms. 


# Bunkr Downloader Pro

Bunkr Downloader Pro, Bunkr, GoFile, Pixeldrain, Streamtape, vTube ve RubyVid gibi çeşitli dosya barındırma servislerinden içerik indirmenize olanak sağlayan güçlü ve kullanıcı dostu bir uygulamadır. Modern bir arayüze sahip olan uygulama, çoklu dil ve tema desteği sunmaktadır.

![Bunkr Downloader Pro](https://github.com/user-attachments/assets/81237149-3441-4442-bfaf-7df0d524703e)

## Özellikler

- **Çoklu Platform Desteği**: Windows, macOS ve Linux'ta çalışır
- **Çoklu Servis Desteği**:
  - Bunkr (bunkr.cr, bunkr.ru, bunkr.red, vb.)
  - GoFile (gofile.io)
  - Pixeldrain (pixeldrain.com)
  - Streamtape (streamtape.com)
  - vTube (vtube.network, vtbe.to)
  - RubyVid (rubyvid.com, stmruby.com, rubystm.com)
- **Kullanıcı Dostu Arayüz**:
  - Koyu/Açık tema desteği
  - İki dilli destek (İngilizce/Türkçe)
  - İndirme ilerleme takibi
  - İndirme istatistikleri
  - Otomatik indirme için pano izleme
- **Gelişmiş Özellikler**:
  - Paralel indirmeler
  - Otomatik klasör oluşturma
  - Şifre korumalı GoFile bağlantıları desteği
  - Video kalite seçimi
  - İndirme kuyruğu yönetimi

## Gereksinimler

- Python 3.7 veya üzeri
- Gerekli Python paketleri:
  ```
  requests
  beautifulsoup4
  tkinter
  sv_ttk
  ```
- FFmpeg (vTube ve RubyVid'den video indirmeleri için gerekli)

## Kurulum

### Windows
1. Python'u [python.org](https://www.python.org/downloads/) adresinden indirin ve kurun
2. FFmpeg'i kurun:
   - [ffmpeg.org](https://ffmpeg.org/download.html) adresinden indirin
   - FFmpeg'i sistem PATH'inize ekleyin
3. Gerekli paketleri yükleyin:
   ```bash
   pip install requests beautifulsoup4 sv_ttk
   ```

### macOS
1. Homebrew ile Python'u kurun:
   ```bash
   brew install python
   ```
2. FFmpeg'i kurun:
   ```bash
   brew install ffmpeg
   ```
3. Gerekli paketleri yükleyin:
   ```bash
   pip3 install requests beautifulsoup4 sv_ttk
   ```

### Linux
1. Python ve FFmpeg'i kurun:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip ffmpeg

   # Fedora
   sudo dnf install python3 python3-pip ffmpeg
   ```
2. Gerekli paketleri yükleyin:
   ```bash
   pip3 install requests beautifulsoup4 sv_ttk
   ```

## Kullanım

1. Uygulamayı çalıştırın:
   ```bash
   python main.py
   ```

2. Temel Kullanım:
   - "İndirme Linki" alanına URL'yi girin
   - "Gözat" düğmesini kullanarak hedef klasörü seçin
   - "İndirmeyi Başlat" düğmesine tıklayın
   - "İndirme Durumu" bölümünden ilerlemeyi takip edin
   - "İndirme İstatistikleri" bölümünden istatistikleri görüntüleyin

3. Gelişmiş Özellikler:
   - **Pano İzleme**: Kopyalanan URL'lerin otomatik indirilmesini etkinleştirin/devre dışı bırakın
   - **Tema Değiştirme**: Koyu ve açık temalar arasında geçiş yapın
   - **Dil Değiştirme**: İngilizce ve Türkçe arasında geçiş yapın
   - **İndirme Kuyruğu**: Birden fazla URL sırayla indirilebilir

## Desteklenen Dosya Türleri

- Resimler: JPG, JPEG, PNG, GIF, WEBP, JFIF
- Videolar: MP4, TS, WEBM, MPG, MOV, M4V, MKV, MPEG, AVI, WMV, FLV
- Arşivler: ZIP, RAR, 7Z, TAR
- Belgeler: PDF
- Ses: MP3, M4A

## Sorun Giderme

1. **FFmpeg Bulunamadı**:
   - FFmpeg'in kurulu olduğundan ve sistem PATH'inize eklendiğinden emin olun
   - Kurulumdan sonra uygulamayı yeniden başlatın

2. **İndirme Hataları**:
   - İnternet bağlantınızı kontrol edin
   - URL'nin geçerli ve erişilebilir olduğunu doğrulayın
   - Mümkünse farklı bir servis kullanmayı deneyin

3. **Kodlama Sorunları**:
   - Uygulama Türkçe karakter kodlamasını otomatik olarak yönetir
   - Sorun devam ederse sistem yerel ayarlarınızın doğru ayarlandığından emin olun

## Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen çekme isteği (Pull Request) göndermekten çekinmeyin.

## Sorumluluk Reddi

Bu uygulama, erişim hakkınız olan içerikleri indirmek için tasarlanmıştır. Lütfen telif hakkı yasalarına ve desteklenen platformların kullanım koşullarına saygı gösterin.
