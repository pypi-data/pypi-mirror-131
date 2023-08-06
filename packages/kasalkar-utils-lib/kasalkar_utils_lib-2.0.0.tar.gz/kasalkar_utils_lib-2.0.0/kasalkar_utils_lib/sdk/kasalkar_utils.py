import requests
  
class Currency_convertor:
    # empty dict to store the conversion rates
    rates = {} 
    def __init__(self):
        url = str.__add__('http://data.fixer.io/api/latest?access_key=', '45c5373efce13fb37dc648f6fa5397a8')
        data = requests.get(url).json()
  
        # Extracting only the rates from the json data
        self.rates = data["rates"] 
  
    # function to do a simple cross multiplication between 
    # the amount and the conversion rates
    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != 'EUR' :
            amount = amount / self.rates[from_currency]
  
        # limiting the precision to 2 decimal places
        amount = round(amount * self.rates[to_currency], 2)
        print('{} {} = {} {}'.format(initial_amount, from_currency, amount, to_currency))
  
# Driver code
if __name__ == "__main__":
    
    c = Currency_convertor()
    c.convert('USD', 'INR', 1)

currency_convertor = Currency_convertor()