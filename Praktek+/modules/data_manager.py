# modules/data_manager.py - Data management module
import csv
import os
from datetime import datetime
from colorama import Fore

def initialize_data():
    """Initialize data files if they don't exist."""
    # Create admin.csv if it doesn't exist
    if not os.path.exists("data/admin.csv"):
        with open("data/admin.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'nama', 'username', 'password'])
            writer.writerow(['A001', 'Admin Klinik', 'admin', 'admin123'])
    
    # Create dokter.csv if it doesn't exist
    if not os.path.exists("data/dokter.csv"):
        with open("data/dokter.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'nama', 'spesialisasi', 'username', 'password'])
            writer.writerow(['D001', 'Dr. Andi', 'Umum', 'drandi', 'doctor123'])
            writer.writerow(['D002', 'Dr. Budi', 'Gigi', 'drbudi', 'doctor123'])
            writer.writerow(['D003', 'Dr. Citra', 'Anak', 'drcitra', 'doctor123'])
            writer.writerow(['D004', 'Dr. Dewi', 'Kulit', 'drdewi', 'doctor123'])
    
    # Create pasien.csv if it doesn't exist
    if not os.path.exists("data/pasien.csv"):
        with open("data/pasien.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'nama', 'username', 'password', 'kontak'])
            writer.writerow(['P001', 'Pasien Test', 'pasien', 'pasien123', '08123456789'])
    
    # Create jadwal_dokter.csv if it doesn't exist
    if not os.path.exists("data/jadwal_dokter.csv"):
        with open("data/jadwal_dokter.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'dokter_id', 'hari', 'jam_mulai', 'jam_selesai', 'kuota'])
            writer.writerow(['J001', 'D001', 'Senin', '08:00', '12:00', '10'])
            writer.writerow(['J002', 'D001', 'Rabu', '13:00', '17:00', '10'])
            writer.writerow(['J003', 'D002', 'Selasa', '08:00', '14:00', '8'])
            writer.writerow(['J004', 'D003', 'Kamis', '09:00', '15:00', '12'])
            writer.writerow(['J005', 'D004', 'Jumat', '10:00', '16:00', '8'])
    
    # Create pendaftaran.csv if it doesn't exist
    if not os.path.exists("data/pendaftaran.csv"):
        with open("data/pendaftaran.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'pasien_id', 'jadwal_id', 'tanggal', 'status', 'nomor_antrian'])

def read_csv(filename):
    """Read CSV file and return data as list of dictionaries."""
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(filename, data):
    """Write data to CSV file."""
    if not data:
        return
    
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def get_doctor_name(doctor_id):
    """Get doctor name from doctor ID."""
    doctors = read_csv("data/dokter.csv")
    for doctor in doctors:
        if doctor['id'] == doctor_id:
            return doctor['nama']
    return "Unknown Doctor"

def get_patient_name(patient_id):
    """Get patient name from patient ID."""
    patients = read_csv("data/pasien.csv")
    for patient in patients:
        if patient['id'] == patient_id:
            return patient['nama']
    return "Unknown Patient"

def get_schedule_details(schedule_id):
    """Get schedule details from schedule ID."""
    schedules = read_csv("data/jadwal_dokter.csv")
    for schedule in schedules:
        if schedule['id'] == schedule_id:
            doctor_name = get_doctor_name(schedule['dokter_id'])
            return f"{doctor_name} - {schedule['hari']} {schedule['jam_mulai']}-{schedule['jam_selesai']}"
    return "Unknown Schedule"