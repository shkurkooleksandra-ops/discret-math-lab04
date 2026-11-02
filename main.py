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
terms = []
for combination, value in zip(combinations, values):
    if value == 1:
        literals = []
        for name, bit in zip(names, combination):
            if bit == 0:
                literals.append("\u00ac" + name)
            else:
                literals.append(name)
        term = "(" + " \u2227 ".join(literals) + ")"
        terms.append(term)
if len(terms) == 0:
    ddnf = "0"
else:
    ddnf = " \u2228 ".join(terms)
print("\nДДНФ:", ddnf)
clauses = []

for combination, value in zip(combinations, values):
    if value == 0:
        literals = []

        for name, bit in zip(names, combination):
            if bit == 0:
                literals.append(name)
            else:
                literals.append("\u00ac" + name)

        clause = "(" + " \u2228 ".join(literals) + ")"
        clauses.append(clause)

if len(clauses) == 0:
    dknf = "1"
else:
    dknf = " \u2227 ".join(clauses)

print("\nДКНФ:", dknf)
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

if values[0] == 0:
    print("Зберігає константу 0: так")
else:
    print("Зберігає константу 0: ні")
if values[7] == 1:
    print("Зберігає константу 1: так")
else:
    print("Зберігає константу 1: ні")
if values == dual_values:
    print("Самодвоїста")
else:
    print("Не самодвоїста")
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
linear = True

for index in (3, 5, 6, 7):
    if coefficients[index] == 1:
        linear = False

if linear:
    print("Лінійна")
else:
    print("Не лінійна")

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
    formula = input("Введіть формулу: ")

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

combinations = list(product((0, 1), repeat=3))
values = []

table = [
    "x1 x2 x3 | f",
    "---------+--"
]

for x1, x2, x3 in combinations:
    variables = {"x1": x1, "x2": x2, "x3": x3}

    value = calculate(expression.body, variables)
    values.append(value)

    table.append(f"{x1}  {x2}  {x3}  | {value}")

print("\n".join(table))