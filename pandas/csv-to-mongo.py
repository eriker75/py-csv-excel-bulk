import csv
import pymongo

batchSize = 1000

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mi_base_de_datos"]
collection = db["mi_coleccion"]

rows = [] 
with open('mi_archivo_grande.csv') as f:
    reader = csv.DictReader(f)

    bulk = collection.initialize_unordered_bulk_op()
    
    for i, row in enumerate(reader):
        rows.append(insert_one(row))
        
        if i % batchSize == 0 and i > 0:
            bulk.execute() 
            rows = []
            print(f"Insertados {i} registros")
            db.client.close() # Hacer commit
            
            bulk = collection.initialize_unordered_bulk_op() 

if rows:
    bulk.execute() 
    db.client.close()