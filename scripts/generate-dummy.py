import psycopg2
import random
from datetime import datetime, timedelta

# ==========================================
# 1. SIMULASI DATA DARI API (MOCKING)
# ==========================================
print("🔄 Mengambil data dari 'API Dummy'...")

dummy_data = []
# Membuat data pendapatan (Accurate) dan beban gaji (Talenta) untuk 14 hari terakhir
for i in range(14): 
    tanggal = (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')
    pendapatan = random.randint(15000000, 50000000) # Acak antara 15jt - 50jt
    beban_gaji = random.randint(3000000, 12000000)  # Acak antara 3jt - 12jt
    
    dummy_data.append({
        "tanggal": tanggal,
        "pendapatan": pendapatan,
        "beban_gaji": beban_gaji
    })

print(f"✅ Berhasil membuat {len(dummy_data)} baris data dummy.")

# ==========================================
# 2. KONEKSI KE DATA WAREHOUSE (SYNOLOGY)
# ==========================================
DB_HOST = "192.168.2.150" # PERHATIAN: Ganti dengan IP lokal Synology kamu
DB_PORT = "5555"        # Menggunakan port yang sudah kita konfigurasi
DB_NAME = "executive_dashboard"
DB_USER = "admin"
DB_PASS = "administrator"

try:
    print("🔄 Menghubungkan ke PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()
    print("✅ Berhasil terhubung!")

    # ==========================================
    # 3. PERSIAPAN TABEL & PROSES INSERT
    # ==========================================
    # Membuat tabel jika belum ada
    create_table_query = """
    CREATE TABLE IF NOT EXISTS laporan_keuangan_harian (
        tanggal DATE PRIMARY KEY,
        pendapatan NUMERIC,
        beban_gaji NUMERIC
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    print("✅ Tabel laporan_keuangan_harian siap.")

    # Memasukkan data (menggunakan UPSERT: Update jika tanggal sudah ada)
    insert_query = """
    INSERT INTO laporan_keuangan_harian (tanggal, pendapatan, beban_gaji)
    VALUES (%(tanggal)s, %(pendapatan)s, %(beban_gaji)s)
    ON CONFLICT (tanggal) 
    DO UPDATE SET 
        pendapatan = EXCLUDED.pendapatan,
        beban_gaji = EXCLUDED.beban_gaji;
    """
    
    for row in dummy_data:
        cur.execute(insert_query, row)
    
    conn.commit()
    print("✅ Data berhasil disimpan ke Database!")

except Exception as e:
    print(f"❌ Terjadi kesalahan: {e}")

finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
    print("🔌 Koneksi ditutup.")