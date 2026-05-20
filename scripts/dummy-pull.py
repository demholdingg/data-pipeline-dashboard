import time
import pandas as pd
import sys

def main():
    try:
        print("Memulai proses penarikan data...")
        time.sleep(1)
        
        # Simulasi data sederhana dengan Pandas
        data = {'id': [1, 2], 'status': ['success', 'pending']}
        df = pd.DataFrame(data)
        print(f"Data berhasil diproses:\n{df}")

        print("Berhasil mensimulasikan koneksi API!")
        print("Menyimpan data ke PostgreSQL di Synology...")
        time.sleep(1)
        
        print("Pipeline PoC Berjalan Sukses dari Runner Synology!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()