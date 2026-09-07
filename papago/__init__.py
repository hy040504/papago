"""
Papago API for Python (v2.0.0)

네이버 파파고 웹 내부 API 기반의 비공식 파이썬 번역 라이브러리입니다.
API Key 또는 Cookie 인증 없이 텍스트 번역 및 언어 감지 기능을 제공합니다.
"""

from papago.translator import Translator
from papago.response import Response

__all__ = ['Translator', 'Response']
__version__ = '2.0.0'
