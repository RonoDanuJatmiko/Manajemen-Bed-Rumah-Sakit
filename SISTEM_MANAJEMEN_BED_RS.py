import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

########## BACKEND ############

class Pasien:
    def __init__(self, nama, umur):
        self.nama = nama
        self.umur = umur

class RumahSakit:
    def __init__(self):
        self.vip = {'jumlah_ruangan': 5, 'bed_per_ruangan': 1, 'okupansi': [0]*5}
        self.kelas_1 = {'jumlah_ruangan': 10, 'bed_per_ruangan': 4, 'okupansi': [0]*10}
        self.kelas_2 = {'jumlah_ruangan': 20, 'bed_per_ruangan': 8, 'okupansi': [0]*20}
        self.isolasi = {'jumlah_ruangan': 10, 'bed_per_ruangan': 1, 'okupansi': [0]*10}
        self.data_pasien = []

    def cek_ketersediaan(self, kelas):
        if kelas in ['vip', 'kelas_1', 'kelas_2', 'isolasi']:
            return self._cek_ketersediaan_kelas(getattr(self, kelas))
        else:
            return None, None

    def _cek_ketersediaan_kelas(self, kelas):
        for i, okupansi in enumerate(kelas['okupansi']):
            if okupansi < kelas['bed_per_ruangan']:
                return i, kelas['bed_per_ruangan'] - okupansi
        return None, None

    def tambah_pasien(self, kelas, nama, umur):
        ruangan, bed_tersedia = self.cek_ketersediaan(kelas)
        if ruangan is not None:
            pasien_baru = Pasien(nama, umur)
            self.data_pasien.append(pasien_baru)
            getattr(self, kelas)['okupansi'][ruangan] += 1
            return True, f"Pasien {nama} umur {umur} tahun ditambahkan ke {kelas} ruangan {ruangan+1}. Bed tersedia: {bed_tersedia-1}"
        else:
            return False, f"Tidak ada bed tersedia di kelas {kelas}. Silakan pilih kelas lain"

############### GUI ####################
### MAIN MENU ###
class rsgui:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEM MANAJEMEN BED RS HARAPAN BAPAK")
        self.rs = RumahSakit()
        self.buat_widget()

    def buat_widget(self):
        self.root.columnconfigure(0, weight=1)
        self.root.configure(background="#68d6ff")

        self.label_selamat_datang = tk.Label(self.root, text="SELAMAT DATANG DI RS HARAPAN BAPAK", font=("Times New Roman", 16), background="#68d6ff")
        self.label_selamat_datang.grid(row=0, column=0, columnspan=3, pady=10)

        self.label_menu = tk.Label(self.root, text="Pilih Jenis Pelayanan:", background="#68d6ff")
        self.label_menu.grid(row=1, column=0, padx=10)

        self.button_tambah_pasien = tk.Button(self.root, text="1. Tambah Pasien", command=self.tambah_pasien_window)
        self.button_tambah_pasien.grid(row=2, column=0, columnspan=1, pady=10)

        self.button_hapus_pasien = tk.Button(self.root, text="2. Hapus Pasien", command=self.hapus_pasien_window)
        self.button_hapus_pasien.grid(row=3, column=0, columnspan=1, pady=10)

        self.button_tampilkan_okupansi = tk.Button(self.root, text="3. Tampilkan Okupansi", command=self.tampilkan_okupansi)
        self.button_tampilkan_okupansi.grid(row=4, column=0, columnspan=1, pady=10)
        
        self.keluar = tk.Button(self.root, text="4. Keluar", command=self.keluar)
        self.keluar.grid(row=5, column=0, columnspan=1, pady=10)

### TAMBAH PASIEN ###
    def tambah_pasien_window(self):
        tambah_window = tk.Toplevel(self.root)
        tambah_window.title("Tambah Pasien")

        label_nama = tk.Label(tambah_window, text="Nama Pasien:")
        label_nama.grid(row=0, column=0, pady=10)
        entry_nama = tk.Entry(tambah_window)
        entry_nama.grid(row=0, column=1, pady=10)

        label_umur = tk.Label(tambah_window, text="Umur Pasien:")
        label_umur.grid(row=1, column=0, pady=10)
        entry_umur = tk.Entry(tambah_window)
        entry_umur.grid(row=1, column=1, pady=10)

        label_kelas = tk.Label(tambah_window, text="Kelas Ruangan")
        label_kelas.grid(row=2, column=0, pady=10)
        jenis_pelayanan_combobox = ttk.Combobox(tambah_window, values=["vip", "kelas_1", "kelas_2", "isolasi"])
        jenis_pelayanan_combobox.grid(row=2, column=1, columnspan=2, pady=10)

        tambah_button = tk.Button(tambah_window, text="Tambah Pasien", command=lambda: self.proses_tambah_pasien(entry_nama.get(), entry_umur.get(), jenis_pelayanan_combobox.get(), tambah_window))
        tambah_button.grid(row=3, column=0, columnspan=2, pady=10)

        back_button = tk.Button(tambah_window, text="Kembali Ke Main Menu", command=tambah_window.destroy)
        back_button.grid(row=4, column=0, columnspan=2, pady=10)

    def proses_tambah_pasien(self, nama, umur, kelas, window):
        if not nama or not umur:
            messagebox.showerror("Data Salah", "Nama dan umur pasien harus diisi")
            return

        try:
            umur = int(umur)
        except ValueError:
            messagebox.showerror("Data Salah", "Umur harus berupa angka")
            return
        
        if umur < 0:
            messagebox.showerror("Data Salah", "Umur harus lebih besar dari 0")
            return

        result, message = self.rs.tambah_pasien(kelas, nama, umur)
        if result:
            messagebox.showinfo("Data Benar", message)
        else:
            messagebox.showerror("Data Salah", message)

        window.destroy()

### HAPUS PASIEN ###
    def hapus_pasien_window(self):
        hapus_window = tk.Toplevel(self.root)
        hapus_window.title("Hapus Pasien")

        label_nama = tk.Label(hapus_window, text="Nama Pasien:")
        label_nama.grid(row=0, column=0, pady=10)
        entry_nama = tk.Entry(hapus_window)
        entry_nama.grid(row=0, column=1, pady=10)

        label_kelas = tk.Label(hapus_window, text="Kelas Ruangan")
        label_kelas.grid(row=2, column=0, pady=10)
        jenis_pelayanan_combobox = ttk.Combobox(hapus_window, values=["vip", "kelas_1", "kelas_2", "isolasi"])
        jenis_pelayanan_combobox.grid(row=2, column=1, columnspan=2, pady=10)

        label_ruangan = tk.Label(hapus_window, text="Ruangan:")
        label_ruangan.grid(row=3, column=0, pady=10)
        entry_ruangan = tk.Entry(hapus_window)
        entry_ruangan.grid(row=3, column=1, pady=10)

        hapus_button = tk.Button(hapus_window, text="Hapus Pasien", command=lambda: self.proses_hapus_pasien(entry_nama.get(), jenis_pelayanan_combobox.get(), entry_ruangan.get(), hapus_window))
        hapus_button.grid(row=4, column=0, columnspan=2, pady=10)

        back_button = tk.Button(hapus_window, text="Kembali Ke Main Menu", command=hapus_window.destroy)
        back_button.grid(row=5, column=0, columnspan=2, pady=10)

    def proses_hapus_pasien(self, nama, kelas, ruangan, window):
        if kelas not in ['vip', 'kelas_1', 'kelas_2', 'isolasi']:
            messagebox.showerror("Data Salah", "Kelas yang dipilih tidak valid")
            return

        try:
            ruangan = int(ruangan)
        except ValueError:
            messagebox.showerror("Data Salah", "Nomor ruangan harus berupa angka")
            return

        ruangan -= 1

        if ruangan < 0:
            messagebox.showerror("Data Salah", "Nomor ruangan harus lebih besar dari 0")
            return

        if ruangan >= getattr(self.rs, kelas)['jumlah_ruangan']:
            messagebox.showerror("Data Salah", "Nomor ruangan tidak valid untuk kelas {}".format(kelas))
            return

        if getattr(self.rs, kelas)['okupansi'][ruangan] > 0:
            getattr(self.rs, kelas)['okupansi'][ruangan] -= 1
            self.rs.data_pasien = [pasien for pasien in self.rs.data_pasien if pasien.nama != nama]
            messagebox.showinfo("Data Benar", f"Pasien {nama} dihapus dari {kelas} ruangan {ruangan + 1}")
        else:
            messagebox.showerror("Data Salah", f"Tidak ada pasien di {kelas} ruangan {ruangan + 1}")

        window.destroy()

### TAMPILKAN OKUPANSI ###
    def tampilkan_okupansi(self):
        okupansi_window = tk.Toplevel(self.root)
        okupansi_window.title("Okupansi Bed Rumah Sakit")

        text_widget = tk.Text(okupansi_window, wrap=tk.WORD, height=20, width=50)
        text_widget.grid(row=0, column=0, padx=10, pady=30)

        text_widget.insert(tk.END, "Okupansi Rumah Sakit:\n")
        for kelas in ['vip', 'kelas_1', 'kelas_2', 'isolasi']:
            text_widget.insert(tk.END, f"Kelas {kelas.upper()}:\n")
            for i, okupansi in enumerate(getattr(self.rs, kelas)['okupansi']):
                text_widget.insert(tk.END, f"  Ruangan {i+1}: {okupansi} dari {getattr(self.rs, kelas)['bed_per_ruangan']} bed terisi\n")

        back_button = tk.Button(okupansi_window, text="Kembali Ke Main Menu", command=okupansi_window.destroy)
        back_button.grid(row=1, column=0, pady=10)
        
### KELUAR ###
    def keluar(self):
        response = messagebox.askquestion("Konfirmasi Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?")
        if response == 'yes':
            self.root.destroy()

### MAIN ###
if __name__ == "__main__":
    root = tk.Tk()
    app = rsgui(root)
    root.mainloop()