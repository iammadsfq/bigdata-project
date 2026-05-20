# Scripts

## Generate TPC-H

Generate TPC-H CSV data locally on the host, then hand the CSV files off to MinIO or Spark.

```bash
# Default SF=1
./scripts/generate_tpch.sh

# Example: SF=10 (~10GB)
./scripts/generate_tpch.sh 10
```

Output is written to `./data/tpch` by default and is used as the handoff directory for the containerized parts of the pipeline.

## Upload to MinIO

Upload generated CSV files to the MinIO `raw` bucket under `tpch/`.

```bash
./scripts/minio/upload.sh
```

You can override the source path, bucket, or prefix:

```bash
./scripts/minio/upload.sh /path/to/tpch raw tpch
```

## Load to Iceberg

Load CSV into Iceberg using PySpark.

```bash
./scripts/load_to_iceberg.sh
```

## Run pipeline

Generate data, upload to MinIO, load to Iceberg, and run a toy query.

```bash
./scripts/run_pipeline.sh
```
