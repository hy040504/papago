"""
네이버 파파고 번역 API 상수 정의 모듈.

파파고 웹 서비스의 내부 API 엔드포인트 URL 및
지원 언어 코드 목록 등의 기본 상수를 관리합니다.
"""

from typing import Dict

# 파파고 웹 내부 API 엔드포인트 (2026년 기준)
PAPAGO_TRANSLATE_URL: str = 'https://papago.naver.com/api/text/translation'
"""파파고 텍스트 번역 요청 엔드포인트"""

PAPAGO_DETECT_URL: str = 'https://papago.naver.com/api/langs/dect'
"""파파고 텍스트 언어 자동 감지 엔드포인트"""

# 하위 호환성을 위한 구 API URL 상수 정의
PAPAGO_API_URL: str = PAPAGO_TRANSLATE_URL

# 기본 HTTP 요청 Content-Type
DEFAULT_CONTENT_TYPE: str = 'application/x-www-form-urlencoded; charset=UTF-8'

# 파파고 지원 언어 코드 및 언어명 딕셔너리
LANGUAGES: Dict[str, str] = {
    'ko': 'Korean',
    'en': 'English',
    'ja': 'Japanese',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'es': 'Spanish',
    'fr': 'French',
    'vi': 'Vietnamese',
    'th': 'Thai',
    'id': 'Indonesian',
    'de': 'German',
    'ru': 'Russian',
    'it': 'Italian',
    'pt': 'Portuguese',
    'hi': 'Hindi',
    'ar': 'Arabic',
    'fa': 'Persian',
    'mm': 'Burmese',
}
