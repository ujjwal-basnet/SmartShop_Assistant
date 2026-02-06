# test/test_vector.py

from app.llm.vector import index_products_from_sqlite, search_products

def test_index_and_search():
    n = index_products_from_sqlite()
    assert n >= 8

    hits = search_products("toothpaste", k=3)
    assert isinstance(hits, list)
    assert len(hits) > 0
    assert any("Toothpaste" in (h.get("name") or "") for h in hits)

    hits2 = search_products("red tshirt", k=3)
    assert any("Red T-Shirt" in (h.get("name") or "") for h in hits2)
