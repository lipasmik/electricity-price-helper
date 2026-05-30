import argparse
from datetime import datetime, timezone
import requests


class ElectricityPriceHelper:

    PRICE_ENDPOINT = "https://api.porssisahko.net/v2/latest-prices.json"

    def fetch_prices(self):
        response = requests.get(self.PRICE_ENDPOINT, timeout=10)
        response.raise_for_status()
        return response.json()["prices"]

    def find_cheapest(self, prices):
        return min(prices, key=lambda h: h["price"])

    def find_hours_under_limit(self, prices, limit):
        now = datetime.now(timezone.utc)

        return sorted(
            [
                h for h in prices
                if h["price"] <= limit
                and self.parse_datetime(h["startDate"]) > now
            ],
            key=lambda h: h["startDate"]
        )

    def find_hours_over_limit(self, prices, limit):
        now = datetime.now(timezone.utc)

        return sorted(
            [
                h for h in prices
                if h["price"] >= limit
                and self.parse_datetime(h["startDate"]) > now
            ],
            key=lambda h: h["startDate"]
        )

    def parse_datetime(self, value):
        return datetime.strptime(
            value,
            "%Y-%m-%dT%H:%M:%S.%f%z"
        )

    def format_time(self, value):
        dt = self.parse_datetime(value)
        return dt.strftime("%d.%m %H:%M")

    def print_hours(self, title, hours):
        if not hours:
            print(f"{title} Ei osumia.")
            return

        print(title)

        for hour in hours:
            start = self.format_time(hour["startDate"])
            end = self.format_time(hour["endDate"])

            print(
                f"{start} - {end}, "
                f"{hour['price']} c/kWh"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Electricity price helper"
    )

    parser.add_argument(
        "--under",
        type=float,
        default=5,
        help="Show hours under this price"
    )

    parser.add_argument(
        "--over",
        type=float,
        default=15,
        help="Show hours over this price"
    )

    args = parser.parse_args()

    helper = ElectricityPriceHelper()
    prices = helper.fetch_prices()

    helper.print_hours(
        "Sauna päälle näihin aikoihin:",
        helper.find_hours_under_limit(prices, args.under)
    )

    helper.print_hours(
        "HUOM! Sähkön hinta korkea lähiaikoina!",
        helper.find_hours_over_limit(prices, args.over)
    )


if __name__ == "__main__":
    main()
