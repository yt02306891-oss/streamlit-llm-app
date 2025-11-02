fruit_list = ['apple', 'banana', 'cherry', 'date']

# リストから偶数だけを抽出する関数
def get_even_indexed_fruits(fruits):
    return [fruits[i] for i in range(len(fruits)) if i % 2 == 0]    
even_indexed_fruits = get_even_indexed_fruits(fruit_list)
print(even_indexed_fruits)  # 出力: ['apple', 'cherry']

# 数値のリストを受け取り、各値に基づいてカテゴリを分類する関数を作成してください

# 条件:

# 1. 値が0以下の場合は "Low" カテゴリに分類してください

# 2. 値が1以上10以下の場合は "Medium" カテゴリに分類してください

# 3. 値が10を超える場合は "High" カテゴリに分類してください

# 4. 入力リストには整数が含まれるものとします

# 結果を辞書形式で返してください。キーがカテゴリ名で、値が該当する数値のリストとします
def categorize_numbers(num_list):
    categories = {"Low": [], "Medium": [], "High": []}
    for num in num_list:
        if num <= 0:
            categories["Low"].append(num)
        elif 1 <= num <= 10:
            categories["Medium"].append(num)
        else:
            categories["High"].append(num)
    return categories
# テスト用の数値リスト
test_numbers = [-5, 0, 3, 7, 10, 15, 20]
categorized_result = categorize_numbers(test_numbers)

print(categorized_result)
# 出力: {'Low': [-5, 0], 'Medium': [3, 7, 10], 'High': [15, 20]}
# 期待される出力:
# {'Low': [-5, 0], 'Medium': [3, 7, 10], 'High': [15, 20]}      


def calculate_bmi(weight, height):
    """体重(kg)と身長(m)からBMIを計算し、カテゴリを返す関数"""
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obesity"
    return bmi, category
# テスト用の体重と身長
weight = 75  # kg
height = 1.74  # m
bmi_value, bmi_category = calculate_bmi(weight, height)
print(f"BMI: {bmi_value:.2f}, Category: {bmi_category}")
# 出力例: BMI: 22.86, Category: Normal weight
# 期待される出力例:
# BMI: 22.86, Category: Normal weight   

