import subprocess
import sys
import pytest
from playwright.sync_api import sync_playwright
from src.price_helper import ElectricityPriceHelper


def test_real_life_price_monitoring_flow() -> None:
    helper = ElectricityPriceHelper()

    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(ElectricityPriceHelper.PRICE_ENDPOINT)

        assert response.ok

        data = response.json()
        api.dispose()

    prices = data["prices"]

    assert len(prices) > 0

    verify_price_limits(helper, prices, low_limit=5, high_limit=10)


@pytest.mark.parametrize("over,under", [("5", "10"), ("10", "10")])
def test_invalid_thresholds_show_error(over: str, under: str) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "src.price_helper", "--over", over, "--under", under],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "--over price threshold must be greater than --under" in result.stderr


def verify_price_limits(
    helper: ElectricityPriceHelper,
    prices: list,
    low_limit: float,
    high_limit: float,
) -> None:
    low_hours = helper.find_hours_under_limit(prices, low_limit)
    high_hours = helper.find_hours_over_limit(prices, high_limit)

    assert all(hour["price"] <= low_limit for hour in low_hours)
    assert all(hour["price"] >= high_limit for hour in high_hours)

    if not low_hours and not high_hours:
        future_prices = [
            hour for hour in prices
            if helper.parse_datetime(hour["startDate"]) > helper.current_time()
        ]

        assert all(low_limit < hour["price"] < high_limit for hour in future_prices)