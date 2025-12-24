import os
import re
from packages.patterns import datetime_fourteen_file, datetime_fourteen_folder

def batch_rename_files_and_folders(folder_path, recursive=False):
    # 1. 檢查路徑是否存在
    if not os.path.exists(folder_path):
        print("路徑不存在！")
        return

    # 使用從patterns導入的正則表達式模式
    file_pattern = re.compile(datetime_fourteen_file)
    folder_pattern = re.compile(datetime_fourteen_folder)

    print(f"開始處理文件夾: {folder_path}")

    # 2. 收集要處理的項目（文件和文件夾）
    items_to_process = []
    
    if recursive:
        # 遞歸處理所有子文件夾
        # 注意：os.walk 會先處理文件夾，然後處理文件
        # 我們需要先處理深層的文件夾，再處理淺層的，避免路徑問題
        all_items = []
        for root, dirs, files in os.walk(folder_path, topdown=False):  # topdown=False 從深層開始
            # 處理文件夾
            for dirname in dirs:
                # 跳過 .DS_Store 文件夾（通常不會有，但以防萬一）
                if dirname == '.DS_Store':
                    continue
                old_path = os.path.join(root, dirname)
                all_items.append(('folder', root, dirname, old_path))
            
            # 處理文件
            for filename in files:
                # 跳過 .DS_Store 文件
                if filename == '.DS_Store':
                    continue
                old_path = os.path.join(root, filename)
                all_items.append(('file', root, filename, old_path))
        
        # 按路徑深度排序，確保先處理深層項目
        items_to_process = sorted(all_items, key=lambda x: x[3].count(os.sep), reverse=True)
    else:
        # 只處理當前文件夾
        for itemname in os.listdir(folder_path):
            # 跳過 .DS_Store
            if itemname == '.DS_Store':
                continue
            
            old_path = os.path.join(folder_path, itemname)
            if os.path.isdir(old_path):
                items_to_process.append(('folder', folder_path, itemname, old_path))
            else:
                items_to_process.append(('file', folder_path, itemname, old_path))

    # 3. 處理項目
    for item_type, root, itemname, old_path in items_to_process:
        if item_type == 'file':
            # 處理文件
            match = file_pattern.match(itemname)
            if match:
                # 取得捕獲組：前14位數字 + 副檔名
                new_name = match.group(1) + match.group(2)
                new_path = os.path.join(root, new_name)

                # 如果新舊文件名相同，跳過
                if new_name == itemname:
                    print(f"[跳過文件] {itemname} -> 文件名已符合規則")
                    continue

                # 檢查新文件名是否已存在，避免覆蓋
                if os.path.exists(new_path):
                    print(f"[跳過文件] {itemname} -> 新文件名 {new_name} 已存在")
                    continue

                try:
                    os.rename(old_path, new_path)
                    print(f"[成功文件] {itemname} -> {new_name}")
                except Exception as e:
                    print(f"[失敗文件] 修改 {itemname} 時發生錯誤: {e}")
            else:
                print(f"[忽略文件] {itemname} (不符合匹配規則)")
        
        else:  # item_type == 'folder'
            # 處理文件夾
            match = folder_pattern.match(itemname)
            if match:
                # 取得捕獲組：前14位數字 + 非數字部分
                # group(1): 前14位數字
                # group(2): 第15位及以後的數字（如果有）
                # group(3): 非數字部分（如-中文）
                new_name = match.group(1) + match.group(3)  # 保留前14位數字和非數字部分
                new_path = os.path.join(root, new_name)

                # 如果新舊文件夾名相同，跳過
                if new_name == itemname:
                    print(f"[跳過文件夾] {itemname} -> 文件夾名已符合規則")
                    continue

                # 檢查新文件夾名是否已存在，避免覆蓋
                if os.path.exists(new_path):
                    print(f"[跳過文件夾] {itemname} -> 新文件夾名 {new_name} 已存在")
                    continue

                try:
                    os.rename(old_path, new_path)
                    print(f"[成功文件夾] {itemname} -> {new_name}")
                except Exception as e:
                    print(f"[失敗文件夾] 修改 {itemname} 時發生錯誤: {e}")
            else:
                print(f"[忽略文件夾] {itemname} (不符合匹配規則)")


# --- 使用範例 ---
# 請將下方的路徑替換為你存放圖片的實際路徑
target_folder = './workbench'
batch_rename_files_and_folders(target_folder, recursive=True)
