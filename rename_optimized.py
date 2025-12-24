import os
import re
from packages.patterns import datetime_fourteen_file, datetime_fourteen_folder


# ==================== 辅助函数：关注点分离 ====================

def validate_path(folder_path):
    """验证路径是否存在"""
    if not os.path.exists(folder_path):
        print("路徑不存在！")
        return False
    return True


def log_message(message, item_type=None, status=None):
    """统一的日志输出函数"""
    prefix = ""
    if status and item_type:
        prefix = f"[{status}{item_type}] "
    elif status:
        prefix = f"[{status}] "
    
    print(f"{prefix}{message}")


def collect_items(folder_path, recursive=False):
    """
    收集要处理的文件和文件夹
    
    返回: list of tuples (item_type, root, itemname, old_path)
    """
    items_to_process = []
    
    if recursive:
        # 递归处理所有子文件夹
        all_items = []
        for root, dirs, files in os.walk(folder_path, topdown=False):
            # 处理文件夹
            for dirname in dirs:
                if dirname == '.DS_Store':
                    continue
                old_path = os.path.join(root, dirname)
                all_items.append(('folder', root, dirname, old_path))
            
            # 处理文件
            for filename in files:
                if filename == '.DS_Store':
                    continue
                old_path = os.path.join(root, filename)
                all_items.append(('file', root, filename, old_path))
        
        # 按路径深度排序，确保先处理深层项目
        items_to_process = sorted(all_items, key=lambda x: x[3].count(os.sep), reverse=True)
    else:
        # 只处理当前文件夹
        for itemname in os.listdir(folder_path):
            if itemname == '.DS_Store':
                continue
            
            old_path = os.path.join(folder_path, itemname)
            if os.path.isdir(old_path):
                items_to_process.append(('folder', folder_path, itemname, old_path))
            else:
                items_to_process.append(('file', folder_path, itemname, old_path))
    
    return items_to_process


def process_file(itemname, root, old_path, file_pattern):
    """处理单个文件"""
    match = file_pattern.match(itemname)
    if not match:
        log_message(f"{itemname} (不符合匹配規則)", item_type="文件", status="忽略")
        return None
    
    # 获取捕获组：前14位数字 + 扩展名
    new_name = match.group(1) + match.group(2)
    new_path = os.path.join(root, new_name)
    
    return new_name, new_path


def process_folder(itemname, root, old_path, folder_pattern):
    """处理单个文件夹"""
    match = folder_pattern.match(itemname)
    if not match:
        log_message(f"{itemname} (不符合匹配規則)", item_type="文件夾", status="忽略")
        return None
    
    # 获取捕获组：前14位数字 + 非数字部分
    new_name = match.group(1) + match.group(3)  # 保留前14位数字和非数字部分
    new_path = os.path.join(root, new_name)
    
    return new_name, new_path


def should_skip_rename(old_name, new_name, new_path, item_type):
    """检查是否需要跳过重命名"""
    # 如果新旧名称相同，跳过
    if new_name == old_name:
        log_message(f"{old_name} -> 名稱已符合規則", item_type=item_type, status="跳過")
        return True
    
    # 检查新名称是否已存在，避免覆盖
    if os.path.exists(new_path):
        log_message(f"{old_name} -> 新名稱 {new_name} 已存在", item_type=item_type, status="跳過")
        return True
    
    return False


def perform_rename(old_path, new_path, item_type):
    """执行重命名操作"""
    try:
        os.rename(old_path, new_path)
        old_name = os.path.basename(old_path)
        new_name = os.path.basename(new_path)
        log_message(f"{old_name} -> {new_name}", item_type=item_type, status="成功")
        return True
    except Exception as e:
        old_name = os.path.basename(old_path)
        log_message(f"修改 {old_name} 時發生錯誤: {e}", item_type=item_type, status="失敗")
        return False


def process_item(item_type, root, itemname, old_path, file_pattern, folder_pattern):
    """处理单个项目（文件或文件夹）"""
    if item_type == 'file':
        result = process_file(itemname, root, old_path, file_pattern)
        item_type_chinese = "文件"
    else:  # item_type == 'folder'
        result = process_folder(itemname, root, old_path, folder_pattern)
        item_type_chinese = "文件夾"
    
    if result is None:
        return  # 不符合规则，已记录日志
    
    new_name, new_path = result
    
    # 检查是否需要跳过
    if should_skip_rename(itemname, new_name, new_path, item_type_chinese):
        return
    
    # 执行重命名
    perform_rename(old_path, new_path, item_type_chinese)


# ==================== 主函数：协调各个模块 ====================

def batch_rename_files_and_folders(folder_path, recursive=False):
    """批量重命名文件和文件夹（主协调函数）"""
    # 1. 验证路径
    if not validate_path(folder_path):
        return
    
    # 2. 编译正则表达式模式
    file_pattern = re.compile(datetime_fourteen_file)
    folder_pattern = re.compile(datetime_fourteen_folder)
    
    log_message(f"開始處理文件夾: {folder_path}", status="開始")
    
    # 3. 收集要处理的项
    items_to_process = collect_items(folder_path, recursive)
    
    # 4. 处理每个项
    for item_type, root, itemname, old_path in items_to_process:
        process_item(item_type, root, itemname, old_path, file_pattern, folder_pattern)


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 使用示例
    target_folder = './workbench'
    batch_rename_files_and_folders(target_folder, recursive=True)
    
    # 也可以这样使用：
    # batch_rename_files_and_folders('/path/to/your/folder', recursive=False)
