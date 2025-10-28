from betalytics_scraper.normalize import map_sample_endpoint

def test_map_sample_endpoint_basic():
    payload = {"items": [{"id":1,"league":"NFL","team":"KC","stat":"yards","value":55}]}
    rows = list(map_sample_endpoint(payload))
    assert rows and rows[0]["team"] == "KC"
