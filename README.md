# Big Data Project (Infra + Lakehouse Load)

This repo contains the dockerized infrastructure and scripts for:

- generating TPC-H CSV data
- loading CSV into an Iceberg lakehouse on MinIO
- producing a data mart via dbt (later step)

## Layout

- docker-compose.yml: MinIO + Hive Metastore + Postgres (metastore DB)
- conf/: Hive and Iceberg-related configuration
- scripts/: data generation and upload scripts

## Services

- MinIO (S3-compatible storage): http://localhost:9000
  - Console: http://localhost:9001
  - Default credentials: minio / minio123
  - Buckets created on startup: lakehouse, raw, warehouse
- Hive Metastore (Thrift): thrift://localhost:9083

## Quick start

This project is intended to run from WSL2 or another Linux shell with Docker and Docker Compose available. The copied `.git/` directory is present, but this checkout does not contain any commits yet, so if you want real git history you should restore it from the remote or re-clone the repository later. For now, the local repo is still fine for running the stack.

1. Start the services

```bash
docker compose up -d
```

2. Verify MinIO UI at http://localhost:9001

3. Generate TPC-H data (CSV)

```bash
# Default SF=1
./scripts/generate_tpch.sh

# Example: SF=10 (~10GB)
./scripts/generate_tpch.sh 10
```

4. Upload CSV to MinIO (raw bucket)

```bash
./scripts/minio/upload.sh
```

5. Load CSV into Iceberg tables (PySpark)

```bash
./scripts/load_to_iceberg.sh
```

6. Run the toy Spark query (CSV vs Iceberg)

```bash
docker compose exec -T spark /opt/spark/bin/spark-submit --packages "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0" /opt/spark/app/toy_query.py
```

## Iceberg catalog configuration

- Spark uses a **hadoop (file-based) catalog** for local dev: metadata stored at `/opt/lakehouse/warehouse` (mounted from host).
- Iceberg and S3A packages are downloaded at PySpark session init time via `spark.jars.packages` (see `spark/load_table.py` and `spark/toy_query.py`). No mounts or `spark-defaults.conf` required.

## Architecture notes & developer guidance

- **Jar initialization (recommended)**: Iceberg and S3A packages are supplied explicitly using `--packages` during `spark-submit`. This is required so dependencies are correctly resolved by the JVM ClassLoader early enough before Iceberg tries to load `HadoopFileIO` and S3A capabilities, avoiding S3A instantiation errors and ensuring portablility. No static mounted jars or `spark-defaults.conf` tweaks required.
- **Catalog**: Hadoop (file-based) catalog for simplicity. For production, switch to Hive Metastore or Nessie.
- Local development: TPC-H CSVs are generated on the host into `./data/tpch` and mounted read-only into Spark. This is fast and eliminates S3A complexity for local iteration.

