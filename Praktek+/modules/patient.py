# modules/patient.py - Patient functionality
import os
from datetime import datetime, timedelta
from tabulate import tabulate
from colorama import Fore, Style
from .data_manager import read_csv, write_csv, get_doctor_name
from .data_structures.queue import Queue
from .data_structures.bst import BST
from .utils import clear_screen, show_breadcrumbs, show_error, show_success, show_help, LoadingAnimation

def patient_menu(patient_id):
    """Display patient menu and handle patient actions."""
    patient_data = None
    patients = read_csv("data/pasien.csv")
    for patient in patients:
        if patient['id'] == patient_id:
            patient_data = patient
            break
    
    if not patient_data:
        show_error("Data pasien tidak ditemukan.")
        return
    
    while True:
        clear_screen()
        show_breadcrumbs(["Main Menu", "Pasien"])
        print(Fore.CYAN + "=" * 60)
        print(Fore.CYAN + Style.BRIGHT + f"MENU PASIEN: {patient_data['nama']}")
        print(Fore.CYAN + "=" * 60)
        print(Fore.WHITE + "1. " + Fore.YELLOW + "Lihat Jadwal Dokter")
        print(Fore.WHITE + "2. " + Fore.YELLOW + "Cari Jadwal Dokter")
        print(Fore.WHITE + "3. " + Fore.YELLOW + "Mendaftar Konsultasi")
        print(Fore.WHITE + "4. " + Fore.YELLOW + "Mengajukan Perubahan Jadwal")
        print(Fore.WHITE + "5. " + Fore.YELLOW + "Lihat Status Pendaftaran")
        print(Fore.WHITE + "6. " + Fore.YELLOW + "Keluar")
        print(Fore.WHITE + "?. " + Fore.YELLOW + "Bantuan")
        
        choice = input(Fore.GREEN + "\nPilihan Anda: " + Fore.WHITE)
        
        if choice == "1":
            view_doctor_schedules()
        elif choice == "2":
            search_doctor_schedules()
        elif choice == "3":
            register_consultation(patient_id)
        elif choice == "4":
            request_schedule_change(patient_id)
        elif choice == "5":
            view_registration_status(patient_id)
        elif choice == "6":
            break
        elif choice == "?":
            show_help("patient")
        else:
            show_error("Pilihan tidak valid. Silakan coba lagi.")

def view_doctor_schedules():
    """View all available doctor schedules."""
    clear_screen()
    show_breadcrumbs(["Main Menu", "Pasien", "Lihat Jadwal"])
    print(Fore.CYAN + "=" * 100)
    print(Fore.CYAN + Style.BRIGHT + "JADWAL PRAKTIK DOKTER")
    print(Fore.CYAN + "=" * 100)
    
    loading = LoadingAnimation("Memuat jadwal dokter...")
    loading.start()
    
    schedules = read_csv("data/jadwal_dokter.csv")
    doctors = read_csv("data/dokter.csv")
    
    # Create doctor dictionary for quick lookup
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = {"nama": doctor['nama'], "spesialisasi": doctor['spesialisasi']}
    
    loading.stop()
    
    if not schedules:
        print(Fore.YELLOW + "Tidak ada jadwal dokter yang tersedia.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for schedule in schedules:
            doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
            table_data.append([
                schedule['id'],
                doctor_info['nama'],
                doctor_info['spesialisasi'],
                schedule['hari'],
                f"{schedule['jam_mulai']}-{schedule['jam_selesai']}",
                schedule['kuota']
            ])
        
        headers = ["ID", "Dokter", "Spesialisasi", "Hari", "Waktu", "Kuota"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")

def search_doctor_schedules():
    """Search for doctor schedules with improved search options."""
    clear_screen()
    show_breadcrumbs(["Main Menu", "Pasien", "Cari Jadwal"])
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "CARI JADWAL DOKTER")
    print(Fore.CYAN + "=" * 50)
    print(Fore.WHITE + "1. " + Fore.YELLOW + "Cari berdasarkan Nama Dokter")
    print(Fore.WHITE + "2. " + Fore.YELLOW + "Cari berdasarkan Spesialisasi")
    print(Fore.WHITE + "3. " + Fore.YELLOW + "Cari berdasarkan Hari")
    print(Fore.WHITE + "4. " + Fore.YELLOW + "Kembali")
    
    choice = input(Fore.GREEN + "\nPilihan Anda: " + Fore.WHITE)
    
    if choice not in ["1", "2", "3"]:
        return
    
    loading = LoadingAnimation("Mencari jadwal...")
    loading.start()
    
    # Build BST for quick searching
    bst = BST()
    
    schedules = read_csv("data/jadwal_dokter.csv")
    doctors = read_csv("data/dokter.csv")
    
    # Create doctor dictionary for quick lookup
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = {"nama": doctor['nama'], "spesialisasi": doctor['spesialisasi']}
    
    results = []
    
    if choice == "1":
        loading.stop()
        search_key = input(Fore.GREEN + "Masukkan nama dokter: " + Fore.WHITE).lower()
        loading.start()
        
        # Simple fuzzy search - includes partial matches
        for schedule in schedules:
            doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
            if search_key in doctor_info['nama'].lower():
                results.append((schedule, doctor_info))
    
    elif choice == "2":
        loading.stop()
        search_key = input(Fore.GREEN + "Masukkan spesialisasi: " + Fore.WHITE).lower()
        loading.start()
        
        for schedule in schedules:
            doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
            if search_key in doctor_info['spesialisasi'].lower():
                results.append((schedule, doctor_info))
    
    elif choice == "3":
        loading.stop()
        days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
        print(Fore.YELLOW + "\nHari yang tersedia:")
        for i, day in enumerate(days, 1):
            print(f"{Fore.WHITE}{i}. {Fore.YELLOW}{day}")
        
        try:
            day_index = int(input(Fore.GREEN + "\nPilih hari (nomor): " + Fore.WHITE)) - 1
            if day_index < 0 or day_index >= len(days):
                show_error("Hari tidak valid.")
                return
            
            selected_day = days[day_index]
            loading.start()
            
            for schedule in schedules:
                doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"})
                if schedule['hari'] == selected_day:
                    results.append((schedule, doctor_info))
                    
        except ValueError:
            show_error("Input tidak valid.")
            return
    
    loading.stop()
    
    clear_screen()
    show_breadcrumbs(["Main Menu", "Pasien", "Cari Jadwal", "Hasil"])
    print(Fore.CYAN + "=" * 100)
    print(Fore.CYAN + Style.BRIGHT + "HASIL PENCARIAN")
    print(Fore.CYAN + "=" * 100)
    
    if not results:
        print(Fore.YELLOW + "Tidak ditemukan jadwal yang sesuai.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for schedule, doctor_info in results:
            table_data.append([
                schedule['id'],
                doctor_info['nama'],
                doctor_info['spesialisasi'],
                schedule['hari'],
                f"{schedule['jam_mulai']}-{schedule['jam_selesai']}",
                schedule['kuota']
            ])
        
        headers = ["ID", "Dokter", "Spesialisasi", "Hari", "Waktu", "Kuota"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")

def register_consultation(patient_id):
    """Register for a doctor consultation."""
    clear_screen()
    show_breadcrumbs(["Main Menu", "Pasien", "Daftar Konsultasi"])
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "PENDAFTARAN KONSULTASI")
    print(Fore.CYAN + "=" * 50)
    
    # Show available schedules
    view_doctor_schedules()
    
    schedule_id = input(Fore.GREEN + "\nMasukkan ID jadwal yang ingin didaftar: " + Fore.WHITE)
    
    loading = LoadingAnimation("Memeriksa jadwal...")
    loading.start()
    
    # Check if schedule exists
    schedules = read_csv("data/jadwal_dokter.csv")
    selected_schedule = None
    for schedule in schedules:
        if schedule['id'] == schedule_id:
            selected_schedule = schedule
            break
    
    if not selected_schedule:
        loading.stop()
        show_error("Jadwal tidak ditemukan.")
        return
    
    # Get doctor info
    doctors = read_csv("data/dokter.csv")
    doctor_name = "Unknown Doctor"
    for doctor in doctors:
        if doctor['id'] == selected_schedule['dokter_id']:
            doctor_name = doctor['nama']
            break
    
    # Check available dates
    days_map = {
        "Senin": 0, "Selasa": 1, "Rabu": 2, "Kamis": 3, "Jumat": 4, "Sabtu": 5, "Minggu": 6
    }
    day_index = days_map.get(selected_schedule['hari'])
    if day_index is None:
        loading.stop()
        show_error("Hari jadwal tidak valid.")
        return
    
    # Find the next occurrence of the day
    today = datetime.now()
    days_ahead = (day_index - today.weekday()) % 7
    if days_ahead == 0:  # Today
        if today.hour >= int(selected_schedule['jam_selesai'].split(':')[0]):
            days_ahead = 7  # Next week
    
    next_occurrence = today + timedelta(days=days_ahead)
    date_str = next_occurrence.strftime("%Y-%m-%d")
    
    # Check if already registered for this schedule on this date
    registrations = read_csv("data/pendaftaran.csv")
    for reg in registrations:
        if (reg['pasien_id'] == patient_id and reg['jadwal_id'] == schedule_id and 
            reg['tanggal'] == date_str and reg['status'] != 'Dibatalkan'):
            loading.stop()
            show_error("Anda sudah terdaftar pada jadwal ini.")
            return
    
    # Check if quota is full
    quota = int(selected_schedule['kuota'])
    registered_count = sum(1 for reg in registrations if 
                           reg['jadwal_id'] == schedule_id and 
                           reg['tanggal'] == date_str and 
                           reg['status'] != 'Dibatalkan')
    
    if registered_count >= quota:
        loading.stop()
        show_error("Kuota jadwal ini sudah penuh.")
        return
    
    # Get queue number
    queue = Queue()
    for i in range(1, quota + 1):
        queue.enqueue(i)
    
    # Remove already taken queue numbers
    for reg in registrations:
        if (reg['jadwal_id'] == schedule_id and reg['tanggal'] == date_str and 
            reg['status'] != 'Dibatalkan' and reg['nomor_antrian'].isdigit()):
            queue_num = int(reg['nomor_antrian'])
            for _ in range(queue.size()):
                num = queue.dequeue()
                if num != queue_num:
                    queue.enqueue(num)
    
    if queue.is_empty():
        loading.stop()
        show_error("Semua nomor antrian sudah terisi.")
        return
    
    queue_number = queue.dequeue()
    
    # Generate registration ID
    new_reg_id = f"R{len(registrations) + 1:03d}"
    
    # Add registration
    new_registration = {
        'id': new_reg_id,
        'pasien_id': patient_id,
        'jadwal_id': schedule_id,
        'tanggal': date_str,
        'status': 'Terdaftar',
        'nomor_antrian': str(queue_number)
    }
    
    registrations.append(new_registration)
    write_csv("data/pendaftaran.csv", registrations)
    
    loading.stop()
    
    print(Fore.GREEN + Style.BRIGHT + f"\nPendaftaran berhasil!")
    print(Fore.YELLOW + f"ID Pendaftaran: {Fore.WHITE}{new_reg_id}")
    print(Fore.YELLOW + f"Jadwal: {Fore.WHITE}{doctor_name} - {selected_schedule['hari']}, {selected_schedule['jam_mulai']}-{selected_schedule['jam_selesai']}")
    print(Fore.YELLOW + f"Tanggal: {Fore.WHITE}{date_str}")
    print(Fore.YELLOW + f"Nomor Antrian: {Fore.WHITE}{queue_number}")
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")

def request_schedule_change(patient_id):
    """Request a change to a registered consultation."""
    clear_screen()
    show_breadcrumbs(["Main Menu", "Pasien", "Ubah Jadwal"])
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "PENGAJUAN PERUBAHAN JADWAL")
    print(Fore.CYAN + "=" * 50)
    
    loading = LoadingAnimation("Memuat pendaftaran...")
    loading.start()
    
    # Show registered consultations
    registrations = read_csv("data/pendaftaran.csv")
    patient_registrations = [reg for reg in registrations if 
                            reg['pasien_id'] == patient_id and 
                            reg['status'] == 'Terdaftar']
    
    schedules = read_csv("data/jadwal_dokter.csv")
    doctors = read_csv("data/dokter.csv")
    
    # Create schedule and doctor dictionaries for quick lookup
    schedule_dict = {}
    for schedule in schedules:
        schedule_dict[schedule['id']] = schedule
    
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = doctor['nama']
    
    loading.stop()
    
    if not patient_registrations:
        print(Fore.YELLOW + "Anda tidak memiliki pendaftaran aktif.")
        input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")
        return
    
    print(Fore.YELLOW + "Pendaftaran aktif Anda:")
    # Convert to list of lists for tabulate
    table_data = []
    for i, reg in enumerate(patient_registrations, 1):
        schedule = schedule_dict.get(reg['jadwal_id'], None)
        if schedule:
            doctor_name = doctor_dict.get(schedule['dokter_id'], "Unknown")
            schedule_info = f"{schedule['hari']} {schedule['jam_mulai']}-{schedule['jam_selesai']}"
            table_data.append([
                i,
                reg['id'],
                doctor_name,
                schedule_info,
                reg['tanggal'],
                reg['nomor_antrian']
            ])
    
    headers = ["No.", "ID", "Dokter", "Jadwal", "Tanggal", "Antrian"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    try:
        reg_index = int(input(Fore.GREEN + "\nPilih nomor pendaftaran yang ingin diubah: " + Fore.WHITE)) - 1
        if reg_index < 0 or reg_index >= len(patient_registrations):
            show_error("Nomor tidak valid.")
            return
        
        selected_reg = patient_registrations[reg_index]
        
        print(Fore.YELLOW + "\nOpsi perubahan:")
        print(Fore.WHITE + "1. " + Fore.YELLOW + "Batalkan pendaftaran")
        print(Fore.WHITE + "2. " + Fore.YELLOW + "Kembali")
        
        choice = input(Fore.GREEN + "\nPilihan Anda: " + Fore.WHITE)
        
        if choice == "1":
            loading = LoadingAnimation("Membatalkan pendaftaran...")
            loading.start()
            
            # Update registration status
            for i, reg in enumerate(registrations):
                if reg['id'] == selected_reg['id']:
                    registrations[i]['status'] = 'Dibatalkan'
                    write_csv("data/pendaftaran.csv", registrations)
                    loading.stop()
                    show_success("Pendaftaran berhasil dibatalkan.")
                    break
        
    except ValueError:
        show_error("Input tidak valid.")

def view_registration_status(patient_id):
    """View patient's registration status."""
    clear_screen()
    show_breadcrumbs(["Main Menu", "Pasien", "Status Pendaftaran"])
    print(Fore.CYAN + "=" * 100)
    print(Fore.CYAN + Style.BRIGHT + "STATUS PENDAFTARAN KONSULTASI")
    print(Fore.CYAN + "=" * 100)
    
    loading = LoadingAnimation("Memuat status pendaftaran...")
    loading.start()
    
    registrations = read_csv("data/pendaftaran.csv")
    patient_registrations = [reg for reg in registrations if reg['pasien_id'] == patient_id]
    
    schedules = read_csv("data/jadwal_dokter.csv")
    doctors = read_csv("data/dokter.csv")
    
    # Create schedule and doctor dictionaries for quick lookup
    schedule_dict = {}
    for schedule in schedules:
        schedule_dict[schedule['id']] = schedule
    
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = doctor['nama']
    
    loading.stop()
    
    if not patient_registrations:
        print(Fore.YELLOW + "Anda belum memiliki pendaftaran konsultasi.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for reg in patient_registrations:
            schedule = schedule_dict.get(reg['jadwal_id'], None)
            if schedule:
                doctor_name = doctor_dict.get(schedule['dokter_id'], "Unknown")
                schedule_info = f"{schedule['hari']} {schedule['jam_mulai']}-{schedule['jam_selesai']}"
                
                # Color-code status
                status = reg['status']
                if status == 'Terdaftar':
                    status_display = Fore.GREEN + status + Style.RESET_ALL
                elif status == 'Dibatalkan':
                    status_display = Fore.RED + status + Style.RESET_ALL
                else:
                    status_display = Fore.YELLOW + status + Style.RESET_ALL
                
                table_data.append([
                    reg['id'],
                    doctor_name,
                    schedule_info,
                    reg['tanggal'],
                    status_display,
                    reg['nomor_antrian']
                ])
        
        headers = ["ID", "Dokter", "Jadwal", "Tanggal", "Status", "Antrian"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")