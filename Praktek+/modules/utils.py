# modules/utils.py
import os
import sys
import time
import threading
from colorama import Fore, Back, Style

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_breadcrumbs(path):
    """Display navigation breadcrumbs."""
    print(Fore.WHITE + Style.DIM + " > ".join(path))
    print()

def show_error(message):
    """Display an error message."""
    print(Fore.RED + f"ERROR: {message}")
    input(Fore.GREEN + "Tekan Enter untuk melanjutkan...")

def show_success(message):
    """Display a success message."""
    print(Fore.GREEN + f"SUKSES: {message}")
    input(Fore.GREEN + "Tekan Enter untuk melanjutkan...")

def show_help(context):
    """Display help information based on context."""
    clear_screen()
    print(Fore.CYAN + "=" * 70)
    print(Fore.CYAN + Style.BRIGHT + f"BANTUAN: {context}")
    print(Fore.CYAN + "=" * 70)
    
    if context == "main":
        print(Fore.YELLOW + "Cara Menggunakan Praktek+:")
        print(Fore.WHITE + "- Gunakan angka untuk memilih menu")
        print(Fore.WHITE + "- Tekan Enter untuk melanjutkan setelah melihat informasi")
        print(Fore.WHITE + "- Untuk keluar dari aplikasi, pilih opsi Keluar di menu utama")
    
    elif context == "admin":
        print(Fore.YELLOW + "Panduan Menu Admin:")
        print(Fore.WHITE + "- Lihat Semua Jadwal: Melihat semua jadwal dokter yang terdaftar")
        print(Fore.WHITE + "- Tambah Jadwal: Menambahkan jadwal praktik baru untuk dokter")
        print(Fore.WHITE + "- Edit Jadwal: Mengubah jadwal yang sudah ada")
        print(Fore.WHITE + "- Hapus Jadwal: Menghapus jadwal yang sudah tidak diperlukan")
        print(Fore.WHITE + "- Lihat Data Pasien: Melihat semua pasien yang terdaftar")
        print(Fore.WHITE + "- Lihat Pendaftaran: Melihat semua pendaftaran konsultasi")
        print(Fore.WHITE + "- Lihat Statistik: Melihat statistik klinik")
    
    elif context == "doctor":
        print(Fore.YELLOW + "Panduan Menu Dokter:")
        print(Fore.WHITE + "- Lihat Jadwal Praktik: Melihat jadwal praktik Anda")
        print(Fore.WHITE + "- Tambah Jadwal: Menambahkan jadwal praktik baru")
        print(Fore.WHITE + "- Edit Jadwal: Mengubah jadwal yang sudah ada")
        print(Fore.WHITE + "- Lihat Pasien Terdaftar: Melihat pasien yang terdaftar pada jadwal Anda")
    
    elif context == "patient":
        print(Fore.YELLOW + "Panduan Menu Pasien:")
        print(Fore.WHITE + "- Lihat Jadwal Dokter: Melihat semua jadwal dokter yang tersedia")
        print(Fore.WHITE + "- Cari Jadwal Dokter: Mencari jadwal berdasarkan nama dokter/spesialisasi/hari")
        print(Fore.WHITE + "- Mendaftar Konsultasi: Mendaftar untuk konsultasi dokter")
        print(Fore.WHITE + "- Mengajukan Perubahan Jadwal: Mengubah atau membatalkan pendaftaran")
        print(Fore.WHITE + "- Lihat Status Pendaftaran: Melihat status pendaftaran Anda")
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali...")

class LoadingAnimation:
    def __init__(self, message="Loading..."):
        self.message = message
        self.is_running = False
        self.animation_thread = None
    
    def start(self):
        self.is_running = True
        self.animation_thread = threading.Thread(target=self._animate)
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def stop(self):
        self.is_running = False
        if self.animation_thread:
            self.animation_thread.join()
        # Clear the loading line
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()
    
    def _animate(self):
        chars = "|/-\\"
        idx = 0
        while self.is_running:
            sys.stdout.write("\r" + Fore.YELLOW + self.message + " " + chars[idx % len(chars)])
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)