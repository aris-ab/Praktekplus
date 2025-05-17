# main.py - Entry point for the application
import os
import sys
from colorama import init, Fore, Back, Style
from modules.auth import authenticate_user
from modules.admin import admin_menu
from modules.doctor import doctor_menu
from modules.patient import patient_menu
from modules.data_manager import initialize_data
from modules.utils import clear_screen, show_breadcrumbs, show_help

init(autoreset=True)  # Initialize colorama with autoreset

def main_menu():
    """Display the main menu of the application."""
    clear_screen()
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "SELAMAT DATANG DI APLIKASI PRAKTEK+")
    print(Fore.CYAN + Style.BRIGHT + "Sistem Manajemen Jadwal Dokter Klinik")
    print(Fore.CYAN + "=" * 50)
    print(Fore.WHITE + "1. " + Fore.YELLOW + "Login")
    print(Fore.WHITE + "2. " + Fore.YELLOW + "Registrasi (Khusus Pasien)")
    print(Fore.WHITE + "3. " + Fore.YELLOW + "Keluar")
    print(Fore.WHITE + "?. " + Fore.YELLOW + "Bantuan")
    
    choice = input(Fore.GREEN + "\nPilihan Anda: " + Fore.WHITE)
    
    if choice == "1":
        user_type, user_id = authenticate_user()
        if user_type == "admin":
            admin_menu(user_id)
        elif user_type == "dokter":
            doctor_menu(user_id)
        elif user_type == "pasien":
            patient_menu(user_id)
        else:
            print(Fore.RED + "Login gagal. Silakan coba lagi.")
            input(Fore.GREEN + "Tekan Enter untuk melanjutkan...")
            main_menu()
    elif choice == "2":
        from modules.auth import register_patient
        register_patient()
        main_menu()
    elif choice == "3":
        print(Fore.CYAN + "Terima kasih telah menggunakan Praktek+.")
        sys.exit()
    elif choice == "?":
        show_help("main")
        main_menu()
    else:
        print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")
        input(Fore.GREEN + "Tekan Enter untuk melanjutkan...")
        main_menu()

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Initialize data if files don't exist
    initialize_data()
    
    try:
        while True:
            main_menu()
    except KeyboardInterrupt:
        print(Fore.CYAN + "\nKeluar dari aplikasi. Terima kasih!")
        sys.exit()