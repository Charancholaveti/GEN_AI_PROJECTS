import chromadb

chroma_client = chromadb.Client()
chroma_collection = chroma_client.create_collection(name="my_collection")

vectorstore = Chroma(
    collection_name="my_collection",
    client=chroma_client,
    embedding_function=embeddings
)
