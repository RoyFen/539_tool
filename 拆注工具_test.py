import os
import re
import pandas as pd

def calculate_bet_cost(bet_numbers, bet_amount):
    """
    根據下注號碼和單注金額計算下注的成本。
    """
    bet_numbers_parts = bet_numbers.split('+')
    first_two_pairs = ''.join(bet_numbers_parts[:2])
    remaining_numbers = ''.join(bet_numbers_parts[2:])
    bet_number_units = [first_two_pairs + remaining_numbers[i:i+2] for i in range(0, len(remaining_numbers), 2)]
    total_cost = len(bet_number_units) * bet_amount
    return total_cost

def split_bet_slips(file_path, num_splits):
    """
    分割包含下注單的檔案為多個檔案，並將它們保存在以原檔案名稱命名的新目錄中。
    同時，將每個分割檔案中所有下注單位的總成本保存到一個Excel檔案中。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        bet_slips = file.read().split('-------------------------------------------------\n')

    total_bet_slips = len(bet_slips) - 1
    slips_per_file = total_bet_slips // num_splits
    extra_slips = total_bet_slips % num_splits

    new_dir_name = os.path.splitext(os.path.basename(file_path))[0]
    new_dir_path = os.path.join(os.path.dirname(file_path), new_dir_name)
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)

    total_costs = []
    start = 0
    for i in range(num_splits):
        end = start + slips_per_file + (1 if i < extra_slips else 0)
        split_content = bet_slips[start:end]
        split_file_content = '-------------------------------------------------\n'.join(split_content)

        total_cost = sum(calculate_bet_cost(re.search(r'下注號碼\s*:\s*([\d\+]+)', slip).group(1),
                                            int(re.search(r'單注金額\s*:\s*(\d+)', slip).group(1)))
                         for slip in split_content if slip.strip())
        total_costs.append(total_cost)

        split_file_name = os.path.join(new_dir_path, f"{new_dir_name}_{i+1}.txt")
        with open(split_file_name, 'w') as split_file:
            split_file.write(split_file_content)

        start = end

    # 將總成本保存到Excel檔案中
    df = pd.DataFrame({'檔案名稱': [f"{new_dir_name}_{i+1}.txt" for i in range(num_splits)],
                       '總成本': total_costs})
    df.to_excel(os.path.join(new_dir_path, f"{new_dir_name}_總成本.xlsx"), index=False)

# 範例使用
file_path = r"C:\Users\o9303\OneDrive\桌面\下注額落差較大的文本\20231212-10車.txt"  # 原始檔案路徑
num_splits = 30  # 分割數量

# 調用函數
split_bet_slips(file_path, num_splits)

# 尚未解決問題 
# 1.成本尚未平均問題 20240103