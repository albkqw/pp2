import os
from functools import reduce


# 1. directory handling
folder = 'sales'
files = os.listdir(folder)
for file in files:
    path = os.path.join(folder, file)
    with open(path, 'r', encoding='utf-8') as f:
        f.read()


# 2. file handling 
products = []

for file in files:
    path = os.path.join(folder, file)

    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                name, quantity = line.strip().split(",")
                products.append((name, int(quantity)))


# 3. data analysis
# all records
total_records = len(products)

# all quantities
quantities = [quantity for name, quantity in products]

# sum
total_quantity = sum(quantities)

# avg
average_quantity = total_quantity / total_records if total_records else 0

# max and min 
max_quantity = max(quantities)
min_quantity = min(quantities)

# map
increased = list(map(lambda x: (x[0], x[1] + 2), products))

# filter
popular = list(filter(lambda x: x[1] > 5, products))

# reduce
product_all = reduce(lambda a, b: a * b, quantities, 1)

# enumerate
print("Products with index:")
for i, (name, quantity) in enumerate(products, start=1):
    print(i, name, quantity)

# zip
names = [name for name, quantity in products]
quantities = [quantity for name, quantity in products]
zipped = list(zip(names, quantities))

# sort
sorted_products = sorted(products, key=lambda x: x[1])

# 4. save Results to File
with open("sales_report.txt", "w") as f:
    f.write(f"Total records: {total_records}\n")
    f.write(f"Average quantity sold: {average_quantity:.2f}\n")
    f.write(f"Highest quantity sold: {max_quantity}\n")
    f.write(f"Lowest quantity sold: {min_quantity}\n\n")
    
    f.write("Popular products:\n")
    for name, quantity in popular:
        f.write(f"{name} {quantity}\n")
