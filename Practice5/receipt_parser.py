import re
import json

def parse_receipt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Find all products
    item_pattern = (
        r'\d+\.\n'            # item number like "1."
        r'(.*?)\n'            # product name
        r'([\d ]+,\d{3})'     # quantity like "2,000"
        r' x '                # " x " between quantity and price
        r'([\d ]+,\d{2})\n'   # unit price like "154,00"
        r'([\d ]+,\d{2})'     # total like "308,00"
    )
    matches = re.findall(item_pattern, text, re.DOTALL)
    # matches is now a list of tuples:
    # [("Натрия хлорид...", "2,000", "154,00", "308,00"), ...]

    
    products = []
    for name, quantity, unit_price, total in matches:
        products.append({
            "name":         name.replace('\n', ' ').strip(),
            "quantity":     quantity.strip(),
            "unit_price":   unit_price.strip(),
            "total":        total.strip()
        })
    
    # Find total, datetime, payment
    total = re.search(r'ИТОГО:\s*\n?([\d ]+,\d{2})', text).group(1).strip()
    datetime = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})', text).group(1)
    payment = re.search(r'(Банковская карта|Наличные):', text).group(1)
    
    result = {
        "products":       products,
        "total":          total,
        "datetime":       datetime,
        "payment_method": payment
    }
    
    return result

if __name__ == "__main__":
    data = parse_receipt("raw.txt")
    print(json.dumps(data, ensure_ascii=False, indent=4))
    