## Data Loading

### Load Vertices
```
dsbulk load -url /path/to/vertices.csv -k <graph_name> -t <vertex_table_name>  -header true
```

### Load Edges
```
dsbulk load -url /path/to/edges.csv -k <graph_name> -t <edge_table_name>  -header true
```

## Data Structure Details

#### vertices.csv Structure
```
publicKey
1
2
3
...
```

#### edges.csv Structure
```
out_publicKey,in_publicKey,trust,datetime
"6","2","4","2010-11-08T13:45:11.728360"
"6","5","2","2010-11-08T13:45:41.533780"
...
```

#### Data Source
https://snap.stanford.edu/data/soc-sign-bitcoin-alpha.html

#### Raw Data Structure of soc-sign-bitcoinotc.csv
```
SOURCE, TARGET, RATING, TIME
```

## Optional: Data ETL
### Run ETL to generate the vertices and edges files:
`PYTHONPATH=. python3 graphdatabook/paths/data/etl.py`
