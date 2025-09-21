---
title: Stanford CS336 Illustrators
emoji: 📊
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# Multi-Page Streamlit App

This project is a multi-page Streamlit application designed for Stanford CS336. The Python environment is managed by [uv](https://github.com/astral-sh/uv).

## Features
- Multi-page navigation using Streamlit's `pages/` directory
- Easy extension: add new `.py` files to `pages/` for more pages
- Fast dependency management with uv

## Quickstart

### Local Development

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

### Docker Deployment

This app is configured to run on HuggingFace Spaces using Docker.

#### Local Docker Testing

1. **Build the Docker image**
   ```bash
   docker build -t stanford-cs336-illustrators .
   ```

2. **Run the container**
   ```bash
   docker run -p 7860:7860 stanford-cs336-illustrators
   ```

3. **Access the app**
   Open your browser to `http://localhost:7860`

#### HuggingFace Spaces Deployment

This project is configured for deployment on HuggingFace Spaces:

1. **Create a new Space** on [HuggingFace Spaces](https://huggingface.co/spaces)
2. **Select Docker** as the SDK
3. **Clone your Space repository** and push this project to it
4. **The Space will automatically build and deploy** using the provided Dockerfile

The configuration is set in the README.md header:
- **SDK**: Docker (uses the provided Dockerfile)
- **Port**: 7860 (standard for HF Spaces)
- **Health check**: Configured for Streamlit

## HuggingFace Spaces Configuration

This project is optimized for deployment on HuggingFace Spaces with the following configuration:

- **Title**: Stanford CS336 Illustrators
- **SDK**: Docker
- **Port**: 7860 (Streamlit default for HF Spaces)
- **License**: MIT

The metadata is configured in the README.md header, which HuggingFace Spaces reads automatically.

## Adding Pages
- Place additional `.py` files in the `pages/` directory.
- Each file will appear as a separate page in the Streamlit sidebar.

## Project Structure
```
├── app.py
├── pages/
│   ├── LEC_2_Floating_Point_Explorer.py
│   └── __pycache__/
├── tests/
│   ├── test_floating_point_explorer.py
│   └── __pycache__/
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── .venv/
```

## Environment Management
- All Python dependencies are managed by uv and listed in `requirements.txt`.
- The virtual environment is created in `.venv/`.

---
For more info on uv: https://github.com/astral-sh/uv
