from datetime import datetime, timedelta, timezone
from src.price_helper import ElectricityPriceHelper


def make_price(start_offset_hours, price):
    now = datetime.now(timezone.utc)

    start = now + timedelta(hours=start_offset_hours)
    end = start + timedelta(hours=1)

    return {
        "price": price,
        "startDate": start.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "endDate": end.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }


def sample_prices():
    return [
        make_price(-2, 20.000),   # mennyt
        make_price(1, 4.999),
        make_price(2, 5.000),
        make_price(3, 9.999),
        make_price(4, 10.000),
        make_price(5, 18.000),
    ]


def test_find_cheapest():
    helper = ElectricityPriceHelper()

    cheapest = helper.find_cheapest(sample_prices())

    assert cheapest["price"] == 4.999


def test_under_limit_boundary():
    helper = ElectricityPriceHelper()

    result = helper.find_hours_under_limit(
        sample_prices(),
        5
    )

    prices = [h["price"] for h in result]

    assert len(result) == 2
    assert 4.999 in prices
    assert 5.000 in prices
    assert 9.999 not in prices


def test_over_limit_boundary():
    helper = ElectricityPriceHelper()

    result = helper.find_hours_over_limit(
        sample_prices(),
        10
    )

    prices = [h["price"] for h in result]

    assert len(result) == 2
    assert 10.000 in prices
    assert 18.000 in prices
    assert 9.999 not in prices


def test_past_hours_filtered_out():
    helper = ElectricityPriceHelper()

    result = helper.find_hours_over_limit(
        sample_prices(),
        15
    )

    assert len(result) == 1
    assert result[0]["price"] == 18.000


def test_format_time():
    helper = ElectricityPriceHelper()

    formatted = helper.format_time(
        "2025-06-15T12:34:00.000000+0000"
    )

    assert formatted == "15.06 12:34"