class Car:
    #   the count for each car sold is added to the store summary
    stock_sold_count = 0
    price_total = 0.00
    extra_features = 0.00

    def __init__(self, name, model, year, colour, price):
        self.__name = name
        self.__model = model
        self.__year = year
        self.__colour = colour
        self.__price = price
        self.__availability = 1

    def get_stock_sold_count(self):
        """Getter function, gets current stock sold count - returns the amount of cars sold in total"""
        return self.stock_sold_count

    def get_price_total(self):
        """Getter function, gets current price total - returns the total price of price total"""
        return self.price_total

    def get_extra_features(self):
        """Getter function, gets extra features - returns the total price of extra features"""
        return self.extra_features

    def get_name(self):
        """Getter function, gets current name - returns the cars name"""
        return self.__name

    def get_model(self):
        """Getter function, gets current model - returns the cars model"""
        return self.__model

    def get_year(self):
        """Getter function, gets current year - returns the cars year"""
        return self.__year

    def get_colour(self):
        """Getter function, gets current colour - returns the cars colour"""
        return self.__colour

    def get_price(self):
        """Getter function, gets current price - returns the cars price"""
        return self.__price

    def get_availability(self):
        """Getter function, gets current availability - returns the cars availability"""
        return self.__availability

    def sell_car(self):
        """sells one car, adds 1 to sold, and adds price + extra features + amount sold to store summary"""
        self.__availability -= 1
        self.stock_sold_count += 1
        self.price_total += self.__price

    #   adds $710 to price total and extra features total
    def extended_warranty(self):
        """adds extended warranty cost to price total and extra features total"""
        self.price_total += 710
        self.extra_features += 710

    #   adds $320 to price total and extra features total
    def after_market(self):
        """adds after market wheels cost to price total and extra features total"""
        self.price_total += 320
        self.extra_features += 320

    #   adds $450 to price total and extra features total
    def tinted_windows(self):
        """adds tinted windows cost to price total and extra features total"""
        self.price_total += 450
        self.extra_features += 450

    #   adds $500 to price total and extra features total
    def liability_coverage(self):
        """adds liability coverage cost to price total and extra features total"""
        self.price_total += 500
        self.extra_features += 500

    #   adds $2000 to price total and extra features total
    def collision_coverage(self):
        """adds collision coverage cost to price total and extra features total"""
        self.price_total += 2000
        self.extra_features += 2000

    #   adds $750 to price total and extra features total
    def sound_system_coverage(self):
        """adds sound system coverage cost to price total and extra features total"""
        self.price_total += 750
        self.extra_features += 750

    #   adds $700 to price total and extra features total
    def theft_coverage(self):
        """adds theft coverage cost to price total and extra features total"""
        self.price_total += 700
        self.extra_features += 700