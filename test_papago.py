#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
파파고 번역 테스트 스크립트
실행: python test_papago.py
"""
import sys
import io

# Windows 콘솔 UTF-8 출력 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from papago import Translator

# SSL 오류가 날 경우 verify_ssl=False 로 설정
t = Translator(verify_ssl=False)

TESTS = [
    ('ko->en 기본',       '안녕하세요',             'ko', 'en',  {}),
    ('en->ko 기본',       'Hello, world!',           'en', 'ko',  {}),
    ('ko->ja 일본어',     '감사합니다',              'ko', 'ja',  {}),
    ('ko->zh-CN 중국어',  '사랑해요',                'ko', 'zh-CN', {}),
    ('en->de 독일어',     'Good morning',            'en', 'de',  {}),
    ('en->fr 프랑스어',   'Thank you very much',     'en', 'fr',  {}),
    ('en->ru 러시아어',   'How are you?',            'en', 'ru',  {}),
    ('en->ar 아랍어',     'Peace be upon you',       'en', 'ar',  {}),
    ('ko->en 존댓말ON',   '어디 가세요?',            'ko', 'en',  {'honorific': True}),
]

print('=' * 60)
print('파파고 번역 API 테스트 (쿠키 불필요)')
print('=' * 60)

# 언어 감지 테스트
print('\n[언어 자동 감지]')
for sample in ['Hello', '안녕하세요', 'こんにちは', 'Bonjour']:
    lang = t.detect(sample)
    print('  {:<25} -> {}'.format(repr(sample), lang))

# 번역 테스트
print('\n[번역 테스트]')
ok = 0
fail = 0
for name, text, src, tgt, kwargs in TESTS:
    try:
        r = t.translate(text, source=src, target=tgt, **kwargs)
        print('\n  [{}]'.format(name))
        print('  원문 : {}'.format(text))
        print('  번역 : {}'.format(r.text))
        print('  언어 : {} -> {}  엔진: {}'.format(r.source, r.target, r.engine))
        ok += 1
    except Exception as e:
        print('\n  [{}] 오류: {}'.format(name, e))
        fail += 1

print('\n' + '=' * 60)
print('결과: {} 성공 / {} 실패'.format(ok, fail))
print('=' * 60)
