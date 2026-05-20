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
docker compose exec -T spark /opt/spark/bin/spark-submit /opt/spark/app/toy_query.py
```

## Iceberg catalog configuration

- Spark will use the Hive Metastore catalog and MinIO via S3A.
- See conf/spark-defaults.conf for the catalog configuration to be used when Spark is added.

