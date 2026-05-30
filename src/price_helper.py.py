# sahko.py
import requests
from datetime import datetime, timezone

PRICE_ENDPOINT = 'https://api.porssisahko.net/v1/latest-prices.json'

def find_cheapest():
    prices_per_hour = requests.get(PRICE_ENDPOINT).json()['prices']
    return min(prices_per_hour, key=lambda x:x['price'])

def find_hours_under_limit(limit: int):
    prices_per_hour = requests.get(PRICE_ENDPOINT).json()['prices']
    now = datetime.now(timezone.utc)
    cheap_hours = [hour for hour in prices_per_hour if hour['price'] <= limit \
                    and datetime.strptime(hour['startDate'], "%Y-%m-%dT%H:%M:%S.%f%z") > now]
    if len(cheap_hours) > 0:
        cheap_hours_sorted = sorted(cheap_hours, key=lambda x: x['startDate'])
        print('Sauna päälle näihin aikoihin:')
        for hour in cheap_hours_sorted:
            print(f"Aika: {hour['startDate']} - {hour['endDate']}, hinta: {hour['price']}")

def find_hours_over_limit(limit: int):
    prices_per_hour = requests.get(PRICE_ENDPOINT).json()['prices']
    now = datetime.now(timezone.utc)
    cheap_hours = [hour for hour in prices_per_hour if hour['price'] >= limit \
                    and datetime.strptime(hour['startDate'], "%Y-%m-%dT%H:%M:%S.%f%z") > now]
    if len(cheap_hours) > 0:
        cheap_hours_sorted = sorted(cheap_hours, key=lambda x: x['startDate'])
        print('HUOM! Sähkön hinta korkea lähiaikoina!')
        for hour in cheap_hours_sorted:
            print(f"Aika: {hour['startDate']} - {hour['endDate']}, hinta: {hour['price']}")

if __name__ == "__main__":
    find_hours_under_limit(5)
    find_hours_over_limit(7)
