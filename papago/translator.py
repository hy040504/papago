import requests
import warnings
from papago.response import Response
from papago.contants import (
    PAPAGO_TRANSLATE_URL,
    PAPAGO_DETECT_URL,
    DEFAULT_CONTENT_TYPE,
    LANGUAGES,
)


class Translator:
    """파파고 웹 내부 API 번역 클래스 (2026년 기준)

    SAZ 패킷 분석 결과:
    - 엔드포인트: https://papago.naver.com/api/text/translation
    - 인증 방식: 쿠키 불필요 (비로그인으로도 동작 확인)
    - 요청 형식: application/x-www-form-urlencoded
    - 요청 파라미터: source, target, text, dict, useGlossary, honorific, dictDisplay

    주의: 공식 OpenAPI가 아닌 웹 내부 API를 사용합니다.
          API 스펙이 예고 없이 변경될 수 있습니다.

    :param verify_ssl: SSL 인증서 검증 여부 (기본값 True, 문제 시 False로 설정)
    :param user_agent: User-Agent 헤더 (기본값 제공)
    """

    DEFAULT_USER_AGENT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/152.0.0.0 Safari/537.36'
    )

    def __init__(self, verify_ssl=True, user_agent=None):
        self.verify_ssl = verify_ssl
        self.user_agent = user_agent or self.DEFAULT_USER_AGENT

    def _build_headers(self):
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

    def _post(self, url, payload):
        """내부 POST 요청 공통 처리"""
        if not self.verify_ssl:
            warnings.filterwarnings('ignore', message='Unverified HTTPS request')
        resp = requests.post(
            url,
            headers=self._build_headers(),
            data=payload,
            verify=self.verify_ssl,
        )
        if resp.status_code != 200:
            raise Exception('HTTP 오류 [{}]: {}'.format(resp.status_code, resp.text))
        return resp

    def translate(self, text, source='ko', target='en',
                  honorific=False, use_dict=True, dict_display=30, use_glossary=False):
        """소스 언어를 대상 언어로 번역한다.

        :param text: 번역할 원문 텍스트
        :param source: 소스 언어 코드 (예: 'ko', 'en')
        :param target: 대상 언어 코드
        :param honorific: 존댓말 사용 여부 (한국어 번역 시 유효)
        :param use_dict: 사전 검색 결과 포함 여부
        :param dict_display: 사전 결과 최대 표시 수
        :param use_glossary: 용어집 사용 여부
        :rtype: Response
        """
        if source not in LANGUAGES:
            raise ValueError('지원하지 않는 소스 언어입니다: {}'.format(source))
        if target not in LANGUAGES:
            raise ValueError('지원하지 않는 대상 언어입니다: {}'.format(target))

        payload = {
            'source': source,
            'target': target,
            'text': text,
            'dict': str(use_dict).lower(),
            'useGlossary': str(use_glossary).lower(),
            'honorific': str(honorific).lower(),
            'dictDisplay': dict_display,
        }
        resp = self._post(PAPAGO_TRANSLATE_URL, payload)
        return Response.parse_json(resp.text)

    def detect(self, text):
        """텍스트의 언어를 자동 감지한다.

        :param text: 감지할 텍스트
        :return: 감지된 언어 코드 문자열 (예: 'ko', 'en')
        """
        payload = {'query': text}
        resp = self._post(PAPAGO_DETECT_URL, payload)
        return resp.json().get('langCode')
