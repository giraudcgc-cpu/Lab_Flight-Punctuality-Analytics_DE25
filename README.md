# Flight Punctuality Analytics - modern data stack
--- 

Project on Swedish airport authority: **how many arrivals and departures are delayed
at Swedish airports, and how does that vary by airline, airport and date?**

A flight is **delayed** when it arrives/departs **more than 15 minutes** after its scheduled time
The pipeline always holds the **last three days including today** for **all 10 Swedavia airports**.


## Getting started(Tools and commands)

Prerequisites: Python 3.13, [uv](https://github.com/astral-sh/uv), git bash (Windows), a
[Swedavia API key](https://apideveloper.swedavia.se/) (sign up -> *Products* -> FlightInfo -> free version),
and access to the team's Snowflake account ([docs/snowflake_setup.md](docs/snowflake_setup.md)).

```bash
git clone <repo-url> && cd <repo>

# 1. virtual environment + packages
uv venv --python 3.12
source .venv/Scripts/activate        # mac/linux: source .venv/bin/activate
uv pip install -r requirements.txt

# 2. secrets -> put your SWEDAVIA_API_KEY and Snowflake values in .env
cp .env.example .env

# 3. dbt packages + connection test
cd data_transformation
set -a; source ../.env; set +a
dbt deps
dbt debug --profiles-dir .
cd ..
```

### Run step by step

```bash
# EDA - open explorations/eda_swedavia.ipynb and select the .venv kernel

# extract & load (Swedavia + Wikipedia -> staging)
python -m data_extract_load.load_pipeline

# transform + test (staging -> warehouse -> marts)
cd data_transformation
dbt build --profiles-dir .
dbt docs generate --profiles-dir . && dbt docs serve --profiles-dir .
cd ..

# dashboard
streamlit run dashboard/app.py
```

### Run with Dagster (the whole pipeline)

```bash
dagster dev -m orchestration.definitions
```

Open <http://localhost:3000> -> *Jobs* -> `job_dlt` -> *Materialize all*. When it succeeds, the
sensor `dlt_load_sensor` starts `job_dbt`. Turn on `schedule_dlt` (daily 06:00 Swedish time)
and the sensor under *Automation*.

---

## Workflow
1. Create a snowflake account
Search online for "snowflake sign up free trial"
Check this Youtube channel "Kokchun Coding Tutorials" for the walkthrough: https://www.youtube.com/watch?v=a1z40Qh2KBk

---

2. Create a project repo/create a folder "general_snowflake_setup" to setup snowflake in your IDE.
Here we build the warehouse, the database, the schema, define the roles, the users, and grants:
warehouse_database.sql
setup_roles.sql
setup_users.sql
grants.sql

---

3. Create environment variables as .env in the main root directory (never committed)
Each tool logs in with its own user and role, following least privilege. 
Uses placeholders for:
SWEDAVIA_API_KEY
SNOWFLAKE_*
DLT_*
DBT_*
REPORTER_*

---

4. Create a dlt folder "data_extract_load" to extract and load data.
dlt process where we pull flights from the Swedavia FlightInfo API and reference tables from Wikipedia, and loads them in "staging" into Snowflake

---

5. Create the dbt folder "dbt_transformation"
dbt  turns the raw staging tables into a star schema ("warehouse") and dashboard-ready tables ("marts") in Snowflake.

Each .sql file in "models/" is one SELECT query. dbt runs it and saves the result as a table in Snowflake, with the same name as the file. 
In "model":
1. "src" reads the raw staging tables loaded by dlt, picks the useful columns and gives them names. 
2. "dim" and "fct" tables build the star schema in "warehouse": dimensions describe "who, where, when" and facts hold one row per arrival or departure with its delay and cancellation.
3. "marts" joins facts and dimensions into simple tables for the dashboard in "marts".

---

6. Dockerization
This project runs into 2 containers. 
Create these files:
"docker-compose.yml" which starts both containers together with one command, and passes them the .env variables and the dashboard key
"dockerfile.dashboard"  builds the dashboard image with Python and Streamlit
"dockerfile.dwh" which is the pipeline  image: Python >  dlt > dbt >  Dagster

---

7. Create the folder: "dashboard"
Create a sub folder "worksheets_snowflake_dash" and it should contain these files to run in order:
0_generate_key.sh  that generates an RSA key pair. The private key stays local (gitignored); the public key goes to Snowflake. 
1_setup_role.sql that creates a dedicated role for the dashboard (e.g. `DASHBOARD_ROLE`)
2_setup_user.sql that creates a service user, assigns the role and attaches the public key (key-pair auth, no password)
3_grants.sql that grants least-privilege access
4_check_access.sql verifies the setup

---

8. Create the folder "orchestration" for Dagster
Build definitions.py

---

9. Azure - Deployment
Go to https://azure.microsoft.com/en-us/free/students and signup
Create a resource group, the folder that holds the Project
Create an Azure Container Registry (ACR) where the Docker images are stored.
Go to the terminal in your IDE and build and push both images (pipeline and dashboard) to the registry
Back to Azure, create a "Container App" from the pipeline image (dlt, dbt, Dagster).
Create a "Web App" from the dashboard image (Streamlit), which gives it a public URL.
Add the .env variables to both apps as environment variables or secrets

---

**Developers:(Christophe, Dennis and Karl )**
