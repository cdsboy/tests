from math import factorial

# Number of card in deck
x = 12.0

# number of cards in deck
y = 99.0

# Number of cards you are drawing
z = 7.0

# number you are checking for
n = 1.0

def calcIt(X, Y, Z, N):
  a = float(factorial(X) / (factorial(N) * factorial(X - N)))
  b = float(factorial(Y - X) / (factorial(Z - N) * factorial((Y - X) - (Z-N))))
  c = float(factorial(Y) / (factorial(Z) * factorial(Y-Z)))
  
  print "Chance: ", 100 * (a * (b / c))

calcIt(x, y, z, n)
calcIt(x, y - 7, 1.0, n)
calcIt(x, y - 8, 1.0, n)
calcIt(x, y - 9, 1.0, n)
calcIt(x, y - 10, 1.0, n)
