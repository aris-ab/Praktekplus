# modules/doctor.py - Doctor functionality
import os
from datetime import datetime
from tabulate import tabulate
from colorama import Fore, Style
from .data_manager import read_csv, write_csv, get_patient_name #
from .data_structures.linked_list import LinkedList #
from .utils import (
    clear_screen, show_breadcrumbs, show_error,
    show_success, show_help, LoadingAnimation, display_header,
    is_valid_time_format, display_subheader
)

def doctor_menu(doctor_id): #
    """Display doctor menu and handle doctor actions without frame."""
    doctor_data = None
    doctors = read_csv("data/dokter.csv") #
    for doctor in doctors: #
        if doctor['id'] == doctor_id: #
            doctor_data = doctor #
            break

    if not doctor_data: #
        show_error("Data dokter tidak ditemukan.") #
        return

    doctor_name_display = Fore.GREEN + Style.BRIGHT + doctor_data['nama'] + Style.NORMAL + Fore.CYAN
    doctor_specialization_display = Fore.YELLOW + doctor_data['spesialisasi'] + Style.RESET_ALL

    while True:
        clear_screen() #
        show_breadcrumbs([Fore.CYAN + "Menu Utama", doctor_name_display]) #
        display_header(f"MENU DOKTER: {doctor_data['nama']}", f"Spesialisasi: {doctor_data['spesialisasi']}", width=70) #

        print(Fore.CYAN + Style.BRIGHT + "PILIHAN MENU" + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 45 + Style.RESET_ALL)

        print(Fore.WHITE + "  " + Style.BRIGHT + "1. " + Fore.YELLOW + "Lihat Jadwal Praktik Saya") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "2. " + Fore.YELLOW + "Tambah Jadwal Praktik") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "3. " + Fore.YELLOW + "Edit Jadwal Praktik") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "4. " + Fore.YELLOW + "Lihat Pasien Terdaftar") #
        print(Fore.CYAN + "-" * 45 + Style.RESET_ALL)
        print(Fore.WHITE + "  " + Style.BRIGHT + "5. " + Fore.RED   + "Keluar") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "?. " + Fore.GREEN + "Bantuan") #
        print()

        choice = input(Fore.MAGENTA + Style.BRIGHT + "➔ Pilihan Anda: " + Fore.WHITE) #

        if choice == "1": #
            view_doctor_schedules(doctor_id) #
        elif choice == "2": #
            add_doctor_schedule(doctor_id) #
        elif choice == "3": #
            edit_doctor_schedule(doctor_id) #
        elif choice == "4": #
            view_registered_patients(doctor_id) #
        elif choice == "5": #
            break
        elif choice == "?": #
            show_help("doctor") #
        else:
            show_error("Pilihan tidak valid. Silakan coba lagi.") #

def view_doctor_schedules(doctor_id): #
    """View schedules for the specified doctor without frame."""
    clear_screen() #
    show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Dokter", Fore.YELLOW + "Jadwal Praktik Saya" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "JADWAL PRAKTIK SAYA".center(70) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 70).center(70) + Style.RESET_ALL) #
    print()

    loading = LoadingAnimation("Memuat jadwal...") #
    loading.start()

    schedules = read_csv("data/jadwal_dokter.csv") #
    doctor_schedules_list = [sch for sch in schedules if sch['dokter_id'] == doctor_id] #

    schedule_list_data = LinkedList() #
    for schedule_item in doctor_schedules_list: #
        schedule_data = { #
            'id': Fore.CYAN + schedule_item['id'] + Style.RESET_ALL, #
            'hari': schedule_item['hari'], #
            'waktu': f"{schedule_item['jam_mulai']} - {schedule_item['jam_selesai']}", #
            'kuota': Fore.MAGENTA + schedule_item['kuota'] + Style.RESET_ALL #
        }
        schedule_list_data.append(schedule_data) #

    loading.stop()

    all_schedules_display = schedule_list_data.display() #
    if not all_schedules_display: #
        print(Fore.YELLOW + Style.BRIGHT + "  Anda tidak memiliki jadwal praktik yang terdaftar saat ini.")
    else:
        table_data = [] #
        for sch_disp_item in all_schedules_display: #
            table_data.append([ #
                sch_disp_item['id'],
                sch_disp_item['hari'],
                sch_disp_item['waktu'],
                sch_disp_item['kuota']
            ])

        headers = [ #
            Style.BRIGHT + Fore.WHITE + "ID Jadwal", "Hari", "Waktu", "Kuota Pasien" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers, tablefmt="rounded_outline", stralign="center")) #
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu...") #


def add_doctor_schedule(doctor_id): #
    clear_screen() #
    show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Dokter", Fore.YELLOW + "Tambah Jadwal" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "TAMBAH JADWAL PRAKTIK".center(50) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 50).center(50) + Style.RESET_ALL) #
    print()

    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"] #
    print(Fore.CYAN + Style.BRIGHT + "  Hari yang tersedia:" + Style.RESET_ALL) #
    for i, day in enumerate(days, 1): #
        print(f"    {Fore.WHITE}{Style.BRIGHT}{i}. {Fore.YELLOW}{day}{Style.RESET_ALL}")
    print()

    try:
        day_choice_input = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Pilih hari (nomor): " + Fore.WHITE) #
        if not day_choice_input.isdigit():
            show_error("Pilihan hari harus berupa angka.") #
            return
        day_index = int(day_choice_input) - 1

        if day_index < 0 or day_index >= len(days): #
            show_error("Hari tidak valid.") #
            return

        selected_day = days[day_index] #
        start_time = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Jam mulai (format HH:MM): " + Fore.WHITE) #
        end_time = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Jam selesai (format HH:MM): " + Fore.WHITE) #
        quota = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Kuota pasien: " + Fore.WHITE) #

        if not is_valid_time_format(start_time) or not is_valid_time_format(end_time): #
            show_error("Format waktu tidak valid (HH:MM).") #
            return

        if not quota.isdigit() or int(quota) <= 0: #
            show_error("Input kuota tidak valid. Harus berupa angka positif.") #
            return

        schedules = read_csv("data/jadwal_dokter.csv") #
        for schedule_item_check in schedules: #
            if (schedule_item_check['dokter_id'] == doctor_id and #
                schedule_item_check['hari'] == selected_day and #
                ((start_time >= schedule_item_check['jam_mulai'] and start_time < schedule_item_check['jam_selesai']) or #
                 (end_time > schedule_item_check['jam_mulai'] and end_time <= schedule_item_check['jam_selesai']) or #
                 (start_time <= schedule_item_check['jam_mulai'] and end_time >= schedule_item_check['jam_selesai']))): #
                show_error(f"Jadwal bertabrakan dengan jadwal yang sudah ada pada {schedule_item_check['hari']} ({schedule_item_check['jam_mulai']}-{schedule_item_check['jam_selesai']}).") #
                return

        new_id = f"J{len(schedules) + 1:03d}" #
        new_schedule = { #
            'id': new_id, #
            'dokter_id': doctor_id, #
            'hari': selected_day, #
            'jam_mulai': start_time, #
            'jam_selesai': end_time, #
            'kuota': quota #
        }
        schedules.append(new_schedule) #
        write_csv("data/jadwal_dokter.csv", schedules) #
        show_success(f"Jadwal berhasil ditambahkan dengan ID {Fore.YELLOW}{new_id}{Fore.GREEN}.") #

    except ValueError:
        show_error("Input tidak valid. Pastikan nomor yang dimasukkan benar.") #


def edit_doctor_schedule(doctor_id): #
    clear_screen() #
    show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Dokter", Fore.YELLOW + "Edit Jadwal" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "EDIT JADWAL PRAKTIK".center(50) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 50).center(50) + Style.RESET_ALL) #
    print()

    # Menampilkan jadwal dokter saat ini
    schedules_current = read_csv("data/jadwal_dokter.csv") #
    doctor_schedules_current = [s for s in schedules_current if s['dokter_id'] == doctor_id] #

    if not doctor_schedules_current: #
        print(Fore.YELLOW + Style.BRIGHT + "  Anda tidak memiliki jadwal untuk diedit.")
        input(Fore.GREEN + Style.BRIGHT + "\n  Tekan Enter untuk kembali...")
        return

    table_data_current = []
    for sched_curr in doctor_schedules_current: #
        table_data_current.append([
            Fore.CYAN + sched_curr['id'] + Style.RESET_ALL, #
            sched_curr['hari'], #
            f"{sched_curr['jam_mulai']}-{sched_curr['jam_selesai']}", #
            Fore.MAGENTA + sched_curr['kuota'] + Style.RESET_ALL #
        ])
    headers_current = [Style.BRIGHT + Fore.WHITE + "ID", "Hari", "Waktu", "Kuota" + Style.RESET_ALL]
    print(tabulate(table_data_current, headers=headers_current, tablefmt="rounded_outline", stralign="center"))
    print()

    schedule_id_input = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Masukkan ID jadwal yang akan diedit: " + Fore.WHITE).upper() #

    schedules_all = read_csv("data/jadwal_dokter.csv") #
    found_schedule_edit = None
    schedule_idx_edit = -1

    for i, schedule_item_edit in enumerate(schedules_all): #
        if schedule_item_edit['id'] == schedule_id_input and schedule_item_edit['dokter_id'] == doctor_id: #
            found_schedule_edit = schedule_item_edit
            schedule_idx_edit = i
            break

    if not found_schedule_edit: #
        show_error(f"Jadwal dengan ID {Fore.YELLOW}{schedule_id_input}{Fore.RED} tidak ditemukan atau bukan milik Anda.") #
        return

    print(Fore.CYAN + Style.BRIGHT + f"\n  Mengedit Jadwal ID: {Fore.YELLOW}{schedule_id_input}{Style.RESET_ALL}")
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"] #
    print(Fore.CYAN + Style.BRIGHT + "\n  Hari yang tersedia:" + Style.RESET_ALL) #
    for j, day_item_edit in enumerate(days, 1): #
        current_marker = Fore.GREEN + " (Saat ini)" + Style.RESET_ALL if found_schedule_edit['hari'] == day_item_edit else ""
        print(f"    {Fore.WHITE}{Style.BRIGHT}{j}. {Fore.YELLOW}{day_item_edit}{Style.RESET_ALL}{current_marker}")
    print()

    try:
        day_choice_edit = input(Fore.MAGENTA + Style.BRIGHT + f"  ➔ Pilih hari baru (nomor, kosongkan jika tidak berubah [{found_schedule_edit['hari']}]): " + Fore.WHITE) #
        selected_day_edit = found_schedule_edit['hari'] #
        if day_choice_edit:
            if not day_choice_edit.isdigit():
                show_error("Pilihan hari harus berupa angka.") #
                return
            day_index_edit = int(day_choice_edit) - 1
            if day_index_edit < 0 or day_index_edit >= len(days): #
                show_error("Hari tidak valid.") #
                return
            selected_day_edit = days[day_index_edit] #

        start_time_edit = input(Fore.MAGENTA + Style.BRIGHT + f"  ➔ Jam mulai baru (HH:MM, kosongkan jika tidak berubah [{found_schedule_edit['jam_mulai']}]): " + Fore.WHITE) #
        end_time_edit = input(Fore.MAGENTA + Style.BRIGHT + f"  ➔ Jam selesai baru (HH:MM, kosongkan jika tidak berubah [{found_schedule_edit['jam_selesai']}]): " + Fore.WHITE) #
        quota_edit = input(Fore.MAGENTA + Style.BRIGHT + f"  ➔ Kuota pasien baru (kosongkan jika tidak berubah [{found_schedule_edit['kuota']}]): " + Fore.WHITE) #

        final_start_time_edit = start_time_edit if start_time_edit else found_schedule_edit['jam_mulai'] #
        final_end_time_edit = end_time_edit if end_time_edit else found_schedule_edit['jam_selesai'] #
        final_quota_edit = quota_edit if quota_edit else found_schedule_edit['kuota'] #

        if start_time_edit and not is_valid_time_format(final_start_time_edit): #
            show_error("Format waktu mulai tidak valid (HH:MM).") #
            return
        if end_time_edit and not is_valid_time_format(final_end_time_edit): #
            show_error("Format waktu selesai tidak valid (HH:MM).") #
            return
        if quota_edit and (not final_quota_edit.isdigit() or int(final_quota_edit) <= 0): #
            show_error("Kuota harus berupa angka positif.") #
            return

        schedules_all[schedule_idx_edit]['hari'] = selected_day_edit #
        schedules_all[schedule_idx_edit]['jam_mulai'] = final_start_time_edit #
        schedules_all[schedule_idx_edit]['jam_selesai'] = final_end_time_edit #
        schedules_all[schedule_idx_edit]['kuota'] = final_quota_edit #

        write_csv("data/jadwal_dokter.csv", schedules_all) #
        show_success(f"Jadwal ID {Fore.YELLOW}{schedule_id_input}{Fore.GREEN} berhasil diperbarui.") #

    except ValueError:
        show_error("Input tidak valid.") #


def view_registered_patients(doctor_id): #
    clear_screen() #
    show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Dokter", Fore.YELLOW + "Pasien Terdaftar" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "PASIEN TERDAFTAR PADA JADWAL SAYA".center(100) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 100).center(100) + Style.RESET_ALL) #
    print()

    loading = LoadingAnimation("Memuat data pasien...") #
    loading.start()

    schedules = read_csv("data/jadwal_dokter.csv") #
    doctor_schedule_ids = [sch['id'] for sch in schedules if sch['dokter_id'] == doctor_id] #

    if not doctor_schedule_ids: #
        loading.stop()
        print(Fore.YELLOW + Style.BRIGHT + "  Anda tidak memiliki jadwal praktik, sehingga tidak ada pasien terdaftar.") #
        input(Fore.GREEN + Style.BRIGHT + "\n  Tekan Enter untuk kembali ke menu...") #
        return

    registrations = read_csv("data/pendaftaran.csv") #
    doctor_registrations = [reg for reg in registrations if reg['jadwal_id'] in doctor_schedule_ids] #
    loading.stop()

    if not doctor_registrations: #
        print(Fore.YELLOW + Style.BRIGHT + "  Belum ada pasien yang terdaftar pada jadwal Anda.") #
    else:
        schedule_dict = {} #
        for sch_item_dict in schedules: #
            if sch_item_dict['id'] in doctor_schedule_ids: #
                schedule_dict[sch_item_dict['id']] = f"{Fore.BLUE}{sch_item_dict['hari']} {sch_item_dict['jam_mulai']}-{sch_item_dict['jam_selesai']}{Style.RESET_ALL}" #

        table_data = [] #
        for reg_item_doc in doctor_registrations: #
            patient_name_doc = get_patient_name(reg_item_doc['pasien_id']) #
            schedule_info_doc = schedule_dict.get(reg_item_doc['jadwal_id'], Fore.RED + "Jadwal Tidak Diketahui" + Style.RESET_ALL) #

            status_doc = reg_item_doc['status'] #
            status_display_doc = status_doc
            if status_doc == 'Terdaftar': #
                status_display_doc = Fore.GREEN + Style.BRIGHT + status_doc + Style.RESET_ALL
            elif status_doc == 'Dibatalkan': #
                status_display_doc = Fore.RED + Style.BRIGHT + status_doc + Style.RESET_ALL
            else: #
                status_display_doc = Fore.YELLOW + Style.BRIGHT + status_doc + Style.RESET_ALL

            table_data.append([ #
                Fore.CYAN + reg_item_doc['id'] + Style.RESET_ALL, #
                Fore.GREEN + patient_name_doc + Style.RESET_ALL,
                schedule_info_doc,
                reg_item_doc['tanggal'], #
                status_display_doc,
                Fore.MAGENTA + reg_item_doc['nomor_antrian'] + Style.RESET_ALL #
            ])

        headers_doc_pat = [ #
            Style.BRIGHT + Fore.WHITE + "ID Reg.", "Nama Pasien", "Jadwal",
            "Tanggal", "Status", "Antrian" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers_doc_pat, tablefmt="rounded_outline", stralign="center")) #
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu...") #