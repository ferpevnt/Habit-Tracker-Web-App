def test_create_and_list_example(client):
    # Create
    r = client.post("/examples/", json={"name": "First"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["name"] == "First"
    assert "id" in data

    # List
    r = client.get("/examples/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["name"] == "First"
