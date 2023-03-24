import ephem

# 設置28星宿的界限
boundaries = {
    '角': 49,
    '亢': 73,
    '氐': 107,
    '房': 131,
    '心': 163,
    '尾': 193,
    '箕': 223,
    '斗': 259,
    '牛': 297,
    '女': 333,
    '虚': 359,
    '危': 25,
    '室': 49,
    '壁': 79,
    '奎': 107,
    '婁': 131,
    '胃': 157,
    '昴': 193,
    '畢': 223,
    '觜': 259,
    '参': 295,
    '井': 333,
    '鬼': 359,
    '柳': 25,
    '星': 49,
    '弧': 79,
    '轸': 107
}

# 設置28星宿的星體名稱和位置
names = [
    '角一',
    '角二',
    '亢一',
    '亢二',
    '氐一',
    '氐二',
    '房一',
    '房二',
    '心一',
    '心二',
    '尾一',
    '尾二',
    '箕',
    '斗一',
    '斗二',
    '牛一',
    '牛二',
    '女一',
    '女二',
    '虚一',
    '虚二',
    '危一',
    '危二',
    '室一',
    '室二',
    '壁一',
    '壁二',
    '奎一',
    '奎二',
    '婁一',
    '婁二',
    '胃一',
    '胃二',
    '昴',
    '畢一',
    '畢二',
    '觜一',
    '觜二',
    '参一',
    '参二',
    '井一',
    '井二',
    '鬼一',
    '鬼二',
    '柳一',
    '柳二',
    '星一',
    '星二',
    '弧一',
    '弧二',
    '轸一',
    '轸二'
]

stars = {}  # 用於存儲星體的字典
for name in names:
    stars[name] = ephem.FixedBody()

# 設置日期和地點
date = '2023/3/23 12:00:00'
lon = '121.5654'  # 經度
lat = '25.0330'  # 緯度
alt = 0  # 高度，以度為單位

# 設置觀測者的地理位置和時間
obs = ephem.Observer()
obs.lon = lon
obs.lat = lat
obs.date = date
obs.elevation = alt

# 計算28星宿的星體
for name in names:
    ra, dec = ephem.constellation((ephem.hours('0:00:00'), ephem.degrees(str(boundaries[name]) + ':00:00')))
    stars[name]._ra = ra
    stars[name]._dec = dec
    stars[name].compute(obs)

# 計算星體之間的距離
for name1 in names:
    for name2 in names:
        if name1 == name2:
            continue
        sep = ephem.separation(stars[name1], stars[name2])
        print(name1 + '和' + name2 + '的距離: ' + str(sep))

