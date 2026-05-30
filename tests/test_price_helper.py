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


def test_print_hours_empty(capsys):
    helper = ElectricityPriceHelper()

    helper.print_hours("Good time to heat the sauna:", [])

    assert "no matching hours." in capsys.readouterr().out


def test_print_hours_formats_output(capsys):
    helper = ElectricityPriceHelper()

    helper.print_hours(
        "Good time to heat the sauna:",
        [make_price(1, 4.5)]
    )

    out = capsys.readouterr().out

    assert "Good time to heat the sauna:" in out
    assert "4.5 c/kWh" in out