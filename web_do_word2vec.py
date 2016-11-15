#!/usr/bin/env python
# coding: utf-8
from bottle import route, run, request
import urllib
import collections
import json
import os
import logging
import sys
import argparse
import MeCab
import re
from gensim.models import word2vec

# 学習済みモデルのロード
# model = word2vec.Word2Vec.load("sample.model")
# model = word2vec.Word2Vec.load("hikinou_100_20_15.model")
# model = word2vec.Word2Vec.load("merge_200_15_15.model")
# model = word2vec.Word2Vec.load("非機能要求_req_30_5_10.model")
model = word2vec.Word2Vec.load("非機能要求_700_200_10_15.model")
# 入力された単語から近い単語をn個表示する
def s(posi='', nega='', n=10):
    threshold = 0.0 # cos距離の閾値
    ps = mecab(posi)
    results = collections.OrderedDict()
    print posi.encode('utf-8', 'ignore')
    # 学習済みモデルからcos距離が最も近い単語n個(topn個)を表示する
    for p in ps:
    	cnt = 1 # 表示した単語の個数カウント用
    	texts = collections.OrderedDict()
    	result = model.most_similar(positive = p, negative = nega, topn = n)
    	# ストップワードの定義
    	stopWords = [ u'機能性', u'信頼性', u'使用性', u'効率性', u'保守性', u'移植性', u'セキュリティ', u'コスト' ]
    	for r in result:
	    	if r[1] >= threshold and not r[0].isdigit() and len(r[0]) > 1 and not re.match("[!-/:-@[-`{-~]", r[0]) and r[0] not in stopWords:
	        	print str(cnt).encode('utf-8'), u'　'.encode('utf-8'), r[0].encode('utf-8'), u'　'.encode('utf-8'), round(r[1], 2)
	        	# text = str(cnt) + '　' + r[0] + '　' + str(round(r[1], 2)) + '\n'
	        	texts[r[0]] = round(r[1], 2)
	        	cnt += 1
    	results[p] = texts
	# f = open(posi + ".json", "w")
	# json.dump(results, f, ensure_ascii=False)
    return json.dumps(results)

def mecab(word=''):
	text = []
	tagger = MeCab.Tagger("-Ochasen")
	tagger.parse('') # <= 空文字列をparseする
	node = tagger.parseToNode(word.encode('utf-8', 'ignore'))
	print "word:" + word.encode('utf-8')
	while node:

		meta = node.feature.split(',')
		if meta[0] == 'BOS/EOS':
			node = node.next
			continue

		surface = node.surface.decode('utf-8', 'ignore')
		print u"surface:".encode('utf-8'), surface.encode('utf-8'), u"   meta:".encode('utf-8'), meta[0].encode('utf-8')

		if meta[0] == '名詞':
			text.append(surface)
		node = node.next

	return text

def utf8_to_unicode( string ):
	return unicode( string, 'utf_8' )

@route("/",method='GET')
def main():
	posi = urllib.unquote(request.query.get('posi'))
	nega = ''
	num = int(request.query.get('num'))
	return s(posi, nega, num)

run(host='0.0.0.0', port=9080)

# if __name__ == '__main__':
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument('--posi', nargs='*', type=utf8_to_unicode)
# 	parser.add_argument('--nega', nargs='*', type=utf8_to_unicode)
# 	parser.add_argument('--num', nargs='?')
# 	word = parser.parse_args()

# 	# posi = []
# 	nega = []
# 	num = 10

# 	if word.posi:
# 		posi = word.posi
# 	if word.nega:
# 		nega = word.nega
# 	if word.num:
# 		num = int(word.num)

# 	s(mecab(posi), mecab(nega), num)
