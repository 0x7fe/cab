from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import igraph as ig
from typing import List

app = FastAPI()

# 允许 CORS 访问（ObservableHQ 需要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GraphData(BaseModel):
    edges: List[List[int]]

@app.post("/label_propagation")
def label_propagation(graph: GraphData):
    g = ig.Graph(edges=graph.edges)
    communities = g.community_label_propagation()
    return {"communities": [list(comm) for comm in communities]}

@app.post("/walktrap")
def walktrap(graph: GraphData):
    g = ig.Graph(edges=graph.edges)
    communities = g.community_walktrap().as_clustering()
    return {"communities": [list(comm) for comm in communities]}

@app.post("/infomap")
def infomap(graph: GraphData):
    g = ig.Graph(edges=graph.edges)
    communities = g.community_infomap()
    return {"communities": [list(comm) for comm in communities]}

@app.get("/")
def home():
    return {"message": "Hello from FastAPI on Vercel!"}

