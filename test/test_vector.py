import pytest

from app.config.settings import config
from app.llm import vector


def test_vector_paths_exist():
    assert config.SQLITE_DB_PATH.exists()
    assert config.SQLITE_DB_PATH.name.endswith(".db")


def test_fetch_products_from_sqlite_returns_rows():
    products = vector.fetch_products_from_sqlite()
    assert isinstance(products, list)
    assert len(products) >= 8
    for p in products:
        assert "id" in p
        assert "name" in p
        assert "description" in p
        assert "price" in p
        assert "quantity" in p
        assert "image_path" in p


def test_product_to_text_is_string():
    products = vector.fetch_products_from_sqlite()
    text = vector._product_to_text(products[0])
    assert isinstance(text, str)
    assert "name:" in text
    assert "description:" in text


@pytest.mark.llm
def test_get_vector_store_returns_chroma():
    store = vector.get_vector_store()
    assert store is not None
    assert "chroma" in store.__class__.__name__.lower()


@pytest.mark.llm
def test_index_products_from_sqlite_and_search():
    n = vector.index_products_from_sqlite()
    assert n >= 8

    hits = vector.search_products("toothpaste for brushing", k=3)
    assert isinstance(hits, list)
    assert len(hits) > 0
    assert any("toothpaste" in (h.get("name") or "").lower() for h in hits)

    hits2 = vector.search_products("red tshirt", k=3)
    assert any("red" in (h.get("name") or "").lower() for h in hits2)


@pytest.mark.llm
def test_get_embedding_text_and_list_shapes():
    v1 = vector.get_embedding("hello")
    assert isinstance(v1, list)
    assert len(v1) == 1
    assert isinstance(v1[0], list)
    assert len(v1[0]) > 1000

    v2 = vector.get_embedding(["a", "b"])
    assert isinstance(v2, list)
    assert len(v2) == 2
    assert isinstance(v2[0], list)
    assert len(v2[0]) == len(v1[0])
