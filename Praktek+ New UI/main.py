# main.py - Entry point for the application
import os
import sys
from colorama import init, Fore, Back, Style
from modules.auth import authenticate_user
from modules.admin import admin_menu
from modules.doctor import doctor_menu
from modules.patient import patient_menu
from modules.data_manager import initialize_data
from modules.utils import clear_screen, show_breadcrumbs, show_help, display_header

init(autoreset=True)

def main_menu():
    """Display the main menu of the application without frame."""
    clear_screen()
    # Menggunakan display_header yang ada, asumsikan bisa dimodifikasi untuk tanpa bingkai jika perlu
    display_header("SELAMAT DATANG DI APLIKASI PRAKTEK+", "Sistem Manajemen Jadwal Dokter Klinik") #

    print(Fore.CYAN + Style.BRIGHT + "MENU UTAMA" + Style.RESET_ALL)
    print(Fore.CYAN + "-" * 35 + Style.RESET_ALL) # Garis pemisah

    print(Fore.WHITE + "  " + Style.BRIGHT + "1. " + Fore.YELLOW + "Login") #
    print(Fore.WHITE + "  " + Style.BRIGHT + "2. " + Fore.YELLOW + "Registrasi (Khusus Pasien)") #
    print(Fore.WHITE + "  " + Style.BRIGHT + "3. " + Fore.RED   + "Keluar Aplikasi") # Diubah agar warna konsisten dengan fungsi
    print(Fore.CYAN + "-" * 35 + Style.RESET_ALL)
    print(Fore.WHITE + "  " + Style.BRIGHT + "?. " + Fore.GREEN + "Bantuan") #
    print()

    choice = input(Fore.MAGENTA + Style.BRIGHT + "➔ Pilihan Anda: " + Fore.WHITE) #

    if choice == "1": #
        user_type, user_id = authenticate_user() #
        if user_type == "admin": #
            admin_menu(user_id) #
        elif user_type == "dokter": #
            doctor_menu(user_id) #
        elif user_type == "pasien": #
            patient_menu(user_id) #
        else:
            # Pesan error sudah ditangani di authenticate_user atau utils.show_error
            # Jika authenticate_user mengembalikan None, None, show_error sudah dipanggil
            # Cukup kembali ke menu utama
            main_menu()
    elif choice == "2": #
        from modules.auth import register_patient #
        register_patient() #
        main_menu()
    elif choice == "3": #
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "\n🙏 Terima kasih telah menggunakan Praktek+.\n   Semoga harimu menyenangkan!\n")
        sys.exit() #
    elif choice == "?": #
        show_help("main") #
        main_menu()
    else:
        # Menggunakan show_error dari utils untuk konsistensi
        from modules.utils import show_error
        show_error("Pilihan tidak valid. Mohon masukkan pilihan yang benar.")
        main_menu()

if __name__ == "__main__":
    if not os.path.exists("data"): #
        os.makedirs("data") #

    initialize_data() #

    try:
        while True:
            main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "\n🙏 Keluar dari aplikasi. Terima kasih telah menggunakan Praktek+!\n") #
        sys.exit() #