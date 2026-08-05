# 参照の追加


# MCP サーバーを作成


# 在庫確認 MCP ツールを追加

def get_inventory_levels() -> dict:
    """全製品の現在の在庫数を返します。"""
    return {
        "Moisturizer": 6,
        "Shampoo": 8,
        "Body Spray": 28,
        "Hair Gel": 5,
        "Lip Balm": 12,
        "Skin Serum": 9,
        "Cleanser": 30,
        "Conditioner": 3,
        "Setting Powder": 17,
        "Dry Shampoo": 45
    }

# 週間販売数 MCP ツールを追加

def get_weekly_sales() -> dict:
    """先週の販売ユニット数を返します。"""
    return {
        "Moisturizer": 22,
        "Shampoo": 18,
        "Body Spray": 3,
        "Hair Gel": 2,
        "Lip Balm": 14,
        "Skin Serum": 19,
        "Cleanser": 4,
        "Conditioner": 1,
        "Setting Powder": 13,
        "Dry Shampoo": 17
    }

# MCP サーバーを起動
