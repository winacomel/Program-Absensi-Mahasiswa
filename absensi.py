import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

def register():
    reg_window = tk.Toplevel(root)
    reg_window.title("Registrasi")

    tk.Label(reg_window, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    reg_username = tk.Entry(reg_window)
    reg_username.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(reg_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    reg_password = tk.Entry(reg_window, show='*')
    reg_password.grid(row=1, column=1, padx=5, pady=5)

    def save_registration():
        username = reg_username.get()
        password = reg_password.get()
        if username and password:
            with open('users.txt', 'a') as file:
                file.write(f'{username},{password}\n')
            messagebox.showinfo("Registrasi Berhasil", "Registrasi berhasil. Silakan login.")
            reg_window.destroy()
        else:
            messagebox.showwarning("Registrasi Gagal", "Username dan password harus diisi.")

    tk.Button(reg_window, text="Register", command=save_registration).grid(row=2, columnspan=2, pady=5)

def login():
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    login_username = tk.Entry(login_window)
    login_username.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    login_password = tk.Entry(login_window, show='*')
    login_password.grid(row=1, column=1, padx=5, pady=5)

    def check_login():
        username = login_username.get()
        password = login_password.get()
        if username and password:
            try:
                with open('users.txt', 'r') as file:
                    users = file.readlines()
                    for user in users:
                        stored_user, stored_pass = user.strip().split(',')
                        if stored_user == username and stored_pass == password:
                            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}")
                            login_window.destroy()
                            show_main_window()  # Menampilkan program absensi setelah login berhasil
                            return
                messagebox.showerror("Login Gagal", "Username atau password salah.")
            except FileNotFoundError:
                messagebox.showerror("Error", "File users.txt tidak ditemukan.")
        else:
            messagebox.showwarning("Login Gagal", "Username dan password harus diisi.")

    tk.Button(login_window, text="Login", command=check_login).grid(row=2, columnspan=2, pady=5)

def absensi():
    nama = entry_nama.get()
    status = combo_status.get()
    mata_kuliah = combo_matkul.get()
    semester = combo_semester.get()
    tanggal = entry_tanggal.get()

    if nama and mata_kuliah and tanggal:
        today_date = datetime.now().strftime("%Y-%m-%d")
        if tanggal == today_date:
            if status == "Izin":
                tree.insert('', 'end', values=(nama, mata_kuliah, status, "", semester, tanggal))
            elif status == "Sakit":
                alasan = entry_alasan.get()
                tree.insert('', 'end', values=(nama, mata_kuliah, status, alasan, semester, tanggal))
            else:
                tree.insert('', 'end', values=(nama, mata_kuliah, status, "", semester, tanggal))
            
            entry_nama.delete(0, 'end')
            entry_alasan.delete(0, 'end')
            combo_status.set("Hadir")
            combo_matkul.set("Pilih Mata Kuliah")
            combo_semester.set("Semester 1")
            entry_tanggal.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Absensi hanya dapat dilakukan untuk hari ini.")
    else:
        messagebox.showerror("Error", "Harap lengkapi semua data.")

def show_main_window():
    main_window = tk.Toplevel(root)
    main_window.title("Aplikasi Absensi Mahasiswa")

    frame_input = ttk.Frame(main_window)
    frame_input.pack(padx=10, pady=10)

    label_nama = ttk.Label(frame_input, text="Nama Mahasiswa:")
    label_nama.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    global entry_nama
    entry_nama = ttk.Entry(frame_input)
    entry_nama.grid(row=0, column=1, padx=5, pady=5)

    label_matkul = ttk.Label(frame_input, text="Mata Kuliah:")
    label_matkul.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    matkul_options = {
        "Semester 1": ["Pilih Mata Kuliah", "Kalkulus", "Fisika", "Kimia"],
        "Semester 2": ["Pilih Mata Kuliah", "Biologi", "Bahasa Inggris", "Sejarah"],
        "Semester 3": ["Pilih Mata Kuliah", "Ekonomi", "PMS", "Pancasila"],
        "Semester 4": ["Pilih Mata Kuliah", "Algoritma", "Pemrograman", "Statistika"],
        "Semester 5": ["Pilih Mata Kuliah", "Jaringan Komputer", "Sistem Operasi", "Basis Data"],
        "Semester 6": ["Pilih Mata Kuliah", "PBO", "Struktur Data", "Kecerdasan Buatan"],
        "Semester 7": ["Pilih Mata Kuliah", "Kriptografi", "Keamanan Jaringan", "Big Data"],
        "Semester 8": ["Pilih Mata Kuliah", "IoT", "Cloud Computing", "Cybersecurity"]
    }

    global combo_matkul
    combo_matkul = ttk.Combobox(frame_input, state="readonly")
    combo_matkul.set("Pilih Mata Kuliah")
    combo_matkul.grid(row=1, column=1, padx=5, pady=5)

    def update_matkul(event):
        selected_semester = combo_semester.get()
        matkul_list = matkul_options[selected_semester]
        combo_matkul['values'] = matkul_list
        combo_matkul.set("Pilih Mata Kuliah")

    global combo_semester
    combo_semester = ttk.Combobox(frame_input, values=["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5", "Semester 6", "Semester 7", "Semester 8"], state="readonly")
    combo_semester.set("Semester 1")
    combo_semester.grid(row=2, column=1, padx=5, pady=5)
    combo_semester.bind("<<ComboboxSelected>>", update_matkul)

    label_tanggal = ttk.Label(frame_input, text="Tanggal (YYYY-MM-DD):")
    label_tanggal.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    global entry_tanggal
    entry_tanggal = ttk.Entry(frame_input)
    entry_tanggal.grid(row=3, column=1, padx=5, pady=5)

    label_status = ttk.Label(frame_input, text="Status Kehadiran:")
    label_status.grid(row=4, column=0, padx=5, pady=5, sticky="w")

    status_options = ["Hadir", "Izin", "Sakit"]
    global combo_status
    combo_status = ttk.Combobox(frame_input, values=status_options, state="readonly")
    combo_status.set("Hadir")
    combo_status.grid(row=4, column=1, padx=5, pady=5)

    label_alasan = ttk.Label(frame_input, text="Alasan Sakit:")
    label_alasan.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    global entry_alasan
    entry_alasan = ttk.Entry(frame_input)
    entry_alasan.grid(row=5, column=1, padx=5, pady=5)

    button_absen = ttk.Button(frame_input, text="Absen", command=absensi)
    button_absen.grid(row=6, columnspan=2, padx=5, pady=5)

    frame_tabel = ttk.Frame(main_window)
    frame_tabel.pack(padx=10, pady=10)

    columns = ("Nama", "Mata Kuliah", "Status", "Alasan Sakit", "Semester", "Tanggal")
    global tree
    tree = ttk.Treeview(frame_tabel, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)

    tree.pack()

root = tk.Tk()
root.title("Login dan Registrasi")

tk.Button(root, text="Login", command=login).pack(padx=10, pady=5)
tk.Button(root, text="Register", command=register).pack(padx=10, pady=5)

root.mainloop()