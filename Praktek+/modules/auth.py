# modules/auth.py - Authentication module
import csv
import os
from colorama import Fore, Style
from .data_structures.linked_list import LinkedList
from .data_manager import read_csv, write_csv
from .utils import clear_screen, show_error, show_success

def authenticate_user():
    """Authenticate a user and return user type and ID."""
    clear_screen()
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "LOGIN")
    print(Fore.CYAN + "=" * 50)
    
    username = input(Fore.YELLOW + "Username: " + Fore.WHITE)
    password = input(Fore.YELLOW + "Password: " + Fore.WHITE)
    
    # Check admin credentials
    admin_data = read_csv("data/admin.csv")
    for admin in admin_data:
        if admin['username'] == username and admin['password'] == password:
            return "admin", admin['id']
    
    # Check doctor credentials
    doctor_data = read_csv("data/dokter.csv")
    for doctor in doctor_data:
        if doctor['username'] == username and doctor['password'] == password:
            return "dokter", doctor['id']
    
    # Check patient credentials
    patient_data = read_csv("data/pasien.csv")
    for patient in patient_data:
        if patient['username'] == username and patient['password'] == password:
            return "pasien", patient['id']
    
    return None, None

def register_patient():
    """Register a new patient."""
    clear_screen()
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "REGISTRASI PASIEN BARU")
    print(Fore.CYAN + "=" * 50)
    
    name = input(Fore.YELLOW + "Nama Lengkap: " + Fore.WHITE)
    username = input(Fore.YELLOW + "Username: " + Fore.WHITE)
    password = input(Fore.YELLOW + "Password: " + Fore.WHITE)
    contact = input(Fore.YELLOW + "Nomor Telepon: " + Fore.WHITE)
    
    # Validate inputs
    if not name or not username or not password or not contact:
        show_error("Semua field harus diisi!")
        return
    
    # Check if username already exists
    patient_data = read_csv("data/pasien.csv")
    for patient in patient_data:
        if patient['username'] == username:
            show_error("Username sudah digunakan. Silakan coba username lain.")
            return
    
    # Generate new ID
    new_id = f"P{len(patient_data) + 1:03d}"
    
    # Add new patient
    new_patient = {
        'id': new_id,
        'nama': name,
        'username': username,
        'password': password,
        'kontak': contact
    }
    
    patient_data.append(new_patient)
    write_csv("data/pasien.csv", patient_data)
    
    show_success(f"Registrasi berhasil! ID Anda adalah {new_id}")