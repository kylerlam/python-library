# datetime: YYYYMMDDHHMMSS
# 正則表達式解釋：
# ^(\d{14}) : 匹配開頭的 14 位數字並捕獲到第 1 組
# .* : 匹配之後直到副檔名前的所有內容
# (\.[a-zA-Z0-9]+)$ : 匹配並捕獲副檔名
datetime_fourteen = r'^(\d{14}).*(\.[a-zA-Z0-9]+)$'
