import json
import QuantLib as ql
from datetime import datetime

class MarketData:
     def __init__(self, data: dict):
        # Pas besoin de charger le JSON ici, c'est déjà un dict
        try:
            self.option_name = data['option_name']
            self.spot = data['spot']
            self.strike = data['strike']
            self.volatility = data['volatility']
            self.rate = data['rate']
            self.option_type = data['option_type'].lower()
            self.subtype = data['subtype'].lower()
            self.maturity_date = self._parse_date(data['maturity_date'])
            self.currency = data['currency'].upper()
        except KeyError as e:
            raise ValueError(f"Missing required market data field: {e}")


        # Set evaluation date and other QuantLib parameters
        self.eval_date = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = self.eval_date

        self.spot_handle = ql.QuoteHandle(ql.SimpleQuote(self.spot))
        self.vol_handle = ql.BlackVolTermStructureHandle(
            ql.BlackConstantVol(self.eval_date, ql.TARGET(), self.volatility, ql.Actual365Fixed())
        )
        self.rate_handle = ql.YieldTermStructureHandle(
            ql.FlatForward(self.eval_date, self.rate, ql.Actual365Fixed())
        )

        # Check for additional parameters based on the option subtype
        self._check_additional_parameters(data)

     def _parse_date(self, date_str):
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return ql.Date(dt.day, dt.month, dt.year)
        except Exception:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

     def _check_additional_parameters(self, data):
        """
        Validates additional parameters based on the option subtype (e.g., barrier).
        """
        if self.subtype == 'barrier':
            try:
                self.barrier_type = data['barrier_type']
                self.barrier_level = data['barrier_level']
                self.rebate = data.get('rebate', 0.0)  # Optional, defaults to 0.0 if not provided
            except KeyError as e:
                raise ValueError(f"Barrier option requires '{e.args[0]}' field.")
        elif self.subtype == 'lookback':
            try:
                self.lookback_type = data['lookback_type']  # Could be "long" or "short"
            except KeyError as e:
                raise ValueError(f"Lookback option requires '{e.args[0]}' field.")

        elif self.subtype == 'vanilla':
            pass  # No additional parameters needed for vanilla options

     def __str__(self):
        """
        String representation of the market data for display purposes.
        """
        return f"Option Name: {self.name}\n" \
               f"Spot: {self.spot}\n" \
               f"Strike: {self.strike}\n" \
               f"Volatility: {self.volatility}\n" \
               f"Rate: {self.rate}\n" \
               f"Option Type: {self.option_type}\n" \
               f"Subtype: {self.subtype}\n" \
               f"Maturity Date: {self.maturity_date}\n"