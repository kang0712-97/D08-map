# 카카오 지도 · 판다스 프로젝트 규칙 (D8)

구조: **검색·좌표 변환은 파이썬(REST 키), 지도 그림은 브라우저(JS 키).**
D7의 키 금고 규칙(키는 `.env`에만, 코드에 직접 쓰지 않음)은 그대로 적용한다.

## 키 규칙
- 장소 검색·주소↔좌표는 파이썬에서 `KAKAO_REST_API_KEY`로만 호출한다. 헤더는 `Authorization: KakaoAK {키}`. 키는 `os.getenv`로만 읽는다.
- REST 키는 `map.html`, Streamlit 화면 등 브라우저로 가는 곳에 절대 넣지 않는다.
- 지도 그림에는 `KAKAO_JS_KEY`(JavaScript 키)만 쓴다. `.env`에서 읽어 HTML을 만들 때 넣는다. 두 키는 서로 다른 값이다.
- 브라우저 쪽 `libraries=services`는 쓰지 않는다. 검색은 파이썬이 한다.
- `.env`를 만들거나 열어 보여 주지 않는다. 새 키 이름은 `.env.example`에만 추가하고 값은 사용자가 직접 넣는다. 대화에 키 값이 나오면 안 된다.
- 요청 주소, 헤더, `response.url`, `res.text`를 출력하지 않는다.

## 좌표 규칙
- 카카오 응답의 `x`는 경도, `y`는 위도이며 문자열이다. `float()`로 바꾸고 변수명은 `위도`·`경도`로 붙인다.
- 지도 SDK는 `new kakao.maps.LatLng(위도, 경도)` 순서. API 요청은 `x=경도, y=위도`.
- 한국 밖 좌표(위도 33~39, 경도 124~132 밖)는 잘못된 값으로 보고 쓰지 않는다.
- `road_address`는 null일 수 있다. 없으면 지번 주소(`address`)를 쓴다.

## 지도 HTML 규칙
- `map.html`은 파이썬이 만든다. 열 때는 `d8-map` 폴더에서 `python -m http.server 8000 --bind 127.0.0.1` 실행 후 `http://localhost:8000/map.html`. file:// 더블클릭을 안내하지 않고, `--bind 127.0.0.1`을 절대 빼지 않는다(빼면 같은 와이파이 사람이 `.env`를 받아 갈 수 있다).
- SDK는 `https://dapi.kakao.com/v2/maps/sdk.js?appkey=JS키&autoload=false` + `kakao.maps.load(...)`.
- 지도 아래에 항상 안내 한 줄을 보여 준다: "지도가 회색이면: ① 카카오맵 사용 설정 ② 지금 주소(포트까지) 등록 ③ 서버 주소로 열기".
- 장소 이름은 `textContent`로, 데이터는 `json.dumps`로 넣는다.
- 마커가 여러 개면 `LatLngBounds`로 전부 보이게 맞춘다. 마커는 최대 200개.
- `map.html`은 `.gitignore`에 넣는다.

## Streamlit 규칙
- 실행은 `streamlit run 파일.py`. 지도 HTML은 `st.iframe(html, height=...)`로 넣고 `st.components.v1.html`은 쓰지 않는다.
- 실행 안내에 "카카오 콘솔 JavaScript SDK 도메인에 `http://localhost:8501` 등록"을 적고, `localhost:8502`·Network URL(IP)·`127.0.0.1`로 열면 지도가 안 뜬다고 알린다.
- `load_dotenv(override=True)`를 쓴다. `.env`를 고치면 `Ctrl+C` 후 다시 `streamlit run` 하라고 안내한다. 에러 결과는 캐시하지 않는다(캐시 함수 안에서는 예외를 내고 밖에서 받는다).
- 날씨 설명 같은 글자는 `st.metric` 변화량 자리에 넣지 않고 `st.caption`을 쓴다.
- `requirements.txt`에 `streamlit>=1.66`.
- API 함수에 `@st.cache_data(ttl=600)`. 표·숫자는 `st.dataframe`, `st.metric`. 에러는 `st.error("한국어 한 줄")`.

## 판다스 규칙
- 동네 필터는 시·도까지 붙인 이름(`"서울특별시 강남구"`)으로 거른다. `"남구"`는 `"강남구"`에도 들어 있다.
- CSV는 `utf-8-sig` → `cp949` 순서로 시도하고, 읽은 인코딩 이름을 출력한다.
- 읽은 뒤 가장 먼저 줄 수·칸 수·빈칸 개수(`shape`, `isna().sum()`)를 보여 준다.
- 숫자 칸은 `pd.to_numeric(..., errors="coerce")`. "무료" 같은 글자는 먼저 0으로 바꾼다.
- 칸 이름은 파일에 실제로 있는 이름만 쓴다. 모르면 `df.columns`를 먼저 출력한다. 새 칸은 사용자가 "새로 만들어"라고 했을 때만 만든다. `데이터기준일자`는 남기고 화면에 기준일을 표시한다.
- 빈 좌표를 카카오로 채울 때는 최대 30줄, 호출마다 `time.sleep(0.1)`. 키·설정·연결 에러(문장이 `⛔`로 시작)가 나면 바로 멈춘다.
- 저장은 `encoding="utf-8-sig"`, `index=False`. 원본 `*_raw.csv`는 `.gitignore`.
- 개수·평균은 코드로 계산하고, 사람이 엑셀 필터로 검산할 수 있게 어떤 조건으로 셌는지 출력한다.

## 공통 규칙 (D7과 같음)
- API 주소는 파일 맨 위 `API = {...}` 한 곳에 두고 `# 🔌` 표시. 요청 줄에는 `# 🔌 API 호출`.
- `requests.get(..., timeout=10)`. 실패는 한국어 한 줄로 안내. 출력 맨 아래에 출처.
- 새 패키지는 `requirements.txt`에 추가하고 설치 명령은 제안만 한다.
- 커밋·푸시는 하지 않고 메시지만 제안한다. 커밋 전에 `git status`를 보여 준다.

## 쓸 수 있는 API
헤더는 모두 `Authorization: KakaoAK {REST API 키}`.

| 용도 | 주소 | 보내는 값 | 주요 칸 |
| --- | --- | --- | --- |
| 키워드 장소 검색 | `https://dapi.kakao.com/v2/local/search/keyword.json` | `query`, (선택) `x`·`y`·`radius`(최대 20000m)·`sort=distance`·`category_group_code`·`size`(최대 15) | `documents[i].place_name`, `road_address_name`, `address_name`, `x`, `y`, `phone`, `category_name`, `place_url`, `distance` |
| 카테고리 장소 검색 (검색어 없이) | `https://dapi.kakao.com/v2/local/search/category.json` | `category_group_code`, `x`, `y`, `radius` | 위와 같음 |
| 주소 → 좌표 | `https://dapi.kakao.com/v2/local/search/address.json` | `query` | `documents[0].x`, `y`, `address_name` |
| 좌표 → 주소 | `https://dapi.kakao.com/v2/local/geo/coord2address.json` | `x`(경도), `y`(위도) | `documents[0].road_address.address_name`(없을 수 있음), `address.address_name` |
| 지도 JavaScript SDK | `https://dapi.kakao.com/v2/maps/sdk.js?appkey=JS키&autoload=false` | (브라우저) | `kakao.maps.Map`, `LatLng(위도, 경도)`, `Marker`, `InfoWindow`, `LatLngBounds` |
| OpenWeather 현재 날씨 | D7 규칙 그대로 | `lat`, `lon`, `appid`, `units=metric`, `lang=kr` | `main.temp`, `weather[0].description` |

카테고리 코드: `CE7` 카페 · `FD6` 음식점 · `CS2` 편의점 · `PM9` 약국 · `HP8` 병원 · `SW8` 지하철역 · `PK6` 주차장 · `MT1` 대형마트 · `BK9` 은행 · `AT4` 관광명소 · `CT1` 문화시설

표에 없는 API는 쓰기 전에 이름·주소·키 필요 여부를 말하고 확인받는다. 구글 지도·네이버 지도 API는 쓰지 않는다.

## 에러 안내
| 상황 | 뜻 | 화면 안내 |
| --- | --- | --- |
| 401 | REST 키가 틀림 (JS 키를 넣은 경우가 많음) | "카카오 REST API 키가 틀렸어요" |
| 403 `disabled OPEN_MAP_AND_LOCAL service` | 카카오맵 사용 설정 OFF | "카카오맵 사용 설정을 켜 주세요" |
| `documents`가 빈 목록 | 그런 장소·주소 없음 | "'○○'을(를) 찾지 못했어요" |
| 지도 자리에 회색 네모 / 아무것도 없음 | JS 키·도메인·사용 설정·file:// 중 하나 | 지도 HTML의 안내 문장 |

## 실수에서 배운 규칙
<!-- AI 실수를 찾을 때마다 한 줄씩: - (10/23) (해라/하지 마라) ___ (왜: ___) -->
