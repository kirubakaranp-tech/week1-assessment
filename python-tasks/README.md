# Python Tasks

Three small Python tasks on the same employee dataset.

| Script | What it covers |
|---|---|
| `tasks/task1_employee.py` | functions with `*args`/`**kwargs`, classes and inheritance, a custom exception, list comprehensions, `map`/`filter`, `continue`/`break` |
| `tasks/task2_file_api.py` | CSV to JSON, writing a filtered CSV, calling an API with `requests`, handling timeouts and a 404, loading a key from `.env` |
| `tasks/task3_numpy_pandas_matplotlib.py` | NumPy arrays, cleaning a messy CSV with Pandas, group-by and joins, four Matplotlib charts |

## Folders

- `data/` - input CSV files
- `output/` - files the scripts create (JSON, CSV and `charts/`)

## Running

```powershell
pip install -r requirements.txt

python tasks\task1_employee.py
python tasks\task2_file_api.py
python tasks\task3_numpy_pandas_matplotlib.py
```

Task 2 needs internet. Copy `.env.example` to `.env` if you want to set an API key
(the sample API works without one).
