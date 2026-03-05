import re

# 1. 
print("1.")
pattern1 = r"ab*"
tests1 = ["a", "ab", "abbb", "ac"]
for t in tests1:
    print(t, "->", bool(re.fullmatch(pattern1, t)))

# 2. 
print("\n2.")
pattern2 = r"ab{2,3}"
tests2 = ["abb", "abbb", "abbbb"]
for t in tests2:
    print(t, "->", bool(re.fullmatch(pattern2, t)))

# 3. 
print("\n3.")
text3 = "hello_world test_case abc_def_ghi A_B"
pattern3 = r"[a-z]+_[a-z]+"
print(re.findall(pattern3, text3))

# 4. 
print("\n4.")
text4 = "Hello world Python JAVA Test"
pattern4 = r"[A-Z][a-z]+"
print(re.findall(pattern4, text4))

# 5. 
print("\n5.")
pattern5 = r"a.*b"
tests5 = ["ab", "axxxb", "a123b", "ac"]
for t in tests5:
    print(t, "->", bool(re.fullmatch(pattern5, t)))

# 6. 
print("\n6.")
text6 = "Hello, world. Python is great"
result6 = re.sub(r"[ ,\.]", ":", text6)
print(result6)

# 7. 
print("\n7.")
snake = "hello_world_example"
components = snake.split("_")
camel = components[0] + ''.join(word.capitalize() for word in components[1:])
print(camel)

# 8. 
print("\n8.")
text8 = "HelloWorldPython"
result8 = re.split(r"(?=[A-Z])", text8)
print(result8)

# 9. 
print("\n9.")
text9 = "HelloWorldPython"
result9 = re.sub(r"(?<!^)(?=[A-Z])", " ", text9)
print(result9)

# 10. 
print("\n10.")
camel10 = "helloWorldExample"
snake10 = re.sub(r"(?<!^)(?=[A-Z])", "_", camel10).lower()
print(snake10)