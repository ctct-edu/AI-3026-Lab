import json
from datetime import datetime

def _load_events(file_path: str = "data/events.txt") -> list:
    events = []
    with open(file_path) as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 4:
                month, day = map(int, parts[2].split("-"))
                events.append((
                    parts[0],                          # 名前
                    parts[1],                          # 種類
                    month * 100 + day,                 # ソート可能な月-日の整数
                    parts[2],                          # 月-日の文字列
                    set(parts[3].split(";")),          # 場所のセット
                ))
    events.sort(key=lambda e: e[2])
    return events


def _load_rates(file_path: str) -> dict:
    rates = {}
    with open(file_path) as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                rates[parts[0]] = float(parts[1])
    return rates

EVENTS = _load_events()
TELESCOPE_RATES = _load_rates("data/telescope_rates.txt")
PRIORITY_MULTIPLIERS = _load_rates("data/priority_multipliers.txt")

# 指定された場所で次に見える天文イベントを特定


# 望遠鏡ランク、時間、優先度に基づいて観測時間のコストを計算
def calculate_observation_cost(telescope_tier: str, hours: float, priority: str) -> str:
    """望遠鏡観測時間のコストを計算します。"""
    tier = telescope_tier.lower()
    pri = priority.lower()

    if tier not in TELESCOPE_RATES:
        return json.dumps({"error": f"Unknown telescope tier '{telescope_tier}'. Choose from: {', '.join(TELESCOPE_RATES)}"})

    if pri not in PRIORITY_MULTIPLIERS:
        return json.dumps({"error": f"Unknown priority '{priority}'. Choose from: {', '.join(PRIORITY_MULTIPLIERS)}"})

    if hours <= 0:
        return json.dumps({"error": "Hours must be greater than zero."})

    base_cost = TELESCOPE_RATES[tier] * hours
    multiplier = PRIORITY_MULTIPLIERS[pri]
    total_cost = base_cost * multiplier

    return json.dumps({
        "telescope_tier": tier,
        "hours": hours,
        "hourly_rate": TELESCOPE_RATES[tier],
        "priority": pri,
        "priority_multiplier": multiplier,
        "base_cost": base_cost,
        "total_cost": total_cost
    })

# 天文観測セッションの詳細をまとめた観測レポートを生成
def generate_observation_report(event_name: str, location: str, telescope_tier: str, hours: float, priority: str, observer_name: str) -> str:
    """
    観測セッション レポートを生成してファイルに保存します。

    Returns:
        生成されたレポートのファイル パスを含む JSON 文字列。
    """
    cost_result = json.loads(calculate_observation_cost(telescope_tier, hours, priority))
    event_result = json.loads(next_visible_event(location))

    if "error" in cost_result:
        return json.dumps(cost_result)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"report_{event_name.replace(' ', '_').lower()}_{timestamp.replace(':', '').replace(' ', '_')}.txt"

    report = f"""======================================
  CONTOSO OBSERVATORIES - セッション レポート
======================================
日付:             {timestamp}
観測者:           {observer_name}
イベント:         {event_name}
場所:             {location}

次の観測可能なイベント
  イベント:       {event_result.get('event', 'N/A')}
  日付:           {event_result.get('date', 'N/A')}

望遠鏡予約
  ランク:         {cost_result['telescope_tier']}
  時間:           {cost_result['hours']}
  時間単価:       ${cost_result['hourly_rate']:.2f}
  優先度:         {cost_result['priority']}
  倍率:           {cost_result['priority_multiplier']}x

コスト サマリー
  基本コスト:     ${cost_result['base_cost']:.2f}
  合計コスト:     ${cost_result['total_cost']:.2f}
======================================
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    return json.dumps({"status": "レポートが生成されました", "file": filename})
