def add_item(data, name, qty, price):
    item = name.strip().lower()

    if not item:
        raise ValueError("Название товара не может быть пустым")

    if not isinstance(qty, int) or qty <= 0:
        raise ValueError("Количество должно быть положительным числом")

    if price < 0:
        raise ValueError("Цена не может быть отрицательным")
    if item in data["items"]:
        data["items"][item]["qty"] += qty
        data["items"][item]["price"] = price
    else:
        data["items"][item] = {
            "qty": qty, 
            "price": price
            } 


def total_value(data):
    total = 0

    for item in data["items"].values():
        total += item["qty"] * item["price"]

    return round(total, 2)


def remove_item(data, name, qty):
    item = name.strip().lower()

    if item not in data["items"]:
        raise KeyError("Такого товара не существует")

    if not isinstance(qty, int) or qty <= 0:
            raise ValueError("Количество должно быть положительным числом")
    
    if data["items"][item]["qty"] < qty:
        raise ValueError("Нету столько товара")

    
    data["items"][item]["qty"] -= qty

    if data["items"][item]["qty"] == 0:
        del data["item"][item]


def report(data):
    lines = []

    for name in sorted(data["items"]):
        qty = data["items"][name]["qty"] 
        price = data["items"][name]["price"]
        cost = qty * price

        text = f"{name}: {qty} шт. x {price:.2f} = {cost:.2f}"

        lines.append(text)
    return lines


# def save(data, path):
# def load(path):
# def report(data):