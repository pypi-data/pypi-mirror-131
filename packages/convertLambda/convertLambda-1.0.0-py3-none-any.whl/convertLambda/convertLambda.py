import re

class convertLambda():
    beta = ''
    def __init__(self, input, omicron):
        self.input = input
        self.omicron = omicron
    def result(self):
        return self.beta
    def lam(self):
        alpha = re.sub('λ', 'lambda ', self.input) # Replace λ with lambda
        self.beta = re.sub(r"([.]+) *", ": ", alpha)
        self.result()
    def nan(self):
        alpha = re.sub("/", " ", self.input)
        self.beta = re.sub(r"([.]+) *", ": ", alpha)
        self.result()
    def run(self):
        check = lambda: self.lam() if self.omicron is True else self.nan()
        check()
    def help(self):
        print("""example code:

a = convertLambda("λx.2*x", True)
a.run()
print(a.result())

The first argument, or 'input', is where you say your input Lambda-Calculas. Example. λx.x

The second argument, or 'omicron' is where a boolean should be. Ex. True. What this means is that
your telling the module wether or not you want to use λ (True); or lambda (False)""")
