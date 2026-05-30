from playwright.sync_api import sync_playwright
from src.price_helper import ElectricityPriceHelper


def test_real_life_price_monitoring_flow():
    helper = ElectricityPriceHelper()

    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(ElectricityPriceHelper.PRICE_ENDPOINT)

        assert response.ok

        data = response.json()
        api.dispose()

    prices = data["prices"]

    assert len(prices) > 0

    low_limit = 5
    high_limit = 10

    low_hours = helper.find_hours_under_limit(prices, low_limit)
    high_hours = helper.find_hours_over_limit(prices, high_limit)

    if low_hours:
        assert all(hour["price"] <= low_limit for hour in low_hours)

    if high_hours:
        assert all(hour["price"] >= high_limit for hour in high_hours)

    if not low_hours and not high_hours:
        future_prices = [
            hour for hour in prices
            if helper.parse_datetime(hour["startDate"]) > helper.current_time()
        ]

        assert len(future_prices) > 0
        assert all(
            low_limit < hour["price"] < high_limit
            for hour in future_prices
        )