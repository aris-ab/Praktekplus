# modules/patient.py - Patient functionality
import os
from datetime import datetime, timedelta
from tabulate import tabulate
from colorama import Fore, Style
from .data_manager import read_csv, write_csv, get_doctor_name #
from .data_structures.queue import Queue #
from .data_structures.bst import BST #
from .utils import (
    clear_screen, show_breadcrumbs, show_error,
    show_success, show_help, LoadingAnimation, display_header,
    display_subheader, is_valid_time_format
)

def patient_menu(patient_id): #
    """Display patient menu and handle patient actions without frame."""
    patient_data = None
    patients = read_csv("data/pasien.csv") #
    for patient in patients: #
        if patient['id'] == patient_id: #
            patient_data = patient #
            break

    if not patient_data: #
        show_error("Data pasien tidak ditemukan.") #
        return

    patient_name_display = Fore.GREEN + Style.BRIGHT + patient_data['nama'] + Style.RESET_ALL

    while True:
        clear_screen() #
        show_breadcrumbs([Fore.CYAN + "Menu Utama", patient_name_display]) #
        display_header(f"MENU PASIEN: {patient_data['nama']}", width=60) #

        print(Fore.CYAN + Style.BRIGHT + "PILIHAN MENU" + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 45 + Style.RESET_ALL)

        print(Fore.WHITE + "  " + Style.BRIGHT + "1. " + Fore.YELLOW + "Lihat Semua Jadwal Dokter") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "2. " + Fore.YELLOW + "Cari Jadwal Dokter") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "3. " + Fore.YELLOW + "Mendaftar Konsultasi") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "4. " + Fore.YELLOW + "Ubah/Batalkan Pendaftaran") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "5. " + Fore.YELLOW + "Lihat Status Pendaftaran Saya") #
        print(Fore.CYAN + "-" * 45 + Style.RESET_ALL)
        print(Fore.WHITE + "  " + Style.BRIGHT + "6. " + Fore.RED   + "Keluar") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "?. " + Fore.GREEN + "Bantuan") #
        print()

        choice = input(Fore.MAGENTA + Style.BRIGHT + "➔ Pilihan Anda: " + Fore.WHITE) #

        if choice == "1": #
            view_doctor_schedules() #
        elif choice == "2": #
            search_doctor_schedules() #
        elif choice == "3": #
            register_consultation(patient_id) #
        elif choice == "4": #
            request_schedule_change(patient_id) #
        elif choice == "5": #
            view_registration_status(patient_id) #
        elif choice == "6": #
            break
        elif choice == "?": #
            show_help("patient") #
        else:
            show_error("Pilihan tidak valid. Silakan coba lagi.") #


def view_doctor_schedules(): #
    clear_screen() #
    show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Pasien", Fore.YELLOW + "Lihat Semua Jadwal" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "JADWAL PRAKTEK DOKTER TERSEDIA".center(100) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 100).center(100) + Style.RESET_ALL) #
    print()

    loading = LoadingAnimation("Memuat jadwal dokter...") #
    loading.start()

    schedules = read_csv("data/jadwal_dokter.csv") #
    doctors = read_csv("data/dokter.csv") #
    doctor_dict = {doc['id']: {"nama": doc['nama'], "spesialisasi": doc['spesialisasi']} for doc in doctors} #
    loading.stop()

    if not schedules: #
        print(Fore.YELLOW + Style.BRIGHT + "  Tidak ada jadwal dokter yang tersedia saat ini.") #
    else:
        table_data = [] #
        for schedule_item in schedules: #
            doctor_info = doctor_dict.get(schedule_item['dokter_id'], {"nama": Fore.RED + "N/A", "spesialisasi": Fore.RED + "N/A"}) #
            table_data.append([ #
                Fore.CYAN + schedule_item['id'] + Style.RESET_ALL,
                Fore.GREEN + doctor_info['nama'] + Style.RESET_ALL,
                Fore.BLUE + doctor_info['spesialisasi'] + Style.RESET_ALL,
                schedule_item['hari'], #
                f"{schedule_item['jam_mulai']}-{schedule_item['jam_selesai']}", #
                Fore.MAGENTA + schedule_item['kuota'] + Style.RESET_ALL #
            ])
        headers = [ #
            Style.BRIGHT + Fore.WHITE + "ID Jadwal", "Dokter", "Spesialisasi", "Hari", "Waktu", "Kuota" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers, tablefmt="rounded_outline", stralign="center")) #
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu...") #


def search_doctor_schedules(): #
    clear_screen() #
    show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Pasien", Fore.YELLOW + "Cari Jadwal" + Style.RESET_ALL]) #
    display_header("CARI JADWAL DOKTER", width=50) #

    print(Fore.CYAN + Style.BRIGHT + "Pilih Kriteria Pencarian:" + Style.RESET_ALL)
    print(Fore.CYAN + "-" * 35 + Style.RESET_ALL)
    print(Fore.WHITE + "  " + Style.BRIGHT + "1. " + Fore.YELLOW + "Berdasarkan Nama Dokter") #
    print(Fore.WHITE + "  " + Style.BRIGHT + "2. " + Fore.YELLOW + "Berdasarkan Spesialisasi") #
    print(Fore.WHITE + "  " + Style.BRIGHT + "3. " + Fore.YELLOW + "Berdasarkan Hari") #
    print(Fore.CYAN + "-" * 35 + Style.RESET_ALL)
    print(Fore.WHITE + "  " + Style.BRIGHT + "4. " + Fore.RED   + "Kembali ke Menu Pasien") #
    print()

    choice = input(Fore.MAGENTA + Style.BRIGHT + "➔ Pilihan Anda: " + Fore.WHITE) #

    if choice == "4": #
        return
    if choice not in ["1", "2", "3"]: #
        show_error("Pilihan kriteria tidak valid.") #
        search_doctor_schedules() # Kembali ke menu pencarian
        return

    loading = LoadingAnimation("Mencari jadwal...") #
    loading.start()

    schedules = read_csv("data/jadwal_dokter.csv") #
    doctors = read_csv("data/dokter.csv") #
    doctor_dict = {doc['id']: {"nama": doc['nama'], "spesialisasi": doc['spesialisasi']} for doc in doctors} #
    results = [] #
    search_term_display = ""

    if choice == "1": #
        loading.stop()
        search_key = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Masukkan nama dokter: " + Fore.WHITE).lower() #
        search_term_display = f"Nama Dokter: '{search_key}'"
        loading.start()
        for schedule in schedules: #
            doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"}) #
            if search_key in doctor_info['nama'].lower(): #
                results.append((schedule, doctor_info)) #
    elif choice == "2": #
        loading.stop()
        search_key = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Masukkan spesialisasi: " + Fore.WHITE).lower() #
        search_term_display = f"Spesialisasi: '{search_key}'"
        loading.start()
        for schedule in schedules: #
            doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"}) #
            if search_key in doctor_info['spesialisasi'].lower(): #
                results.append((schedule, doctor_info)) #
    elif choice == "3": #
        loading.stop()
        days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"] #
        print(Fore.CYAN + Style.BRIGHT + "\n  Hari yang tersedia:" + Style.RESET_ALL) #
        for i, day in enumerate(days, 1): #
            print(f"    {Fore.WHITE}{Style.BRIGHT}{i}. {Fore.YELLOW}{day}{Style.RESET_ALL}")
        print()
        try:
            day_choice_input = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Pilih hari (nomor): " + Fore.WHITE) #
            if not day_choice_input.isdigit():
                show_error("Pilihan hari harus berupa angka.") #
                search_doctor_schedules()
                return
            day_index = int(day_choice_input) - 1 #
            if day_index < 0 or day_index >= len(days): #
                show_error("Hari tidak valid.") #
                search_doctor_schedules()
                return
            selected_day = days[day_index] #
            search_term_display = f"Hari: '{selected_day}'"
            loading.start()
            for schedule in schedules: #
                doctor_info = doctor_dict.get(schedule['dokter_id'], {"nama": "Unknown", "spesialisasi": "Unknown"}) #
                if schedule['hari'] == selected_day: #
                    results.append((schedule, doctor_info)) #
        except ValueError: #
            show_error("Input tidak valid.") #
            search_doctor_schedules()
            return
    loading.stop()

    clear_screen() #
    show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Pasien", Fore.YELLOW + "Cari Jadwal", Fore.BLUE + "Hasil" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + f"HASIL PENCARIAN ({search_term_display})".center(100) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 100).center(100) + Style.RESET_ALL) #
    print()

    if not results: #
        print(Fore.YELLOW + Style.BRIGHT + "  Tidak ditemukan jadwal yang sesuai dengan kriteria pencarian Anda.") #
    else:
        table_data = [] #
        for schedule_res, doctor_info_res in results: #
            table_data.append([ #
                Fore.CYAN + schedule_res['id'] + Style.RESET_ALL,
                Fore.GREEN + doctor_info_res['nama'] + Style.RESET_ALL,
                Fore.BLUE + doctor_info_res['spesialisasi'] + Style.RESET_ALL,
                schedule_res['hari'], #
                f"{schedule_res['jam_mulai']}-{schedule_res['jam_selesai']}", #
                Fore.MAGENTA + schedule_res['kuota'] + Style.RESET_ALL #
            ])
        headers_res = [ #
            Style.BRIGHT + Fore.WHITE + "ID Jadwal", "Dokter", "Spesialisasi", "Hari", "Waktu", "Kuota" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers_res, tablefmt="rounded_outline", stralign="center")) #
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu...") #


def register_consultation(patient_id): #
    clear_screen() #
    show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Pasien", Fore.YELLOW + "Daftar Konsultasi" + Style.RESET_ALL]) #
    display_header("PENDAFTARAN KONSULTASI", width=50) #

    print(Fore.CYAN + Style.BRIGHT + "  Jadwal Dokter Tersedia:" + Style.RESET_ALL)
    # Panggil view_doctor_schedules secara internal untuk menampilkan tabel jadwal
    # Ini akan menggunakan gaya frameless jika view_doctor_schedules sudah disesuaikan
    view_doctor_schedules() # Tampilkan semua jadwal
    print() # Tambah baris baru setelah tabel jadwal

    schedule_id_input = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Masukkan ID jadwal yang ingin didaftar: " + Fore.WHITE).upper() #

    loading = LoadingAnimation("Memeriksa jadwal dan kuota...") #
    loading.start()

    schedules = read_csv("data/jadwal_dokter.csv") #
    selected_schedule = None
    for schedule_item_reg in schedules: #
        if schedule_item_reg['id'] == schedule_id_input: #
            selected_schedule = schedule_item_reg #
            break

    if not selected_schedule: #
        loading.stop()
        show_error(f"Jadwal dengan ID {Fore.YELLOW}{schedule_id_input}{Fore.RED} tidak ditemukan.") #
        return

    doctors = read_csv("data/dokter.csv") #
    doctor_name_reg = Fore.RED + "Dokter Tidak Dikenal" + Style.RESET_ALL
    for doctor_item_reg in doctors: #
        if doctor_item_reg['id'] == selected_schedule['dokter_id']: #
            doctor_name_reg = Fore.GREEN + doctor_item_reg['nama'] + Style.RESET_ALL #
            break

    days_map = {"Senin": 0, "Selasa": 1, "Rabu": 2, "Kamis": 3, "Jumat": 4, "Sabtu": 5, "Minggu": 6} #
    day_index_reg = days_map.get(selected_schedule['hari']) #
    if day_index_reg is None: #
        loading.stop()
        show_error("Hari jadwal tidak valid dalam sistem.") #
        return

    today = datetime.now() #
    days_ahead = (day_index_reg - today.weekday() + 7) % 7 #
    if days_ahead == 0 and today.hour >= int(selected_schedule['jam_selesai'].split(':')[0]): #
        days_ahead = 7 #
    next_occurrence = today + timedelta(days=days_ahead) #
    date_str = next_occurrence.strftime("%Y-%m-%d") #

    registrations_all = read_csv("data/pendaftaran.csv") #
    for reg_check in registrations_all: #
        if (reg_check['pasien_id'] == patient_id and reg_check['jadwal_id'] == schedule_id_input and #
            reg_check['tanggal'] == date_str and reg_check['status'] == 'Terdaftar'): #
            loading.stop()
            show_error(f"Anda sudah terdaftar pada jadwal ini ({Fore.YELLOW}{doctor_name_reg}{Fore.RED} - {Fore.YELLOW}{selected_schedule['hari']}, {date_str}{Fore.RED}).") #
            return

    quota_val = int(selected_schedule['kuota']) #
    registered_count = sum(1 for reg_count in registrations_all if #
                           reg_count['jadwal_id'] == schedule_id_input and
                           reg_count['tanggal'] == date_str and
                           reg_count['status'] == 'Terdaftar') #

    if registered_count >= quota_val: #
        loading.stop()
        show_error(f"Kuota untuk jadwal {Fore.YELLOW}{doctor_name_reg}{Fore.RED} pada tanggal {Fore.YELLOW}{date_str}{Fore.RED} sudah penuh.") #
        return

    queue_number = registered_count + 1 #
    new_reg_id = f"R{len(registrations_all) + 1:03d}" #
    new_registration = { #
        'id': new_reg_id, #
        'pasien_id': patient_id, #
        'jadwal_id': schedule_id_input, #
        'tanggal': date_str, #
        'status': 'Terdaftar', #
        'nomor_antrian': str(queue_number) #
    }
    registrations_all.append(new_registration) #
    write_csv("data/pendaftaran.csv", registrations_all) #
    loading.stop()

    display_subheader("🎉 PENDAFTARAN BERHASIL 🎉", width=50) #
    print(Fore.GREEN + Style.BRIGHT + f"  Selamat! Pendaftaran Anda telah berhasil." + Style.RESET_ALL) #
    print(Fore.CYAN + "  --------------------------------------------------")
    print(f"  {Fore.YELLOW}ID Pendaftaran  : {Style.BRIGHT}{Fore.WHITE}{new_reg_id}{Style.RESET_ALL}") #
    print(f"  {Fore.YELLOW}Dokter          : {Style.BRIGHT}{doctor_name_reg}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Jadwal          : {Style.BRIGHT}{Fore.WHITE}{selected_schedule['hari']}, {selected_schedule['jam_mulai']}-{selected_schedule['jam_selesai']}{Style.RESET_ALL}") #
    print(f"  {Fore.YELLOW}Tanggal         : {Style.BRIGHT}{Fore.WHITE}{date_str}{Style.RESET_ALL}") #
    print(f"  {Fore.YELLOW}Nomor Antrian   : {Style.BRIGHT}{Fore.MAGENTA}{queue_number}{Style.RESET_ALL}") #
    print(Fore.CYAN + "  --------------------------------------------------")
    print(Fore.GREEN + "  Mohon datang tepat waktu. Terima kasih!")
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu...") #


def request_schedule_change(patient_id): #
    clear_screen() #
    show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Pasien", Fore.YELLOW + "Ubah/Batalkan Pendaftaran" + Style.RESET_ALL]) #
    display_header("UBAH / BATALKAN PENDAFTARAN", width=50) #

    loading = LoadingAnimation("Memuat pendaftaran Anda...") #
    loading.start()

    registrations = read_csv("data/pendaftaran.csv") #
    patient_registrations_active = [reg for reg in registrations if #
                            reg['pasien_id'] == patient_id and
                            reg['status'] == 'Terdaftar'] #

    schedules = read_csv("data/jadwal_dokter.csv") #
    doctors = read_csv("data/dokter.csv") #
    schedule_dict_req = {sch['id']: sch for sch in schedules} #
    doctor_dict_req = {doc['id']: doc['nama'] for doc in doctors} #
    loading.stop()

    if not patient_registrations_active: #
        print(Fore.YELLOW + Style.BRIGHT + "  Anda tidak memiliki pendaftaran aktif yang dapat diubah atau dibatalkan.") #
        input(Fore.GREEN + Style.BRIGHT + "\n  Tekan Enter untuk kembali ke menu...") #
        return

    display_subheader("PENDAFTARAN AKTIF ANDA", width=100) #
    table_data_req = []
    reg_map_req = {}
    for i, reg_item_req in enumerate(patient_registrations_active, 1): #
        reg_map_req[str(i)] = reg_item_req['id']
        schedule_req = schedule_dict_req.get(reg_item_req['jadwal_id'], None) #
        if schedule_req: #
            doctor_name_req = Fore.GREEN + doctor_dict_req.get(schedule_req['dokter_id'], Fore.RED + "N/A") + Style.RESET_ALL
            schedule_info_req = f"{schedule_req['hari']} {schedule_req['jam_mulai']}-{schedule_req['jam_selesai']}" #
            table_data_req.append([ #
                Fore.MAGENTA + str(i) + Style.RESET_ALL,
                Fore.CYAN + reg_item_req['id'] + Style.RESET_ALL,
                doctor_name_req,
                schedule_info_req,
                reg_item_req['tanggal'], #
                Fore.BLUE + reg_item_req['nomor_antrian'] + Style.RESET_ALL #
            ])
    headers_req = [ #
        Style.BRIGHT + Fore.WHITE + "No.", "ID Reg.", "Dokter", "Jadwal", "Tanggal", "Antrian" + Style.RESET_ALL
    ]
    print(tabulate(table_data_req, headers=headers_req, tablefmt="rounded_outline", stralign="center")) #
    print()

    try:
        reg_choice_input = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Pilih nomor pendaftaran yang ingin diatur (atau '0' untuk batal): " + Fore.WHITE) #
        if reg_choice_input == '0':
            print(Fore.YELLOW + "  Tidak ada tindakan yang diambil.")
            input(Fore.GREEN + Style.BRIGHT + "\n  Tekan Enter untuk kembali...")
            return
        if not reg_choice_input.isdigit() or reg_choice_input not in reg_map_req: #
            show_error("Nomor pendaftaran tidak valid.") #
            return
        selected_reg_id_req = reg_map_req[reg_choice_input]

        print(Fore.CYAN + Style.BRIGHT + "\n  PILIHAN TINDAKAN" + Style.RESET_ALL)
        print(Fore.CYAN + "  " + "-" * 30 + Style.RESET_ALL)
        print(Fore.WHITE + "    " + Style.BRIGHT + "1. " + Fore.RED + "Batalkan Pendaftaran Ini") #
        print(Fore.WHITE + "    " + Style.BRIGHT + "2. " + Fore.YELLOW + "Kembali ke Menu Pasien") #
        print()

        action_choice_input = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Pilihan tindakan Anda: " + Fore.WHITE) #

        if action_choice_input == "1": #
            confirm_cancel_input = input(Fore.RED + Style.BRIGHT + f"    Apakah Anda yakin ingin membatalkan pendaftaran ID {Fore.YELLOW}{selected_reg_id_req}{Fore.RED}? (y/N): " + Fore.WHITE).lower()
            if confirm_cancel_input == 'y':
                loading = LoadingAnimation("Membatalkan pendaftaran...") #
                loading.start()
                updated_registrations = []
                cancelled_successfully = False
                for i_req, reg_item_update in enumerate(registrations): #
                    if reg_item_update['id'] == selected_reg_id_req: #
                        registrations[i_req]['status'] = 'Dibatalkan' #
                        cancelled_successfully = True
                    # This logic was flawed. It should be registrations[i_req] to build the updated list
                    # For simplicity and correctness, let's re-read and filter or directly modify and write
                # Corrected logic:
                for reg_to_write in registrations:
                    if reg_to_write['id'] == selected_reg_id_req:
                        reg_to_write['status'] = 'Dibatalkan' #
                        cancelled_successfully = True # Should be set if found
                
                if cancelled_successfully:
                    write_csv("data/pendaftaran.csv", registrations) #
                    loading.stop()
                    show_success(f"Pendaftaran ID {Fore.YELLOW}{selected_reg_id_req}{Fore.GREEN} berhasil dibatalkan.") #
                else: # Should not happen if selected_reg_id_req is valid
                    loading.stop()
                    show_error("Gagal menemukan pendaftaran untuk dibatalkan.") #
            else:
                print(Fore.YELLOW + "    Pembatalan tidak dilakukan.")
                input(Fore.GREEN + Style.BRIGHT + "\n    Tekan Enter untuk melanjutkan...")
        elif action_choice_input == "2": #
            return
        else:
            show_error("Pilihan tindakan tidak valid.") #
    except ValueError: #
        show_error("Input tidak valid.") #


def view_registration_status(patient_id): #
    clear_screen() #
    show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Pasien", Fore.YELLOW + "Status Pendaftaran Saya" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "STATUS PENDAFTARAN KONSULTASI SAYA".center(100) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 100).center(100) + Style.RESET_ALL) #
    print()
    loading = LoadingAnimation("Memuat status pendaftaran Anda...") #
    loading.start()

    registrations = read_csv("data/pendaftaran.csv") #
    patient_registrations_status = [reg for reg in registrations if reg['pasien_id'] == patient_id] #

    schedules = read_csv("data/jadwal_dokter.csv") #
    doctors = read_csv("data/dokter.csv") #
    schedule_dict_status = {sch['id']: sch for sch in schedules} #
    doctor_dict_status = {doc['id']: doc['nama'] for doc in doctors} #
    loading.stop()

    if not patient_registrations_status: #
        print(Fore.YELLOW + Style.BRIGHT + "  Anda belum memiliki riwayat pendaftaran konsultasi.") #
    else:
        table_data_status = []
        sorted_registrations_status = sorted(patient_registrations_status, key=lambda x: (x['tanggal'], x['id']), reverse=True)

        for reg_item_status in sorted_registrations_status: #
            schedule_status = schedule_dict_status.get(reg_item_status['jadwal_id'], None) #
            if schedule_status: #
                doctor_name_status = Fore.GREEN + doctor_dict_status.get(schedule_status['dokter_id'], Fore.RED + "N/A") + Style.RESET_ALL
                schedule_info_status = f"{schedule_status['hari']} {schedule_status['jam_mulai']}-{schedule_status['jam_selesai']}" #

                status_val = reg_item_status['status'] #
                status_display_val = status_val
                if status_val == 'Terdaftar': #
                    status_display_val = Fore.GREEN + Style.BRIGHT + status_val + Style.RESET_ALL
                elif status_val == 'Dibatalkan': #
                    status_display_val = Fore.RED + Style.BRIGHT + status_val + Style.RESET_ALL
                else: #
                    status_display_val = Fore.YELLOW + Style.BRIGHT + status_val + Style.RESET_ALL

                table_data_status.append([ #
                    Fore.CYAN + reg_item_status['id'] + Style.RESET_ALL, #
                    doctor_name_status,
                    Fore.BLUE + schedule_info_status + Style.RESET_ALL,
                    reg_item_status['tanggal'], #
                    status_display_val,
                    Fore.MAGENTA + reg_item_status['nomor_antrian'] + Style.RESET_ALL #
                ])
        headers_status_view = [ #
            Style.BRIGHT + Fore.WHITE + "ID Reg.", "Dokter", "Jadwal", "Tanggal", "Status", "Antrian" + Style.RESET_ALL
        ]
        print(tabulate(table_data_status, headers=headers_status_view, tablefmt="rounded_outline", stralign="center")) #
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu...") #
