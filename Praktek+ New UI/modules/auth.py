# modules/auth.py - Authentication module
import csv
import os
from colorama import Fore, Style
from .data_structures.linked_list import LinkedList
from .data_manager import read_csv, write_csv #
from .utils import clear_screen, show_error, show_success, display_header

def authenticate_user(): #
    """Authenticate a user and return user type and ID."""
    clear_screen() #
    display_header("LOGIN PENGGUNA", width=50) #

    print(Fore.CYAN + "  Silakan masukkan kredensial Anda:" + Style.RESET_ALL)
    username = input(Fore.YELLOW + Style.BRIGHT + "  👤 Username: " + Fore.WHITE) #
    password = input(Fore.YELLOW + Style.BRIGHT + "  🔑 Password: " + Fore.WHITE) #
    print()

    # Check admin credentials
    admin_data = read_csv("data/admin.csv") #
    for admin in admin_data: #
        if admin['username'] == username and admin['password'] == password: #
            print(Fore.GREEN + Style.BRIGHT + "  Login sebagai Admin berhasil!")
            input(Fore.GREEN + Style.BRIGHT + "\n  Tekan Enter untuk melanjutkan..." + Style.RESET_ALL)
            return "admin", admin['id'] #

    # Check doctor credentials
    doctor_data = read_csv("data/dokter.csv") #
    for doctor in doctor_data: #
        if doctor['username'] == username and doctor['password'] == password: #
            print(Fore.GREEN + Style.BRIGHT + f"  Login sebagai Dokter ({doctor['nama']}) berhasil!") #
            input(Fore.GREEN + Style.BRIGHT + "\n  Tekan Enter untuk melanjutkan..." + Style.RESET_ALL)
            return "dokter", doctor['id'] #

    # Check patient credentials
    patient_data = read_csv("data/pasien.csv") #
    for patient in patient_data: #
        if patient['username'] == username and patient['password'] == password: #
            print(Fore.GREEN + Style.BRIGHT + f"  Login sebagai Pasien ({patient['nama']}) berhasil!") #
            input(Fore.GREEN + Style.BRIGHT + "\n  Tekan Enter untuk melanjutkan..." + Style.RESET_ALL)
            return "pasien", patient['id'] #

    show_error("Username atau password salah.") #
    return None, None #

def register_patient(): #
    """Register a new patient."""
    clear_screen() #
    display_header("REGISTRASI PASIEN BARU", width=50) #

    print(Fore.CYAN + "  Mohon isi data diri Anda dengan lengkap:" + Style.RESET_ALL)
    name = input(Fore.YELLOW + Style.BRIGHT + "  Nama Lengkap   : " + Fore.WHITE) #
    username = input(Fore.YELLOW + Style.BRIGHT + "  Username       : " + Fore.WHITE) #
    password = input(Fore.YELLOW + Style.BRIGHT + "  Password       : " + Fore.WHITE) #
    contact = input(Fore.YELLOW + Style.BRIGHT + "  Nomor Telepon  : " + Fore.WHITE) #
    print()

    if not name or not username or not password or not contact: #
        show_error("Semua field harus diisi!") #
        return

    if not contact.isdigit():
        show_error("Nomor telepon harus berupa angka.")
        return

    patient_data = read_csv("data/pasien.csv") #
    for patient in patient_data: #
        if patient['username'] == username: #
            show_error("Username sudah digunakan. Silakan coba username lain.") #
            return

    new_id = f"P{len(patient_data) + 1:03d}" #
    new_patient = { #
        'id': new_id, #
        'nama': name, #
        'username': username, #
        'password': password, #
        'kontak': contact #
    }
    patient_data.append(new_patient) #
    write_csv("data/pasien.csv", patient_data) #
    show_success(f"Registrasi berhasil! ID Pasien Anda adalah {Fore.YELLOW}{new_id}{Fore.GREEN}.") #