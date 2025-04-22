import QuantLib as ql

class EuropeanOptionPricer:
    def __init__(self, market_data):
        """
        Initialize the pricer for European options using the market data.
        """
        self.market_data = market_data
        
        # Access market data attributes directly
        self.strike = self.market_data.strike
        self.maturity_date = self.market_data.maturity_date
        self.option_type = self.market_data.option_type
        self.subtype = self.market_data.subtype

        # Validate and create payoff based on option type
        if self.option_type == 'call':
            self.payoff = ql.PlainVanillaPayoff(ql.Option.Call, self.strike)
        elif self.option_type == 'put':
            self.payoff = ql.PlainVanillaPayoff(ql.Option.Put, self.strike)
        else:
            raise ValueError(f"Unsupported option type: {self.option_type}")

        # Set up the Black-Scholes process with handles from market_data
        self.process = ql.BlackScholesProcess(
            self.market_data.spot_handle,
            self.market_data.rate_handle,
            self.market_data.vol_handle
        )

    def price(self):
        """
        Price the option based on the subtype provided (e.g., vanilla, barrier).
        """
        if self.subtype == 'barrier':
            return self.price_barrier()
        else:
            return self.price_vanilla()

    def price_vanilla(self):
        """
        Price a standard European vanilla option (call/put).
        """
        exercise = ql.EuropeanExercise(self.maturity_date)
        option = ql.VanillaOption(self.payoff, exercise)

        # Use analytic engine for European option pricing
        engine = ql.AnalyticEuropeanEngine(self.process)
        option.setPricingEngine(engine)
        return option.NPV()

    def price_barrier(self):
        """
        Price a European barrier option (up-and-in, up-and-out, etc.).
        """
        # Get barrier parameters from market data
        barrier_type = self._get_barrier_type()
        barrier_level = self.market_data.barrier_level
        rebate = self.market_data.rebate  # Optional rebate
        
        exercise = ql.EuropeanExercise(self.maturity_date)
        
        # Create a barrier option
        option = ql.BarrierOption(barrier_type, barrier_level, rebate, self.payoff, exercise)
        engine = ql.AnalyticBarrierEngine(self.process)
        option.setPricingEngine(engine)
        
        return option.NPV()


    def _get_barrier_type(self):
        """
        Helper method to map barrier type from string to QuantLib constant.
        """
        if self.market_data.barrier_type == 'up-and-in':
            return ql.Barrier.UpIn
        elif self.market_data.barrier_type == 'up-and-out':
            return ql.Barrier.UpOut
        elif self.market_data.barrier_type == 'down-and-in':
            return ql.Barrier.DownIn
        elif self.market_data.barrier_type == 'down-and-out':
            return ql.Barrier.DownOut
        else:
            raise ValueError(f"Invalid barrier type: {self.market_data.barrier_type}")
