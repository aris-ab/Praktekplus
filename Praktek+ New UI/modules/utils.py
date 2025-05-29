# modules/utils.py
import os
import sys
import time
import threading
import re # Untuk validasi format waktu
from colorama import Fore, Back, Style

def clear_screen(): #
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear') #

def display_header(title, subtitle=None, width=50, use_frame=True, top_char="═", side_char="║", corner_char="╔╗╚╝"): #
    """Display a formatted header, optionally without frame."""
    clear_screen() # Pindahkan clear_screen ke awal pemanggilan fungsi menu jika header tidak selalu membersihkan layar
    if use_frame:
        print(Fore.CYAN + Style.BRIGHT + corner_char[0] + top_char * (width - 2) + corner_char[1])
        print(side_char + title.center(width - 2) + side_char)
        if subtitle:
            print(side_char + subtitle.center(width - 2) + side_char)
        print(corner_char[2] + top_char * (width - 2) + corner_char[3] + Style.RESET_ALL)
    else:
        print(Fore.CYAN + Style.BRIGHT + title.center(width) + Style.RESET_ALL)
        if subtitle:
            print(Fore.CYAN + Style.NORMAL + subtitle.center(width) + Style.RESET_ALL)
    print()

def display_subheader(title, width=50, char="-"): #
    """Display a formatted subheader."""
    print(Fore.CYAN + Style.BRIGHT + title.center(width, char) + Style.RESET_ALL)
    print() # Spasi setelah subheader

def show_breadcrumbs(path): #
    """Display navigation breadcrumbs."""
    breadcrumb_str = Fore.WHITE + Style.DIM + "📍 Lokasi: "
    for i, p_item in enumerate(path):
        breadcrumb_str += p_item
        if i < len(path) - 1:
            breadcrumb_str += Fore.WHITE + Style.DIM + " > "
    breadcrumb_str += Style.RESET_ALL
    print(breadcrumb_str)
    print()

def show_error(message): #
    """Display an error message."""
    print(Back.RED + Fore.WHITE + Style.BRIGHT + f"⛔ ERROR: {message}" + Style.RESET_ALL)
    input(Fore.YELLOW + Style.BRIGHT + "\nTekan Enter untuk melanjutkan..." + Style.RESET_ALL)

def show_success(message): #
    """Display a success message."""
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + f"✅ SUKSES: {message}" + Style.RESET_ALL)
    input(Fore.YELLOW + Style.BRIGHT + "\nTekan Enter untuk melanjutkan..." + Style.RESET_ALL)

def is_valid_time_format(time_str): #
    """Validate time format HH:MM."""
    return re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time_str) is not None

def show_help(context):
    """Display help information based on context."""
    clear_screen()
    # Menggunakan display_header dengan bingkai untuk halaman bantuan agar menonjol
    display_header(f"BANTUAN APLIKASI: {context.upper()}", width=70, use_frame=True)

    help_text = {
        "main": [
            (Fore.YELLOW + "  Selamat datang di Praktek+!", ""),
            (Fore.WHITE + "  Ini adalah sistem manajemen jadwal dokter klinik.", ""),
            (Fore.CYAN + "\n  Navigasi Utama:", ""),
            (Fore.WHITE + "  - Gunakan " + Style.BRIGHT + "angka" + Style.NORMAL + " pada keyboard untuk memilih opsi menu.", ""),
            (Fore.WHITE + "  - Tekan " + Style.BRIGHT + "Enter" + Style.NORMAL + " untuk melanjutkan setelah setiap aksi atau pesan.", ""),
            (Fore.WHITE + "  - Opsi " + Style.BRIGHT + "'?'" + Style.NORMAL + " akan menampilkan layar bantuan ini.", ""),
            (Fore.WHITE + "  - Untuk keluar, pilih opsi " + Style.BRIGHT + "'Keluar'" + Style.NORMAL + " dari menu utama.", "")
        ],
        "admin": [
            (Fore.YELLOW + "  Panduan Menu Admin:", ""),
            (Fore.CYAN + "\n  Manajemen Jadwal Dokter:", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Lihat Semua Jadwal:" + Style.NORMAL + " Menampilkan semua jadwal dokter yang ada.", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Tambah Jadwal:" + Style.NORMAL + " Menambahkan jadwal praktik baru untuk dokter.", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Edit Jadwal:" + Style.NORMAL + " Mengubah detail jadwal yang sudah ada.", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Hapus Jadwal:" + Style.NORMAL + " Menghapus jadwal (hanya jika tidak ada pendaftaran aktif).", ""),
            (Fore.CYAN + "\n  Manajemen Data & Statistik:", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Lihat Data Pasien:" + Style.NORMAL + " Menampilkan semua pasien yang terdaftar di sistem.", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Lihat Pendaftaran:" + Style.NORMAL + " Melihat semua riwayat pendaftaran konsultasi.", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Lihat Statistik:" + Style.NORMAL + " Menampilkan statistik penting klinik.", "")
        ],
        "doctor": [
            (Fore.YELLOW + "  Panduan Menu Dokter:", ""),
            (Fore.CYAN + "\n  Manajemen Jadwal Pribadi:", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Lihat Jadwal Praktik Saya:" + Style.NORMAL + " Menampilkan semua jadwal praktik Anda.", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Tambah Jadwal Praktik:" + Style.NORMAL + " Membuat jadwal praktik baru untuk Anda.", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Edit Jadwal Praktik:" + Style.NORMAL + " Mengubah detail jadwal praktik Anda yang sudah ada.", ""),
            (Fore.CYAN + "\n  Manajemen Pasien:", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Lihat Pasien Terdaftar:" + Style.NORMAL + " Menampilkan pasien yang terdaftar pada jadwal praktik Anda.", "")
        ],
        "patient": [
            (Fore.YELLOW + "  Panduan Menu Pasien:", ""),
            (Fore.CYAN + "\n  Pencarian & Pendaftaran Konsultasi:", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Lihat Jadwal Dokter:" + Style.NORMAL + " Menampilkan semua jadwal dokter yang tersedia.", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Cari Jadwal Dokter:" + Style.NORMAL + " Mencari jadwal berdasarkan nama dokter, spesialisasi, atau hari.", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Mendaftar Konsultasi:" + Style.NORMAL + " Melakukan pendaftaran untuk konsultasi dengan dokter.", ""),
            (Fore.CYAN + "\n  Manajemen Pendaftaran Pribadi:", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Ubah/Batalkan Pendaftaran:" + Style.NORMAL + " Membatalkan pendaftaran yang sudah dibuat.", ""),
            (Fore.WHITE + "  - " + Style.BRIGHT + "Lihat Status Pendaftaran Saya:" + Style.NORMAL + " Melihat status semua pendaftaran Anda.", "")
        ]
    }

    if context in help_text:
        for line, note in help_text[context]:
            # Perbaikan di sini: Menggunakan Style.DIM bukan Fore.DIM
            print(f"{line}{Style.DIM}{note}{Style.RESET_ALL}") #
    else:
        print(Fore.RED + "  Konteks bantuan tidak ditemukan.")
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu sebelumnya..." + Style.RESET_ALL)


class LoadingAnimation: #
    def __init__(self, message=Fore.YELLOW + "Memuat..." + Style.RESET_ALL): #
        self.message = message
        self.is_running = False #
        self.animation_thread = None #
        self._lock = threading.Lock()

    def start(self): #
        self.is_running = True #
        self.animation_thread = threading.Thread(target=self._animate, daemon=True) #
        self.animation_thread.start() #

    def stop(self): #
        self.is_running = False #
        if self.animation_thread: #
            self.animation_thread.join() #
        with self._lock:
            sys.stdout.write("\r" + " " * (len(str(self.message)) + 15) + "\r") #
            sys.stdout.flush() #

    def _animate(self): #
        chars = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        idx = 0
        while self.is_running: #
            with self._lock:
                # Hapus baris sebelumnya sebelum mencetak yang baru
                # Pastikan self.message adalah string untuk len()
                current_message = str(self.message)
                sys.stdout.write("\r" + " " * (len(current_message) + 15) + "\r")
                sys.stdout.write(Fore.MAGENTA + Style.BRIGHT + "\r⚙️  " + current_message + " " + chars[idx % len(chars)] + Style.RESET_ALL)
                sys.stdout.flush() #
            idx += 1
            time.sleep(0.08)
