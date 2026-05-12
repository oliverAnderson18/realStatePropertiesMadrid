# Madrid Real Estate Platform

## Project Description

This project is a simplified real estate listings platform inspired by marketplaces such as Idealista, Fotocasa, Pisos.com and Otodom.

The application scrapes real estate listings from pisos.com, cleans and normalizes the extracted data, stores it in a MySQL database, and exposes a web interface where users can browse, filter, sort and open property detail pages.

The platform includes:

- Property scraping using Selenium
- Data cleaning and normalization using Pandas
- MySQL database storage
- Property listing page
- Property detail page
- Filtering and sorting system
- Optional AI-powered search using Ollama + Llama3

The AI search allows users to search properties using natural language queries such as:

```text
cheap flat in Chamartín with 2 bedrooms
```

The application can also be used without AI through the classic filters.

---

# Project Structure

## `data/`

Contains the generated datasets.

### `data/properties.csv`

Raw scraped dataset generated from pisos.com.

### `data/properties_clean.csv`

Cleaned and normalized dataset used for database import.

---

## `scripts/`

Contains the Python data pipeline.

### `scripts/scraper.py`

Scrapes 100 property listings from pisos.com in Madrid's urban area using Selenium.

Extracted fields include:

- title
- URL
- image
- price
- location
- bedrooms
- bathrooms
- square meters
- floor

### `scripts/clean.py`

Cleans and normalizes the scraped dataset using Pandas.

Main tasks:

- normalizing property types
- extracting numeric values
- handling missing or inconsistent values
- standardizing floors and property categories

### `scripts/to_mysql.py`

Imports the cleaned CSV dataset into the MySQL database.

---

## `views/`

Contains the EJS templates used by the web application.

### `views/index.ejs`

Main property listing page.

Includes:

- classic filters
- AI search box
- sorting
- property cards

### `views/detail.ejs`

Property details page.

Displays full property information and the original external listing link.

---

## `public/`

Contains static frontend assets.

### `public/styles.css`

Application styling and responsive UI.

---

## `database/`

Contains database initialization files.

### `database/ddl-properties.sql`

Creates the MySQL database schema and `properties` table.

This file is automatically executed by Docker when the MySQL container is created for the first time.

---

## Root Files

### `app.js`

Main Node.js + Express backend application.

Responsible for:

- connecting to MySQL
- querying properties
- applying filters
- applying sorting
- rendering pages
- integrating optional AI search with Ollama

### `docker-compose.yml`

Creates and runs the MySQL container using Docker.

It also mounts the database schema into MySQL so the table is created automatically on first startup.

### `requirements.txt`

Python dependencies.

### `package.json`

Node.js dependencies.

---

# Requirements

Before running the project, install:

- Python 3.12+
- Node.js
- Docker Desktop
- Google Chrome

For AI search:

- Ollama
- Llama3 model

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd realStatePropertiesMadrid
```

---

## 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Install Node.js Dependencies

```bash
npm install
```

---

# How to Run the Project

## 1. Start MySQL Database

```bash
docker-compose up -d
```

The database and table are created automatically from:

```text
database/ddl-properties.sql
```

Important: MySQL only runs initialization scripts the first time the Docker volume is created. If you change the SQL schema later, recreate the volume with:

```bash
docker-compose down -v
docker-compose up -d
```

---

## 2. Import Provided Dataset into MySQL

The repository already includes:

- `data/properties.csv`
- `data/properties_clean.csv`

Import the cleaned dataset:

```bash
python scripts/to_mysql.py
```

---

## 3. Start the Web Application

```bash
node app.js
```

Open the application at:

```text
http://localhost:3000
```

---

# Optional: Rebuild Dataset From Scratch

The CSV files are already included, so this step is not required.

If you want to regenerate the dataset:

```bash
python scripts/scraper.py
python scripts/clean.py
python scripts/to_mysql.py
```

---

# AI Search

The application works without AI using classic filters.

To enable AI-powered search, install Ollama and run:

```bash
ollama run llama3
```

Then start the Node.js application as usual:

```bash
node app.js
```

Example AI searches:

```text
Flat in Salamanca with 2 bedrooms
3 bedroom place with at least 80 square meters ordered from cheapest to most expensive
```

The AI converts user intent into structured filters before querying the database.
