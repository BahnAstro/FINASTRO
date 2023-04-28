import pandas as pd
from collections import defaultdict

# 讀取CSV文件
df = pd.read_csv("/Users/x/PLANET_ALLDATA_PERFECT_WUXING_Y2006to2023.csv")

# 預先定義的角度
angles = [0, 30, 45, 60, 90, 120, 144, 150, 180, 240, 270, 300, 330]

moon_phases_angles = [0, 45, 90, 135, 180, -135, -90, -45]

moon_phase_tolerance = 3

# 需要比較的列名
numerical_columns_to_compare = ['Year_Degree', 'Life_degree', 'Sun_ELONG', 'Moon_ELONG', 'Mercury_ELONG', 'Venus_ELONG', 'Mars_ELONG', 'Saturn_ELONG',
                                'Jupiter_ELONG', 'Uranus_ELONG', 'Pluto_ELONG', 'Neptune_ELONG', 'Lilith_ELONG', 'Selena_ELONG',
                                'Moon_South_Node_ELONG', 'Moon_North_Node_ELONG', 'ASC', 'MC', 'Part_of_Fortune']


# 添加餘奴所需的列
string_columns_to_compare = ['旺', 'Mars_ELONG_Mansion_positions', 'Mars_ELONG_Zodiac_signs', 'Saturn_ELONG_Mansion_positions', 'Saturn_ELONG_Zodiac_signs', 
                             'Mercury_ELONG_Mansion_positions', 'Mercury_ELONG_Zodiac_signs', 'Jupiter_ELONG_Mansion_positions', 'Jupiter_ELONG_Zodiac_signs', 
                             'Moon_South_Node_ELONG_Mansion_positions', 'Moon_South_Node_ELONG_Zodiac_signs', 'Moon_North_Node_ELONG_Mansion_positions',
                             'Moon_North_Node_ELONG_Zodiac_signs', 'Lilith_ELONG_Mansion_positions', 'Lilith_ELONG_Zodiac_signs',
                             'Selena_ELONG_Mansion_positions', 'Selena_ELONG_Zodiac_signs']



# 儲存結果的字典
results = defaultdict(lambda: defaultdict(str))

# 允許的角度誤差
tolerance = 2


# 遍歷所有行
for i, current_row in df.iterrows():
    if i == 0:  # 第1行為birth chart
        birth_chart = current_row

    if i >= 0:
        # Calculate Moon Phase
        moon_sun_aspect_difference = current_row['Moon_ELONG'] - current_row['Sun_ELONG']
        moon_phase = None

        if -moon_phase_tolerance <= moon_sun_aspect_difference <= moon_phase_tolerance:
            moon_phase = "NewMoon_朔月"
        elif 45 - moon_phase_tolerance <= moon_sun_aspect_difference <= 45 + moon_phase_tolerance:
            moon_phase = "WaxingCrescent_眉月"
        elif 90 - moon_phase_tolerance <= moon_sun_aspect_difference <= 90 + moon_phase_tolerance:
            moon_phase = "FirstQuarter_上弦月"
        elif 135 - moon_phase_tolerance <= moon_sun_aspect_difference <= 135 + moon_phase_tolerance:
            moon_phase = "WaxingGibbous_上凸月"
        elif 180 - moon_phase_tolerance <= moon_sun_aspect_difference <= 180 + moon_phase_tolerance:
            moon_phase = "FullMoon_望月"
        elif -180 + moon_phase_tolerance <= moon_sun_aspect_difference <= -180 - moon_phase_tolerance:
            moon_phase = "WaningGibbous_下凸月"
        elif -90 + moon_phase_tolerance <= moon_sun_aspect_difference <= -90 - moon_phase_tolerance:
            moon_phase = "LastQuarter_下弦月"
        elif -45 + moon_phase_tolerance <= moon_sun_aspect_difference <= -45 - moon_phase_tolerance:
            moon_phase = "WaningCrescent_殘月"

        if moon_phase:
            results[current_row['Time']]["Moon_Phase"] = moon_phase
        else:
            results[current_row['Time']]["Moon_Phase"] = "NA"
    
    if i >= 0: 
        for birth_col in numerical_columns_to_compare:
            for current_col in numerical_columns_to_compare:
                # Compare birth_col with current_col for birth chart and current row
                for angle in angles:
                    difference = abs(birth_chart[birth_col] - current_row[current_col]) % 360

                    # 檢查角度差是否在允許的誤差範圍內
                    if angle - tolerance <= difference <= angle + tolerance:
                 
                        suffix = "minus" if difference < angle else "plus"
                        key = f"Birth_{birth_col}_vs_Current_{current_col}_{angle}_{suffix}_{abs(angle - difference)}"
                        results[current_row['Time']][f"{birth_col}_vs_{current_col}_aspects"] += key + "; "

                # Compare all elements in current row
                for current_col_1 in numerical_columns_to_compare:
                    if current_col != current_col_1:
                        for angle in angles:
                            difference = abs(current_row[current_col] - current_row[current_col_1]) % 360

                            # 檢查角度差是否在允許的誤差範圍內
                            if angle - tolerance <= difference <= angle + tolerance:
                     
                                suffix = "minus" if difference < angle else "plus"
                                key = f"Current_{current_col}_vs_Current_{current_col_1}_{angle}_{suffix}_{abs(angle - difference)}"
                                results[current_row['Time']][f"{current_col}_vs_{current_col_1}_aspects"] += key + "; "
        
        # Compare all elements in current row
        for idx1, current_col_1 in enumerate(numerical_columns_to_compare):
            for idx2, current_col_2 in enumerate(numerical_columns_to_compare):
                if idx1 < idx2:  # 只比较一次
                    for angle in angles:
                        difference = abs(current_row[current_col_1] - current_row[current_col_2]) % 360

                        # 检查角度差是否在允许的误差范围内
                        if angle - tolerance <= difference <= angle + tolerance:

                            suffix = "minus" if difference < angle else "plus"
                            key = f"Current_{current_col_1}_vs_Current_{current_col_2}_{angle}_{suffix}_{abs(angle - difference)}"
                            results[current_row['Time']][f"{current_col_1}_vs_{current_col_2}_aspects"] += key + "; "

        # 餘奴方法
        for birth_col, current_col, element, yunu_guard, yunu_offend in [('Lilith_ELONG', 'Mercury_ELONG', 'Water', "餘奴護主", "餘奴犯主"),
                                                                        ('Moon_North_Node_ELONG', 'Saturn_ELONG', 'Earth', "餘奴護主", "餘奴犯主"),
                                                                        ('Moon_South_Node_ELONG', 'Mars_ELONG', 'Fire', "餘奴護主", "餘奴犯主"),
                                                                        ('Selena_ELONG', 'Jupiter_ELONG', 'Wood', "餘奴護主", "餘奴犯主")]:

            if birth_col in numerical_columns_to_compare and current_col in numerical_columns_to_compare:
                yunu_results = []
                yunu_elements = []
                yunu_conditions = []

                for angle in angles:
                    # Birth chart difference
                    birth_difference = abs(birth_chart[birth_col] - current_row[current_col]) % 360
                    # Current chart difference
                    current_difference = abs(current_row[birth_col] - current_row[current_col]) % 360

                    #本命vs流年=  birth_difference, 'birth'； 流年vs流年 = current_difference, 'current'
                    for difference, chart_type in [(birth_difference, 'birth'), (current_difference, 'current')]:
                        if angle - tolerance <= difference <= angle + tolerance:
                            if current_row['旺'] == element:
                                yunu_result = yunu_guard
                            else:
                                yunu_result = yunu_offend

                            yunu_elements.append(element)
                            yunu_conditions.append(f"{chart_type}_{birth_col}_vs_{current_col}_aspects")
                            yunu_results.append(yunu_result)

                # Check Mansion_positions
                mansion_positions_conditions = [(birth_chart[f'{birth_col}_Mansion_positions'], current_row[f'{current_col}_Mansion_positions']),
                                                (birth_chart[f'{current_col}_Mansion_positions'], current_row[f'{birth_col}_Mansion_positions']),
                                                (current_row[f'{birth_col}_Mansion_positions'], current_row[f'{current_col}_Mansion_positions'])]

                for b_mansion, c_mansion in mansion_positions_conditions:
                    if b_mansion == c_mansion:
                        if current_row['旺'] == element:
                            yunu_result = yunu_guard
                        else:
                            yunu_result = yunu_offend

                        yunu_elements.append(element)
                        yunu_conditions.append(f"{birth_col}_Mansion_positions_vs_{current_col}_Mansion_positions")
                        yunu_results.append(yunu_result)

                # Check Zodiac_signs
                zodiac_signs_conditions = [(birth_chart[f'{birth_col}_Zodiac_signs'], current_row[f'{current_col}_Zodiac_signs']),
                                            (birth_chart[f'{current_col}_Zodiac_signs'], current_row[f'{birth_col}_Zodiac_signs']),
                                            (current_row[f'{birth_col}_Zodiac_signs'], current_row[f'{current_col}_Zodiac_signs'])]

                for b_zodiac, c_zodiac in zodiac_signs_conditions:
                    if b_zodiac == c_zodiac:
                        if current_row['旺'] == element:
                            yunu_result = yunu_guard
                        else:
                            yunu_result = yunu_offend

                        yunu_elements.append(element)
                        yunu_conditions.append(f"{birth_col}_Zodiac_signs_vs_{current_col}_Zodiac_signs")
                        yunu_results.append(yunu_result)

                # Save the results
                if yunu_results:
                    results[current_row['Time']]["Yunu"] = "; ".join(yunu_results)
                    results[current_row['Time']]["Yunu_Element"] = "; ".join(yunu_elements)
                    results[current_row['Time']]["Yunu_Reason"] = "; ".join(yunu_conditions)
                else:
                    if "Yunu" not in results[current_row['Time']]:
                        results[current_row['Time']]["Yunu"] = "NA"
                        results[current_row['Time']]["Yunu_Element"] = "NA"
                        results[current_row['Time']]["Yunu_Reason"] = "NA"


# 將結果轉換為DataFrame並輸出為CSV文件
results_df = pd.DataFrame.from_dict(results, orient='index')
results_df.reset_index(inplace=True)
results_df.rename(columns={'index': 'Time'}, inplace=True)

# 按照 Time 列对结果进行排序
results_df['Time'] = pd.to_datetime(results_df['Time'])
results_df.sort_values(by='Time', inplace=True)

# 保存结果到 CSV 文件
results_df.to_csv('/Users/x/aspects_results_2006to2023_clean.csv', index=False)
