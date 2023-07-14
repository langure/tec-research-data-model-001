# Readme Research


Database schema creation: 

```bash
CREATE SCHEMA research_001 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
```

Steps to run:

Create a new virtual environment

```bash
python -m venv venv source ./venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a new .env file with the example.env as template

initialize database

```bash
python main.py --initializeDB
```

Provide data in the channels.xlsx file

run

```bash
python main.py
```

<img width="579" alt="ER" src="https://github.com/langure/tec-research-data-model-001/assets/106360071/7ce00420-5186-4f12-95bf-1c8be7ab3e9d">
