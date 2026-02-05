from langchain.tools import tool
from app.llm.vector import get_vector_store
from langchain.tools.retriever import create_retriever_tool

# Vector store retriever tool

@tool
def product_search(query: str, k: int = 3):
    """
    Search products by similarity using the vector store.
    Returns top-k products with metadata (name, price, image_path, etc.)
    """
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    results = retriever.get_relevant_documents(query)
    return [r.metadata for r in results]


def get_rag_tool():
    """
    Wrap the vector store retriever as a LangChain retriever tool for agents.
    """
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    rag_tool = create_retriever_tool(
        retriever,
        name="product_search",
        description="""
        Search and return product details such as name, color, price,
        description, and image path.
        """
    )
    return rag_tool
