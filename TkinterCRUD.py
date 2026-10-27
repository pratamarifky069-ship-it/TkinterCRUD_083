import tkinter as tk
from tkinter import messagebox
import sqlite3

# Membuat database dan tabel
def create_db():
    conn = sqlite3.connect("nilai_siswa.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_db()

# Fungsi menentukan prediksi fakultas
def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Dapat Ditemukan"

# Fungsi submit nilai
def submit_nilai():
    nama = entry_nama.get().strip()

    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror(
            "Error",
            "Semua nilai harus diisi dengan angka!"
        )
        return

    if not nama:
        messagebox.showerror(
            "Error",
            "Nama siswa tidak boleh kosong!"
        )
        return

    if bio < 0 or bio > 100 or fis < 0 or fis > 100 or ing < 0 or ing > 100:
        messagebox.showerror(
            "Error",
            "Nilai harus antara 0 sampai 100!"
        )
        return

    hasil_prediksi = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    conn.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil_prediksi))

    conn.commit()
    conn.close()

    hasil.config(text="Hasil Prediksi: " + hasil_prediksi)

    messagebox.showinfo(
        "Hasil Prediksi",
        "Nama: " + nama + "\nPrediksi Fakultas: " + hasil_prediksi
    )

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)


# Efek ketika kursor berada di tombol
def on_enter(e):
    btn_submit["bg"] = "#50fa7b"
    btn_submit["fg"] = "black"


# Efek ketika kursor meninggalkan tombol
def on_leave(e):
    btn_submit["bg"] = "#243f60"
    btn_submit["fg"] = "white"


# Membuat jendela aplikasi
root = tk.Tk()
root.title("Prediksi Fakultas")
root.geometry("500x600")
root.configure(bg="#f0f4f8")
root.resizable(False, False)


# Header aplikasi
judul = tk.Label(
    root,
    text="Aplikasi Prediksi Fakultas",
    font=("Arial", 18, "bold"),
    bg="#243f60",
    fg="white",
    pady=20
)
judul.pack(fill="x")

# Frame untuk form input
form = tk.Frame(root, bg="#f0f4f8")
form.pack(pady=20)

# Input nama siswa
tk.Label(
    form,
    text="Nama Siswa",
    font=("Arial", 11, "bold"),
    bg="#f0f4f8"
).grid(row=0, column=0, sticky="w", pady=8)

entry_nama = tk.Entry(form, width=30, font=("Arial", 11))
entry_nama.grid(row=0, column=1, padx=10, pady=8)

# Input nilai Biologi
tk.Label(
    form,
    text="Nilai Biologi",
    font=("Arial", 11, "bold"),
    bg="#f0f4f8"
).grid(row=1, column=0, sticky="w", pady=8)

entry_bio = tk.Entry(form, width=30, font=("Arial", 11))
entry_bio.grid(row=1, column=1, padx=10, pady=8)


