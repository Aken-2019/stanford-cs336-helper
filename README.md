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

## Overview
This project is a multi-page Streamlit application designed for Stanford CS336. 
An ready-to-deploy Docker configuration is included for easy deployment on HuggingFace Spaces. You can find a ready-to-use instance at https://huggingface.co/spaces/HuggingHarry/stanford-cs336-helper.

The above instance may be overloaded or temporarily unavailable due to resource constraints on HuggingFace Spaces. If you encounter issues accessing the app, please consider deploying your own instance using the provided Docker configuration.


## Contribution Guidelines
Contributions are welcome! Please follow the steps below to set up the project locally or deploy it using Docker.

### Prequisites
- Python 3.9 or higher
- Docker (for containerized deployment)

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

This project is configured for deployment on HuggingFace Spaces. To deploy, check [HuggingFace Spaces Overview](https://huggingface.co/docs/hub/en/spaces-overview) for detailed instructions.