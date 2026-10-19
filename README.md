# IoT Environmental & Forest Monitoring Pipeline

Repositori ini berisi studi kasus pengolahan data telemetri sensor *IoT* dan penginderaan jauh untuk pemantauan lingkungan serta deteksi dini gangguan ekosistem hutan, mengacu pada materi pemanfaatan data multi-sensor satelit[cite: 4].

## Fitur Proyek
- **Data Preprocessing & Cleansing**: Membersihkan data kosong (*missing values*) akibat tutupan awan serta anomali pembacaan sensor[cite: 4].
- **Early Warning Thresholding**: Otomatisasi deteksi status risiko deforestasi berdasarkan ambang batas pantulan optik dan radar[cite: 4].
- **Cloud-Ready Data Aggregation**: Rekapitulasi status simpul sensor (*node*) untuk integrasi dasbor pemantauan lingkungan.

## Cara Menjalankan
1. Install dependencies:
   ```bash
   pip install -r requirements.txt