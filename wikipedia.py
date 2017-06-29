#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:19:59 2017

@author: hiroyuki
"""
# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for
from gensim.models import word2vec
import numpy as np
import os

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# メッセージをランダムに表示するメソッド
def picked_up():
    messages = [
        "こんにちは、あなたの名前を入力してください",
        "やあ！お名前は何ですか？",
        "あなたの名前を教えてね"
    ]
    # NumPy の random.choice で配列からランダムに取り出し
    return np.random.choice(messages)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "ようこそ"
    message = picked_up()
    # index.html をレンダリングする
    return render_template('index.html',
                           message=message, title=title)

# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    mdl = word2vec.Word2Vec.load("../word2vec.gensim.model")
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        word = request.form['word']
        # Return Result Vector
        #for x in out:
        #    print(x[0], x[1])
        # index.html をレンダリングする
        out = mdl.most_similar(positive=[word])
        return render_template('index.html',
                               result=out, word=word)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に
           