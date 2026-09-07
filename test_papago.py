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
    ('자동감지 (영어->한국어)',  'Hello, nice to meet you!', 'auto', None, {}),
    ('자동감지 (일어->한국어)',  'こんにちは、お元気ですか？', 'auto', None, {}),
    ('자동감지 (불어->한국어)',  'Bonjour tout le monde',    'auto', None, {}),
    ('자동감지 (한글->영어)',    '오늘 날씨 정말 좋네요',    'auto', None, {}),
    ('명시적 ko->en 기본',       '안녕하세요',               'ko',   'en',  {}),
    ('명시적 en->ko 기본',       'Hello, world!',             'en',   'ko',  {}),
    ('명시적 ko->en 존댓말ON',   '어디 가세요?',              'ko',   'en',  {'honorific': True}),
]

print('=' * 60)
print('파파고 번역 API 테스트 (자동 감지 & 한국어 자동 번역)')
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
