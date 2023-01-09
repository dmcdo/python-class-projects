from math import floor, ceil

class Category:
    def __init__(self, name):
        self._name = name
        self._bal = 0
        self._wallet = []
    
    def get_name(self):
        return self._name
    
    def get_wallet(self):
        return tuple(self._wallet)

    def add_revenue(self, amount, desc=''):
        self._bal += amount
        self._wallet.append({
            'amount': amount,
            'description': desc
        })

    def add_expense(self, amount, desc=''):
        if amount <= self._bal:
            self.add_revenue(-amount, desc)
            return True

        return False

    def transfer_money(self, amount, other):
        if amount <= self._bal:
            self.add_expense(amount, f'Send money to {other._name}')
            other.add_revenue(amount, f'Send money from {self._name}')
            return True

        return False

    def get_balance(self):
        return self._bal

    def check_category_balance(self, amount):
        return amount > self._bal

    def __str__(self):
        out = '*' * floor((30 - len(self._name)) / 2) + self._name + \
              '*' *  ceil((30 - len(self._name)) / 2) + '\n'

        for transaction in self._wallet:
            samt = f"{transaction['amount']:.2f}"
            desc = transaction['description']

            out += desc + (' ' * (30 - len(desc) - len(samt))) + samt + '\n'

        return f'{out}Total: {self._bal:<.2f}'