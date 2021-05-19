# encoding=utf-8
"""
Editor : Yusang Jeon

라이엇 API를 활용한 천상계 데이터 수집
같은 디렉토리에 lol_api_key.txt가 있어야함.


"""

import pandas as pd
import requests
import urllib
import os

url_base = 'https://kr.api.riotgames.com'

def get_api_key():
    """
    api key : 2021-05-17
    """
    dir = os.path.dirname(__file__)
    path_key = os.path.join(dir, 'lol_api_key.txt')

    f = open(path_key, 'r')
    # f = open("lol_api_key.txt", 'r')
    api_key = f.readline()
    f.close()

    return api_key

def make_url_league(league, api_key, tier=0):
    """
    솔랭 리그별 플레이어 리스트 불러오는 url 만들기
    """

    league_list = ['challenger', 'grandmaster', 'master', 'diamond', 'platinum']
    tier_list = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}
    query = {}

    if league in league_list:
        if league == 'challenger':
            print("챌린저 리그를 불러옵니다...")
            url_league = '/challengerleagues/by-queue/RANKED_SOLO_5x5'
        elif league == 'grandmaster':
            print("그랜드마스터 리그를 불러옵니다...")
            url_league = '/grandmasterleagues/by-queue/RANKED_SOLO_5x5'
        elif league == 'master':
            print("마스터 리그를 불러옵니다...")
            url_league = '/masterleagues/by-queue/RANKED_SOLO_5x5'
        else:
            print("플레 or 다이아 리그를 불러옵니다...")
            url_league = f'/entries/RANKED_SOLO_5x5/{league.upper()}/{tier_list[tier]}'
            query['page'] = 1   # 일단 1페이지만 포함
    else:
        raise ValueError

    query['api_key'] = api_key
    option = urllib.parse.urlencode(query)

    # 리그별 소환사 목록 불러오기
    url = url_base + '/lol/league/v4' + url_league + f'?{option}'

    return url

def make_url_summoner(id, api_key):

    query = {}
    query['api_key'] = api_key
    option = urllib.parse.urlencode(query)

    url = url_base + f'/lol/summoner/v4/summoners/{id}' + f'?{option}'

    return url

def make_url_matches():
    pass


# request
def get_league_df(url):

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Response code is not 200")

    temp = response.text
    temp = temp.replace('true', 'True')
    temp = temp.replace('false', 'False')

    data_dict = eval(temp)

    df = pd.DataFrame(data_dict['entries'])
    # print(df.columns)
    # print(df['veteran'].head())

    return df

def get_summoner_df(url):

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Response code is not 200")

    data_dict = eval(response.text)
    df = pd.DataFrame([data_dict])

    # column 순서 변경
    col1 = ["name"]
    col2 = df.columns.to_list()
    col2.remove("name")
    df = df[col1 + col2]

    print(df.columns)

    return df

def get_grandmaster_df():
    api_key = get_api_key()
    url_league = make_url_league(league='grandmaster', api_key=api_key)
    df_league = get_league_df(url_league)

    df = df_league[['summonerName', 'leaguePoints']]
    df = df.sort_values('leaguePoints', ascending=False)
    df = df.reset_index(drop=True)

    return df

def get_challenger_df():
    api_key = get_api_key()
    url_league = make_url_league(league='challenger', api_key=api_key)
    df_league = get_league_df(url_league)

    df = df_league[['summonerName', 'leaguePoints']]
    df = df.sort_values('leaguePoints', ascending=False)
    df = df.reset_index(drop=True)

    return df


# ----------------------------

if __name__ == '__main__':

    # df = get_grandmaster_df()
    df = get_challenger_df()

    # df.to_csv('challenger_list.csv')

    df = get_grandmaster_df()
    df.to_csv('grandmaster_list.csv')


    # print(df.loc[0])
    #
    # df_summoners = pd.DataFrame()
    # for summoner_id in df_league['summonerId']:
    #     url_summoner = make_url_summoner(id=summoner_id, api_key=api_key)
    #     temp_df = get_summoner_df(url_summoner)
    #
    #     # df_summoners.loc[len(df_summoners)] = temp_df     # wrong code
    #     df_summoners = pd.concat([df_summoners, temp_df])
    #
    # print(df_summoners)

