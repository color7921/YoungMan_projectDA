# 프로젝트 소개 및 목적
---
### 소개
전자 및 수기 영수증의 텍스트를 추출해서 DB화 시키는 프로젝트 입니다. <br/><br/>
개발 기간 : `2023.12.25 ~ 2024.01.18`

### Docker 사용법
- docker-compose.yml 파일을 임의의 폴더에 다운
- 도커 실행 -> 임의의 폴더 경로에서 cmd 실행
- http://localhost:3000/ 접속

### Flask 사용법
- venv 가상 환경 설정 후 pip install -r requirements.txt 명령어 입력
- app.py에서 실행

### 개발 목적
**1. 영수증 내 필요 정보를 추출 및 정규화**
- OCR 기술을 사용하여 이미지에서 필요한 정보를 텍스트로 추출
- 영수증 내 필요 정보는 구매 기업, 날짜, 품목, 가격, 단가, 갯수
- 인식률이 높은 전자 기록식 영수증을 우선 인식
- 인식률이 낮은 수기 영수증은 AI 기술을 이용하여 데이터 처리

**2. 다양한 형태의 수기 영수증 처리** 
- 형태가 비교적 일정한 전자 기록식 영수증과 달리 수기 영수증은 형태 예측이 어려움
- 머신러닝, 딥러닝 기술을 사용하여 이미지 내부에서 필요 정보를 추출하거나 텍스트 라벨링 필요

**3. 정제된 데이터의 관리 기능 구현**
- 사용자는 추출된 영수증 정보를 확인할 수 있고 수정 가능
- 과거 기록을 볼 수 있으며 저장된 정보를 엑셀로 변환하여 제공
- 기타 사용자 편의를 제공하는 기능 구현

### 개발 목표
1. 수기 영수증을 DB화 하여 필요한 정보(날짜, 품목, 가격, 수량) 등의 정보를 저장하는것
2. 저장된 정보를 관리하고 엑셀 파일로 변환시켜서 따로 편하게 관리하는 것

### 시연 영상
### [▶영상 보러가기](https://youtu.be/aQxviNjqf3I)

# 목차
---
* [팀소개](#팀소개)
* [개발 일지](#개발-일지)
* [사용 기술](#사용-기술)
* [프로젝트 개념도](#프로젝트-개념도)
* [엉수증 변환결과](#영수증-변환-결과)

# 팀소개
---
|담당|이름|github|
|------|---|---|
|FE|남지수|https://github.com/JisooOvO/containership|
|BE|김윤성|https://github.com/ORENOL/YoungmanProject_backend|
|DA|강희진|https://github.com/color7921/YoungMan_projectDA|

# 개발 일지
---
 
### <1주차>
- AI 허브 사이트에서 데이터 수집 (OCR 딥러닝을 위한 수필 데이터 수집)
- 데이터 모델링 검색 (OCR 검색)
- 컬럼 6개 정도로 임의로 만들고 이미지 전처리 방법 찾기 (opencv line)
- 원하는 컬럼만 추출해서 JSON 객체로 바꾸는 방법 찾기
- Flask 이용법 찾아보기

### <2주차>
- 코드 분류하기(json 객체 다운, 텍스트 변환)
- 영수증을 컬럼별로 구분하는 방법 찾기
- 영수증을 행별로 잘라서 특정 컬럼만 추출하기
- 영수증 컬럼별 구하기 완료
- 영수증 날짜 구하기 완료
- 영수증 컬럼, 날짜를 json 객체에 담아 Flask를 이용해서 보내기 완료
- Spring Boot와 Flask를 연결시켜서 Spring Boot의 데이터베이스에 저장 완료

### <3주차>
- AI hub 데이터의 라벨링 데이터를 이용해서 easyOCR 모델 학습
- 예외 처리 설정하여 분석률 높임
- 전자 영수증 다 찍고 테스트
- 수기 영수증 어떻게 할 건지 고민
- easyOCR fine tuning
- AI허브 데이터(라벨링json, 이미지)를 어떻게 이용할지 검색

### <4주차>
- Mnist, pytorch 를 이용해 한글 손글씨 인식 모델 개발
- 한글 손글씨 데이터셋인 phd08 을 구했고 txt → png 파일로 변환중
- data split을 이용해 손글씨 모델 개발하기
- 수기 영수증 1개 성공 (조건 : 글자를 박스안에 맞춰야 하고 흩날리게 쓰면 안됨)
- Mnist 내장 데이터셋 실행
- 최종 결과 보고서 작성
- 발표 준비 자료 작성
  
# Notion_Link
https://www.notion.so/AI-bb1b347feb924633902d73b60667424b

# 사용 기술
---
- Python 3.11.4
- Flask 3.0.0
- easyocr 1.7.1
- Numpy 1.26.2
- opencv 4.8.1.78
- Pillow 10.2.0
- Tensorflow 2.15.0
- Torch 1.9.0
- Torchvision 0.10.0
- Jupyter 1.0.0

# 프로젝트 개념도
---
![asd](https://github.com/color7921/YoungMan_projectDA/assets/132988693/927a1a52-d6fe-4bf9-83c7-5c6ebbf1758e)

# 영수증 변환 결과
---
![213123](https://github.com/color7921/YoungMan_projectDA/assets/132988693/54063cb1-730b-4c5f-9400-36ef9d15cc40)

