#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from tests.compat import json
from papago.response import Response


class TestResponse(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_json_current_api(self):
        """현재 API 응답 구조 파싱 테스트 (최상위 translatedText)"""
        body = json.dumps({
            'translatedText': 'Hello',
            'srcLangType': 'ko',
            'tarLangType': 'en',
            'engineType': 'N2MT',
        })
        response = Response.parse_json(body)
        self.assertEqual(response.code, Response.SUCCESS_CODE)
        self.assertEqual(response.text, 'Hello')
        self.assertEqual(response.source, 'ko')
        self.assertEqual(response.target, 'en')
        self.assertEqual(response.engine, 'N2MT')

    def test_parse_json_legacy_api(self):
        """구버전 API 응답 구조 호환 파싱 테스트 (message.result.translatedText)"""
        body = json.dumps({
            'message': {
                'result': {'translatedText': 'Hello', 'srcLangType': 'ko'}
            }
        })
        response = Response.parse_json(body)
        self.assertEqual(response.code, Response.SUCCESS_CODE)
        self.assertEqual(response.text, 'Hello')
        self.assertEqual(response.source, 'ko')

    def test_parse_failed_json(self):
        """에러 응답 파싱 테스트"""
        body = json.dumps({'errorCode': 405, 'errorMessage': 'Not Found Resources'})
        response = Response.parse_json(body)
        self.assertNotEqual(response.code, Response.SUCCESS_CODE)
        self.assertEqual(response.message, 'Not Found Resources')
