# Monash-SpatialScope
The coding space for the Monash-Centric Spatial Transcriptomics Platform - focusing on **CosMx/Xenium + ImJoy**

## Requirements
- Python 3.8+
- .h5ad file (from Seurat or Scanpy)
- R for preprocessing (convert to `.h5ad`)
- Modern browser (for ImJoy)

## Run locally

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000


