from playwright.sync_api import sync_playwright


PRICE_ENDPOINT = "https://api.porssisahko.net/v2/latest-prices.json"


def test_latest_prices_api_available():
    with sync_playwright() as p:
        api = p.request.new_context()

        response = api.get(PRICE_ENDPOINT)

        assert response.ok

        data = response.json()

        assert "prices" in data
        assert len(data["prices"]) > 0

        first_price = data["prices"][0]

        assert "price" in first_price
        assert "startDate" in first_price
        assert "endDate" in first_price

        api.dispose()