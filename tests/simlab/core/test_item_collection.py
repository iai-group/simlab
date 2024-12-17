"""Tests for item collection."""

import pytest

from simlab.core.item_collection import ItemCollection


@pytest.fixture
def item_collection() -> ItemCollection:
    """Returns an item collection for testing."""
    return ItemCollection("imdb_movies")


def test_get_random_item(item_collection: ItemCollection) -> None:
    """Tests get random item."""
    item = item_collection.get_random_item()
    assert item.id is not None
    assert all(key in item.properties for key in ["title", "year", "genre"])


def test_get_item_by_id(item_collection: ItemCollection) -> None:
    """Tests get item by ID."""
    item = item_collection.get_random_item()
    item_id = item.id
    item_by_id = item_collection.get_item_by_id(item_id)

    assert item_by_id.id == item.id
    assert item_by_id.properties == item.properties


def test_get_items(item_collection: ItemCollection) -> None:
    """Tests get items."""
    items = item_collection.get_items({"genre": "action"})
    print(items)
    assert len(items) == 2
    assert all(item.properties["genre"] == "action" for item in items)


def test_get_possible_property_values(item_collection: ItemCollection) -> None:
    """Tests get possible property values."""
    possible_values = item_collection.get_possible_property_values("genre")
    assert (
        set(possible_values).difference({"action", "romance", "comedy"})
        == set()
    )


def test_get_possible_properties(item_collection: ItemCollection) -> None:
    """Tests get possible properties."""
    properties = item_collection.get_possible_properties()
    assert set(properties) == {"title", "year", "genre", "rating"}
