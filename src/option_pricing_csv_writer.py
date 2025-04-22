import os
import csv

class OptionPricingCSVWriter:
    def __init__(self, market_data, option_price):
        self.market_data = market_data
        self.option_price = option_price
        self.filename = f'reports/prices_{self.market_data.maturity_date}.csv'
        
        # Create reports directory if it doesn't exist
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
    
    def write_to_csv(self):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write header if the file is empty
            if file.tell() == 0:
                writer.writerow(['Option Name', 'Option Type', 'Subtype', 'Maturity Date', 'Pricing Date', 'Price', 'Currency'])
            
            # WXrite the option data
            writer.writerow([self.market_data.option_name,
                             self.market_data.option_type,
                             self.market_data.subtype,
                             self.market_data.maturity_date,
                             self.market_data.eval_date,
                             self.option_price,
                             self.market_data.currency])