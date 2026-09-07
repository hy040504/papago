"""PAPAGO Translate API for Python"""

# 현재 파파고 웹 내부 API 엔드포인트 (2026년 기준)
PAPAGO_TRANSLATE_URL = 'https://papago.naver.com/api/text/translation'
PAPAGO_DETECT_URL = 'https://papago.naver.com/api/langs/dect'

# 하위 호환성 유지
PAPAGO_API_URL = PAPAGO_TRANSLATE_URL

DEFAULT_CONTENT_TYPE = 'application/x-www-form-urlencoded; charset=UTF-8'

# SAZ 패킷 분석 기준 지원 언어 목록 (langDetection nbests 참고)
LANGUAGES = {
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
