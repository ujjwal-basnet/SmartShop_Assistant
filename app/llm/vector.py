from app.config.settings import config
from langchain_openai import OpenAIEmbeddings
from tenacity import retry, stop_after_attempt, wait_random_exponential
from loguru import logger
from langchain_chroma import Chroma
from langchain.docstore.document import Document
import os

# ------------------------------
# Embeddings setup
# ------------------------------

Embedding_Model = config.OPENAI_EMBEDDING_MODEL
Embedding_Dim = config.OPENAI_EMBEDDING_DIM

embeddings_model = OpenAIEmbeddings(
    model=Embedding_Model,
    api_key=config.OPENAI_API_KEY
)

@retry(wait=wait_random_exponential(min=1, max=2), stop=stop_after_attempt(2))
def get_embedding(data) -> list:
    """
    Return embeddings for a string or list of strings.
    Always returns a list of vectors.
    """
    if isinstance(data, str):
        result = embeddings_model.embed_query(data)
        logger.info(f'Embedding dimensions: {len(result)}')
        return [result]

    if isinstance(data, list):
        result = embeddings_model.embed_documents(data)
        logger.info(f'Embedding dimensions: {len(result[0])}')
        return result

    else:
        raise ValueError("Only string or list is supported currently")

# ------------------------------
# Vector Store setup (Chroma)
# ------------------------------

PERSIST_DIR = "app/vector_db"

def get_vector_store():
    """
    Load or initialize Chroma vector store
    """
    if not os.path.exists(PERSIST_DIR):
        os.makedirs(PERSIST_DIR)

    vector_store = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings_model
    )
    return vector_store

# ------------------------------
# Index products
# ------------------------------

def index_products(products: list):
    """
    Index a list of product dicts into Chroma vector store.
    Each product dict must include:
    id, name, description, color, category, image_path, price
    """
    docs = []
    for p in products:
        # Combine relevant fields as text
        text = f"{p['name']} {p['description']} color:{p['color']} category:{p['category']}"
        docs.append(
            Document(
                page_content=text,
                metadata=p
            )
        )

    vector_store = get_vector_store()
    vector_store.add_documents(docs)
    vector_store.persist()
    logger.info(f"Indexed {len(products)} products into vector store.")

# ------------------------------
# Search products
# ------------------------------

def search_products(query: str, k: int = 3):
    """
    Search the vector store for top-k similar products
    Returns a list of product metadata dicts
    """
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return [r.metadata for r in results]

# ------------------------------
# Example usage
# ------------------------------

if __name__ == "__main__":
    sample_products = [
        {
            "id": 1,
            "name": "Red Saree",
            "description": "Elegant red saree for weddings",
            "color": "red",
            "category": "saree",
            "image_path": "images/red_saree.png",
            "price": 50
        },
        {
            "id": 2,
            "name": "Blue Saree",
            "description": "Light blue saree for casual wear",
            "color": "blue",
            "category": "saree",
            "image_path": "images/blue_saree.png",
            "price": 45
        },
        {
            "id": 3,
            "name": "Green Saree",
            "description": "Green saree with golden embroidery",
            "color": "green",
            "category": "saree",
            "image_path": "images/green_saree.png",
            "price": 55
        }
    ]

    # Index sample products
    index_products(sample_products)

    # Search example
    query = "elegant red saree for wedding"
    results = search_products(query, k=3)
    for item in results:
        print(item["name"], item["price"], item["image_path"])
