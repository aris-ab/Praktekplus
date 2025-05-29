# modules/admin.py - Admin functionality
import os
from tabulate import tabulate
from colorama import Fore, Style
import modules.data_manager as dm #
import modules.data_structures.linked_list as ll
import modules.utils as utils #

def admin_menu(admin_id): #
    """Display admin menu and handle admin actions without frame."""
    while True:
        utils.clear_screen() #
        utils.show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Admin" + Style.RESET_ALL]) #
        utils.display_header("MENU ADMIN KLINIK", width=50) #

        print(Fore.CYAN + Style.BRIGHT + "PILIHAN MENU" + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 45 + Style.RESET_ALL)

        print(Fore.WHITE + "  " + Style.BRIGHT + "1. " + Fore.YELLOW + "Lihat Semua Jadwal Dokter") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "2. " + Fore.YELLOW + "Tambah Jadwal Dokter") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "3. " + Fore.YELLOW + "Edit Jadwal Dokter") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "4. " + Fore.YELLOW + "Hapus Jadwal Dokter") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "5. " + Fore.YELLOW + "Lihat Data Pasien") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "6. " + Fore.YELLOW + "Lihat Pendaftaran Konsultasi") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "7. " + Fore.YELLOW + "Lihat Statistik Klinik") #
        print(Fore.CYAN + "-" * 45 + Style.RESET_ALL)
        print(Fore.WHITE + "  " + Style.BRIGHT + "8. " + Fore.RED   + "Keluar") #
        print(Fore.WHITE + "  " + Style.BRIGHT + "?. " + Fore.GREEN + "Bantuan") #
        print()

        choice = input(Fore.MAGENTA + Style.BRIGHT + "➔ Pilihan Anda: " + Fore.WHITE) #

        if choice == "1": #
            view_all_schedules() #
        elif choice == "2": #
            add_doctor_schedule() #
        elif choice == "3": #
            edit_doctor_schedule() #
        elif choice == "4": #
            delete_doctor_schedule() #
        elif choice == "5": #
            view_patient_data() #
        elif choice == "6": #
            view_all_registrations() #
        elif choice == "7": #
            view_clinic_statistics() #
        elif choice == "8": #
            break
        elif choice == "?": #
            utils.show_help("admin") #
        else:
            utils.show_error("Pilihan tidak valid. Silakan coba lagi.") #

# --- Fungsi lainnya di admin.py (view_all_schedules, add_doctor_schedule, dst.) ---
# Perlu disesuaikan untuk menghilangkan header berbingkai jika `display_header` tidak dimodifikasi
# dan hanya menggunakan `utils.display_subheader` atau print judul biasa.
# Contoh untuk view_all_schedules:

def view_all_schedules(): #
    """View all doctor schedules without frame."""
    utils.clear_screen() #
    utils.show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Admin", Fore.YELLOW + "Lihat Jadwal" + Style.RESET_ALL]) #
    # Tidak menggunakan display_header dengan bingkai, tapi subheader atau print biasa
    print(Fore.CYAN + Style.BRIGHT + "JADWAL PRAKTEK DOKTER".center(80) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 80).center(80) + Style.RESET_ALL) #
    print()

    loading = utils.LoadingAnimation("Memuat data jadwal...") #
    loading.start()

    schedules = dm.read_csv("data/jadwal_dokter.csv") #
    doctors = dm.read_csv("data/dokter.csv") #

    doctor_dict = {} #
    for doctor in doctors: #
        doctor_dict[doctor['id']] = doctor['nama'] #

    schedule_list = ll.LinkedList() #
    for schedule in schedules: #
        doctor_name = doctor_dict.get(schedule['dokter_id'], Fore.RED + "Dokter Tidak Dikenal" + Fore.YELLOW) #
        schedule_data = { #
            'id': Fore.CYAN + schedule['id'] + Style.RESET_ALL,
            'dokter': Fore.GREEN + doctor_name + Style.RESET_ALL,
            'hari': schedule['hari'], #
            'waktu': f"{schedule['jam_mulai']} - {schedule['jam_selesai']}", #
            'kuota': Fore.MAGENTA + schedule['kuota'] + Style.RESET_ALL #
        }
        schedule_list.append(schedule_data) #

    loading.stop()

    all_schedules_data = schedule_list.display() #
    if not all_schedules_data: #
        print(Fore.YELLOW + Style.BRIGHT + "  Tidak ada jadwal yang tersedia saat ini.")
    else:
        table_data = [] #
        for sch_item in all_schedules_data: #
            table_data.append([ #
                sch_item['id'],
                sch_item['dokter'],
                sch_item['hari'],
                sch_item['waktu'],
                sch_item['kuota']
            ])

        headers = [ #
            Style.BRIGHT + Fore.WHITE + "ID",
            Style.BRIGHT + Fore.WHITE + "Dokter",
            Style.BRIGHT + Fore.WHITE + "Hari",
            Style.BRIGHT + Fore.WHITE + "Waktu",
            Style.BRIGHT + Fore.WHITE + "Kuota" + Style.RESET_ALL
            ]
        print(tabulate(table_data, headers=headers, tablefmt="rounded_outline", stralign="center")) #
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu...") #


def add_doctor_schedule(): #
    utils.clear_screen() #
    utils.show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Admin", Fore.YELLOW + "Tambah Jadwal" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "TAMBAH JADWAL DOKTER".center(50) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 50).center(50) + Style.RESET_ALL) #
    print()

    doctors = dm.read_csv("data/dokter.csv") #
    print(Fore.CYAN + Style.BRIGHT + "  Dokter yang tersedia:" + Style.RESET_ALL) #
    for i, doctor in enumerate(doctors, 1): #
        print(f"    {Fore.WHITE}{Style.BRIGHT}{i}. {Fore.GREEN}{doctor['nama']} {Style.DIM}({doctor['spesialisasi']}){Style.RESET_ALL}")
    print()

    try:
        doctor_choice = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Pilih dokter (nomor): " + Fore.WHITE) #
        if not doctor_choice.isdigit():
            utils.show_error("Pilihan dokter harus berupa angka.") #
            return
        doctor_index = int(doctor_choice) - 1

        if doctor_index < 0 or doctor_index >= len(doctors): #
            utils.show_error("Dokter tidak ditemukan.") #
            return

        doctor_id = doctors[doctor_index]['id'] #

        days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"] #
        print(Fore.CYAN + Style.BRIGHT + "\n  Hari yang tersedia:" + Style.RESET_ALL) #
        for i, day in enumerate(days, 1): #
            print(f"    {Fore.WHITE}{Style.BRIGHT}{i}. {Fore.YELLOW}{day}{Style.RESET_ALL}")
        print()

        day_choice_input = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Pilih hari (nomor): " + Fore.WHITE) #
        if not day_choice_input.isdigit():
            utils.show_error("Pilihan hari harus berupa angka.") #
            return
        day_index = int(day_choice_input) - 1

        if day_index < 0 or day_index >= len(days): #
            utils.show_error("Hari tidak valid.") #
            return

        selected_day = days[day_index] #
        start_time = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Jam mulai (format HH:MM): " + Fore.WHITE) #
        end_time = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Jam selesai (format HH:MM): " + Fore.WHITE) #
        quota = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Kuota pasien: " + Fore.WHITE) #

        if not utils.is_valid_time_format(start_time) or not utils.is_valid_time_format(end_time): #
            utils.show_error("Format waktu tidak valid (HH:MM).") #
            return

        if not quota.isdigit() or int(quota) <= 0: #
            utils.show_error("Input kuota tidak valid. Harus berupa angka positif.") #
            return

        schedules = dm.read_csv("data/jadwal_dokter.csv") #
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
        dm.write_csv("data/jadwal_dokter.csv", schedules) #

        utils.show_success(f"Jadwal berhasil ditambahkan dengan ID {Fore.YELLOW}{new_id}{Fore.GREEN}.") #

    except ValueError:
        utils.show_error("Input tidak valid. Pastikan nomor yang dimasukkan benar.") #


def edit_doctor_schedule(): #
    utils.clear_screen() #
    utils.show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Admin", Fore.YELLOW + "Edit Jadwal" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "EDIT JADWAL DOKTER".center(50) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 50).center(50) + Style.RESET_ALL) #
    print()

    # Menampilkan jadwal yang ada dengan gaya yang lebih bersih
    schedules_pre = dm.read_csv("data/jadwal_dokter.csv") #
    doctors_pre = dm.read_csv("data/dokter.csv") #
    doctor_dict_pre = {doc['id']: doc['nama'] for doc in doctors_pre}

    if not schedules_pre: #
        print(Fore.YELLOW + Style.BRIGHT + "  Tidak ada jadwal yang tersedia untuk diedit.")
        input(Fore.GREEN + Style.BRIGHT + "\n  Tekan Enter untuk kembali...")
        return

    table_data_pre = []
    for sched in schedules_pre: #
        doc_name = doctor_dict_pre.get(sched['dokter_id'], Fore.RED + "N/A" + Style.RESET_ALL)
        table_data_pre.append([
            Fore.CYAN + sched['id'] + Style.RESET_ALL,
            Fore.GREEN + doc_name + Style.RESET_ALL,
            sched['hari'], #
            f"{sched['jam_mulai']}-{sched['jam_selesai']}", #
            Fore.MAGENTA + sched['kuota'] + Style.RESET_ALL #
        ])
    headers_pre = [
        Style.BRIGHT + Fore.WHITE + "ID", "Dokter", "Hari", "Waktu", "Kuota" + Style.RESET_ALL
    ]
    print(tabulate(table_data_pre, headers=headers_pre, tablefmt="rounded_outline", stralign="center"))
    print()

    schedule_id = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Masukkan ID jadwal yang akan diedit: " + Fore.WHITE).upper() #

    schedules = dm.read_csv("data/jadwal_dokter.csv") #
    found_schedule = None
    schedule_idx = -1

    for i, schedule_item in enumerate(schedules): #
        if schedule_item['id'] == schedule_id: #
            found_schedule = schedule_item
            schedule_idx = i
            break

    if not found_schedule: #
        utils.show_error(f"Jadwal dengan ID {schedule_id} tidak ditemukan.") #
        return

    print(Fore.CYAN + Style.BRIGHT + f"\n  Mengedit Jadwal ID: {Fore.YELLOW}{schedule_id}{Style.RESET_ALL}")
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"] #
    print(Fore.CYAN + Style.BRIGHT + "\n  Hari yang tersedia:" + Style.RESET_ALL) #
    for j, day_item in enumerate(days, 1): #
        current_marker = Fore.GREEN + " (Saat ini)" + Style.RESET_ALL if found_schedule['hari'] == day_item else ""
        print(f"    {Fore.WHITE}{Style.BRIGHT}{j}. {Fore.YELLOW}{day_item}{Style.RESET_ALL}{current_marker}")
    print()

    try:
        day_choice = input(Fore.MAGENTA + Style.BRIGHT + f"  ➔ Pilih hari baru (nomor, kosongkan jika tidak berubah [{found_schedule['hari']}]): " + Fore.WHITE) #
        selected_day = found_schedule['hari'] #
        if day_choice:
            if not day_choice.isdigit():
                utils.show_error("Pilihan hari harus berupa angka.") #
                return
            day_idx = int(day_choice) - 1
            if day_idx < 0 or day_idx >= len(days): #
                utils.show_error("Hari tidak valid.") #
                return
            selected_day = days[day_idx] #

        start_time = input(Fore.MAGENTA + Style.BRIGHT + f"  ➔ Jam mulai baru (HH:MM, kosongkan jika tidak berubah [{found_schedule['jam_mulai']}]): " + Fore.WHITE) #
        end_time = input(Fore.MAGENTA + Style.BRIGHT + f"  ➔ Jam selesai baru (HH:MM, kosongkan jika tidak berubah [{found_schedule['jam_selesai']}]): " + Fore.WHITE) #
        quota = input(Fore.MAGENTA + Style.BRIGHT + f"  ➔ Kuota pasien baru (kosongkan jika tidak berubah [{found_schedule['kuota']}]): " + Fore.WHITE) #

        final_start_time = start_time if start_time else found_schedule['jam_mulai'] #
        final_end_time = end_time if end_time else found_schedule['jam_selesai'] #
        final_quota = quota if quota else found_schedule['kuota'] #

        if start_time and not utils.is_valid_time_format(final_start_time): #
            utils.show_error("Format waktu mulai tidak valid (HH:MM).") #
            return
        if end_time and not utils.is_valid_time_format(final_end_time): #
            utils.show_error("Format waktu selesai tidak valid (HH:MM).") #
            return
        if quota and (not final_quota.isdigit() or int(final_quota) <= 0): #
            utils.show_error("Kuota harus berupa angka positif.") #
            return

        schedules[schedule_idx]['hari'] = selected_day #
        schedules[schedule_idx]['jam_mulai'] = final_start_time #
        schedules[schedule_idx]['jam_selesai'] = final_end_time #
        schedules[schedule_idx]['kuota'] = final_quota #

        dm.write_csv("data/jadwal_dokter.csv", schedules) #
        utils.show_success(f"Jadwal ID {Fore.YELLOW}{schedule_id}{Fore.GREEN} berhasil diperbarui.") #

    except ValueError:
        utils.show_error("Input tidak valid.") #


def delete_doctor_schedule(): #
    utils.clear_screen() #
    utils.show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Admin", Fore.YELLOW + "Hapus Jadwal" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "HAPUS JADWAL DOKTER".center(50) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 50).center(50) + Style.RESET_ALL) #
    print()

    schedules_list = dm.read_csv("data/jadwal_dokter.csv") #
    if not schedules_list: #
        print(Fore.YELLOW + Style.BRIGHT + "  Tidak ada jadwal yang tersedia untuk dihapus.")
        input(Fore.GREEN + Style.BRIGHT + "\n  Tekan Enter untuk kembali...")
        return

    # Reuse view_all_schedules logic for display if possible, or simplify display here
    view_all_schedules() # Panggil fungsi view_all_schedules yang sudah diperbarui
    print()

    schedule_id = input(Fore.MAGENTA + Style.BRIGHT + "  ➔ Masukkan ID jadwal yang akan dihapus: " + Fore.WHITE).upper() #

    schedules = dm.read_csv("data/jadwal_dokter.csv") #
    registrations = dm.read_csv("data/pendaftaran.csv") #

    active_registrations = [reg for reg in registrations if reg['jadwal_id'] == schedule_id and reg['status'] != 'Dibatalkan'] #

    if active_registrations: #
        utils.show_error(f"Tidak dapat menghapus jadwal {Fore.YELLOW}{schedule_id}{Fore.RED} karena ada pendaftaran aktif.") #
        return

    schedule_to_delete = None
    for sch_item_del in schedules: #
        if sch_item_del['id'] == schedule_id: #
            schedule_to_delete = sch_item_del
            break

    if not schedule_to_delete:
        utils.show_error(f"Jadwal dengan ID {Fore.YELLOW}{schedule_id}{Fore.RED} tidak ditemukan.") #
        return

    confirm = input(Fore.RED + Style.BRIGHT + f"  Apakah Anda yakin ingin menghapus jadwal ID {Fore.YELLOW}{schedule_id}{Fore.RED}? (y/N): " + Fore.WHITE).lower()
    if confirm == 'y':
        updated_schedules = [sch_upd for sch_upd in schedules if sch_upd['id'] != schedule_id] #
        dm.write_csv("data/jadwal_dokter.csv", updated_schedules) #
        utils.show_success(f"Jadwal ID {Fore.YELLOW}{schedule_id}{Fore.GREEN} berhasil dihapus.") #
    else:
        print(Fore.YELLOW + "  Penghapusan dibatalkan.")
        input(Fore.GREEN + Style.BRIGHT + "\n  Tekan Enter untuk melanjutkan...")


def view_patient_data(): #
    utils.clear_screen() #
    utils.show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Admin", Fore.YELLOW + "Data Pasien" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "DATA PASIEN TERDAFTAR".center(80) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 80).center(80) + Style.RESET_ALL) #
    print()

    loading = utils.LoadingAnimation("Memuat data pasien...") #
    loading.start()

    patients = dm.read_csv("data/pasien.csv") #
    loading.stop()

    if not patients: #
        print(Fore.YELLOW + Style.BRIGHT + "  Tidak ada data pasien terdaftar.") #
    else:
        table_data = [] #
        for patient_item in patients: #
            table_data.append([ #
                Fore.CYAN + patient_item['id'] + Style.RESET_ALL, #
                Fore.GREEN + patient_item['nama'] + Style.RESET_ALL, #
                patient_item['username'], #
                patient_item['kontak'] #
            ])

        headers = [ #
            Style.BRIGHT + Fore.WHITE + "ID", "Nama", "Username", "Kontak" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers, tablefmt="rounded_outline", stralign="center")) #
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu...") #


def view_all_registrations(): #
    utils.clear_screen() #
    utils.show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Admin", Fore.YELLOW + "Data Pendaftaran" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "DATA PENDAFTARAN KONSULTASI".center(110) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 110).center(110) + Style.RESET_ALL) #
    print()

    loading = utils.LoadingAnimation("Memuat data pendaftaran...") #
    loading.start()

    registrations = dm.read_csv("data/pendaftaran.csv") #
    loading.stop()

    if not registrations: #
        print(Fore.YELLOW + Style.BRIGHT + "  Tidak ada data pendaftaran.") #
    else:
        table_data = [] #
        for reg_item in registrations: #
            patient_name = dm.get_patient_name(reg_item['pasien_id']) #
            schedule_details = dm.get_schedule_details(reg_item['jadwal_id']) #

            status = reg_item['status'] #
            status_display = status
            if status == 'Terdaftar': #
                status_display = Fore.GREEN + Style.BRIGHT + status + Style.RESET_ALL
            elif status == 'Dibatalkan': #
                status_display = Fore.RED + Style.BRIGHT + status + Style.RESET_ALL
            else: #
                status_display = Fore.YELLOW + Style.BRIGHT + status + Style.RESET_ALL

            table_data.append([ #
                Fore.CYAN + reg_item['id'] + Style.RESET_ALL,
                Fore.GREEN + patient_name + Style.RESET_ALL,
                Fore.BLUE + schedule_details + Style.RESET_ALL,
                reg_item['tanggal'], #
                status_display,
                Fore.MAGENTA + reg_item['nomor_antrian'] + Style.RESET_ALL #
            ])

        headers = [ #
            Style.BRIGHT + Fore.WHITE + "ID Reg.", "Pasien", "Dokter & Jadwal",
            "Tanggal", "Status", "Antrian" + Style.RESET_ALL
        ]
        print(tabulate(table_data, headers=headers, tablefmt="rounded_outline", stralign="center")) #
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu...") #


def view_clinic_statistics(): #
    utils.clear_screen() #
    utils.show_breadcrumbs([Fore.CYAN + "Menu Utama", Fore.GREEN + "Admin", Fore.YELLOW + "Statistik" + Style.RESET_ALL]) #
    print(Fore.CYAN + Style.BRIGHT + "STATISTIK KLINIK".center(70) + Style.RESET_ALL) #
    print(Fore.CYAN + ("-" * 70).center(70) + Style.RESET_ALL) #
    print()

    loading = utils.LoadingAnimation("Menganalisis data...") #
    loading.start()

    schedules = dm.read_csv("data/jadwal_dokter.csv") #
    doctors = dm.read_csv("data/dokter.csv") #
    patients = dm.read_csv("data/pasien.csv") #
    registrations = dm.read_csv("data/pendaftaran.csv") #

    active_registrations = [reg for reg in registrations if reg['status'] != 'Dibatalkan'] #
    reg_by_day = {} #
    for reg in active_registrations: #
        schedule_id = reg['jadwal_id'] #
        day = None
        for sch in schedules: #
            if sch['id'] == schedule_id: #
                day = sch['hari'] #
                break
        if day: #
            reg_by_day[day] = reg_by_day.get(day, 0) + 1 #

    reg_by_doctor = {} #
    for reg in active_registrations: #
        schedule_id = reg['jadwal_id'] #
        doctor_id = None
        for sch in schedules: #
            if sch['id'] == schedule_id: #
                doctor_id = sch['dokter_id'] #
                break
        if doctor_id: #
            doctor_name = None
            for doc_item in doctors: #
                if doc_item['id'] == doctor_id: #
                    doctor_name = doc_item['nama'] #
                    break
            if doctor_name: #
                reg_by_doctor[doctor_name] = reg_by_doctor.get(doctor_name, 0) + 1 #

    reg_by_status = {} #
    for reg in registrations: #
        status = reg['status'] #
        reg_by_status[status] = reg_by_status.get(status, 0) + 1 #

    loading.stop()

    print(f"  {Fore.YELLOW}Total Dokter: {Fore.WHITE}{len(doctors)}{Style.RESET_ALL}") #
    print(f"  {Fore.YELLOW}Total Pasien: {Fore.WHITE}{len(patients)}{Style.RESET_ALL}") #
    print(f"  {Fore.YELLOW}Total Jadwal: {Fore.WHITE}{len(schedules)}{Style.RESET_ALL}") #
    print(f"  {Fore.YELLOW}Total Pendaftaran Aktif: {Fore.WHITE}{len(active_registrations)}{Style.RESET_ALL}") #
    print()

    utils.display_subheader("PENDAFTARAN PER HARI", width=70) #
    if not reg_by_day: #
        print(Fore.YELLOW + "  Belum ada data pendaftaran.") #
    else:
        table_data_day = []
        for day, count in sorted(reg_by_day.items(), key=lambda x: x[1], reverse=True): #
            table_data_day.append([Fore.GREEN + day + Style.RESET_ALL, Fore.MAGENTA + str(count) + Style.RESET_ALL])
        headers_day = [Style.BRIGHT + Fore.WHITE + "Hari", "Jumlah Pendaftaran" + Style.RESET_ALL] #
        print(tabulate(table_data_day, headers=headers_day, tablefmt="rounded_outline", stralign="center")) #
    print()

    utils.display_subheader("PENDAFTARAN PER DOKTER", width=70) #
    if not reg_by_doctor: #
        print(Fore.YELLOW + "  Belum ada data pendaftaran.") #
    else:
        table_data_doc = []
        for doctor_name, count in sorted(reg_by_doctor.items(), key=lambda x: x[1], reverse=True): #
            table_data_doc.append([Fore.GREEN + doctor_name + Style.RESET_ALL, Fore.MAGENTA + str(count) + Style.RESET_ALL])
        headers_doc = [Style.BRIGHT + Fore.WHITE + "Dokter", "Jumlah Pendaftaran" + Style.RESET_ALL] #
        print(tabulate(table_data_doc, headers=headers_doc, tablefmt="rounded_outline", stralign="center")) #
    print()

    utils.display_subheader("PENDAFTARAN PER STATUS", width=70) #
    if not reg_by_status: #
        print(Fore.YELLOW + "  Belum ada data pendaftaran.") #
    else:
        table_data_status = [] #
        for status, count in reg_by_status.items(): #
            status_colored = status
            if status == "Terdaftar": status_colored = Fore.GREEN + Style.BRIGHT + status + Style.RESET_ALL
            elif status == "Dibatalkan": status_colored = Fore.RED + Style.BRIGHT + status + Style.RESET_ALL
            else: status_colored = Fore.YELLOW + Style.BRIGHT + status + Style.RESET_ALL
            table_data_status.append([status_colored, Fore.MAGENTA + str(count) + Style.RESET_ALL])
        headers_status = [Style.BRIGHT + Fore.WHITE + "Status", "Jumlah" + Style.RESET_ALL] #
        print(tabulate(table_data_status, headers=headers_status, tablefmt="rounded_outline", stralign="center")) #
    print()
    input(Fore.GREEN + Style.BRIGHT + "Tekan Enter untuk kembali ke menu...") #