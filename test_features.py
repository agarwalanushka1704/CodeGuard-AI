from feature_extractor import extract_features


sample_code = """
def calculate_total(items):

    total = 0

    for item in items:

        if item["price"] > 0:

            total += item["price"]

    return total


items = [
    {"price": 100},
    {"price": 200},
    {"price": 300}
]

print(calculate_total(items))
"""


features = extract_features(sample_code)


print("\n========== CODEGUARD FEATURE EXTRACTION ==========\n")

if features.get("syntax_error"):

    print("Syntax Error:")
    print(features["syntax_message"])

else:

    for feature, value in features.items():

        print(f"{feature:25} : {value}")


print("\n==================================================")