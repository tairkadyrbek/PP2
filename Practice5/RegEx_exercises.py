import re

# 1 'a' followed by zero or more 'b's
print(re.findall(r'ab*', "ac abbb ab a"))

# 2 'a' followed by two or three 'b's
print(re.findall(r'ab{2,3}\b', "ab abb abbb abbbb"))

# 3 Sequences of lowercase letters joined with underscore
print(re.findall(r'[a-z]+_[a-z]+', "hello_world hey_hey ABC"))

# 4 One uppercase letter followed by lowercase letters
print(re.findall(r'[A-Z][a-z]+', "Hello World well WIN"))

# 5 'a' followed by anything, ending in 'b'
print(re.findall(r'a.*?b', "aXYZb axb alfefeb"))

# 6 Replace space, comma or dot with colon
print(re.sub(r'[ ,.]', ':', "one two,three.four"))

# 7 Snake case to camel case
print(re.sub(r'_([a-z])', lambda m: m.group(1).upper(), "hello_world_woo"))

# 8 Split string at uppercase letters
print(re.split(r'(?=[A-Z])', "HelloWorldPeople"))

# 9 Insert spaces between words starting with capital letters
print(re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', "HelloWorldPeople"))

# 10 Camel case to snake case
print(re.sub(r'(?<=[a-z])([A-Z])', lambda m: '_' + m.group(1).lower(), "helloWorldPeopleYee"))

