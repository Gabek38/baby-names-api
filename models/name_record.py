class NameRecord:
    def __init__(self, name, sex, count, year):
        self.name = name
        self.sex = sex
        self.count = count
        self.year = year

    def __repr__(self):
        return f"NameRecord(name={self.name}, sex={self.sex}, count={self.count}, year={self.year})"