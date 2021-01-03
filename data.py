#*******************************
# made by DuckBill
#*******************************
################################ import libaray ################################
import pandas as pd
import numpy as np
import copy


################################ read_csv ################################
dia_df = pd.read_csv('diamonds.csv')


################################ 기능 구현 ################################
# 1. 보유 데이터의 % (%표현 필요함)
def dia():
    new_df = copy.deepcopy(dia_df)
    new_df['carat'] = np.where(new_df['carat'] < 0.2, 0.2, new_df['carat'])
    new_df['carat'] = np.where((new_df['carat'] < 0.41) & (new_df['carat'] > 0.2), 0.41, new_df['carat'])
    new_df['carat'] = np.where((new_df['carat'] < 0.71) & (new_df['carat'] > 0.41), 0.71, new_df['carat'])
    new_df['carat'] = np.where(new_df['carat'] > 0.71, 1.05, new_df['carat'])
    return new_df.to_json()

# 2. 캐럿당 가격 평균
def price_per_carat(num1, num2):
    x = dia_df[(num1 < dia_df['carat']) & (num2 > dia_df['carat'])][['carat', 'price']]
    y = dia_df[(num1 < dia_df['carat']) & (num2 > dia_df['carat'])].groupby('carat').mean()['price']
    return [x, y]

# 3. 원하는 가격대로 구입 가능한 조합(캐럿 + 색 + 컷 + 투명도) 캐럿 기준
def price_combination(num1, num2):
    new_frame = dia_df[(dia_df['price'] > num1) & (dia_df['price'] < num2)]
    return new_frame[['carat', 'cut', 'color', 'clarity', 'price']].groupby(['cut', 'color', 'clarity']).filter(lambda g: (g.nunique() > 1).any())


# 4. 보유한 다이아의 예상 가격
def price_predict(option_dic):
    carat = float(option_dic['carat'])
    cut = option_dic['cut']
    color = option_dic['color']
    clarity = option_dic['clarity']

    share_percent={
        'carat' :106,
        'color' :32,
        'cut' :9,
        'clarity' :1
    }

    tot = 0
    # 이 캐럿의 평균 가격
    if carat != 0.0:
        cnt = 0
        for _ in range(10):
            a = dia_df[dia_df['carat'] == carat + cnt]['price']
            b = dia_df[dia_df['carat'] == carat - cnt]['price']
            if not a.empty:
                _carat = a.mean()
                tot += 72
                break
            elif not b.empty:
                _carat = b.mean()
                tot += 72
                break
            else:
                cnt += 0.01
        else:
            _carat = 0
    else:
        _carat = 0
    # 이 컷의 평균 가격
    if cut != 'NONE':
        a = dia_df[dia_df['cut'] == cut]
        if not a.empty:
            _cut = a['price'].mean()
            tot += 21
        else:
            _cut = 0
    else:
        _cut = 0
    # 이 컬러의 평균 가격
    if color != 'NONE':
        a = dia_df[dia_df['color'] == color]
        if not a.empty:
            _color = a['price'].mean()
            tot += 6
        else:
            _color = 0
    else:
        _color = 0
    # 이 투명도의 평균 가격
    if clarity != 'NONE':
        a = dia_df[dia_df['clarity'] == clarity]
        if not a.empty:
            _clarity = a['price'].mean()
            tot += 1
        else:
            _clarity = 0
    else:
        _clarity = 0

    if tot == 0:
        return "원하시는 데이터를 찾을 수 없습니다."

    _sum = _carat * (72 / tot) + _cut * (21 / tot) + _color * (6 / tot) + _clarity * (1 / tot)
    # 다 더해서 평균!
    return "예상 판매 금액은 {}달러 입니다!".format(_sum)

# 5. 가격 결정 기준
def standard_set_price():
    # cut
    cut_dict = {
        'Ideal': 1,
        'Premium': 0.75,
        'Very Good': 0.5,
        'Good': 0.25,
        'Fair': 0
    }
    # color
    color_dict = {
        'J': 1,
        'I': 0.8333333333333333,
        'H': 0.6666666666666667,
        'G': 0.5,
        'F': 0.3333333333333333,
        'E': 0.1666666666666667,
        'D': 0
    }
    # clarity
    clarity_dict = {
        'IF': 1,
        'VVS1': 0.8571428571428574,
        'VVS2': 0.7142857142857145,
        'VS1': 0.5714285714285716,
        'VS2': 0.4285714285714287,
        'SI1': 0.2857142857142857,
        'SI2': 0.1428571428571429,
        'I1': 0
    }
    # carat -> color -> cut -> clarity 순서
    new_df = dia_df.replace({'cut': cut_dict,
                            'color': color_dict,
                            'clarity': clarity_dict})
    rank = new_df[['price', 'carat', 'cut', 'color', 'clarity']].corr()['price']
    
    return rank.sort_values(ascending = False).keys().tolist()