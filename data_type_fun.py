# --- Data type examples ---

# Integer
my_int = 42
print(f"Integer: {my_int} (type: {type(my_int)})")

# Float
my_float = 3.14159
print(f"Float: {my_float} (type: {type(my_float)})")

# String
my_string = "Python is Fun!"
print(f"String: '{my_string}' (type: {type(my_string)})")

# --- String manipulation examples ---

# Uppercase and lowercase
print("Uppercase:", my_string.upper())
print("Lowercase:", my_string.lower())

# Replace text
new_string = my_string.replace("Fun", "Awesome")
print("After replace:", new_string)

# Split into words
words = my_string.split(" ")
print("Split into words:", words)

# Join words back together
joined_string = "-".join(words)
print("Joined with dashes:", joined_string)

# String slicing
print("First 6 characters:", my_string[:6])
print("Last 4 characters:", my_string[-4:])

# String formatting with f-strings
name = "Broadus"
age = 40
height = 5.6
print(f"My name is {name}, I am {age} years old, and my height is {height} feet.")

# Type casting
age_str = str(age)  # int → str
pi_int = int(my_float)  # float → int (truncates)
print(f"Age as string: '{age_str}' (type: {type(age_str)})")
print(f"Pi as int: {pi_int} (type: {type(pi_int)})")

print(age, my_float)