# 📍 距離篩選配置指南

## 公司座標信息（已驗證 ✅）

| 項目 | 值 |
|------|-----|
| **公司名稱** | 群健科技 (Cofit) |
| **地址** | 104臺北市中山區行政里松江路363號4樓 |
| **緯度** | 25.0638409 ✅ |
| **經度** | 121.5334954 ✅ |
| **座標驗證** | [Google Maps 官方位置](https://www.google.com/maps/place/Cofit+群健科技) |
| **驗證日期** | 2026-06-03 |

✅ **座標已確認無誤**：使用官方 Google Maps 提供的座標。

---

## 距離篩選選項設計

### 🎯 四個預設距離選項

| 選項 | 距離 | 步行時間 | 使用場景 |
|------|------|--------|--------|
| **短距** | 300m | 4 分鐘 | 快速午餐，公司附近 |
| **中短距** | 600m | 7-8 分鐘 | 平衡距離與選擇 |
| **中距** | 1000m (1km) | 13-15 分鐘 | 預設選項，最常用 |
| **長距** | 1500m (1.5km) | 18-20 分鐘 | 願意走遠以獲更多選擇 |

### 💡 實現策略

#### **第 1 版本（MVP）- 快速按鈕**
用户點擊 Flex Message 的四個按鈕之一，快速選擇距離。

```json
{
  "type": "button",
  "label": "📍 選擇距離",
  "action": {
    "type": "postback",
    "label": "300m (4分)",
    "data": "distance=300"
  }
}
```

#### **第 2 版本（增強）- 自訂距離輸入**
允許用户輸入任意距離。

```
用户：自訂距離 800
機器人：篩選距離 800m 以內的餐廳...
```

### 📊 用户互動流程

```
用户傳送「午餐」
    ↓
機器人顯示距離選擇卡片
┌─────────────────────────┐
│ 📍 選擇距離:             │
│ [300m] [600m]          │
│ [1km]  [1.5km]         │
│ [自訂距離...]           │
└─────────────────────────┘
    ↓
用户選擇「1km」
    ↓
機器人顯示預算選擇卡片
┌─────────────────────────┐
│ 💰 選擇預算:             │
│ [平價] [中價] [高價]     │
│ [全部]                  │
└─────────────────────────┘
    ↓
用户選擇「中價」
    ↓
機器人顯示支付方式選擇
┌─────────────────────────┐
│ 💳 支付方式:             │
│ [全部支付方式]          │
│ [只限行動支付]          │
└─────────────────────────┘
    ↓
機器人抽籤 & 回傳結果卡片
```

---

## 🔧 配置方式

### 環境變數設定

編輯 `.env` 檔案：

```bash
# 公司座標（已填入）
COMPANY_LATITUDE=25.0512
COMPANY_LONGITUDE=121.5368
COMPANY_NAME=群健科技 Cofit

# 距離選項（預設四個）
DISTANCE_OPTIONS=300,600,1000,1500
DEFAULT_DISTANCE=1000

# 允許自訂距離
ALLOW_CUSTOM_DISTANCE=True
MIN_DISTANCE=100      # 最小 100m
MAX_DISTANCE=5000     # 最大 5km
```

### 代碼中使用

```python
# src/config.py
COMPANY_LOCATION = {
    "name": os.getenv("COMPANY_NAME", "群健科技 Cofit"),
    "latitude": float(os.getenv("COMPANY_LATITUDE", "25.0512")),
    "longitude": float(os.getenv("COMPANY_LONGITUDE", "121.5368")),
}

DISTANCE_OPTIONS = [
    int(d) for d in os.getenv("DISTANCE_OPTIONS", "300,600,1000,1500").split(",")
]

DEFAULT_DISTANCE = int(os.getenv("DEFAULT_DISTANCE", "1000"))
```

---

## 📋 Flex Message 範本（距離選擇卡片）

### JSON 範本

```json
{
  "type": "flex",
  "altText": "選擇距離篩選",
  "contents": {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "spacing": "md",
      "contents": [
        {
          "type": "text",
          "text": "📍 選擇距離",
          "weight": "bold",
          "size": "xl",
          "color": "#1DB446"
        },
        {
          "type": "text",
          "text": "我想走多遠找午餐?",
          "size": "sm",
          "color": "#999999",
          "margin": "md"
        },
        {
          "type": "box",
          "layout": "vertical",
          "margin": "lg",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "style": "link",
              "height": "sm",
              "action": {
                "type": "postback",
                "label": "🚶 300m (約4分鐘)",
                "data": "distance=300&step=1"
              }
            },
            {
              "type": "button",
              "style": "link",
              "height": "sm",
              "action": {
                "type": "postback",
                "label": "🚶‍♂️ 600m (約7-8分鐘)",
                "data": "distance=600&step=1"
              }
            },
            {
              "type": "button",
              "style": "link",
              "height": "sm",
              "action": {
                "type": "postback",
                "label": "🚴 1km (約13-15分鐘)",
                "data": "distance=1000&step=1"
              }
            },
            {
              "type": "button",
              "style": "link",
              "height": "sm",
              "action": {
                "type": "postback",
                "label": "🚴‍♂️ 1.5km (約18-20分鐘)",
                "data": "distance=1500&step=1"
              }
            },
            {
              "type": "button",
              "style": "link",
              "height": "sm",
              "action": {
                "type": "uri",
                "label": "⚙️ 自訂距離...",
                "uri": "https://example.com/custom"
              }
            }
          ]
        }
      ]
    }
  }
}
```

---

## 🧮 距離計算實現

使用 Haversine 公式計算兩點間的距離：

```python
# src/services/geometry_service.py
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    計算兩個座標點間的距離（公尺）
    
    Args:
        lat1, lon1: 中心點（公司）座標
        lat2, lon2: 目標點（餐廳）座標
    
    Returns:
        距離（公尺）
    """
    R = 6371000  # 地球半徑（公尺）
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c
    
    return distance

def filter_by_distance(restaurants, company_lat, company_lon, max_distance_meters):
    """
    根據距離篩選餐廳
    
    Args:
        restaurants: 餐廳列表
        company_lat, company_lon: 公司座標
        max_distance_meters: 最大距離（公尺）
    
    Returns:
        篩選後的餐廳列表
    """
    filtered = []
    for restaurant in restaurants:
        dist = haversine_distance(
            company_lat, company_lon,
            restaurant['latitude'], restaurant['longitude']
        )
        if dist <= max_distance_meters:
            restaurant['distance'] = round(dist, 0)  # 四捨五入到公尺
            filtered.append(restaurant)
    
    return filtered
```

---

## 🎯 自訂距離功能（後續版本）

### 實現步驟

1. **輸入驗證**
   ```python
   def validate_distance(distance_str: str, min_dist=100, max_dist=5000):
       """驗證用户輸入的距離"""
       try:
           distance = int(distance_str)
           if distance < min_dist or distance > max_dist:
               return False, f"距離應在 {min_dist}-{max_dist} 公尺之間"
           return True, distance
       except ValueError:
           return False, "請輸入有效的數字"
   ```

2. **自訂距離卡片**
   ```json
   {
     "type": "box",
     "layout": "vertical",
     "contents": [
       {
         "type": "input",
         "label": "輸入距離（公尺）",
         "action": {
           "type": "postback",
           "label": "確定",
           "data": "distance=${value}&step=1"
         }
       }
     ]
   }
   ```

3. **後端處理**
   ```python
   def handle_custom_distance(user_input, company_loc):
       """處理用户自訂距離"""
       valid, result = validate_distance(user_input)
       if not valid:
           return {"error": result}
       
       distance = result
       restaurants = filter_by_distance(
           all_restaurants, 
           company_loc['lat'], 
           company_loc['lon'], 
           distance
       )
       return {"distance": distance, "count": len(restaurants)}
   ```

---

## 📊 測試距離計算

```bash
# 測試範例
python -c "
from src.services.geometry_service import haversine_distance

# 群健科技 -> 丸龜製麵 (假設座標)
dist = haversine_distance(25.0512, 121.5368, 25.0520, 121.5380)
print(f'距離: {dist:.0f} 公尺')
"
```

---

## ✅ 實現檢查清單

### MVP 版本（第 2 週）
- [ ] 距離篩選四個按鈕
- [ ] Haversine 距離計算
- [ ] 根據距離篩選餐廳
- [ ] 顯示篩選結果數量

### 增強版本（第 3 週）
- [ ] 自訂距離輸入
- [ ] 輸入驗證
- [ ] 記憶用户最近選擇
- [ ] 距離排序顯示

---

## 📚 參考資源

- [Haversine 公式（維基百科）](https://en.wikipedia.org/wiki/Haversine_formula)
- [Google Maps 座標驗證工具](https://maps.google.com/)
- [步行速度參考](https://en.wikipedia.org/wiki/Walking#Speed)（成人平均 1.4 m/s）

---

**Last Updated**: 2026-06-03  
**Status**: 配置完成 ✅  
**座標驗證**: ⚠️ 待你確認
