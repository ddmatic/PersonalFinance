class Record:

    def __init__(self,  category, amount):
        self.category = category
        self.amount = amount

    def __repr__(self):
        return "Record('{}, {}')".format(
            self.category,
            self.amount)