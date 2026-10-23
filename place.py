"""카카오 로컬 API로 장소 검색 (미션 ①)

사용: python place.py  → 검색어를 입력하면 장소 5개를 보여 줘요.
다른 파일에서: from place import search_place
"""
import os

import requests
from dotenv import load_dotenv

# 🔌 API 주소는 여기 한 곳에만
API = {
    "keyword": "https://dapi.kakao.com/v2/local/search/keyword.json",
}

# 한국 밖 좌표는 잘못된 값으로 보고 버린다 (뒤바뀐 좌표·0 좌표 걸러내기)
LAT_RANGE = (33, 39)
LON_RANGE = (124, 132)


class PlaceError(Exception):
    """화면에 그대로 보여 줄 수 있는 한국어 한 줄 에러. (키·주소·헤더는 담지 않는다)"""


def search_place(검색어, size=5):
    """키워드로 장소를 찾아 [{"이름", "주소", "위도", "경도"}, ...] 로 돌려준다.

    결과가 없으면 빈 목록 []. 키·설정·연결 문제는 PlaceError(⛔로 시작).
    """
    load_dotenv(override=True)
    key = os.getenv("KAKAO_REST_API_KEY")  # REST 키는 os.getenv 로만 읽는다
    if not key:
        raise PlaceError("⛔ .env 에 KAKAO_REST_API_KEY 가 없어요")

    try:
        res = requests.get(  # 🔌 API 호출
            API["keyword"],
            headers={"Authorization": f"KakaoAK {key}"},
            params={"query": 검색어, "size": size},
            timeout=10,
        )
    except requests.RequestException:
        raise PlaceError("⛔ 카카오에 연결하지 못했어요. 인터넷을 확인해 주세요") from None

    if res.status_code == 401:
        raise PlaceError("⛔ 카카오 REST API 키가 틀렸어요")
    if res.status_code == 403:
        raise PlaceError("⛔ 카카오맵 사용 설정을 켜 주세요")
    if res.status_code != 200:
        raise PlaceError(f"⛔ 카카오 응답이 이상해요 (상태 {res.status_code})")

    장소들 = []
    for doc in res.json().get("documents", []):
        # x = 경도, y = 위도, 그리고 글자로 온다 → float()
        경도 = float(doc["x"])
        위도 = float(doc["y"])
        if not (LAT_RANGE[0] <= 위도 <= LAT_RANGE[1] and LON_RANGE[0] <= 경도 <= LON_RANGE[1]):
            continue
        # 도로명 주소는 비어 있을 수 있다 → 없으면 지번 주소
        주소 = doc.get("road_address_name") or doc.get("address_name", "")
        장소들.append({"이름": doc["place_name"], "주소": 주소, "위도": 위도, "경도": 경도})
    return 장소들


if __name__ == "__main__":
    검색어 = input("검색어 (예: 성수동 카페): ").strip()
    try:
        결과 = search_place(검색어)
    except PlaceError as e:
        print(e)
    else:
        if not 결과:
            print(f"'{검색어}'을(를) 찾지 못했어요")
        for i, p in enumerate(결과, 1):
            print(f"{i}. {p['이름']} · {p['주소']} · ({p['위도']}, {p['경도']})")
    print("출처: 카카오 로컬 API")
