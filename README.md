## Nawa GPT-Codebase 

### 1. **Create conda env :**

```bash
conda create -n gpt-orch python=3.11
```

### 2. **Activate env :**

```bash
conda activate gpt-orch
```

### 3. Installing dependencies.

There are two options, using pip or poetry:
- For the long term project, it is preferable to use poetry, it is lock your dependencies to lower the chances you have dependencies conflict
- But, if project needs to be done short in time use pip instead.

Click in the link, to install Poetry: https://python-poetry.org/docs/


### 3.a. **Install All Dependencies using PIP:**
   ```bash
   pip install -r requirements.txt
   ```

### 3.b. **Install All Dependencies using Poetry :**
   ```bash
   poetry install
   ```

### 4. **How to run** :
1. **Set up Additional resource.**
   - PostgresDB with vector extensions for vectorstore
   - Redis for History Chat Engine
2. **Set up your FAQ list in PG DB.**
   - Checkout Databank_Ingestion/Databank-create.ipynb.
   - Store the data that want to be ingested in FAQ_Data.
3. **Set up Open AI key and additional resource in .env files.**
   - change the env file to .env.
   - Fill out all the necessary path and openai key.
4. **Run FastAPI locally.**
   ```bash
   make run
   ```
**List of available endpoints**

| API Service     | Method |            Full Path            |
|-----------------|--------|:-------------------------------:|
| GPT Completions | `POST` | `{Endpoint}:8080/conversation`  |
| Delete History  | `POST` | `{Endpoint}:8080/clear-history` |

