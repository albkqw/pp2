import re
import json


with open("raw.txt", "r", encoding="utf-8") as file:
    receipt_text = file.read()

# product names
product_pattern = r"\d+\.\s*\n([^\n]+)"
products = re.findall(product_pattern, receipt_text)

# price info
price_pattern = r"\b\d{1,3}(?:\s\d{3})*,\d{2}\b"
prices = re.findall(price_pattern, receipt_text)

def price_to_float(price):
    return float(price.replace(" ", "").replace(",", "."))

price_values = [price_to_float(p) for p in prices]

# total
total_pattern = r"ИТОГО:\s*\n?([\d\s,]+)"
total_match = re.search(total_pattern, receipt_text)

total = None
if total_match:
    total = price_to_float(total_match.group(1))

# date info
datetime_pattern = r"Время:\s*([\d\.]+\s[\d:]+)"
datetime_match = re.search(datetime_pattern, receipt_text)

datetime_value = datetime_match.group(1) if datetime_match else None

# payment method
payment_pattern = r"(Банковская карта|Наличные)"
payment_match = re.search(payment_pattern, receipt_text)

payment_method = payment_match.group(1) if payment_match else None

# ---------- STRUCTURED OUTPUT ----------
parsed_data = {
    "products": products,
    "prices": price_values,
    "total": total,
    "datetime": datetime_value,
    "payment_method": payment_method
}

print(json.dumps(parsed_data, indent=4, ensure_ascii=False))