import re
import json

def file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def price(price):
    return float(price.replace(" ", "").replace(",", "."))

def products(text):

    pattern=r'\d+\.\s*\n(.+?)\n([\d, ]+) x ([\d ]+,\d{2})\n([\d ]+,\d{2})'

    matches=re.findall(pattern, text)

    products=[]

    for name, qty, unit, total in matches:
        products.append({
            "name": name.strip(),
            "quantity": float(qty.replace(",", ".")),
            "unit_price": price(unit),
            "total_price": price(total)
        })

    return products

def extractprices(text):
    return re.findall(r'\d{1,3}(?: \d{3})*,\d{2}', text)

def extracttotal(text):
    match=re.search(r'ИТОГО:\s*\n([\d ]+,\d{2})', text)
    return price(match.group(1)) if match else None

def extractpayment_method(text):
    match=re.search(r'(Банковская карта|Наличные|Карта)', text)
    return match.group(1) if match else None

def extractdatetime(text):
    match=re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})', text)
    if match:
        return {"date":match.group(1), "time":match.group(2)}

def calculatetotal(products):
    return sum(p["total_price"] for p in products)


# MAIN
text=file("raw.txt")

products=products(text)
result={
    "products":products,
    "product_names":[p["name"] for p in products],
    "all_prices":extractprices(text),
    "receipt_total":extracttotal(text),
    "calculated_total":calculatetotal(products),
    "payment_method":extractpayment_method(text),
    "datetime":extractdatetime(text)
}

print(json.dumps(result, indent=4, ensure_ascii=False))
