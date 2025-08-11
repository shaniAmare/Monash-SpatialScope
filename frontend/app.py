from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import anndata as ad
import numpy as np
import pandas as pd
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow access from browser
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load h5ad file on server startup
adata = ad.read_h5ad("test.h5ad")

# Try to detect spatial coordinates
if "spatial" in adata.obsm:
    coords = pd.DataFrame(adata.obsm["spatial"], columns=["x", "y"])
else:
    coords = adata.obs[["x", "y"]]

# Prepare gene list and metadata
GENES = list(adata.var_names)
META_COLS = ["cell_type", "cluster", "niche"]
OBS = adata.obs[META_COLS] if all(col in adata.obs.columns for col in META_COLS) else adata.obs

@app.get("/genes")
def list_genes():
    return {"genes": GENES}

@app.get("/meta")
def get_metadata_columns():
    return {"meta": list(OBS.columns)}

@app.get("/meta_values")
def get_metadata(column: str):
    if column in OBS.columns:
        values = OBS[column].astype(str).unique().tolist()
        return {"values": values}
    return {"error": "Column not found"}

@app.get("/cells")
def get_cells(gene: str = None):
    df = coords.copy()
    df["cell_id"] = adata.obs_names

    if gene and gene in GENES:
        expr = adata[:, gene].X
        df["expression"] = expr.toarray().flatten() if hasattr(expr, "toarray") else expr
    else:
        df["expression"] = 0

    for col in META_COLS:
        if col in OBS.columns:
            df[col] = OBS[col].astype(str).values

    return df.to_dict(orient="records")
