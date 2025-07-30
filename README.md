# 🎨 The Joy of Painting API

This project explores the ETL (Extract, Transform, Load) process by organizing episode data from *The Joy of Painting* with Bob Ross. It transforms messy datasets into a structured SQL database and exposes the data via an API with filter support.

## 📌 Objective

- **Extract**: Load data from various formats (CSV, JSON)
- **Transform**: Clean and normalize the data
- **Load**: Store it in a structured SQL database
- **Serve**: Build an API to allow filtering episodes by:
  - Month of original broadcast
  - Subject matter (e.g., mountain, lake)
  - Color palette (e.g., phthalo blue, titanium white)

## Database Schema

The data is structured using a normalized relational schema to support many-to-many relationships between paintings, colors, and subjects.

📄 **[View Schema Diagram](assets/Bob_Ross_ERD.png)**

##  Database Setup

To create the database locally, run:

```bash
# PostgreSQL example
createdb bob_ross
psql -d bob_ross -f schema/schema.sql
