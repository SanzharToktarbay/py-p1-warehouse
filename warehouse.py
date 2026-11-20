import json
import argparse
import sys


class WarehouseParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def add_item(data, name, qty, price):
    item = name.strip().lower()

    if not item:
        raise ValueError("Название товара не может быть пустым")

    if not isinstance(qty, int) or qty <= 0:
        raise ValueError("Количество должно быть положительным числом")

    if type(price) not in (int, float) or price < 0:
        raise ValueError("Цена должна быть неотрицательным числом")
    
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
        available = data["items"][item]["qty"]
        raise ValueError(
        f"на складе только {available} шт. товара «{item}»"
    )

    
    data["items"][item]["qty"] -= qty

    if data["items"][item]["qty"] == 0:
        del data["items"][item]


def report(data):
    lines = []

    for name in sorted(data["items"]):
        qty = data["items"][name]["qty"] 
        price = data["items"][name]["price"]
        cost = qty * price

        text = f"{name}: {qty} шт. x {price:.2f} = {cost:.2f}"

        lines.append(text)
    return lines


def save(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



def load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
            return {"items": {}}


def run_menu(data, path):
    while True:
        print("\n========== СКЛАД МАГАЗИНА ==========")
        print("1. Добавить товар")
        print("2. Списать товар")
        print("3. Посмотреть остатки")
        print("4. Общая стоимость склада")
        print("5. Выход")

        choice = input("\nВыберите действие: ").strip()

        try:
            if choice == "1":
                name = input("Название товара: ")
                qty = int(input("Количество: "))
                price = float(input("Цена: "))

                add_item(data, name, qty, price)
                save(data, path)

                item = name.strip().lower()
                print(
                    f"Добавлено: {item} — {qty} шт. "
                    f"по {price:.2f}"
                )

            elif choice == "2":
                name = input("Название товара: ")
                qty = int(input("Количество для списания: "))

                remove_item(data, name, qty)
                save(data, path)

                item = name.strip().lower()
                remaining = data["items"].get(
                    item, {}
                ).get("qty", 0)

                print(
                    f"Списано: {item} — {qty} шт. "
                    f"Осталось: {remaining}"
                )

            elif choice == "3":
                lines = report(data)

                if not lines:
                    print("Склад пуст.")
                else:
                    for line in lines:
                        print(line)

            elif choice == "4":
                total = total_value(data)
                print(f"Стоимость склада: {total:.2f}")

            elif choice == "5":
                print("До свидания!")
                break

            else:
                print("Ошибка: неизвестный пункт меню")


        except (ValueError, KeyError, OSError) as error:
            message = error.args[0] if error.args else str(error)
            print(f"Ошибка: {message}")


def main():
    try:
        parser = WarehouseParser(
            description="Программа учета товаров на складе"
        )

        parser.add_argument("--file", default="store.json")

        commands = parser.add_subparsers(
            dest="command", required=True
        )

        p_add = commands.add_parser("add")
        p_add.add_argument("name")
        p_add.add_argument("qty", type=int)
        p_add.add_argument("price", type=float)

        p_remove = commands.add_parser("remove")
        p_remove.add_argument("name")
        p_remove.add_argument("qty", type=int)

        commands.add_parser("list")
        commands.add_parser("total")
        commands.add_parser("menu")

        args = parser.parse_args()
        data = load(args.file)

        if args.command == "add":
            add_item(data, args.name, args.qty, args.price)
            save(data, args.file)

            name = args.name.strip().lower()

            print(
                f"Добавлено: {name} — {args.qty} шт. "
                f"по {args.price:.2f}"
            )

        elif args.command == "remove":
            name = args.name.strip().lower()

            remove_item(data, args.name, args.qty)
            save(data, args.file)

            remaining = data["items"].get(
                name, {}
            ).get("qty", 0)

            print(
                f"Списано: {name} — {args.qty} шт. "
                f"Осталось: {remaining}"
            )

        elif args.command == "list":
            for line in report(data):
                print(line)

        elif args.command == "total":
            total = total_value(data)
            print(f"Стоимость склада: {total:.2f}")

        elif args.command == "menu":
            run_menu(data, args.file)

    except (ValueError, KeyError, OSError) as error:
        message = error.args[0] if error.args else str(error)
        print(f"Ошибка: {message}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())


