from itertools import product
import ast

while True:
    text = input("Введіть 8 значень функції через пробіл: ")
    parts = text.split()
    if len(parts) != 8:
        print("Потрібно ввести рівно 8 значень")
    elif not all(part in ("0", "1") for part in parts):
        print("Дозволені тільки числа 0 і 1")
    else:
        break
values = []
for part in parts:
    values.append(int(part))
combinations = list(product((0, 1), repeat=3))
table = [
    "x1 x2 x3 | f",
    "---------+--"
]

for combination, value in zip(combinations, values):
    x1, x2, x3 = combination
    table.append(f"{x1}  {x2}  {x3}  | {value}")
print("\n".join(table))
dual_values = []
for value in reversed(values):
    dual_values.append(1 - value)
print("\nЗначення двоїстої функції:", dual_values)
names = ("x1", "x2", "x3")


def normal_form(values, target):
    inner = " \u2227 " if target == 1 else " \u2228 "
    outer = " \u2228 " if target == 1 else " \u2227 "
    terms = []

    for combination, value in zip(product((0, 1), repeat=3), values):
        if value == target:
            literals = [
                name if bit == target else "\u00ac" + name
                for name, bit in zip(("x1", "x2", "x3"), combination)
            ]
            terms.append("(" + inner.join(literals) + ")")

    return outer.join(terms) if terms else str(1 - target)


print("\nДДНФ:", normal_form(values, 1))
print("\nДКНФ:", normal_form(values, 0))
row = values.copy()
coefficients = []

while len(row) > 0:
    coefficients.append(row[0])

    next_row = []

    for i in range(len(row) - 1):
        next_row.append(row[i] ^ row[i + 1])

    row = next_row

print("\nКоефіцієнти полінома Жегалкіна:", coefficients)
monomials = (
    "1", "x3", "x2", "x2*x3",
    "x1", "x1*x3", "x1*x2", "x1*x2*x3"
)

polynomial_terms = []

for coefficient, monomial in zip(coefficients, monomials):
    if coefficient == 1:
        polynomial_terms.append(monomial)

if len(polynomial_terms) == 0:
    polynomial = "0"
else:
    polynomial = " \u2295 ".join(polynomial_terms)

print("\nПоліном Жегалкіна:", polynomial)
print("\nВластивості функції:")

print("Зберігає константу 0:", "так" if values[0] == 0 else "ні")
print("Зберігає константу 1:", "так" if values[7] == 1 else "ні")
print("Самодвоїста:", "так" if values == dual_values else "ні")
monotone = True

for i in range(8):
    for j in range(8):
        inputs_increase = all(
            a <= b
            for a, b in zip(combinations[i], combinations[j])
        )

        if inputs_increase and values[i] > values[j]:
            monotone = False

if monotone:
    print("Монотонна")
else:
    print("Не монотонна")
linear = all(coefficients[i] == 0 for i in (3, 5, 6, 7))
print("Лінійна:", "так" if linear else "ні")

allowed_names = ("x1", "x2", "x3")
allowed_nodes = (
    ast.Expression,
    ast.Name, ast.Load,
    ast.Constant,
    ast.BoolOp, ast.And, ast.Or,
    ast.UnaryOp, ast.Not,
    ast.BinOp, ast.BitXor,
)


def calculate(node, variables):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Name):
        return variables[node.id]

    if isinstance(node, ast.UnaryOp):
        return 1 - calculate(node.operand, variables)

    if isinstance(node, ast.BoolOp):
        results = []

        for operand in node.values:
            results.append(calculate(operand, variables))

        if isinstance(node.op, ast.And):
            return int(all(results))
        else:
            return int(any(results))

    if isinstance(node, ast.BinOp):
        left = calculate(node.left, variables)
        right = calculate(node.right, variables)
        return left ^ right

    raise ValueError("Невідомий елемент формули.")


while True:
    formula = input("Введіть формулу в синтаксисі Python (наприклад (x1 and x2) ^ (not x3)): ")

    try:
        expression = ast.parse(formula, mode="eval")

        for node in ast.walk(expression):
            if not isinstance(node, allowed_nodes):
                raise ValueError("Недозволена операція або елемент формули.")

            if isinstance(node, ast.Name):
                if node.id not in allowed_names:
                    raise ValueError(f"Невідома змінна: {node.id}")

            if isinstance(node, ast.Constant):
                if type(node.value) is not int or node.value not in (0, 1):
                    raise ValueError("Дозволені лише сталі 0 та 1.")

        break

    except SyntaxError:
        print("Перевірте запис формули та дужки. Спробуйте ще раз.")

    except ValueError as error:
        print(error)


def analyze(values):
    combinations = list(product((0, 1), repeat=3))

    table = [
        "x1 x2 x3 | f",
        "---------+--"
    ]
    for combination, value in zip(combinations, values):
        x1, x2, x3 = combination
        table.append(f"{x1}  {x2}  {x3}  | {value}")

    print("\n".join(table))


values = []

for x1, x2, x3 in product((0, 1), repeat=3):
    variables = {"x1": x1, "x2": x2, "x3": x3}
    value = calculate(expression.body, variables)
    values.append(value)

analyze(values)
