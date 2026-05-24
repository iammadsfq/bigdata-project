Proyek Big Data: TPC-H Lakehouse & Data Mart (Spark + Iceberg + MinIO + dbt)

========================================================================
1. Inisialisasi Environment & Services
========================================================================
Jalankan infrastruktur Docker (MinIO, Spark, dbt):

  docker compose up -d --build

* Script End-to-End: Anda bisa menjalankan seluruh langkah di bawah secara otomatis 
  (generate data, upload, load ke Iceberg, run dbt, dan run test) dengan satu perintah:

  bash scripts/run_pipeline.sh 1


========================================================================
2. Generate Data TPC-H (CSV)
========================================================================
Generate TPC-H dataset dengan DBGEN (default Scale Factor = 1):

  # Untuk SF 1 (~1GB)
  bash scripts/generate_tpch.sh 1

  # Untuk SF 10 (~10GB)
  bash scripts/generate_tpch.sh 10


========================================================================
3. Upload CSV ke MinIO raw bucket
========================================================================
Unggah data CSV hasil generate ke MinIO raw bucket:

  bash scripts/minio/upload.sh


========================================================================
4. Load CSV ke Iceberg Lakehouse
========================================================================
Jalankan script loading untuk memindahkan data CSV di MinIO raw bucket ke tabel Iceberg:

  bash scripts/load_to_iceberg.sh


========================================================================
5. Eksekusi Transformasi & Pengujian dbt
========================================================================
Jalankan model transformasi dan lakukan pengujian kualitas data mart:

  # Transformasi ke Data Mart
  docker compose exec dbt dbt run --profiles-dir . --project-dir .

  # Verifikasi Data Quality Tests
  docker compose exec dbt dbt test --profiles-dir . --project-dir .


========================================================================
6. Benchmarking
========================================================================
Kami menyediakan dua script benchmarking untuk membandingkan performa pemrosesan query:

  # 1. CSV vs Iceberg (Format Kolom)
  # Perbandingan query langsung ke raw CSV di MinIO vs Iceberg (Parquet) di MinIO
  ./scripts/spark_submit.sh benchmark_csv_vs_iceberg.py

  # 2. Unpartitioned vs Partitioned (Partition Pruning)
  # Perbandingan query filter pada tabel Iceberg biasa vs tabel Iceberg yang dipartisi berdasarkan tahun (years(l_shipdate))
  ./scripts/spark_submit.sh benchmark_partitioning.py


========================================================================
7. Verifikasi
========================================================================
Untuk mengecek jumlah baris tabel Iceberg langsung di catalog lakehouse:

  bash scripts/spark_submit.sh verify_tables.py


========================================================================
8. Reset Environment
========================================================================
Jika Anda ingin menghapus seluruh data (MinIO & Iceberg) dan memulai ulang stack dari awal (clean slate):

  bash scripts/reset_clean.sh
