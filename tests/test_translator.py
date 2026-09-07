#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, MagicMock
from papago.translator import Translator


class TestTranslator(unittest.TestCase):
    def setUp(self):
        """
        현재 API는 네이버 쿠키 인증 방식을 사용합니다.
        실제 테스트를 위해서는 브라우저에서 복사한 COOKIE 환경변수가 필요합니다.
        단위 테스트는 mock을 사용합니다.
        """
        self.translator = Translator(verify_ssl=False)

    @patch('papago.translator.requests.post')
    def test_translate(self, mock_post):
        """기본 번역 테스트 (mock)"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = '{"translatedText":"Hello.","srcLangType":"ko","tarLangType":"en","engineType":"N2MT"}'
        mock_post.return_value = mock_resp

        response = self.translator.translate('안녕하세요', source='ko', target='en')
        self.assertEqual(response.text, 'Hello.')
        self.assertEqual(response.source, 'ko')
        self.assertEqual(response.target, 'en')

    @patch('papago.translator.requests.post')
    def test_translate_with_honorific(self, mock_post):
        """존댓말 옵션 번역 테스트"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = '{"translatedText":"Hello.","srcLangType":"ko","tarLangType":"en","engineType":"N2MT"}'
        mock_post.return_value = mock_resp

        response = self.translator.translate('안녕하세요', source='ko', target='en', honorific=True)
        self.assertIsNotNone(response.text)
        # honorific=True 가 payload에 포함됐는지 확인
        call_kwargs = mock_post.call_args
        self.assertIn('honorific', call_kwargs[1]['data'])
        self.assertEqual(call_kwargs[1]['data']['honorific'], 'true')

    @patch('papago.translator.requests.post')
    def test_detect(self, mock_post):
        """언어 감지 테스트"""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'langCode': 'ko'}
        mock_post.return_value = mock_resp

        lang = self.translator.detect('안녕하세요')
        self.assertEqual(lang, 'ko')

    def test_translate_invalid_source(self):
        """지원하지 않는 소스 언어 예외 테스트"""
        self.assertRaises(ValueError, self.translator.translate, 'test', 'xx', 'en')

    def test_translate_invalid_target(self):
        """지원하지 않는 대상 언어 예외 테스트"""
        self.assertRaises(ValueError, self.translator.translate, 'test', 'ko', 'xx')

    def test_translate_new_languages(self):
        """신규 추가 언어(ar, ru, de 등)가 ValueError 없이 통과하는지 확인"""
        from papago.contants import LANGUAGES
        for lang in ['ar', 'ru', 'de', 'it', 'pt', 'hi', 'fa', 'mm']:
            self.assertIn(lang, LANGUAGES)
