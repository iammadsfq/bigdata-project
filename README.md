# Proyek Big Data: TPC-H Lakehouse & Data Mart (Spark + Iceberg + MinIO + dbt)

Arsitektur Big Data end-to-end yang mengimplementasikan **Data Lakehouse** (Apache Iceberg dengan format file Parquet pada Object Storage MinIO), **Data Orchestration** (dbt-spark), dan **Data Processing** (Apache Spark).

## Arsitektur Alur Data
1. **Generate**: Data TPC-H berupa CSV di-generate via script DBGEN.
2. **Load**: Data CSV di-load ke Data Lakehouse (tabel Apache Iceberg di bucket MinIO `lakehouse/warehouse`) via PySpark.
3. **Transform**: dbt melakukan transformasi data dari Iceberg Lakehouse menjadi Data Mart (`tpch_mart.fct_customer_revenue`) via Spark Thrift Server.
4. **Test**: dbt test memverifikasi kualitas data mart (unique & not-null constraints).

---

## Quick Start

### 1. Inisialisasi Environment & Services
Jalankan stack infrastruktur Docker (MinIO, Spark, dbt):
```bash
docker compose up -d --build
```

### 2. Generate Data TPC-H (CSV)
Generate TPC-H dataset dengan DBGEN (default Scale Factor = 1):
```bash
# Untuk SF 1 (~1GB)
bash scripts/generate_tpch.sh 1

# Untuk SF 10 (~10GB)
bash scripts/generate_tpch.sh 10
```

### 3. Load CSV ke Iceberg Lakehouse
Jalankan pipeline loading untuk memindahkan data CSV local ke tabel Iceberg di MinIO:
```bash
bash scripts/load_to_iceberg.sh
```

### 4. Eksekusi Transformasi & Pengujian dbt
Jalankan model transformasi dan lakukan pengujian kualitas data mart:
```bash
# Transformasi ke Data Mart
docker compose exec dbt dbt run --profiles-dir . --project-dir .

# Verifikasi Data Quality Tests
docker compose exec dbt dbt test --profiles-dir . --project-dir .
```

---

## Struktur Repositori & File Penting
- `Dockerfile.spark`: Image Spark custom yang mem-bake AWS S3A & Iceberg connectors langsung ke system classpath JVM.
- `Dockerfile.dbt`: Image dbt custom dengan pre-installed `dbt-spark[PyHive]` adapter.
- `conf/spark-defaults.conf`: Konfigurasi global catalog Iceberg (`lakehouse`) dan endpoint MinIO.
- `conf/log4j2.properties`: Konfigurasi filter log untuk mereduksi log verbosity Spark JVM.
- `spark/session.py`: Wrapper SparkSession yang dinamis untuk standalone PySpark scripts.
- `dbt/dbt_project.yml`: Konfigurasi project dbt (staging dimaterialisasi sebagai `table` agar kompatibel dengan Iceberg Hadoop Catalog).
- `dbt/profiles.yml`: Konfigurasi profile koneksi dbt ke Spark Thrift Server (port `10000`).

---

## Verifikasi Mandiri (Optional)
Untuk mengecek jumlah baris tabel Iceberg langsung di catalog `lakehouse`:
```bash
bash scripts/spark_submit.sh verify_tables.py
```