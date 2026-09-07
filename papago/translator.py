"""
네이버 파파고 번역 실행 클라이언트 모듈.

파파고 웹 내부 API를 호출하여 텍스트 번역 및 언어 감지 기능을 수행합니다.
별도의 API Key 또는 Cookie 인증 없이 사용이 가능합니다.
"""

from typing import Optional, Dict, Any
import warnings
import requests

from papago.response import Response
from papago.contants import (
    PAPAGO_TRANSLATE_URL,
    PAPAGO_DETECT_URL,
    DEFAULT_CONTENT_TYPE,
    LANGUAGES,
)


class Translator:
    """파파고 웹 내부 API 기반 번역 실행 클라이언트 클래스.

    Naver Papago 서비스의 비공식 웹 API를 활용하여
    텍스트 번역 및 언어 감지 기능을 제공합니다.

    Attributes:
        verify_ssl (bool): SSL 인증서 검증 여부
        user_agent (str): HTTP 요청 시 사용할 User-Agent 헤더 문자열

    Example:
        >>> from papago import Translator
        >>> translator = Translator()
        >>> res = translator.translate("Hello", source="auto")  # 자동으로 영어 감지 후 한국어로 번역!
        >>> print(res.text)
        '안녕하세요'
    """

    DEFAULT_USER_AGENT: str = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/152.0.0.0 Safari/537.36'
    )

    def __init__(self, verify_ssl: bool = True, user_agent: Optional[str] = None) -> None:
        """Translator 인스턴스를 초기화합니다.

        Args:
            verify_ssl: SSL 인증서 검증 여부 (기본값: True).
                        사내 보안 망이나 프록시 환경에서 SSLError 발생 시 False로 설정합니다.
            user_agent: 사용자 지정 User-Agent 문자열 (미지정 시 기본값 사용).
        """
        self.verify_ssl: bool = verify_ssl
        self.user_agent: str = user_agent or self.DEFAULT_USER_AGENT

    def _build_headers(self) -> Dict[str, str]:
        """HTTP 요청 공통 헤더 딕셔너리를 생성합니다.

        Returns:
            Dict[str, str]: Origin, Referer, Content-Type 등이 포함된 헤더 딕셔너리
        """
        return {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ko',
            'Content-Type': DEFAULT_CONTENT_TYPE,
            'Origin': 'https://papago.naver.com',
            'Referer': 'https://papago.naver.com/',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': self.user_agent,
        }

    def _post(self, url: str, payload: Dict[str, Any]) -> requests.Response:
        """파파고 API에 POST 요청을 전송하고 응답을 반환합니다.

        Args:
            url: 요청 엔드포인트 URL
            payload: POST 요청 폼 데이터 딕셔너리

        Returns:
            requests.Response: requests 응답 객체

        Raises:
            Exception: HTTP 상태 코드가 200 OK가 아닌 경우 예외 발생
        """
        if not self.verify_ssl:
            warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        resp: requests.Response = requests.post(
            url,
            headers=self._build_headers(),
            data=payload,
            verify=self.verify_ssl,
        )
        if resp.status_code != 200:
            raise Exception(f'HTTP 오류 [{resp.status_code}]: {resp.text}')

        return resp

    def translate(
        self,
        text: str,
        source: str = 'auto',
        target: Optional[str] = None,
        honorific: bool = False,
        use_dict: bool = True,
        dict_display: int = 30,
        use_glossary: bool = False,
    ) -> Response:
        """원문 텍스트를 대상 언어로 번역합니다.

        `source='auto'` 지정 시 원문 언어를 자동으로 감지하며:
          - 감지된 언어가 외국어인 경우 -> 한국어('ko')로 자동 번역됩니다.
          - 감지된 언어가 한국어('ko')인 경우 -> 영어('en')로 자동 번역됩니다.

        Args:
            text: 번역할 원문 문자열
            source: 원문 언어 코드 (기본값: 'auto' - 자동 감지)
            target: 대상 언어 코드 (기본값: None - source='auto' 시 자동으로 설정됨)
            honorific: 높임말 옵션 적용 여부 (기본값: False, 한국어 번역 시 적용)
            use_dict: 사전 검색 결과 데이터 포함 여부 (기본값: True)
            dict_display: 사전 검색 결과 표시 최대 개수 (기본값: 30)
            use_glossary: 사용자 용어집 적용 여부 (기본값: False)

        Returns:
            Response: 번역 결과 객체 (translatedText, source, target, engine 등 포함)

        Raises:
            ValueError: 지원하지 않는 소스/타겟 언어 코드가 지정된 경우 예외 발생
            Exception: 번역 API 호출 시 네트워크 오류가 발생한 경우 예외 발생
        """
        # 언어 자동 감지 처리
        if source == 'auto':
            detected = self.detect(text)
            source = detected if (detected and detected in LANGUAGES and detected != 'auto') else 'en'
            if target is None:
                target = 'en' if source == 'ko' else 'ko'
        else:
            if target is None:
                target = 'en' if source == 'ko' else 'ko'

        if source not in LANGUAGES:
            raise ValueError(f'지원하지 않는 소스 언어입니다: {source}')
        if target not in LANGUAGES:
            raise ValueError(f'지원하지 않는 대상 언어입니다: {target}')

        payload: Dict[str, Any] = {
            'source': source,
            'target': target,
            'text': text,
            'dict': str(use_dict).lower(),
            'useGlossary': str(use_glossary).lower(),
            'honorific': str(honorific).lower(),
            'dictDisplay': dict_display,
        }

        resp: requests.Response = self._post(PAPAGO_TRANSLATE_URL, payload)
        return Response.parse_json(resp.text)

    def detect(self, text: str) -> Optional[str]:
        """입력 텍스트의 언어를 자동으로 감지합니다.

        Args:
            text: 언어를 판별할 원문 문자열

        Returns:
            Optional[str]: 감지된 언어 코드 (예: 'ko', 'en', 'ja' 등), 감지 실패 시 None

        Raises:
            Exception: 언어 감지 API 호출 시 네트워크 오류가 발생한 경우 예외 발생
        """
        payload: Dict[str, str] = {'query': text}
        resp: requests.Response = self._post(PAPAGO_DETECT_URL, payload)
        data: Dict[str, Any] = resp.json()
        return data.get('langCode')
