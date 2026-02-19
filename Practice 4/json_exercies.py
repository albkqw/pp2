import json

with open('data.json', 'r') as file:
    data = json.load(file)

l = data.get('imdata')

print("Interface Status")
print("=" * 90)

print(f"{'DN':<50} {'Speed':<10} {'MTU':<10}")

print("-" * 90)

for i in l:
    d1 = i['l1PhysIf']['attributes']['dn']
    d2 = i['l1PhysIf']['attributes']['speed']
    d3 = i['l1PhysIf']['attributes']['mtu']

    print(f"{d1:<50} {d2:<10} {d3:<10}")
