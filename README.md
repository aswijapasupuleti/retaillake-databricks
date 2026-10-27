# Retail Lakehouse - Databricks E-Commerce Pipeline

## Project Overview
This project implements an end-to-end, production-grade real-time e-commerce analytics data lakehouse on Databricks using the Medallion Architecture (Bronze, Silver, Gold). Utilizing the Brazilian E-Commerce Public Dataset by Olist, the pipeline simulates realistic incremental daily data drops to handle real-world scenarios including streaming file ingestion via Databricks Auto Loader, deduplication, late-arriving data, and analytics-ready dimensional modeling.

## Architecture Flow
Raw Landing Volume (CSV) ➔ Simulated Daily Drops ➔ Bronze Layer (Auto Loader / Delta) ➔ Silver Layer (Cleaned & Conformed) ➔ Gold Layer (Aggregated Analytics)

## Bronze Layer Ingestion & Validation
The Bronze layer ingests raw streaming files incrementally into Delta tables, preserving source-file metadata (`_source_file`) for auditing and debugging.


<img width="533" height="384" alt="{43F72CC8-C9B9-494D-A92B-4072689946B0}" src="https://github.com/user-attachments/assets/c2349d3f-b298-4cff-9d7a-c8cf97341f24" />
