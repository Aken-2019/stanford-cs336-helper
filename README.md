# Multi-Page Streamlit App

This project is a multi-page Streamlit application. The Python environment is managed by [uv](https://github.com/astral-sh/uv).

## Features
- Multi-page navigation using Streamlit's `pages/` directory
- Easy extension: add new `.py` files to `pages/` for more pages
- Fast dependency management with uv

## Quickstart

1. **Install uv**
   ```bash
   curl -Ls https://astral.sh/uv/install.sh | bash
   ```
2. **Create and activate the environment**
   ```bash
   uv venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```
4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Adding Pages
- Place additional `.py` files in the `pages/` directory.
- Each file will appear as a separate page in the Streamlit sidebar.

## Project Structure
```
├── app.py
├── pages/
│   ├── page1.py
│   └── page2.py
├── requirements.txt
├── README.md
└── .venv/
```

## Environment Management
- All Python dependencies are managed by uv and listed in `requirements.txt`.
- The virtual environment is created in `.venv/`.

---
For more info on uv: https://github.com/astral-sh/uv
