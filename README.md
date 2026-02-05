# SwiftSend: Logistics Efficiency & Customer Satisfaction Dashboard

## Repository Outline


1. `folder images` - berisi semua visualisasi dan juga insight ny.
2. `README.md` - Penjelasan gambaran umum project, analisis, dan rekomendasi bisnis.
3. `SwiftSend_DAG.py` -  berfungsi sebagai skrip definisi Directed Acyclic Graph (DAG) pada Apache Airflow untuk mengotomatisasi seluruh alur kerja (pipeline) data logistik SwiftSend secara terjadwal.
4. `SwiftSend_data_clean.csv` - berisi dataset yang sudah di clean 
5. `SwiftSend_data_raw.csv` - berisi dataset yang masih raw atau mentah
6. `SwiftSend_ddl.txt` berfungsi untuk menyimpan perintah Data Definition Language (DDL) yang digunakan untuk mendefinisikan struktur indeks pada Elasticsearch atau skema tabel yang diperlukan dalam pemrosesan data SwiftSend.
7. `SwiftSend_GX.ipynb` -  berfungsi sebagai notebook untuk melakukan validasi kualitas data menggunakan framework Great Expectations (GX) guna memastikan seluruh data logistik yang masuk ke pipeline memenuhi standar dan kriteria yang telah ditentukan.


## Problem Background

* **URL Dataset:** [Kaggle - E-Commerce Shipping Data](https://www.kaggle.com/datasets/prachi13/customer-analytics)
* **Latar Belakang:** SwiftSend menghadapi tantangan besar berupa tingginya angka keterlambatan pengiriman yang berdampak langsung pada penurunan kepuasan pelanggan. Sebagai Data Analyst, proyek ini bertujuan untuk memetakan titik hambat (*bottleneck*) dalam proses logistik guna memberikan rekomendasi berbasis data kepada manajemen.
* **Tujuan:** Membangun dashboard pemantauan efisiensi pengiriman untuk mengidentifikasi korelasi antara diskon, beban gudang (blok), dan moda transportasi terhadap ketepatan waktu serta rating pelanggan.
* **User:** Manajer Logistik, Tim Operasional Gudang, dan Divisi Customer Experience.

## Project Output

Output utama dari proyek ini adalah **Dashboard Analitik Logistik** yang interaktif, terdiri dari 6 visualisasi kunci:

* **Metric Card:** Skor rata-rata kepuasan pelanggan (2.991).
* **Grouped Bar Chart & Heatmap:** Identifikasi beban kerja dan titik panas keterlambatan di Blok Gudang (Blok F terdeteksi paling kritis).
* **Horizontal Bar Chart:** Distribusi volume pengiriman berdasarkan moda transportasi (Dominasi jalur laut).
* **Pie Chart:** Proporsi tingkat kepentingan produk (Low, Medium, High).
* **Line Chart:** Tren volatilitas rating pelanggan terhadap besaran diskon.

## Data

Data yang digunakan berasal dari dataset pengiriman internasional e-commerce dengan karakteristik sebagai berikut:

* **Sumber:** Kaggle - Customer Analytics.
* **Karakteristik:** Terdiri dari 10.999 baris data dengan kolom kunci seperti `Warehouse_block`, `Mode_of_Shipment`, `Customer_rating`, `Discount_offered`, dan `Reached_on_Time_Y_N`.
* **Kualitas Data:** Data telah dibersihkan dan siap digunakan untuk analisis korelasi logistik.

## Method

Proyek ini menggunakan metode **Exploratory Data Analysis (EDA)** dan **Data Visualization** melalui ELK Stack (Elasticsearch & Kibana). Analisis difokuskan pada pemetaan distribusi frekuensi dan identifikasi anomali pada variabel pengiriman tepat waktu serta kepuasan pelanggan.

## Stacks

* **Data Storage:** Elasticsearch
* **Visualization Tool:** Kibana (Lens, Metric, Heatmap, Bar Chart)
* **Data Source:** CSV (Kaggle Dataset)

## Insight & Recommendations

1. **Optimalisasi Blok F:** Berdasarkan Heatmap dan Bar Chart, Blok F menangani volume tertinggi sekaligus angka keterlambatan terbesar (2.194 paket). Direkomendasikan audit operasional dan redistribusi staf ke blok ini.
2. **Prioritas Produk High Importance:** Mengingat rating produk bernilai tinggi sangat sensitif terhadap diskon (Line Chart), perusahaan harus menerapkan jalur prioritas (*fast track*) bagi kategori ini untuk menjaga reputasi layanan.
3. **Efisiensi Jalur Laut:** Dengan 7.462 pengiriman via kapal, gangguan pada moda ini akan melumpuhkan performa perusahaan. Diversifikasi rute atau moda perlu dipertimbangkan saat terjadi lonjakan pesanan.