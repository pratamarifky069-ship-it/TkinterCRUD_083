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


