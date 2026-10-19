import numpy as np
import pandas as pd
from datetime import datetime

# Menjaga konsistensi random seed
np.random.seed(42)

print('=== PIPELINE IoT & PEMANTAUAN LINGKUNGAN: SENSOR & SATELIT TELEMETRY ===')

# ================= ================= =================
# 1. SIMULASI DATA TELEMETRY SENSOR IoT / PENGINDERAAN JAUH
# ================= ================= =================
n_samples = 1200
timestamps = pd.date_range(start='2026-10-01', periods=n_samples, freq='h')

sensor_nodes = ['NODE-AMAZON-01', 'NODE-CONGO-02', 'NODE-BORNEO-03']

raw_telemetry = {
    'timestamp': timestamps,
    'node_id': np.random.choice(sensor_nodes, size=n_samples),
    'optical_reflectance_nir': np.random.normal(loc=0.45, scale=0.10, size=n_samples), # Data Sentinel-2 (NIR)
    'radar_backscatter_db': np.random.normal(loc=-12.5, scale=2.0, size=n_samples), # Data Sentinel-1 (SAR)
    'moisture_index': np.random.uniform(0.1, 0.9, size=n_samples)
}

df_iot = pd.DataFrame(raw_telemetry)

# Menyisipkan noise / missing values akibat gangguan cuaca atau awan di wilayah tropis[cite: 4]
df_iot.loc[df_iot.sample(frac=0.03, random_state=42).index, 'optical_reflectance_nir'] = np.nan
df_iot.loc[df_iot.sample(frac=0.02, random_state=42).index, 'radar_backscatter_db'] = 999.0 # Error sensor

print(f'Total Telemetry Data Received: {len(df_iot)} records[cite: 4]')
print(f"Missing Values (Optical/Cloud): {df_iot['optical_reflectance_nir'].isna().sum()} items[cite: 4]")
print(f"Sensor Error Anomalies (Radar): {(df_iot['radar_backscatter_db'] == 999.0).sum()} items\n")

# ================= ================= =================
# 2. DATA PREPROCESSING & CLEANSING
# ================= ================= =================
df_clean = df_iot.copy()
# Membersihkan error nilai ekstrem pada radar
df_clean.loc[df_clean['radar_backscatter_db'] > 10, 'radar_backscatter_db'] = np.nan

# Mengisi missing values menggunakan nilai median/mean
df_clean['optical_reflectance_nir'] = df_clean['optical_reflectance_nir'].fillna(df_clean['optical_reflectance_nir'].mean())
df_clean['radar_backscatter_db'] = df_clean['radar_backscatter_db'].fillna(df_clean['radar_backscatter_db'].median())

# ================= ================= =================
# 3. DETEKSI DINI GANGGUAN / DEFORESTASI (EARLY WARNING)
# ================= ================= =================
def detect_environmental_alert(row):
    # Logika sederhana: penurunan pantulan vegetasi (NIR) dan perubahan backscatter radar menunjukkan gangguan
    if row['optical_reflectance_nir'] < 0.30 and row['moisture_index'] < 0.3:
        return 'ALERT_DEFORESTATION_RISK'
    elif row['radar_backscatter_db'] > -10.0:
        return 'ALERT_ANOMALY_SURFACE'
    else:
        return 'NORMAL_FOREST_COVER'

df_clean['environmental_status'] = df_clean.apply(detect_environmental_alert, axis=1)

# ================= ================= =================
# 4. REKAPITULASI STATUS UNTUK DASHBOARD / CLOUD SYNC
# ================= ================= =================
summary = df_clean.groupby('node_id').agg(
    last_update=('timestamp', 'max'),
    avg_nir_reflectance=('optical_reflectance_nir', 'mean'),
    avg_radar_db=('radar_backscatter_db', 'mean'),
    total_alerts=('environmental_status', lambda x: (x != 'NORMAL_FOREST_COVER').sum())
).reset_index()

print('--- RINGKASAN STATUS MONITORING LINGKUNGAN (CLOUD READY) ---')
print(summary.to_string(index=False))

# Menyimpan hasil olahan ke file CSV
df_clean.to_csv('processed_environmental_telemetry.csv', index=False)
print('\n[SUCCESS] Data telemetri bersih berhasil disimpan ke "processed_environmental_telemetry.csv"')