import json
from market_data import MarketData
from european_option_pricer import EuropeanOptionPricer
from option_pricing_csv_writer import OptionPricingCSVWriter

def main():
    json_path = "data/market_data.json"

    with open(json_path, 'r') as f:
        option_list = json.load(f)

    for option_data in option_list:
        try:
            market_data = MarketData(option_data)
            option_pricer = EuropeanOptionPricer(market_data)
            option_price = option_pricer.price()

            print(f"\nPriced Option: {market_data.option_name}")
            print(f"Price: {option_price:.4f} {market_data.currency}")

            csv_writer = OptionPricingCSVWriter(market_data, option_price)
            csv_writer.write_to_csv()

        except Exception as e:
            print(f"Error pricing {option_data.get('option_name', 'Unknown')}: {e}")

if __name__ == "__main__":
    main()