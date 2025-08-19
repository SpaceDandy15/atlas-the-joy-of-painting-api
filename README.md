# 🎨 The Joy of Painting API

This project explores the ETL (Extract, Transform, Load) process by organizing episode data from *The Joy of Painting* with Bob Ross. It transforms messy datasets into a structured SQL database and exposes the data via an API with filter support.

---

## 📌 Objective

- **Extract**: Load data from various formats (CSV, JSON)  
- **Transform**: Clean and normalize the data  
- **Load**: Store it in a structured SQL database  
- **Serve**: Build an API to allow filtering episodes by:
  - Month of original broadcast
  - Subject matter (e.g., mountain, lake)
  - Color palette (e.g., phthalo blue, titanium white)

---

## 🗂 Database Schema

The data is structured using a normalized relational schema to support many-to-many relationships between paintings, colors, and subjects.

📄 **View Schema Diagram**:  
![ERD Diagram](assets/Bob_Ross_ERD.png)

---

## ⚙️ Database Setup & ETL Process

To create the database and load data locally:

bash
# PostgreSQL example
createdb bob_ross
psql -d bob_ross -f schema/schema.sql

# Load cleaned data into the database using ETL script
python etl/load_data.py
The ETL scripts handle all CSV/JSON parsing, normalization, and database insertion.
Includes error handling for missing or inconsistent data.

🚀 API Usage
After loading data, start the API server:

bash
Copy code
python app.py
Example Endpoints:

http
Copy code
GET /episodes?month=January      # List episodes aired in January
GET /episodes?subject=mountain   # Filter episodes with mountains
GET /episodes?color=phthalo blue # Filter episodes by color palette

🔧 Tech Stack
<p> <img alt="Python" src="https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white" /> <img alt="PostgreSQL" src="https://img.shields.io/badge/-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white" /> <img alt="VS Code" src="https://img.shields.io/badge/-VS%20Code-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white" /> <img alt="Prettier" src="https://img.shields.io/badge/-Prettier-F7B93E?style=flat-square&logo=prettier&logoColor=white" /> <img alt="Postman" src="https://img.shields.io/badge/-Postman-FF6C37?style=flat-square&logo=postman&logoColor=white" /> <img alt="Git" src="https://img.shields.io/badge/-Git-F05032?style=flat-square&logo=git&logoColor=white" /> <img alt="HTML" src="https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" /> <img alt="CSS3" src="https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3&logoColor=white" /> <img alt="JavaScript" src="https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" /> <img alt="MySQL" src="https://img.shields.io/badge/-MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white" /> </p>
💡 Challenges & Lessons Learned
Cleaning inconsistent data across multiple sources

Designing a normalized relational database for many-to-many relationships

Building a RESTful API for dynamic filtering

Efficiently handling large datasets in Python

📸 Screenshots / Demo
### Postman API Test
![Postman Demo](assets/postman.png)

👤 About Me
Hi, I’m Malik Vance, a Fullstack Software Engineer passionate about bridging the gap between hardware and software.

LinkedIn
👤 **Connect with Me**  
[LinkedIn Profile](https://www.linkedin.com/in/malik-vance)

☕ Support Me
<a href="https://www.buymeacoffee.com/SpaceDandy15" target="_blank"> <img src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png" alt="Buy Me A Coffee" width="150" > </a> ```
