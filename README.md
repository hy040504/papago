<div align="center">

# 🦜 Papago Python API (v2.0.0)

**별도의 API Key나 쿠키 인증 없이 작동하는 파이썬용 비공식 네이버 파파고 번역 모듈**

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.style=for-the-badge.svg)](https://opensource.org/licenses/MIT)
[![API Status](https://img.shields.io/badge/Papago%20API-Active-brightgreen?style=for-the-badge&logo=naver&logoColor=white)](https://papago.naver.com/)

[주요 기능](#-주요-기능) • [설치 방법](#-설치-방법) • [빠른 시작](#-빠른-시작) • [API 명세](#-api-상세-사용법) • [지원 언어](#-지원-언어-목록) • [테스트](#-테스트-실행)

---

</div>

<br>

## ✨ 주요 기능

| 기능 | 설명 |
| :--- | :--- |
| **🔓 인증 키 불필요** | Naver Developers API Key(`Client ID/Secret`)나 브라우저 `Cookie` 인증이 일절 필요 없습니다. |
| **🔍 언어 자동 감지** | 텍스트를 입력받아 언어 코드를 판별하는 `detect()` 메서드를 제공합니다. |
| **💬 높임말 옵션** | 한국어 번역 시 자연스러운 높임말(`honorific=True`)을 적용할 수 있습니다. |
| **🌍 18개 다국어 지원** | 한/영/일/중 외에도 독일어, 러시아어, 아랍어, 힌디어, 포르투갈어 등 총 18개 언어를 지원합니다. |
| **🛡️ SSL Bypass 지원** | 사내 보안망이나 로컬 프록시 환경에서 `verify_ssl=False` 옵션을 지정할 수 있습니다. |

<br>

## 📦 설치 방법

### 1️⃣ 소스코드 클론 및 설치

```bash
git clone https://github.com/hy040504/papago.git
cd papago
python setup.py install
```

### 2️⃣ 개발용 의존성 설치

```bash
pip install -r test-requirements.txt
```

<br>

## 🚀 빠른 시작

```python
from papago import Translator

# 번역기 인스턴스 생성
translator = Translator()

# 1. 기본 번역 (한국어 -> 영어)
res = translator.translate("안녕하세요, 만나서 반갑습니다!")
print(f"번역 결과 : {res.text}")     # Hello, nice to meet you!
print(f"소스 언어 : {res.source}")   # ko
print(f"타겟 언어 : {res.target}")   # en
print(f"번역 엔진 : {res.engine}")   # PRETRANS 또는 N2MT

# 2. 언어 자동 감지
lang = translator.detect("こんにちは")
print(f"감지된 언어: {lang}")         # ja
```

<br>

## 📖 API 상세 사용법

### 1. `Translator(verify_ssl=True, user_agent=None)`

번역 요청을 수행하는 메인 클래스입니다.

```python
# 기본 사용
translator = Translator()

# SSL 인증서 오류 발생하는 환경 (프록시/사내망)
translator = Translator(verify_ssl=False)
```

---

### 2. `translate(text, source='ko', target='en', honorific=False, use_dict=True)`

원문 텍스트를 대상 언어로 번역합니다.

```python
# 높임말 옵션 사용 (ko -> en 또는 en -> ko 등)
res = translator.translate(
    text="어디 가세요?",
    source="ko",
    target="en",
    honorific=True
)
print(res.text)  # Where are you going?
```

#### 📌 매개변수 (Parameters)

- `text` *(str)*: 번역할 텍스트
- `source` *(str)*: 원문 언어 코드 (기본값: `'ko'`)
- `target` *(str)*: 번역할 언어 코드 (기본값: `'en'`)
- `honorific` *(bool)*: 높임말 적용 여부 (기본값: `False`)
- `use_dict` *(bool)*: 사전 검색 결과 포함 여부 (기본값: `True`)

#### 📌 반환값 (`Response` 객체)

- `res.text` *(str)*: 번역된 결과 문자열
- `res.source` *(str)*: 감지된/지정된 원문 언어 코드
- `res.target` *(str)*: 대상 언어 코드
- `res.engine` *(str)*: 번역에 사용된 엔진 (`PRETRANS`, `N2MT` 등)
- `res.code` *(int)*: 성공 시 `0`

---

### 3. `detect(text)`

텍스트의 언어를 자동으로 감지합니다.

```python
lang_code = translator.detect("Peace be upon you")
print(lang_code)  # en
```

<br>

## 🌐 지원 언어 목록

| 언어 코드 | 언어명 (English) | 한국어명 |
| :---: | :--- | :--- |
| `ko` | Korean | 한국어 |
| `en` | English | 영어 |
| `ja` | Japanese | 일본어 |
| `zh-CN` | Chinese (Simplified) | 중국어 (간체) |
| `zh-TW` | Chinese (Traditional) | 중국어 (번체) |
| `es` | Spanish | 스페인어 |
| `fr` | French | 프랑스어 |
| `vi` | Vietnamese | 베트남어 |
| `th` | Thai | 태국어 |
| `id` | Indonesian | 인도네시아어 |
| `de` | German | 독일어 |
| `ru` | Russian | 러시아어 |
| `it` | Italian | 이탈리아어 |
| `pt` | Portuguese | 포르투갈어 |
| `hi` | Hindi | 힌디어 |
| `ar` | Arabic | 아랍어 |
| `fa` | Persian | 페르시아어 |
| `mm` | Burmese | 미얀마어 |

<br>

## 🧪 테스트 실행

### pytest 단위 테스트

```bash
python -m pytest tests/ -v
```

### 샘플 실행 스크립트 (`test_papago.py`)

다국어 번역 및 높임말, 언어 감지 전체 흐름을 테스트합니다.

```bash
python -X utf8 test_papago.py
```

<br>

## ⚠️ 유의 사항 (Disclaimer)

- 본 모듈은 파파고 웹 서비스의 내부 API 엔드포인트를 이용하는 비공식(Unofficial) 패키지입니다.
- 네이버 측의 웹 API 규격 변경에 따라 예고 없이 작동이 중단되거나 변경될 수 있습니다.

<br>

## 📄 라이선스

This project is licensed under the [MIT License](LICENSE).
