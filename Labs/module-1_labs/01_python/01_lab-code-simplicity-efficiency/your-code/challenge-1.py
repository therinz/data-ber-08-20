"""
This is a dumb calculator that can add and subtract whole numbers from zero to five.
When you run the code, you are prompted to enter two numbers (in the form of English
word instead of number) and the operator sign (also in the form of English word).
The code will perform the calculation and give the result if your input is what it
expects.

The code is very long and messy. Refactor it according to what you have learned about
code simplicity and efficiency.
"""

def calc(n1, n2, op):
    return n1 + n2 if op == "plus" else n1 - n2

print('Welcome to this calculator!')
print('It can add and subtract whole numbers from zero to five')
a = input('Please choose your first number (zero to five): ').lower()
b = input('What do you want to do? plus or minus: ').lower()
c = input('Please choose your second number (zero to five): ').lower()

text2num = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
num2text = {v: k for k, v in text2num.items()}
ops = ["plus", "minus"]

if a not in text2num or c not in text2num or b not in ops:
    print("I am not able to answer this question. Check your input.")
else:
    result = calc(text2num[a], text2num[c], b)
    print(f"{a} {b} {c} equals {num2text[result]}")

print("Thanks for using this calculator, goodbye :)")
