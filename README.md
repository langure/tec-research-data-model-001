# tec-research-data-model-001
Sharing resources for research.


Database schema creation:
CREATE SCHEMA `research_001` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;

Steps to run:

Create a new virtual environment

python -m venv venv
source ./venv/bin/activate


Install dependencies

pip install -r requirements.txt

Create a new .env file with the example.env as template

initialize database

python main.py --initializeDB

Provide data in the channels.xlsx file

run

python main.py