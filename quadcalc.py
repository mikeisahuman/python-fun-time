# -*- coding: utf-8 -*-

## This code is desiged to give the results of the quadratic formula.
## It was originally written for Python 3.x >> note that one must have 'input' for 3.x, 'raw_input' for 2.x

counter = 0
newLine = "\n"
welcomeMessage = newLine + "Welcome to the quadratic equation calculator!" + newLine*2
imagMessage = "WARNING: The numbers you have entered lead to imaginary (complex) solutions.\n  B^2 - 4*A*C = "

print(welcomeMessage)

qEQ = "A x^2 + B x + C = 0"

while True :
	if counter == 0 :
		print("We will solve an equation like:" + newLine + qEQ + newLine)

	OK = input("Type 'OK' to continue, or 'nevermind' to quit:" + newLine)

	if (OK[0] == "O" or OK[0] == "o") and (OK[1] == "K" or OK[1] == "k") :
		print("chose OK")
	else :
		print("chose to quit" + newLine*2)
		break

	A = float(input(newLine + "What is your 'A'?" + newLine))
	B = float(input("What is your 'B'?" + newLine))
	C = float(input("What is your 'C'?" + newLine))

	print("You have chosen:" + newLine + "A = " + str(A) + ", B = " + str(B) + ", C = " + str(C) + newLine)

	check = B**2 - 4*A*C

	if check < 0 :
		print(imagMessage + str(check) + newLine)
		continue
#break
	else :
		quadResultP = (-B + check**(0.5))/(2*A)
		quadResultM = (-B - check**(0.5))/(2*A)
		print("Your solutions are:\n(+) -> " + str(quadResultP) + "\n(-) -> " + str(quadResultM) + newLine)
		counter += 1
		print("Done " + str(counter) + newLine )
		continue
