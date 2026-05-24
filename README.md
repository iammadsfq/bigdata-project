# Proyek Big Data: TPC-H Lakehouse & Data Mart (Spark + Iceberg + MinIO + dbt)

Arsitektur Big Data end-to-end yang mengimplementasikan **Data Lakehouse** (Apache Iceberg dengan format file Parquet pada Object Storage MinIO), **Data Orchestration** (dbt-spark), dan **Data Processing** (Apache Spark).

## Arsitektur Alur Data
1. **Generate**: Data TPC-H [(link)](https://www.tpc.org/tpch/) berupa CSV yang di-generate via script DBGEN.
2. **Load**: Data CSV di-load ke Data Lakehouse (tabel Apache Iceberg di bucket MinIO `lakehouse/warehouse`) via PySpark.
3. **Transform**: dbt melakukan transformasi data dari Iceberg Lakehouse menjadi Data Mart (`tpch_mart.fct_customer_revenue`) via Spark Thrift Server.
4. **Test**: dbt test memverifikasi kualitas data mart (unique & not-null constraints).

## Quick Start

### 1. Inisialisasi Environment & Services
Jalankan infrastruktur Docker (MinIO, Spark, dbt):
```bash
docker compose up -d --build
```

> [!TIP]
> **Script End-to-End**: Anda bisa menjalankan seluruh langkah di bawah secara otomatis (generate data, upload, load ke Iceberg, run dbt, dan run test) dengan satu perintah:
> ```bash
> # Menjalankan seluruh pipeline untuk SF 1
> bash scripts/run_pipeline.sh 1
> ```

### 2. Generate Data TPC-H (CSV)
Generate TPC-H dataset dengan DBGEN (default Scale Factor = 1):
```bash
# Untuk SF 1 (~1GB)
bash scripts/generate_tpch.sh 1

# Untuk SF 10 (~10GB)
bash scripts/generate_tpch.sh 10
```

### 3. Upload CSV ke MinIO raw bucket
Unggah data CSV hasil generate ke MinIO raw bucket:
```bash
bash scripts/minio/upload.sh
```

### 4. Load CSV ke Iceberg Lakehouse
Jalankan script loading untuk memindahkan data CSV di MinIO raw bucket ke tabel Iceberg:
```bash
bash scripts/load_to_iceberg.sh
```

### 5. Eksekusi Transformasi & Pengujian dbt
Jalankan model transformasi dan lakukan pengujian kualitas data mart:
```bash
# Transformasi ke Data Mart
docker compose exec dbt dbt run --profiles-dir . --project-dir .

# Verifikasi Data Quality Tests
docker compose exec dbt dbt test --profiles-dir . --project-dir .
```

## Benchmarking
Kami menyediakan dua script benchmarking untuk membandingkan performa pemrosesan query:

1. **CSV vs Iceberg (Format Kolom)**:
   Perbandingan query langsung ke raw CSV di MinIO vs Iceberg (Parquet) di MinIO:
   ```bash
   ./scripts/spark_submit.sh benchmark_csv_vs_iceberg.py
   ```

2. **Unpartitioned vs Partitioned (Partition Pruning)**:
   Perbandingan query filter pada tabel Iceberg biasa vs tabel Iceberg yang dipartisi berdasarkan tahun (`years(l_shipdate)`):
   ```bash
   ./scripts/spark_submit.sh benchmark_partitioning.py
   ```

## Struktur Repositori & File Penting
- `Dockerfile.spark`: Custom Spark image yang mem-bake AWS S3A & Iceberg connectors langsung ke system classpath JVM.
- `Dockerfile.dbt`: Custom dbt image dengan pre-installed `dbt-spark[PyHive]` adapter.
- `conf/spark-defaults.conf`: Konfigurasi global catalog Iceberg (`lakehouse`) dan endpoint MinIO.
- `conf/log4j2.properties`: Konfigurasi filter log untuk mereduksi log verbosity Spark JVM.
- `spark/session.py`: Wrapper SparkSession yang dinamis untuk standalone PySpark scripts.
- `dbt/dbt_project.yml`: Konfigurasi project dbt (staging dimaterialisasi sebagai `table` agar kompatibel dengan Iceberg Hadoop Catalog).
- `dbt/profiles.yml`: Konfigurasi profile koneksi dbt ke Spark Thrift Server (port `10000`).

## Web Interfaces (Monitoring & GUI)
Setelah infrastruktur berjalan, Anda dapat mengakses beberapa web interface berikut untuk memantau pipeline:
* **MinIO Console**: [http://localhost:9001](http://localhost:9001) (Credentials: `minio` / `minio123`) - Untuk eksplorasi storage bucket (`raw`, `lakehouse`, `warehouse`) dan file metadata Iceberg.
* **Spark UI**: [http://localhost:4040](http://localhost:4040) - Untuk memantau status query, job, dan execution plan dari Spark Thrift Server.
* **dbt Docs**: [http://localhost:8080](http://localhost:8080) - Dokumentasi skema dan visualisasi data lineage graph dari data mart.

## Verifikasi
Untuk mengecek jumlah baris tabel Iceberg langsung di catalog `lakehouse`:
```bash
bash scripts/spark_submit.sh verify_tables.py
```

## Reset Environment
Jika Anda ingin menghapus seluruh data (MinIO & Iceberg) dan memulai ulang stack dari awal (*clean slate*):
```bash
bash scripts/reset_clean.sh
```

## Anggota Tim
| NIM | Nama |
| :--- | :--- |
| 13522080 | Julian Chandra Sutadi |
| 13523031 | Rafen Max Alessandro |
| 13523135 | Ahmad Syafiq |

## Deklarasi Penggunaan AI / LLM
Proyek ini dikembangkan dengan bantuan AI / Large Language Models (LLM):
* **GitHub Copilot** - Digunakan untuk menyusun struktur dan implementasi awal proyek
* **Antigravity (3.5 Flash)** - Digunakan untuk debugging yang lebih mendalam dan menyempurnakan pipeline secara end-to-end.

## Referensi Eksternal
* [Hands-On with Apache Iceberg on Your Laptop: Deep Dive with Apache Spark, Nessie, MinIO, and More (Hackernoon)](https://hackernoon.com/hands-on-with-apache-iceberg-on-your-laptop-deep-dive-with-apache-spark-nessie-minio-and-more)
