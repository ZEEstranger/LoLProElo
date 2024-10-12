"""
Модуль для функций
"""

import pandas as pd

def elo_calculation(start_elo_1, start_elo_2, k_factor, side_win):

    # Общие параметры
    diff_rait_1 = start_elo_2 - start_elo_1
    diff_rait_2 = start_elo_1 - start_elo_2
    w_expected_1 = round(1 / (pow(10, diff_rait_1 / 600) + 1), 2)
    w_expected_2 = round(1 / (pow(10, diff_rait_2 / 600) + 1), 2)

    if side_win == 1:
        w_real_1, w_real_2 = 1, 0
    elif side_win == 2:
        w_real_1, w_real_2 = 0, 1
    else:
        raise KeyError

    p_after_1 = round(start_elo_1 + k_factor * (w_real_1 - w_expected_1))
    p_after_2 = round(start_elo_2 + k_factor * (w_real_2 - w_expected_2))

    return p_after_1, p_after_2

def insert_game():
    team_1_name = input("insert blue team name\n")
    team_1_elo = int(input("insert blue team elo\n"))
    team_2_name = input("insert red team name\n")
    team_2_elo = int(input("insert red team elo\n"))
    win_side = int(input("input 0 if blue side win else input 1\n"))
    k_factor = int(input("input k-factor\n"))

    team_1_elo, team_2_elo = elo_calculation(team_1_elo, team_2_elo, k_factor, win_side)

    print(team_1_name, team_1_elo)
    print(team_2_name, team_2_elo)

def excel_import(file_name:str, sheet_name_custom=None) -> list:
    
    if sheet_name_custom:
        df = pd.read_excel(file_name, sheet_name=sheet_name_custom)
    else:
        df = pd.read_excel(file_name)
    print(df)

    blue_teams = df.values.tolist()

    return blue_teams

def team_dict_build(team_rating_list:list) -> dict:
    
    team_dict = {
        team[0]: {
            "region": team[1],
            "elo": int(team[2])
        } 
        for team in team_rating_list
    }

    return team_dict

def df_to_excel(file_name, df:pd.DataFrame):
    
    df.to_excel(file_name)

if __name__ == '__main__':

    # Словарь команд
    team_dict = team_dict_build(excel_import('team_rating.xlsx', 'Team Active Elo 2010'))

    print(team_dict)

    match_history = excel_import('LoL_Event_Cycle_2010.xlsx', 'ESL Major Series 7')

    for match in match_history:
        for game in str(match[2]):
            new_elo_team_1, new_elo_team_2 = elo_calculation(
                team_dict.get(match[0])["elo"],
                team_dict.get(match[1])["elo"],
                int(match[3]),
                int(game)
            )

            team_dict[match[0]]["elo"] = new_elo_team_1
            team_dict[match[1]]["elo"] = new_elo_team_2

    s = pd.DataFrame.from_dict(team_dict).T

    print(s)
    s.to_excel("output.xlsx", index=True, index_label="Team Name")

    # for team in team_dict:
        # print(team_dict[team])
