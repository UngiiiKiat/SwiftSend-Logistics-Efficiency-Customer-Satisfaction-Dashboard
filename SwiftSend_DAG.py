'''
Milestone 3

Nama  : Rangga irwanto Putra Kiat
Batch : FTDS-034

Program ini dibuat untuk melakukan automatisasi Pipeline ETL (Extract, Transform, Load).
Data diambil dari PostgreSQL, dibersihkan menggunakan pandas (Data Cleaning), 
dan dimuat ke dalam Elasticsearch untuk visualisasi di Kibana.
'''

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from elasticsearch import Elasticsearch, helpers
import os

# fungsi untuk pipeline
def fetch_from_postgres():
    '''
    Fungsi untuk mengambil data mentah dari database PostgreSQL.
    Data diambil dari tabel 'table_m3' dan disimpan sementara dalam format CSV.
    '''
    # Memastikan folder data ada di dalam container
    os.makedirs('/opt/airflow/data', exist_ok=True)
    
    # Koneksi string ke Postgres Docker
    engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres:5432/milestone3')
    
    # query = 'SELECT * FROM "public"."table_m3"'
    query = 'SELECT * FROM table_m3'
    
    df = pd.read_sql(query, engine)
    # Simpan sebagai file temporary untuk tahap cleaning
    df.to_csv('/opt/airflow/data/P2M3_Rangga_Kiat_data_raw.csv', index=False)

def clean_data():
    '''
    Fungsi untuk melakukan pembersihan data (Data Cleaning).
    Kriteria: Hapus duplikat, handling missing values, dan normalisasi nama kolom.
    '''
    # Membaca data mentah
    df = pd.read_csv('/opt/airflow/data/P2M3_Rangga_Kiat_data_raw.csv')
    
    # Hapus data duplikat
    df.drop_duplicates(inplace=True)
    
    # Handling missing value
    df.fillna('Unknown', inplace=True) # mengisi missing value dengan Unknown
    
    # Normalisasi kolom (Lowercase)
    df.columns = [col.lower() for col in df.columns] # semua kolom memakai huruf kecil
    
    # Normalisasi kolom (Hapus spasi/simbol dan ganti spasi/titik menjadi underscore)
    df.columns = [col.strip().replace(' ', '_').replace('.', '_') for col in df.columns]
    
    # Menyimpan hasil ke file clean
    df.to_csv('/opt/airflow/data/P2M3_Rangga_Kiat_data_clean.csv', index=False)

def load_to_elasticsearch():
    '''
    Fungsi untuk memuat data yang telah dibersihkan ke NoSQL (Elasticsearch).
    Data dibaca dari file CSV clean dan dikirim menggunakan metode bulk helpers.
    '''
    # Membaca file yang benar hasil dari fungsi clean_data
    df = pd.read_csv('/opt/airflow/data/P2M3_Rangga_Kiat_data_clean.csv')
    
    # Koneksi ke Elasticsearch Docker
    es = Elasticsearch(["http://elasticsearch:9200"])
    
    # Konversi dataframe ke format dictionary untuk Elasticsearch
    records = df.to_dict(orient='records')
    
    actions = [
        {
            "_index": "milestone3",
            "_source": record
        }
        for record in records
    ]
    
    # Proses upload bulk
    helpers.bulk(es, actions)


# definisi DAG

# Konfigurasi argumen default sesuai kriteria start_date 01 Nov 2024
default_args = {
    'owner': 'RanggaKiat',
    'start_date': datetime(2024, 11, 1),
}

with DAG(
    dag_id='milestone3',
    default_args=default_args,
    # Penjadwalan: Setiap hari Sabtu (6), jam 09:10, 09:20, dan 09:30 
    schedule_interval='10,20,30 9 * * 6',
    catchup=False,
    tags=['MILESTONE', 'logistics']
) as dag:

    # Task 1: Fetch
    task_fetch = PythonOperator(
        task_id='fetch_from_postgres',
        python_callable=fetch_from_postgres
    )

    # Task 2: Cleaning
    task_clean = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data
    )

    # Task 3: Load
    task_load = PythonOperator(
        task_id='post_to_elasticsearch', # Task ID disesuaikan kriteria instruksi
        python_callable=load_to_elasticsearch
    )

    # Urutan eksekusi: Fetch -> Clean -> Load
    task_fetch >> task_clean >> task_load