# LA 교통 사고가 속도에 미치는 영향 분석 시스템

![시연 GIF](./demo.gif)

<br>

## 목차

1. [개요](#개요)
2. [주요 기능](#주요-기능)
3. [기술 스택](#기술-스택)
4. [개발 기간](#개발-기간)
5. [설치 방법](#설치-방법)
6. [시작하기](#시작하기)

<br>

## 개요

교통 사고는 도로 위의 안전과 효율성에 큰 영향을 미칩니다. 특히 사고 발생 후 교통 흐름과 속도에 미치는 영향은 사고 현장의 처리 속도와 교통 관리 체계의 효율성에 따라 달라집니다.

본 프로젝트는 2012년 3월부터 6월 사이, 로스앤젤레스(LA)에서 발생한 교통 사고 데이터를 기반으로 사고 발생 전후의 교통 속도 변화를 분석하는 시스템을 개발하는 것을 목표로 합니다. 이를 통해 교통 사고가 교통 흐름에 미치는 영향을 정량적으로 분석하고 사고 발생 시 교통 속도 저하를 최소화할 수 있는 방안을 모색하는데 기여합니다.

이 시스템은 도시 교통 관리와 사고 대응 전략을 개선하는 데 유용한 데이터를 제공하며 교통 사고에 대한 예측 및 대응 시스템을 강화하는 데 중요한 역할을 할 수 있습니다.

<br>

## 주요 기능

### 1. 전체 교통사고 속도 분석

전체 교통사고에 대한 속도 변화 분석함으로써 교통 흐름에 미친 영향을 파악할 수 있습니다. 분석된 결과 데이터를 다음 2가지 그래프로 시각화합니다.

- `산점도` : 교통사고 발생 전후의 속도 차이를 한눈에 볼 수 있게 해줍니다.

- `히스토그램` : 교통사고 발생 전후의 속도 변화 분포를 분석할 수 있습니다.

### 2. 개별 교통사고 속도 분석

사용자가 선택한 교통사고 발생 전후의 속도를 분석합니다. 교통 사고 발생으로부터 5분 전에서 30분 후까지의 속도 변화를 확인할 수 있습니다. 또한, STGCN 모델을 통해 추출한 예측 데이터와 실제 데이터를 비교 분석합니다.

<br>

## 기술 스택

- **프론트엔드**: React, Tailwind
- **백엔드**: Flask, Python
- **데이터 분석**: Pandas, NumPy, Matplotlib
- **예측 모델**: STGCN
- **기타**: Google Maps API

<br>

## 개발 기간

- 2024년 11월 09일 ~ 2024년 12월 14일

<br>

## 설치 방법

**환경**

```
운영체제: Windows 11
Python: 3.12.x
Node.js: 20.x
```

GitHub에서 레포지토리를 클론합니다

```bash
git clone https://github.com/NamYunje2002/la-traffic-crash-analysis.git
```

<br>

## 시작하기

### 백엔드(플라스크)

(1) 터미널을 열고, 새로운 가상환경을 생성한 후 활성화합니다.

```bash
python -m venv venv
.\venv\scripts\activate
```

(2) 실행에 필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

(3) 구글 맵 API 사용을 위해 `.env` 파일의 GOOGLE_MAPS_API_KEY에 API 키를 추가합니다.

```bash
GOOGLE_MAPS_API_KEY = your_api_key

(생략)
```

(4) 플라스크를 실행합니다.

- 일반 실행

```
python app.py
```

- 개발 서버 실행

```
flask --debug run
```
<br>

### 프론트엔드(리액트)

(1) 새로운 터미널을 연 뒤, 가상환경을 활성화하고 `frontend` 디렉토리로 이동합니다.

```
.\venv\scripts\activate
cd frontend
```

(2) 필요한 모듈을 설치하고 실행합니다.

```
npm install
npm start
```

(3) http://localhost:3000 에서 대시보드를 확인할 수 있습니다.

> 반드시 플라스크를 실행한 상태에서 리액트를 실행해야 합니다.
