number = 5.1
print(type(number))
print(number)
#Binary representation of 5 is 101
print(bin(9))
a = 1.2e3
print(type(a))

print(format(145,'o'))

# Circle area Circle Area = πr2
# pi = 3.14
pi = 3.14 
print(pi*84**2)

# If you cross a 490-meter-long street in 7 minutes, 
# then what is your speed in meters per second? Print your answer without any decimal point in it
distance = 490
time = 7 * 60 # converting minutes to seconds
speed = distance / time
print(int(speed))


###################################### strings
name = "John Doe"
print(type(name))
print(name)
print(name[0]) # accessing the first character
print(name[1]) # accessing the second character

first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print(full_name)
# String formatting
print(f"Hello, {full_name}!")
# string lazy evaluation
print("The value of pi is approximately {:.2f}".format(pi))

print(full_name[:4]) # slicing the string to get the first name
print(full_name[5:]) # slicing the string to get the last name

print(len(full_name)) # getting the length of the string
print(full_name[-3:]) # slicing the string to get the last 5 characters

print('doe' in full_name) # checking if 'doe' is in full_name
print("HP" not in full_name) # checking if 'HP' is not in full_name

print(''' This is a multi-line string.
It can span multiple lines.''')