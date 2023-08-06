'''Testing for:
1) when starting calculator - memory is set to 0
2) test addition
3) test subtraction
4) test multiplication
5) test division
6) test root
7) reset memory back to 0
'''

class calculator:

  memory = 0

  def addition(self, x):
    self.memory = self.memory + x
    return self.memory

  def subtraction(self, x):
    self.memory = self.memory - x
    return self.memory

  def multiplication(self, x):
    self.memory = self.memory * x
    return self.memory

  def division(self, x):
    self.memory = self.memory / x
    return self.memory

  def nroot(self, x):
    self.memory = x**(1/float(self.memory))
    return self.memory

  def reset(self):
    self.memory = 0
    return 'Memory cleared'