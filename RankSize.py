import requests
import time

def get_season_rank(api_key, season_id, matching_team_mode):
    base_url = "https://open-api.bser.io/v1/"
    endpoint = f"{base_url}rank/top/{season_id}/{matching_team_mode}"
    headers = {"x-api-key": api_key}
    try:
        response = requests.get(endpoint, headers=headers)
        time.sleep(1) 
        if response.status_code == 200:
            data = response.json()
            for user in data['topRanks']:
                if user['rank'] == 1:
                    return user['nickname']
        else:
            print(f"에러 응답. 상태 코드: {response.status_code}")
    except Exception as e:
        print(f"오류 발생: {e}")

def get_user_stats(api_key, user_num, season_id):
    base_url = "https://open-api.bser.io/v1/"
    endpoint = f"{base_url}user/stats/{user_num}/{season_id}"
    headers = {"x-api-key": api_key}
    try:
        response = requests.get(endpoint, headers=headers)
        time.sleep(1) 
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"에러 응답. 상태 코드: {response.status_code}")
    except Exception as e:
        print(f"오류 발생: {e}")

def get_season_rank(api_key, season_id, matching_team_mode):
    base_url = "https://open-api.bser.io/v1/"
    endpoint = f"{base_url}rank/top/{season_id}/{matching_team_mode}"
    headers = {"x-api-key": api_key}
    try:
        response = requests.get(endpoint, headers=headers)
        time.sleep(1) 
        if response.status_code == 200:
            data = response.json()
            return [user['userNum'] for user in data['topRanks'] if 1 <= user['rank'] <= 10]
        else:
            print(f"에러 응답. 상태 코드: {response.status_code}")
    except Exception as e:
        print(f"오류 발생: {e}")

def get_season_number(season_id):
    return (season_id + 1) // 2

if __name__ == "__main__":
    api_key = "API_KEY" # 자신의 API 키로 변경
    mode_names = {1: "솔로", 2: "듀오", 3: "스쿼드"}
    max_rank_sizes = {}
    for matching_team_mode in [1, 2, 3]:
        print(f"{mode_names[matching_team_mode]} 모드 진행 중...")
        for season_id in range(1, 22, 2):
            season_number = get_season_number(season_id)
            print(f"시즌 {season_number} 진행 중...")
            rank_sizes = []
            user_nums = get_season_rank(api_key, season_id, matching_team_mode)
            if user_nums is not None:
                for user_num in user_nums:
                    user_stats = get_user_stats(api_key, user_num, season_id)
                    if user_stats is not None:
                        for stats in user_stats['userStats']:
                            if stats['matchingTeamMode'] == matching_team_mode:
                                rank_sizes.append(stats['rankSize'])
            if rank_sizes:
                max_rank_sizes[(mode_names[matching_team_mode], season_number)] = max(rank_sizes)
    print("모든 요청이 완료되었습니다.")
    print("각 모드와 시즌에 대한 rankSize 최대값:")
    for key, value in max_rank_sizes.items():
        print(f"{key}: {value}")