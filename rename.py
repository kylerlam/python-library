import os
import re
from packages.patterns import datetime_fourteen

def batch_rename_files(folder_path):
    # 1. 檢查路徑是否存在
    if not os.path.exists(folder_path):
        print("路徑不存在！")
        return

    # 使用從patterns導入的正則表達式模式
    pattern = re.compile(datetime_fourteen)

    print(f"開始處理文件夾: {folder_path}")

    # 2. 遍歷文件夾
    for filename in os.listdir(folder_path):
        # 獲取文件的完整路徑（只處理文件，跳過子文件夾）
        old_path = os.path.join(folder_path, filename)
        if os.path.isdir(old_path):
            continue

        # 3. 用 re 匹配並執行修改
        match = pattern.match(filename)
        if match:
            # 取得捕獲組：前14位數字 + 副檔名
            new_name = match.group(1) + match.group(2)
            new_path = os.path.join(folder_path, new_name)

            # 檢查新文件名是否已存在，避免覆蓋
            if os.path.exists(new_path) and old_path != new_path:
                print(f"[跳過] {filename} -> 新文件名 {new_name} 已存在")
                continue

            try:
                os.rename(old_path, new_path)
                print(f"[成功] {filename} -> {new_name}")
            except Exception as e:
                print(f"[失敗] 修改 {filename} 時發生錯誤: {e}")
        else:
            print(f"[忽略] {filename} (不符合匹配規則)")


# --- 使用範例 ---
# 請將下方的路徑替換為你存放圖片的實際路徑
target_folder = './workbench'
batch_rename_files(target_folder)
