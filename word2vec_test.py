# -*- coding: utf-8 -*-
from gensim.models import word2vec
import logging
# 進捗表示用
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Word2Vecの学習に使用する分かち書き済みのテキストファイルの準備
# sentences = word2vec.Text8Corpus('merge_corpus.txt')
sentences = word2vec.Text8Corpus('非機能要求_700.txt')
# sentences = word2vec.LineSentence('非機能要求.txt')

# Word2Vecのインスタンス作成
# sentences : 対象となる分かち書きされているテキスト
# size      : 出力するベクトルの次元数
# min_count : この数値よりも登場回数が少ない単語は無視する
# window    : 一つの単語に対してこの数値分だけ前後をチェックする
model = word2vec.Word2Vec(sentences, size=200, min_count=10, window=15)

# 学習結果を出力する
# model.save("merge_30_5_10.model")
model.save("非機能要求_700_200_10_15.model")

if __name__ == '__main__':
    print "Finish!!!"