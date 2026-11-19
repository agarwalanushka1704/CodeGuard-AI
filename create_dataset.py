# ==========================================
# CODEGUARD AI - DATASET GENERATOR
# ==========================================

import os
import numpy as np
import pandas as pd

from feature_extractor import extract_features


# ==========================================
# OUTPUT PATH
# ==========================================

OUTPUT_PATH = "dataset/code_dataset.csv"


# ==========================================
# SAMPLE PYTHON PROGRAMS
# ==========================================

samples = [

    # 1
    """
def add(a, b):
    return a + b

result = add(10, 20)
print(result)
""",

    # 2
    """
def calculate_average(numbers):
    total = 0
    for number in numbers:
        total += number
    return total / len(numbers)

values = [10, 20, 30, 40]
print(calculate_average(values))
""",

    # 3
    """
def check_number(number):
    if number > 0:
        return "Positive"
    elif number < 0:
        return "Negative"
    else:
        return "Zero"

print(check_number(10))
""",

    # 4
    """
def find_largest(numbers):
    largest = numbers[0]

    for number in numbers:
        if number > largest:
            largest = number

    return largest

print(find_largest([4, 8, 2, 9, 5]))
""",

    # 5
    """
def count_even(numbers):
    count = 0

    for number in numbers:
        if number % 2 == 0:
            count += 1

    return count

print(count_even([1, 2, 3, 4, 5, 6]))
""",

    # 6
    """
def factorial(n):
    result = 1

    for i in range(1, n + 1):
        result *= i

    return result

print(factorial(5))
""",

    # 7
    """
def search_item(items, target):
    for item in items:
        if item == target:
            return True

    return False

print(search_item([1, 2, 3, 4], 3))
""",

    # 8
    """
def calculate_discount(price, discount):
    if price > 0 and discount >= 0 and discount <= 100:
        return price - (price * discount / 100)

    return price

print(calculate_discount(1000, 10))
""",

    # 9
    """
def process_numbers(numbers):
    result = []

    for number in numbers:
        if number > 0:
            result.append(number * 2)
        else:
            result.append(0)

    return result

print(process_numbers([2, -1, 4, -3]))
""",

    # 10
    """
def login(username, password):
    if username == "admin":
        if password == "1234":
            return True
        else:
            return False
    else:
        return False

print(login("admin", "1234"))
""",

    # 11
    """
def calculate_grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"

print(calculate_grade(82))
""",

    # 12
    """
def sum_matrix(matrix):
    total = 0

    for row in matrix:
        for value in row:
            total += value

    return total

matrix = [[1, 2], [3, 4]]
print(sum_matrix(matrix))
""",

    # 13
    """
def validate_user(user):
    if user is not None:
        if "name" in user:
            if user["name"]:
                return True

    return False
""",

    # 14
    """
def calculate_tax(income):
    if income <= 250000:
        tax = 0
    elif income <= 500000:
        tax = income * 0.05
    elif income <= 1000000:
        tax = income * 0.20
    else:
        tax = income * 0.30

    return tax

print(calculate_tax(750000))
""",

    # 15
    """
def reverse_string(text):
    result = ""

    for character in text:
        result = character + result

    return result

print(reverse_string("hello"))
""",

    # 16
    """
def remove_duplicates(numbers):
    result = []

    for number in numbers:
        if number not in result:
            result.append(number)

    return result

print(remove_duplicates([1, 2, 2, 3, 3, 4]))
""",

    # 17
    """
def read_file(filename):
    try:
        file = open(filename, "r")
        data = file.read()
        file.close()
        return data
    except Exception:
        return None

print(read_file("data.txt"))
""",

    # 18
    """
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 0

print(divide(10, 2))
""",

    # 19
    """
def get_user_data(users, user_id):
    for user in users:
        if user["id"] == user_id:
            return user

    return None

print(get_user_data([], 1))
""",

    # 20
    """
def calculate_statistics(numbers):
    total = 0
    minimum = numbers[0]
    maximum = numbers[0]

    for number in numbers:
        total += number

        if number < minimum:
            minimum = number

        if number > maximum:
            maximum = number

    average = total / len(numbers)

    return total, minimum, maximum, average
""",

    # 21
    """
def complex_logic(a, b, c, d):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    return True

    return False
""",

    # 22
    """
def nested_processing(data):
    result = []

    for group in data:
        for item in group:
            if item > 0:
                if item % 2 == 0:
                    result.append(item * 2)

    return result
""",

    # 23
    """
def risky_operation(user_input):
    result = eval(user_input)
    return result

print(risky_operation("2 + 2"))
""",

    # 24
    """
def execute_command(command):
    import os
    os.system(command)

execute_command("echo hello")
""",

    # 25
    """
def duplicate_logic(numbers):
    total = 0
    total = total + numbers[0]
    total = total + numbers[1]
    total = total + numbers[2]
    total = total + numbers[3]

    return total
""",

    # 26
    """
def poorly_structured(data):
    x = 0

    for a in data:
        if a > 0:
            for b in data:
                if b > 0:
                    if a != b:
                        x += a * b

    return x
""",

    # 27
    """
def process_order(order):
    if order is not None:
        if order.get("items"):
            if order.get("customer"):
                if order["customer"].get("address"):
                    return "Order accepted"

    return "Invalid order"
""",

    # 28
    """
def clean_data(data):
    cleaned = []

    for value in data:
        if value is not None:
            if isinstance(value, str):
                if value.strip():
                    cleaned.append(value.strip())

    return cleaned
""",

    # 29
    """
def calculate_price(price, quantity, tax):
    subtotal = price * quantity
    tax_amount = subtotal * tax
    total = subtotal + tax_amount

    return total
""",

    # 30
    """
def fibonacci(n):
    sequence = [0, 1]

    for i in range(2, n):
        sequence.append(sequence[i - 1] + sequence[i - 2])

    return sequence[:n]

print(fibonacci(10))
""",

    # 31
    """
def classify_age(age):
    if age < 0:
        return "Invalid"
    elif age < 13:
        return "Child"
    elif age < 20:
        return "Teenager"
    elif age < 60:
        return "Adult"
    else:
        return "Senior"

print(classify_age(21))
""",

    # 32
    """
def find_common(first, second):
    result = []

    for item in first:
        if item in second:
            result.append(item)

    return result

print(find_common([1, 2, 3], [2, 3, 4]))
""",

    # 33
    """
def validate_password(password):
    if len(password) >= 8:
        if any(character.isdigit() for character in password):
            if any(character.isupper() for character in password):
                return True

    return False
""",

    # 34
    """
def calculate_bill(items):
    total = 0

    for item in items:
        price = item["price"]
        quantity = item["quantity"]
        total += price * quantity

    return total
""",

    # 35
    """
def process_data(data):
    result = []

    for item in data:
        if item > 10:
            result.append(item * 2)
        elif item > 5:
            result.append(item + 5)
        else:
            result.append(0)

    return result
""",

    # 36
    """
def complex_search(data, target):
    for group in data:
        for item in group:
            if item == target:
                return True
            elif item > target:
                if item - target < 5:
                    return True

    return False
""",

    # 37
    """
def unsafe_file(filename):
    file = open(filename)
    content = file.read()
    file.close()
    return content

print(unsafe_file("input.txt"))
""",

    # 38
    """
def convert_values(values):
    converted = []

    for value in values:
        try:
            converted.append(int(value))
        except Exception:
            converted.append(0)

    return converted
""",

    # 39
    """
def calculate_result(a, b):
    if a > 10 and b > 10:
        return a * b
    elif a > 10 or b > 10:
        return a + b
    else:
        return a - b
""",

    # 40
    """
def simple_message(name):
    message = "Hello " + name
    return message

print(simple_message("User"))
"""
]


# ==========================================
# CREATE DATASET
# ==========================================

rows = []

for index, code in enumerate(samples, start=1):

    features = extract_features(code)

    # Skip invalid samples
    if features.get("syntax_error"):
        print(f"Skipping sample {index}: syntax error")
        continue

    # --------------------------------------
    # AUTOMATIC PROTOTYPE LABELING
    # --------------------------------------
    #
    # These labels are heuristic labels for
    # dataset construction. They are NOT
    # real-world ground truth.
    #

    complexity = features["complexity"]
    nesting = features["nesting_depth"]
    duplicates = features["duplicate_lines"]
    long_lines = features["long_lines"]
    risky_calls = features["risky_calls"]
    comments = features["comments"]
    lines = features["lines"]

    # Quality starts high
    quality = 100

    quality -= complexity * 2
    quality -= nesting * 4
    quality -= duplicates * 5
    quality -= long_lines * 1.5
    quality -= risky_calls * 8

    # Small documentation bonus
    if lines > 10 and comments > 0:
        quality += 3

    quality = max(0, min(100, quality))


    # Bug risk
    risk = 5

    risk += complexity * 3
    risk += nesting * 5
    risk += duplicates * 4
    risk += risky_calls * 12
    risk += long_lines * 1.5

    risk = max(0, min(100, risk))


    # --------------------------------------
    # SAVE ROW
    # --------------------------------------

    row = {
        "lines": features["lines"],
        "functions": features["functions"],
        "branches": features["branches"],
        "loops": features["loops"],
        "exception_handlers": features["exception_handlers"],
        "boolean_operations": features["boolean_operations"],
        "complexity": features["complexity"],
        "nesting_depth": features["nesting_depth"],
        "long_lines": features["long_lines"],
        "duplicate_lines": features["duplicate_lines"],
        "comments": features["comments"],
        "comment_ratio": features["comment_ratio"],
        "risky_calls": features["risky_calls"],
        "quality_score": round(quality, 2),
        "bug_risk": round(risk, 2)
    }

    rows.append(row)


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(rows)
# ==========================================
# PROTOTYPE DATASET AUGMENTATION
# ==========================================
#
# The original 40 programs are expanded with
# controlled feature variation.
#
# This is still a synthetic prototype dataset.
# It is NOT real-world ground truth.
# ==========================================

np.random.seed(42)

base_df = df.copy()

augmented_rows = []

for _, row in base_df.iterrows():

    # Create 5 variations of every sample
    for _ in range(5):

        new_row = row.copy()

        # ----------------------------------
        # Small structural variations
        # ----------------------------------

        integer_features = [
            "lines",
            "functions",
            "branches",
            "loops",
            "exception_handlers",
            "boolean_operations",
            "complexity",
            "nesting_depth",
            "long_lines",
            "duplicate_lines",
            "comments",
            "risky_calls"
        ]

        for feature in integer_features:

            original_value = int(new_row[feature])

            variation = np.random.choice(
                [-1, 0, 0, 0, 1]
            )

            new_value = max(
                0,
                original_value + variation
            )

            new_row[feature] = new_value

        # ----------------------------------
        # Comment ratio
        # ----------------------------------

        if new_row["lines"] > 0:

            new_row["comment_ratio"] = round(
                min(
                    1.0,
                    max(
                        0.0,
                        new_row["comments"] / new_row["lines"]
                    )
                ),
                3
            )

        # ----------------------------------
        # Quality score variation
        # ----------------------------------

        quality_noise = np.random.normal(
            loc=0,
            scale=3.5
        )

        quality_adjustment = (
            new_row["complexity"] * 0.4
            + new_row["nesting_depth"] * 0.6
            + new_row["duplicate_lines"] * 0.8
            + new_row["risky_calls"] * 1.2
        )

        new_row["quality_score"] = round(
            max(
                0,
                min(
                    100,
                    float(row["quality_score"])
                    - quality_adjustment
                    + quality_noise
                )
            ),
            2
        )

        # ----------------------------------
        # Bug risk variation
        # ----------------------------------

        risk_noise = np.random.normal(
            loc=0,
            scale=4.0
        )

        risk_adjustment = (
            new_row["complexity"] * 0.5
            + new_row["nesting_depth"] * 0.8
            + new_row["duplicate_lines"] * 0.7
            + new_row["risky_calls"] * 1.5
        )

        new_row["bug_risk"] = round(
            max(
                0,
                min(
                    100,
                    float(row["bug_risk"])
                    + risk_adjustment
                    + risk_noise
                )
            ),
            2
        )

        augmented_rows.append(new_row)


# ==========================================
# COMBINE ORIGINAL + AUGMENTED DATA
# ==========================================

augmented_df = pd.DataFrame(
    augmented_rows
)

df = pd.concat(
    [
        base_df,
        augmented_df
    ],
    ignore_index=True
)


# ==========================================
# SHUFFLE DATASET
# ==========================================

df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# ==========================================
# SAVE CSV
# ==========================================

os.makedirs("dataset", exist_ok=True)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==========================================
# RESULT
# ==========================================

print("\n===================================")
print("       DATASET CREATED")
print("===================================")

print("\nTotal samples:", len(df))

print("\nColumns:")
print(list(df.columns))

print("\nSaved to:")
print(OUTPUT_PATH)

print("\nDataset preview:")
print(df.head())

print("\nDataset generation completed successfully.")