from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import igraph as ig
from typing import List, Optional
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def set_fixed_seed(seed=42):
    random.seed(seed)
    ig.set_random_number_generator(random)

class GraphData(BaseModel):
    c_edges: List[List[int]]
    weights: Optional[List[float]] = None

@app.post("/label_propagation")
def label_propagation(graph: GraphData):
    set_fixed_seed()
    if graph.weights:
        g = ig.Graph(edges=graph.c_edges, edge_attrs={'weight': graph.weights})
    else:
        g = ig.Graph(edges=graph.c_edges)
    communities = g.community_label_propagation(weights=g.es['weight'])
    return {"communities": [list(comm) for comm in communities]}

@app.post("/walktrap")
def walktrap(graph: GraphData):
    set_fixed_seed()
    if graph.weights:
        g = ig.Graph(edges=graph.c_edges, edge_attrs={'weight': graph.weights})
    else:
        g = ig.Graph(edges=graph.c_edges)
    communities = g.community_walktrap(weights=g.es['weight']).as_clustering()
    return {"communities": [list(comm) for comm in communities]}

@app.post("/infomap")
def infomap(graph: GraphData):
    set_fixed_seed()
    if graph.weights:
        g = ig.Graph(edges=graph.c_edges, edge_attrs={'weight': graph.weights})
    else:
        g = ig.Graph(edges=graph.c_edges)
    communities = g.community_infomap()
    return {"communities": [list(comm) for comm in communities]}

@app.get("/")
def home():
    return {"message": "Hello from FastAPI on Vercel!"}

