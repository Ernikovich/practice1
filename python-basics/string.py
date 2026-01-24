# Quotes Inside Quotes
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

# Multiline Strings
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)
# Or three single quotes
a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)

# Strings are Arrays
a = "Hello, World!"
print(a[1])


# Looping Through a String
for x in "banana":
  print(x)


# Check if NOT
txt = "The best things in life are free!"
print("free" in txt)


# Slicing
b = "Hello, World!"
print(b[2:5])

# Slice From the Start
b = "Hello, World!"
print(b[:5])

# Upper Case
a = "Hello, World!"
print(a.upper())

# Lower Case
a = "Hello, World!"
print(a.lower())


# Remove Whitespace
# The strip() method removes any whitespace from the beginning or the end:
a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

# The replace() method replaces a string with another string:
a = "Hello, World!"
print(a.replace("H", "J"))

# String Format
age = 36
txt = f"My name is John, I am {age}"
print(txt)

# Display the price with 2 decimals:
price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)

# Perform a math operation in the placeholder, and return the result:
txt = f"The price is {20 * 59} dollars"
print(txt)

# Escape Character
txt = "We are the so-called \"Vikings\" from the north."

# Code	Result	
# \'	Single Quote	
# \\	Backslash	
# \n	New Line	
# \r	Carriage Return	
# \t	Tab	
# \b	Backspace	
# \f	Form Feed	
# \ooo	Octal value	
# \xhh	Hex value