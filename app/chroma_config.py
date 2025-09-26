import chromadb
import pandas as pd
import uuid

def get_or_create_portfolio_collection(csv_path="app/my_portfolio.csv", client_path="vectorstore"):
    client = chromadb.PersistentClient(client_path)
    collection = client.get_or_create_collection(name="portfolio")
    # Only ingest if empty
    if not collection.count():
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            collection.add(
                documents=row["Techstack"],
                metadatas={"links": row["Links"]},
                ids=[str(uuid.uuid4())]
            )
    return collection