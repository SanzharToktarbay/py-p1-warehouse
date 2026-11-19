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




# def save(data, path):
# def load(path):
# def report(data):