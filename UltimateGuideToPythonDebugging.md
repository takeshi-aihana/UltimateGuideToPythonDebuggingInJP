# Python をデバッグするための究極のガイド

* (原文: [Ultimate Guide to Python Debugging](https://martinheinz.dev/blog/24)/)

---

## はじめに

たとえ分かりやすく読みやすいコードを書いたとしても、あるいは様々なテストでコードを検証していようとも、もしくはあなたが経験豊富な開発者であったとしても、不可解なバグはいや応無しに現れるので何らかの方法でデバッグする必要が出てきます。
多くのひとたちは自分のコードで起こったことを確認するのにたくさんの ``print`` 文に頼っています。
このアプローチは「理想的」とはほど遠く、コードのどこに問題があるのかを探し出すためにもっと良い方法がたくさんあります。
この記事では、それらのいくつかを紹介します。

---

## ログの取得は必須です

ログを取得するなどの設定をせずにアプリケーションを作成したとしたら、結局は後悔することになるでしょう。
あなたのアプリケーションからログを出さないと、バグを解決するのがとても難しくなる可能性があります。
幸いにも Python でログを取得する設定はとても簡単です：

```python
In [1]: import logging

In [2]: logging.basicConfig( 
   ...:         filename='application.log', 
   ...:         level=logging.WARNING, 
   ...:         format='[%(asctime)s] {%(pathname)s:%(lineno)d %(levelname)s - %(message)s}', 
   ...:         datefmt='%H:%M:%S' 
   ...: )
   
In [3]: logging.error('Some serious error occured.')

In [4]: logging.info('This is a log.')

In [5]: logging.warning('Function you are using is deprecated.')

```

これだけでファイルにログを記録してくれます。
このファイルの中身は次のようなものになります
（ファイルの在り処は ``logging.getLoggerClass().root.handlers[0].baseFilename`` でわかります）：

```Python

In [6]: %ls application.log
application.log

In [7]: %cat application.log
[2020-06-19 12:24:28,083] {<ipython-input-4-20cb3f234e3c>:1 ERROR - Some serious error occured.}
[2020-06-19 12:25:12,542] {<ipython-input-6-bb807406f93c>:1 WARNING - Function you are using is deprecated.}

# ログファイルが保管されている場所
In [8]: logging.getLoggerClass().root.handlers[0].baseFilename
Out[8]: '$HOME/work/GITHUB/Ultimate_Guide_to_Python_Debugging/samples/application.log'

```

この設定だけで十分であるように見えますが（たいていの場合は十分なのですが）、妥当な設定とログの書式、そして見やすいログがあれば作業がもっと楽になります。
上の設定をさらに改善し拡張する方法は、``.ini`` または ``.yaml`` ファイルを使い、それを Python のロガーに読んでもらうというものです。
これが、その設定例です：

```YAML
version 1

disable_existing_loggers: true

formatters:
  standard:
    format: "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    datefmt: '%H:%M:%S'

handlers:
  console:  # stdout にログを出力するハンドラ
    class: logging.StreamHandler
    level: DEBUG
    formatter: standard  # 上で定義した formatter を使用する
    stream: ext://sys.stdout
  file:  # ファイルにログを出力するハンドラ
    class: logging.handlers.RotatingFileHandler
    level: WARNING
    formatter: standard  # 上で定義した formatter を使用する
    filename: /tmp/warnings.log
    maxBytes: 10485760 # 記録するサイズの上限は10Mバイト
    backupCount: 10
    encoding: utf8

root:  # 複数のロガーを階層化して管理する - これが全てのロガーの Root となる設定
  level: ERROR
  handlers: [console, file]  # 上で定義した二つのハンドラにアタッチする

loggers:  # "root" から派生したロガーの定義
  mymodule:  # "mymodule" 用のロガー 
    level: INFO
    handlers: [file]  # このロガーは上で定義した "file" ハンドラだけ使う
    propagate: no  # このロガーはログを "root" へは伝搬しない
```

Python のコードの中に、この類の大きな設定を「持ち込む」とトレースや変更、そして保守が難しくなってしまう場合があります。
YAML ファイルの中に入れておけば、上記のようなかなり特殊な設定を使った複数のロガーを設定したり切り替えたりするのがとても簡単になります。

これらの設定項目がどこからきたものなのか疑問に思ったならば、ドキュメントが[ここ](https://docs.python.org/3.8/library/logging.config.html)にあります。
さらに、それらの大部分は、冒頭の例でご覧になったように、単なる「*キーワード引数*」です。
そしてファイルの中に設定があるということは、どういうわけか読み込んであげる必要があるということです。
したがって YAML ファイルを使った一番簡単な方法は：

```Python
In [1]: import yaml

In [2]: from logging import config

In [3]: %ls config.yaml
config.yaml

In [4]: with open('config.yaml', 'rt') as f: 
   ...:     config_data = yaml.safe_load(f.read()) 
   ...:     config.dictConfig(config_data) 
   ...:

In [6]: config
Out[6]: <module 'logging.config' from '/usr/lib/python3.6/logging/config.py'>

```

実際のところ Python のロガーは YAML ファイルを直接的にはサポートしていませんが、*ディクショナリ* 型の設定形式はサポートしています。
これは ``yaml.safe_load()`` メソッドを使って YAML ファイルから簡単に生成できます。
もし古い ``.ini`` 形式のファイルを使う傾向がおありだったとしても、ここで私が言いたいことは、[このドキュメント](https://docs.python.org/3/howto/logging.html#configuring-logging)にあるように *ディクショナリ* 型の設定形式の方が新しいアプリケーションで推奨されるアプローチであるということです。
その他の例についてはドキュメントの [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html#an-example-dictionary-based-configuration) の章を参照ください。

---

## ログを取得するデコレータ

前項で紹介したログの取得に関するヒントに続いて次は、バグの多い関数を呼び出した時のログが必要になったという状況下で役に立つヒントを紹介します。
このような場合は関数の本体に直接手を加えるのではなく、特定のログレベルとオプションのメッセージで、全ての関数呼び出しのログを取得する専用のデコレータが利用できます。
それではデコレータを見てみましょう：

```Python
#!/usr/bin/env python3

from functools import wraps, partial
import logging
import sys

def attach_wrapper(obj, func=None):    # オブジェクトの属性として関数を接続するヘルパー関数
    if func is None:
        return partial(attach_wrapper, obj)

setattr(obj, func.__name__, func)
    return func

def log(level, message):               # 実際のデコレータ
    def decorate(func):
        logger = logging.getLogger(func.__module__)        # ロガーを取得する
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        log_message = f'{func.__name__} - {message}'

        @wraps(func)
        def wrapper(*args, **kwargs):  # デコレートする関数を実行する前にメッセージをログする
            logger.log(level, log_message)
            return func(*args, **kwargs)

        @attach_wrapper(wrapper)       # 属性として set_level() を wrapper() に接続する
        def set_level(new_level):      # ログのレベルをセットする関数
            nonlocal level
            level = new_level

        @attach_wrapper(wrapper)       # 属性として set_message() を wrapper() に接続する
        def set_message(new_message):  # ログのメッセージをセットする関数
            nonlocal log_message
            log_message = f'{func.__name__} - {new_message}'

        return wrapper
    return decorate


# 使用例
@log(logging.WARN, 'example-param')
def somebuggyfunc(args):
    return args

def main():
    somebuggyfunc('some args')

    # 内部のデコレータ関数にアクセスしてログレベルとログメッセージを変更する
    somebuggyfunc.set_level(logging.CRITICAL)
    somebuggyfunc.set_message('new-message')
    
    somebuggyfunc('some args');

if __name__ == "__main__":
    sys.exit(main())
```

嘘を言うつもりはありませんが、このコードを理解するには少し時間がかかるかもしれません（それよりもコピー＆ペーストして実際に使ってみたくなるかもしれませんが）。
まず、このアイディアは ``log()`` 関数が引数をいくつか受け取り、内部のラッパー関数でもそれらを利用できるようにするというものです。
ここで渡している引数は、デコレータに接続されているアクセス専用関数を追加することで対応できるようにしています。
``functools.wraps()`` というデコレータについて ー
これをで使用しなかったら関数の名前（``func.__name__``）がデコレータの名前で置き換えられてしまいます。
しかし関数名をログとして記録させたいので、これは問題です。
そこで ``functools.wrap()`` を使って関数の名前や docstring、引数のリストをデコレータの関数にコピーすることで、この問題を解決しています。

なにはともあれ、こちらが上のコードの出力結果です。どうです？ かなりいい感じですよね。

```shell
2020-06-22 15:53:38,292 - __main__ - WARNING - somebuggyfunc - example-param
2020-06-22 15:53:38,292 - __main__ - CRITICAL - somebuggyfunc - new-message
```

---

## `__repr__` でもっとログを読みやすくする



