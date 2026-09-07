"""
파파고 번역 응답 객체 모듈.

API 응답 JSON 결과 데이터를 파싱하여 표준화된 Response 인스턴스로 변환합니다.
"""

from typing import Optional, Dict, Any
from papago.compat import json


class Response:
    """파파고 번역 결과 응답 모델 클래스.

    API 요청의 결과를 파싱하여 번역 텍스트, 언어 정보, 번역 엔진 등을 보관합니다.

    Attributes:
        code (int): 성공 여부 코드 (성공 시 0)
        message (Optional[str]): 에러 발생 시 에러 메시지
        text (Optional[str]): 번역된 결과 텍스트
        source (Optional[str]): 감지된/지정된 원문 언어 코드 (예: 'ko')
        target (Optional[str]): 번역 대상 언어 코드 (예: 'en')
        engine (Optional[str]): 사용된 파파고 번역 엔진 (예: 'N2MT', 'PRETRANS')
    """

    SUCCESS_CODE: int = 0

    def __init__(
        self,
        code: Optional[int] = None,
        message: Optional[str] = None,
        text: Optional[str] = None,
        source: Optional[str] = None,
        target: Optional[str] = None,
        engine: Optional[str] = None,
    ) -> None:
        """Response 인스턴스를 초기화합니다.

        Args:
            code: 상태 코드 (기본값: SUCCESS_CODE = 0)
            message: 에러 메시지
            text: 번역 결과 문자열
            source: 원문 언어 코드
            target: 대상 언어 코드
            engine: 번역 엔진 유형
        """
        self.code: int = self.SUCCESS_CODE if code is None else code
        self.message: Optional[str] = message
        self.text: Optional[str] = text
        self.source: Optional[str] = source
        self.target: Optional[str] = target
        self.engine: Optional[str] = engine

    @classmethod
    def parse_json(cls, body: str) -> "Response":
        """JSON 응답 문자열로부터 Response 인스턴스를 파싱하여 생성합니다.

        현재 파파고 웹 API(최상위 필드)와 구버전 OpenAPI 응답 구조를 모두 호환 처리합니다.

        Args:
            body: HTTP 응답 바디 JSON 문자열

        Returns:
            Response: 파싱된 응답 객체
        """
        json_dict: Dict[str, Any] = json.loads(body)

        # 현재 파파고 웹 API 응답 구조 (최상위에 translatedText 존재)
        if 'translatedText' in json_dict:
            text: Optional[str] = json_dict.get('translatedText')
            source: Optional[str] = json_dict.get('srcLangType')
            target: Optional[str] = json_dict.get('tarLangType')
            engine: Optional[str] = json_dict.get('engineType')
            return cls(text=text, source=source, target=target, engine=engine)

        # 구버전 OpenAPI 응답 구조 호환 (message.result.translatedText)
        if 'message' in json_dict:
            result: Dict[str, Any] = json_dict['message'].get('result', {})
            text = result.get('translatedText')
            source = result.get('srcLangType')
            target = result.get('tarLangType')
            return cls(text=text, source=source, target=target)

        # 에러 발생 응답 파싱
        return cls(
            code=json_dict.get('errorCode'),
            message=json_dict.get('errorMessage'),
        )

    def __repr__(self) -> str:
        return (
            f"Response(code={self.code}, message={self.message!r}, "
            f"text={self.text!r}, source={self.source!r}, target={self.target!r}, engine={self.engine!r})"
        )

    def __str__(self) -> str:
        return self.__unicode__()

    def __unicode__(self) -> str:
        return u'Response(code={code}, message={message}, text={text}, source={source}, target={target}, engine={engine})'.format(
            code=self.code,
            message=self.message,
            text=self.text,
            source=self.source,
            target=self.target,
            engine=self.engine,
        )
