with open("data.txt", "w") as f:
    f.write("Some data.\n")
    f.write("Second line.\n")

print("File created and written.")

with open("data.txt", "a") as f:
    f.write("Appended line.\n")

print("Data appended.")