# modules/admin.py - Admin functionality
import os
from tabulate import tabulate
from colorama import Fore, Style
# Perbaikan import menggunakan alias (solusi alternatif opsi 3)
import modules.data_manager as dm
import modules.data_structures.linked_list as ll
import modules.utils as utils

def admin_menu(admin_id):
    """Display admin menu and handle admin actions."""
    while True:
        utils.clear_screen()
        utils.show_breadcrumbs(["Main Menu", "Admin"])
        print(Fore.CYAN + "=" * 50)
        print(Fore.CYAN + Style.BRIGHT + "MENU ADMIN KLINIK")
        print(Fore.CYAN + "=" * 50)
        print(Fore.WHITE + "1. " + Fore.YELLOW + "Lihat Semua Jadwal Dokter")
        print(Fore.WHITE + "2. " + Fore.YELLOW + "Tambah Jadwal Dokter")
        print(Fore.WHITE + "3. " + Fore.YELLOW + "Edit Jadwal Dokter")
        print(Fore.WHITE + "4. " + Fore.YELLOW + "Hapus Jadwal Dokter")
        print(Fore.WHITE + "5. " + Fore.YELLOW + "Lihat Data Pasien")
        print(Fore.WHITE + "6. " + Fore.YELLOW + "Lihat Pendaftaran Konsultasi")
        print(Fore.WHITE + "7. " + Fore.YELLOW + "Lihat Statistik Klinik")
        print(Fore.WHITE + "8. " + Fore.YELLOW + "Keluar")
        print(Fore.WHITE + "?. " + Fore.YELLOW + "Bantuan")
        
        choice = input(Fore.GREEN + "\nPilihan Anda: " + Fore.WHITE)
        
        if choice == "1":
            view_all_schedules()
        elif choice == "2":
            add_doctor_schedule()
        elif choice == "3":
            edit_doctor_schedule()
        elif choice == "4":
            delete_doctor_schedule()
        elif choice == "5":
            view_patient_data()
        elif choice == "6":
            view_all_registrations()
        elif choice == "7":
            view_clinic_statistics()
        elif choice == "8":
            break
        elif choice == "?":
            utils.show_help("admin")
        else:
            utils.show_error("Pilihan tidak valid. Silakan coba lagi.")

def view_all_schedules():
    """View all doctor schedules."""
    utils.clear_screen()
    utils.show_breadcrumbs(["Main Menu", "Admin", "Lihat Jadwal"])
    print(Fore.CYAN + "=" * 80)
    print(Fore.CYAN + Style.BRIGHT + "JADWAL PRAKTEK DOKTER")
    print(Fore.CYAN + "=" * 80)
    
    loading = utils.LoadingAnimation("Memuat data jadwal...")
    loading.start()
    
    schedules = dm.read_csv("data/jadwal_dokter.csv")
    doctors = dm.read_csv("data/dokter.csv")
    
    # Create doctor dictionary for quick lookup
    doctor_dict = {}
    for doctor in doctors:
        doctor_dict[doctor['id']] = doctor['nama']
    
    # Create linked list to store schedule data
    schedule_list = ll.LinkedList()
    for schedule in schedules:
        doctor_name = doctor_dict.get(schedule['dokter_id'], "Unknown Doctor")
        schedule_data = {
            'id': schedule['id'],
            'dokter': doctor_name,
            'hari': schedule['hari'],
            'waktu': f"{schedule['jam_mulai']} - {schedule['jam_selesai']}",
            'kuota': schedule['kuota']
        }
        schedule_list.append(schedule_data)
    
    loading.stop()
    
    # Display schedules
    all_schedules = schedule_list.display()
    if not all_schedules:
        print(Fore.YELLOW + "Tidak ada jadwal yang tersedia.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for schedule in all_schedules:
            table_data.append([
                schedule['id'], 
                schedule['dokter'], 
                schedule['hari'], 
                schedule['waktu'], 
                schedule['kuota']
            ])
        
        headers = ["ID", "Dokter", "Hari", "Waktu", "Kuota"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")

def add_doctor_schedule():
    """Add a new doctor schedule."""
    utils.clear_screen()
    utils.show_breadcrumbs(["Main Menu", "Admin", "Tambah Jadwal"])
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "TAMBAH JADWAL DOKTER")
    print(Fore.CYAN + "=" * 50)
    
    # Show available doctors
    doctors = dm.read_csv("data/dokter.csv")
    print(Fore.YELLOW + "Dokter yang tersedia:")
    for i, doctor in enumerate(doctors, 1):
        print(f"{Fore.WHITE}{i}. {Fore.YELLOW}{doctor['nama']} ({doctor['spesialisasi']})")
    
    try:
        doctor_index = int(input(Fore.GREEN + "\nPilih dokter (nomor): " + Fore.WHITE)) - 1
        if doctor_index < 0 or doctor_index >= len(doctors):
            utils.show_error("Dokter tidak ditemukan.")
            return
        
        doctor_id = doctors[doctor_index]['id']
        
        days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
        print(Fore.YELLOW + "\nHari yang tersedia:")
        for i, day in enumerate(days, 1):
            print(f"{Fore.WHITE}{i}. {Fore.YELLOW}{day}")
        
        day_index = int(input(Fore.GREEN + "\nPilih hari (nomor): " + Fore.WHITE)) - 1
        if day_index < 0 or day_index >= len(days):
            utils.show_error("Hari tidak valid.")
            return
        
        selected_day = days[day_index]
        start_time = input(Fore.GREEN + "Jam mulai (format HH:MM): " + Fore.WHITE)
        end_time = input(Fore.GREEN + "Jam selesai (format HH:MM): " + Fore.WHITE)
        quota = input(Fore.GREEN + "Kuota pasien: " + Fore.WHITE)
        
        # Validate inputs
        if not start_time or not end_time or not quota.isdigit():
            utils.show_error("Input tidak valid.")
            return
        
        # Generate new schedule ID
        schedules = dm.read_csv("data/jadwal_dokter.csv")
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
        dm.write_csv("data/jadwal_dokter.csv", schedules)
        
        utils.show_success(f"Jadwal berhasil ditambahkan dengan ID {new_id}")
        
    except ValueError:
        utils.show_error("Input tidak valid.")

def edit_doctor_schedule():
    """Edit an existing doctor schedule."""
    utils.clear_screen()
    utils.show_breadcrumbs(["Main Menu", "Admin", "Edit Jadwal"])
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "EDIT JADWAL DOKTER")
    print(Fore.CYAN + "=" * 50)
    
    # Show existing schedules
    view_all_schedules()
    
    schedule_id = input(Fore.GREEN + "\nMasukkan ID jadwal yang akan diedit: " + Fore.WHITE)
    
    schedules = dm.read_csv("data/jadwal_dokter.csv")
    found = False
    
    for i, schedule in enumerate(schedules):
        if schedule['id'] == schedule_id:
            found = True
            
            days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
            print(Fore.YELLOW + "\nHari yang tersedia:")
            for j, day in enumerate(days, 1):
                print(f"{Fore.WHITE}{j}. {Fore.YELLOW}{day}")
            
            try:
                day_index = int(input(Fore.GREEN + "\nPilih hari baru (nomor): " + Fore.WHITE)) - 1
                if day_index < 0 or day_index >= len(days):
                    utils.show_error("Hari tidak valid.")
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
                    utils.show_error("Kuota harus berupa angka.")
                    return
                
                # Update schedule
                schedules[i]['hari'] = selected_day
                schedules[i]['jam_mulai'] = start_time
                schedules[i]['jam_selesai'] = end_time
                schedules[i]['kuota'] = quota
                
                dm.write_csv("data/jadwal_dokter.csv", schedules)
                utils.show_success("Jadwal berhasil diperbarui.")
                
            except ValueError:
                utils.show_error("Input tidak valid.")
            
            break
    
    if not found:
        utils.show_error("Jadwal tidak ditemukan.")

def delete_doctor_schedule():
    """Delete a doctor schedule."""
    utils.clear_screen()
    utils.show_breadcrumbs(["Main Menu", "Admin", "Hapus Jadwal"])
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "HAPUS JADWAL DOKTER")
    print(Fore.CYAN + "=" * 50)
    
    # Show existing schedules
    view_all_schedules()
    
    schedule_id = input(Fore.GREEN + "\nMasukkan ID jadwal yang akan dihapus: " + Fore.WHITE)
    
    schedules = dm.read_csv("data/jadwal_dokter.csv")
    registrations = dm.read_csv("data/pendaftaran.csv")
    
    # Check if there are active registrations for this schedule
    active_registrations = [reg for reg in registrations if reg['jadwal_id'] == schedule_id and reg['status'] != 'Dibatalkan']
    
    if active_registrations:
        utils.show_error("Tidak dapat menghapus jadwal karena ada pendaftaran aktif.")
        return
    
    # Remove schedule
    updated_schedules = [sch for sch in schedules if sch['id'] != schedule_id]
    
    if len(updated_schedules) < len(schedules):
        dm.write_csv("data/jadwal_dokter.csv", updated_schedules)
        utils.show_success("Jadwal berhasil dihapus.")
    else:
        utils.show_error("Jadwal tidak ditemukan.")

def view_patient_data():
    """View registered patients."""
    utils.clear_screen()
    utils.show_breadcrumbs(["Main Menu", "Admin", "Data Pasien"])
    print(Fore.CYAN + "=" * 80)
    print(Fore.CYAN + Style.BRIGHT + "DATA PASIEN TERDAFTAR")
    print(Fore.CYAN + "=" * 80)
    
    loading = utils.LoadingAnimation("Memuat data pasien...")
    loading.start()
    
    patients = dm.read_csv("data/pasien.csv")
    
    loading.stop()
    
    if not patients:
        print(Fore.YELLOW + "Tidak ada data pasien terdaftar.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for patient in patients:
            table_data.append([
                patient['id'],
                patient['nama'],
                patient['username'],
                patient['kontak']
            ])
        
        headers = ["ID", "Nama", "Username", "Kontak"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")

def view_all_registrations():
    """View all consultation registrations."""
    utils.clear_screen()
    utils.show_breadcrumbs(["Main Menu", "Admin", "Data Pendaftaran"])
    print(Fore.CYAN + "=" * 110)
    print(Fore.CYAN + Style.BRIGHT + "DATA PENDAFTARAN KONSULTASI")
    print(Fore.CYAN + "=" * 110)
    
    loading = utils.LoadingAnimation("Memuat data pendaftaran...")
    loading.start()
    
    registrations = dm.read_csv("data/pendaftaran.csv")
    
    loading.stop()
    
    if not registrations:
        print(Fore.YELLOW + "Tidak ada data pendaftaran.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for reg in registrations:
            patient_name = dm.get_patient_name(reg['pasien_id'])
            schedule_details = dm.get_schedule_details(reg['jadwal_id'])
            
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
                schedule_details,
                reg['tanggal'],
                status_display,
                reg['nomor_antrian']
            ])
        
        headers = ["ID", "Pasien", "Dokter & Jadwal", "Tanggal", "Status", "Antrian"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")

def view_clinic_statistics():
    """View basic clinic statistics."""
    utils.clear_screen()
    utils.show_breadcrumbs(["Main Menu", "Admin", "Statistik"])
    print(Fore.CYAN + "=" * 70)
    print(Fore.CYAN + Style.BRIGHT + "STATISTIK KLINIK")
    print(Fore.CYAN + "=" * 70)
    
    loading = utils.LoadingAnimation("Menganalisis data...")
    loading.start()
    
    schedules = dm.read_csv("data/jadwal_dokter.csv")
    doctors = dm.read_csv("data/dokter.csv")
    patients = dm.read_csv("data/pasien.csv")
    registrations = dm.read_csv("data/pendaftaran.csv")
    
    # Count active registrations
    active_registrations = [reg for reg in registrations if reg['status'] != 'Dibatalkan']
    
    # Count registrations by day
    reg_by_day = {}
    for reg in active_registrations:
        schedule_id = reg['jadwal_id']
        day = None
        for sch in schedules:
            if sch['id'] == schedule_id:
                day = sch['hari']
                break
        
        if day:
            reg_by_day[day] = reg_by_day.get(day, 0) + 1
    
    # Count registrations by doctor
    reg_by_doctor = {}
    for reg in active_registrations:
        schedule_id = reg['jadwal_id']
        doctor_id = None
        for sch in schedules:
            if sch['id'] == schedule_id:
                doctor_id = sch['dokter_id']
                break
        
        if doctor_id:
            doctor_name = None
            for doc in doctors:
                if doc['id'] == doctor_id:
                    doctor_name = doc['nama']
                    break
            
            if doctor_name:
                reg_by_doctor[doctor_name] = reg_by_doctor.get(doctor_name, 0) + 1
    
    # Count registrations by status
    reg_by_status = {}
    for reg in registrations:
        status = reg['status']
        reg_by_status[status] = reg_by_status.get(status, 0) + 1
    
    loading.stop()
    
    print(Fore.YELLOW + f"Total Dokter: {Fore.WHITE}{len(doctors)}")
    print(Fore.YELLOW + f"Total Pasien: {Fore.WHITE}{len(patients)}")
    print(Fore.YELLOW + f"Total Jadwal: {Fore.WHITE}{len(schedules)}")
    print(Fore.YELLOW + f"Total Pendaftaran Aktif: {Fore.WHITE}{len(active_registrations)}")
    
    print(Fore.CYAN + "\n" + "-" * 30)
    print(Fore.CYAN + Style.BRIGHT + "PENDAFTARAN PER HARI")
    print(Fore.CYAN + "-" * 30)
    
    if not reg_by_day:
        print(Fore.YELLOW + "Belum ada data pendaftaran.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for day, count in sorted(reg_by_day.items(), key=lambda x: x[1], reverse=True):
            table_data.append([day, count])
        
        headers = ["Hari", "Jumlah Pendaftaran"]
        print(tabulate(table_data, headers=headers, tablefmt="simple"))
    
    print(Fore.CYAN + "\n" + "-" * 30)
    print(Fore.CYAN + Style.BRIGHT + "PENDAFTARAN PER DOKTER")
    print(Fore.CYAN + "-" * 30)
    
    if not reg_by_doctor:
        print(Fore.YELLOW + "Belum ada data pendaftaran.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for doctor, count in sorted(reg_by_doctor.items(), key=lambda x: x[1], reverse=True):
            table_data.append([doctor, count])
        
        headers = ["Dokter", "Jumlah Pendaftaran"]
        print(tabulate(table_data, headers=headers, tablefmt="simple"))
    
    print(Fore.CYAN + "\n" + "-" * 30)
    print(Fore.CYAN + Style.BRIGHT + "PENDAFTARAN PER STATUS")
    print(Fore.CYAN + "-" * 30)
    
    if not reg_by_status:
        print(Fore.YELLOW + "Belum ada data pendaftaran.")
    else:
        # Convert to list of lists for tabulate
        table_data = []
        for status, count in reg_by_status.items():
            table_data.append([status, count])
        
        headers = ["Status", "Jumlah"]
        print(tabulate(table_data, headers=headers, tablefmt="simple"))
    
    input(Fore.GREEN + "\nTekan Enter untuk kembali ke menu...")
