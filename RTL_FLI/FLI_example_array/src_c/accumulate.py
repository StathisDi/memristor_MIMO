class Accumulator:
    def __init__(self):
        self.total = 1

    def add(self, value):
        self.total += value
        return self.total


# Instance of Accumulator
accumulator_instance = Accumulator()


def accumulate(value):
    return accumulator_instance.add(value)


# vsim -gui work.top_array -voptargs=+acc
