# Option Pricing Project

## 🧠 Description
This project implements a financial derivative pricing tool for **European Vanilla Options** and **European Barrier Options** using the **QuantLib** library. The program accepts market data in JSON format, processes it, and returns the option pricing based on specified parameters.





## 📁 Project Structure
OptionPricer/
├── src/                           # Main source code
│   ├── main.py                    # Entry point
│   ├── market_data.py             # Loads and validates input data
│   ├── european_option_pricer     # Pricing logic for vanilla and barrier options
|   ├── option_pricing_csv_writer  # CSV Writer
│
├── data/                     # Input data files
│   └── market_data.json      # JSON file with option parameters
│
├── reports/                               # Output folder for pricing results
│   └── prices_{pricingdate}.csv           # CSV report of priced options
│
├── README.md                 # Project description and usage guide

