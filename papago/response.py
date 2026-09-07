from papago.compat import json


class Response:
    """번역 결과 응답 객체

    SAZ 패킷 분석 기준 (2026년) 응답 구조:
    - 구버전: json['message']['result']['translatedText']
    - 현재:   json['translatedText'] (최상위 필드)
    """
    SUCCESS_CODE = 0

    def __init__(self, code=None, message=None, text=None, source=None, target=None, engine=None):
        self.code = self.SUCCESS_CODE if code is None else code
        self.message = message
        self.text = text
        self.source = source
        self.target = target
        self.engine = engine

    @classmethod
    def parse_json(cls, body):
        """JSON 문자열로부터 Response 인스턴스를 생성한다.

        현재 API 응답의 최상위 필드에서 직접 데이터를 추출한다:
          - translatedText : 번역 결과
          - srcLangType    : 감지된 소스 언어
          - tarLangType    : 대상 언어
          - engineType     : 번역 엔진 종류 (예: N2MT)
        """
        json_dict = json.loads(body)

        # 현재 API 응답 구조: 최상위에 translatedText 존재
        if 'translatedText' in json_dict:
            text = json_dict.get('translatedText')
            source = json_dict.get('srcLangType')
            target = json_dict.get('tarLangType')
            engine = json_dict.get('engineType')
            return Response(text=text, source=source, target=target, engine=engine)

        # 구버전 API 응답 구조 호환 (message.result.translatedText)
        if 'message' in json_dict:
            result = json_dict['message'].get('result', {})
            text = result.get('translatedText')
            source = result.get('srcLangType')
            target = result.get('tarLangType')
            return Response(text=text, source=source, target=target)

        # 에러 응답
        return Response(
            code=json_dict.get('errorCode'),
            message=json_dict.get('errorMessage')
        )

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'Response(code={code}, message={message}, text={text}, source={source}, target={target}, engine={engine})'.format(
            code=self.code,
            message=self.message,
            text=self.text,
            source=self.source,
            target=self.target,
            engine=self.engine,
        )
