# Built-in imports
import random  # Generate random numbers
import math  # Access mathematical functions like sqrt, factorial, etc.
import datetime  # Work with dates and times

# Your custom module
import hello_world  # Assumes this is in the same directory

# Popular 3rd-party import
import matplotlib.pyplot as plt  # Plotting graphs

# Obscure/fun 3rd-party import
import pyfiglet  # Create ASCII art text

# --- Using the imports ---

# Random number between 0 and 10
number = random.randint(0, 10)
print(f"Random number: {number}")

# Math example: square root of the number
print(f"Square root: {math.sqrt(number):.2f}")

# Current date/time
now = datetime.datetime.now()
print(f"Current date/time: {now}")

# Call a function from your custom module
hello_world.say_hello()  # Assuming your hello_world module has this

# Simple matplotlib plot of random numbers
x_values = list(range(5))
y_values = [random.randint(0, 10) for _ in range(5)]
plt.plot(x_values, y_values, marker='o')
plt.title("Random Numbers Plot")
plt.xlabel("Index")
plt.ylabel("Random Value")
plt.show()

# Fun ASCII art with pyfiglet
ascii_banner = pyfiglet.figlet_format("Hello Imports!")
print(ascii_banner)
