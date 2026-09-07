# Papago API with Python (v2.0.0)

파이썬용 비공식 파파고(Papago) 번역 모듈입니다.  
최신 파파고 웹 내부 API 규격을 분석하여 별도의 **API Key(Client ID/Secret) 및 쿠키 없이** 번역 및 언어 감지 기능을 제공합니다.

---

## 🚀 주요 특징 (Key Features)

- **인증 불필요**: API 키 및 브라우저 쿠키 없이 바로 작동합니다.
- **언어 자동 감지**: 입력 텍스트의 언어를 자동으로 판별하는 `detect()` 기능 추가.
- **높임말 옵션**: 한국어 번역 시 높임말(`honorific=True`) 적용 가능.
- **확장된 다국어 지원**: 한국어, 영어, 일본어, 중국어 외에도 독일어, 러시아어, 아랍어, 포르투갈어, 힌디어 등 총 18개 언어 지원.
- **SSL 오류 대응**: 환경에 따른 SSL 인증서 검증 옵션 (`verify_ssl=False`) 제공.

---

## 📦 설치 (Installation)

### 수동 설치 (Manual Installation)

```bash
$ git clone https://github.com/hy040504/papago.git
$ cd papago
$ python setup.py install
```

---

## 💻 사용법 (Usage)

### 1. 기본 번역 (Basic Translation)

```python
from papago import Translator

translator = Translator()

# 기본 번역 (한국어 -> 영어)
response = translator.translate('안녕하세요')
print(response.text)    # Hello
print(response.source)  # ko
print(response.target)  # en
print(response.engine)  # PRETRANS / N2MT

# 언어 지정 번역 (한국어 -> 일본어)
response = translator.translate('감사합니다', source='ko', target='ja')
print(response.text)    # ありがとうございます。
```

### 2. 언어 자동 감지 (Language Detection)

```python
lang_code = translator.detect('こんにちは')
print(lang_code)  # ja
```

### 3. 높임말 옵션 (Honorific)

```python
response = translator.translate('어디 가세요?', source='ko', target='en', honorific=True)
print(response.text)  # Where are you going?
```

### 4. SSL 인증서 오류 발생 시 (SSL Bypass)

기업망이나 로컬 프록시 환경 등 SSL 인증서 검증 오류가 발생하는 경우 `verify_ssl=False` 옵션을 지정할 수 있습니다.

```python
translator = Translator(verify_ssl=False)
```

---

## 🌐 지원 언어 코드 (Supported Languages)

| 코드 | 언어 (Language) |
|---|---|
| `ko` | Korean (한국어) |
| `en` | English (영어) |
| `ja` | Japanese (일본어) |
| `zh-CN` | Chinese Simplified (중국어 간체) |
| `zh-TW` | Chinese Traditional (중국어 번체) |
| `es` | Spanish (스페인어) |
| `fr` | French (프랑스어) |
| `vi` | Vietnamese (베트남어) |
| `th` | Thai (태국어) |
| `id` | Indonesian (인도네시아어) |
| `de` | German (독일어) |
| `ru` | Russian (러시아어) |
| `it` | Italian (이탈리아어) |
| `pt` | Portuguese (포르투갈어) |
| `hi` | Hindi (힌디어) |
| `ar` | Arabic (아랍어) |
| `fa` | Persian (페르시아어) |
| `mm` | Burmese (미얀마어) |

---

## 🧪 테스트 실행 (Running Tests)

### 단위 테스트 (Unit Tests)

```bash
$ python -m pytest tests/ -v
```

### 실제 번역 동작 테스트 스크립트

```bash
$ python test_papago.py
```

---

## 📄 라이선스 (License)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
