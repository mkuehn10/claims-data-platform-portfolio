# PySpark + Delta Lake mini-lab

This local exercise models a Databricks medallion-style step: ingest synthetic CSV, validate and transform it, merge updates into a Delta table, and inspect physical partition layout.

## Run locally

Prerequisites: Java 17 and Python 3.10+.

```powershell
uv run --with-requirements requirements.txt python lab.py
```

If Java is not installed locally, run the same lab in its container:

```powershell
docker build -t claims-spark-delta-lab .
docker run --rm claims-spark-delta-lab
```

The script recreates `output/` on every run, reads `data/orders.csv`, writes a Delta table partitioned by `order_date`, applies `data/order_updates.csv` with `MERGE`, prints query results, and lists partition directories. Delete `output/` after experimenting.

## What to inspect

- Change a duplicate `order_id` or invalid quantity to see validation fail before write.
- Compare logical `groupBy("order_date")` output with physical `order_date=...` directories.
- Run twice: deterministic cleanup prevents accidental dependence on prior local state.
- Inspect `output/orders_delta/_delta_log`; transaction-log JSON/Parquet records table actions, not a second copy of business rows.

## Azure service mapping

| Local lab element | Typical Azure implementation |
| --- | --- |
| CSV under `data/` | ADLS Gen2 landing zone, usually `abfss://...` |
| Manual script start | ADF pipeline trigger and/or Databricks Job workflow |
| Local Spark + Delta | Azure Databricks cluster/serverless compute and Delta tables |
| Paths and in-code schema | Unity Catalog catalogs/schemas/volumes, grants, lineage, managed/external tables |
| Local source control/checks | Azure Repos + Azure Pipelines (or another Azure DevOps CI/CD flow) |

ADF commonly orchestrates movement and dependencies; Databricks Jobs commonly execute notebook or wheel tasks. Their responsibilities can overlap, so the split should follow ownership, observability, and operational needs.

## Honest boundaries

This is not a Databricks deployment. It does not exercise ADLS identity/RBAC, Unity Catalog policies, Auto Loader, cluster policies, streaming checkpoints, performance tuning, CI/CD deployment, or production-scale data. Local filesystem partition listing is only an observable analogue to cloud object layout. Partitioning tiny data is pedagogical and would create harmful small files in production.

## Interview talking points

- Explain why explicit schemas and pre-write quality checks beat blind inference.
- Describe Delta `MERGE` as an atomic upsert and discuss deduplicating the source before merge.
- Distinguish table partitioning from Spark shuffle partitions and explain low-cardinality partition choices.
- Map local steps to ADLS, ADF, Jobs, Unity Catalog, and Azure DevOps while stating what was not validated.
