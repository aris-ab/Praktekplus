# modules/doctor.py - Doctor functionality
import os
from datetime import datetime
from tabulate import tabulate
from colorama import Fore, Style
from .data_manager import read_csv, write_csv, get_patient_name
from .data_structures.linked_list import LinkedList
from .utils import clear_screen, show_breadcrumbs, show_error, show_success, show_help, LoadingAnimation

def doctor_menu(doctor_id):
    """Display doctor menu and handle doctor actions."""
    doctor_data = None
    doctors = read_csv("data/dokter.csv")
    for doctor in doctors:
        if doctor['id'] == doctor_id:
            doctor_data = doctor
            break
    
    if not doctor_data:
        show_error("Data dokter tidak ditemukan.")
        return
    
    while True:
        clear_screen()
        show_breadcrumbs(["Main Menu", "Dokter"])
        print(Fore.CYAN + "=" * 70)
        print(Fore.CYAN + Style.BRIGHT + f"MENU DOKTER: {doctor_data['nama']} - {doctor_data['spesialisasi']}")
        print(Fore.CYAN + "=" * 70)
        print(Fore.WHITE + "1. " + Fore.YELLOW + "Lihat Jadwal Praktik Saya")
        print(Fore.WHITE + "2. " + Fore.YELLOW + "Tambah Jadwal Praktik")
        print(Fore.WHITE + "3. " + Fore.YELLOW + "Edit Jadwal Praktik")
        print(Fore.WHITE + "4. " + Fore.YELLOW + "Lihat Pasien Terdaftar")
        print(Fore.WHITE + "5. " + Fore.YELLOW + "Keluar")
        print(Fore.WHITE + "?. " + Fore.YELLOW + "Bantuan")
        
        choice = input(Fore.GREEN + "\nPilihan Anda: " + Fore.WHITE)
        
        if choice == "1":
            view_doctor_schedules(doctor_id)
        elif choice == "2":
            add_doctor_schedule(doctor_id)
        elif choice == "3":
            edit_doctor_schedule(doctor_id)
        elif choice == "4":
            view_registered_patients(doctor_id)
        elif choice == "5":
            break
        elif choice == "?":
            show_help("doctor")
        else:
            show_error("Pilihan tidak valid. Silakan coba lagi.")

def view_doctor_schedules(doctor_id):
    """View schedules for the specified doctor."""
    clear_screen()
    show_breadcrumbs(["Main Menu", "Dokter", "Jadwal Praktik"])
    print(Fore.CYAN + "=" * 70)
    print(Fore.CYAN + Style.BRIGHT + "JADWAL PRAKTIK SAYA")
    print(Fore.CYAN + "=" * 70)
    
    loading = LoadingAnimation("Memuat jadwal...")
    loading.start()
    
    schedules = read_csv("data/jadwal_dokter.csv")
    
    # Filter schedules for this doctor
    doctor_schedules = [sch for sch in schedules if sch['dokter_id'] == doctor_id]
    
    # Create linked list to store schedule data
    schedule_list = LinkedList()
    for schedule in doctor_schedules:
        schedule_data = {
            'id': schedule['id'],
            'hari': schedule['hari'],
            'waktu': f"{schedule['jam_mulai']} - {schedule['jam_selesai']}",
            'kuota': schedule['kuota']
        }
        schedule_list.append(schedule_data)
    
    loading.stop()
    
    # Display schedules
    all_schedules = schedule_list.display()
    if not all_schedules:
        print(Fore.YELLOW + "Anda tidak memiliki jadwal praktik.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for schedule in all_schedules:
            table_data.append([
                schedule['id'],
                schedule['hari'],
                schedule['waktu'],
                schedule['kuota']
            ])
        
        headers = ["ID", "Hari", "Waktu", "Kuota Pasien"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")

def add_doctor_schedule(doctor_id):
    """Add a new schedule for the doctor."""
    clear_screen()
    show_breadcrumbs(["Main Menu", "Dokter", "Tambah Jadwal"])
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "TAMBAH JADWAL PRAKTIK")
    print(Fore.CYAN + "=" * 50)
    
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    print(Fore.YELLOW + "Hari yang tersedia:")
    for i, day in enumerate(days, 1):
        print(f"{Fore.WHITE}{i}. {Fore.YELLOW}{day}")
    
    try:
        day_index = int(input(Fore.GREEN + "\nPilih hari (nomor): " + Fore.WHITE)) - 1
        if day_index < 0 or day_index >= len(days):
            show_error("Hari tidak valid.")
            return
        
        selected_day = days[day_index]
        start_time = input(Fore.GREEN + "Jam mulai (format HH:MM): " + Fore.WHITE)
        end_time = input(Fore.GREEN + "Jam selesai (format HH:MM): " + Fore.WHITE)
        quota = input(Fore.GREEN + "Kuota pasien: " + Fore.WHITE)
        
        # Validate inputs
        if not start_time or not end_time or not quota.isdigit():
            show_error("Input tidak valid.")
            return
        
        # Check for overlapping schedules
        schedules = read_csv("data/jadwal_dokter.csv")
        for schedule in schedules:
            if (schedule['dokter_id'] == doctor_id and 
                schedule['hari'] == selected_day and
                ((start_time >= schedule['jam_mulai'] and start_time < schedule['jam_selesai']) or
                 (end_time > schedule['jam_mulai'] and end_time <= schedule['jam_selesai']) or
                 (start_time <= schedule['jam_mulai'] and end_time >= schedule['jam_selesai']))):
                show_error("Jadwal bertabrakan dengan jadwal yang sudah ada.")
                return
        
        # Generate new schedule ID
        new_id = f"J{len(schedules) + 1:03d}"
        
        # Add new schedule
        new_schedule = {
            'id': new_id,
            'dokter_id': doctor_id,
            'hari': selected_day,
            'jam_mulai': start_time,
            'jam_selesai': end_time,
            'kuota': quota
        }
        
        schedules.append(new_schedule)
        write_csv("data/jadwal_dokter.csv", schedules)
        
        show_success(f"Jadwal berhasil ditambahkan dengan ID {new_id}")
        
    except ValueError:
        show_error("Input tidak valid.")

def edit_doctor_schedule(doctor_id):
    """Edit doctor's schedule."""
    clear_screen()
    show_breadcrumbs(["Main Menu", "Dokter", "Edit Jadwal"])
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "EDIT JADWAL PRAKTIK")
    print(Fore.CYAN + "=" * 50)
    
    # Show doctor's schedules first
    view_doctor_schedules(doctor_id)
    
    schedule_id = input(Fore.GREEN + "\nMasukkan ID jadwal yang akan diedit: " + Fore.WHITE)
    
    schedules = read_csv("data/jadwal_dokter.csv")
    found = False
    
    for i, schedule in enumerate(schedules):
        if schedule['id'] == schedule_id and schedule['dokter_id'] == doctor_id:
            found = True
            
            days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
            print(Fore.YELLOW + "\nHari yang tersedia:")
            for j, day in enumerate(days, 1):
                print(f"{Fore.WHITE}{j}. {Fore.YELLOW}{day}")
            
            try:
                day_index = int(input(Fore.GREEN + "\nPilih hari baru (nomor): " + Fore.WHITE)) - 1
                if day_index < 0 or day_index >= len(days):
                    show_error("Hari tidak valid.")
                    return
                
                selected_day = days[day_index]
                start_time = input(Fore.GREEN + f"Jam mulai baru (format HH:MM, sebelumnya {schedule['jam_mulai']}): " + Fore.WHITE)
                end_time = input(Fore.GREEN + f"Jam selesai baru (format HH:MM, sebelumnya {schedule['jam_selesai']}): " + Fore.WHITE)
                quota = input(Fore.GREEN + f"Kuota pasien baru (sebelumnya {schedule['kuota']}): " + Fore.WHITE)
                
                # Use previous values if fields are left empty
                if not start_time:
                    start_time = schedule['jam_mulai']
                if not end_time:
                    end_time = schedule['jam_selesai']
                if not quota:
                    quota = schedule['kuota']
                elif not quota.isdigit():
                    show_error("Kuota harus berupa angka.")
                    return
                
                # Update schedule
                schedules[i]['hari'] = selected_day
                schedules[i]['jam_mulai'] = start_time
                schedules[i]['jam_selesai'] = end_time
                schedules[i]['kuota'] = quota
                
                write_csv("data/jadwal_dokter.csv", schedules)
                show_success("Jadwal berhasil diperbarui.")
                
            except ValueError:
                show_error("Input tidak valid.")
            
            break
    
    if not found:
        show_error("Jadwal tidak ditemukan atau bukan milik Anda.")

def view_registered_patients(doctor_id):
    """View patients registered for doctor's schedules."""
    clear_screen()
    show_breadcrumbs(["Main Menu", "Dokter", "Pasien Terdaftar"])
    print(Fore.CYAN + "=" * 100)
    print(Fore.CYAN + Style.BRIGHT + "PASIEN TERDAFTAR PADA JADWAL SAYA")
    print(Fore.CYAN + "=" * 100)
    
    loading = LoadingAnimation("Memuat data pasien...")
    loading.start()
    
    # Get doctor's schedules
    schedules = read_csv("data/jadwal_dokter.csv")
    doctor_schedule_ids = [sch['id'] for sch in schedules if sch['dokter_id'] == doctor_id]
    
    if not doctor_schedule_ids:
        loading.stop()
        print(Fore.YELLOW + "Anda tidak memiliki jadwal praktik.")
        input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")
        return
    
    # Get registrations for doctor's schedules
    registrations = read_csv("data/pendaftaran.csv")
    doctor_registrations = [reg for reg in registrations if reg['jadwal_id'] in doctor_schedule_ids]
    
    loading.stop()
    
    if not doctor_registrations:
        print(Fore.YELLOW + "Belum ada pasien yang terdaftar pada jadwal Anda.")
    else:
        # Get schedule details
        schedule_dict = {}
        for sch in schedules:
            if sch['id'] in doctor_schedule_ids:
                schedule_dict[sch['id']] = f"{sch['hari']} {sch['jam_mulai']}-{sch['jam_selesai']}"
        
        # Convert to list of lists for tabulate
        table_data = []
        for reg in doctor_registrations:
            patient_name = get_patient_name(reg['pasien_id'])
            schedule_info = schedule_dict.get(reg['jadwal_id'], "Unknown")
            
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
                patient_name,
                schedule_info,
                reg['tanggal'],
                status_display,
                reg['nomor_antrian']
            ])
        
        headers = ["ID Pendaftaran", "Nama Pasien", "Jadwal", "Tanggal", "Status", "Antrian"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")