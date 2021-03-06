# atcoder_samplechecker

AtCoderのサンプル入出力を用いたコードチェックを自動で行うプログラムです。



##  利用にあたっての基本的な流れ

1. 利用にあたって必要となるソフトウェア(Python)、Pythonライブラリ(beautiful soup4)をPCにインストールします
2. main.pyをクリックしてプログラムを起動します。この際、カレントディレクトリは、一連のプログラム群が格納されたディレクトリとしておいてください
3. メインウィンドウ上にあるディレクトリ設定ボタンから、コンテストの解答コードが保存されたディレクトリのパスをC&Pなどを用いて記入後、OKボタンをクリックして設定を保存します。
4. サンプル入出力を用いた簡易チェックを行いたい問題の情報（どの種類のコンテストで、何回目のコンテストで、コンテストのナンバリングアルファベットは何か）をメインウィンドウの記入欄に記入し、『チェック開始』ボタンをクリックします
5. サンプル入出力を用いて実行した際の出力テキスト、およびサンプル入出力例が画面下部のテキストボックス内に表示され、併せて解答のジャッジメントが行われます



## 利用にあたっての注意

### 利用可能な解答コード

​	このプログラムはPythonの解答コードを前提としており、他のプログラミング言語のコードではサンプルチェック機能を利用することはできません。

### 必要となるソフトウェア・ライブラリについて

　このプログラムは、Pythonと当コード内で利用されている外部ライブラリがインストールされたコンピュータでのみ利用が可能です。なお、一連の機能実装と内部処理の改善、テストなどを終え次第実行ファイル化したものを公開する予定です。

　現時点でプログラムを動作させたい方は、以下をご利用のコンピュータ内にインストールしていただくよう、よろしくお願いします。

- Python

- プログラム内で利用されているPythonの外部ライブラリ

  - beutifulsoup4 (Webスクレイピング)

    指定したコンテスト番号から生成されたURLを使ってサンプル入出力データを取得・保存する際に利用します

### ジャッジメントの厳密性について

　このプログラムにおけるジャッジメントシステムはかなりざっくりしており、次のような場合において、不正解であるはずの解答コードが正解扱いになったり、逆に正解であるはずの解答コードが不正解になる場合が存在します。サンプルチェックを行った後でも、再度問題文などを確認の上、出力内容が適正かどうか確認することをお勧めします。

#### 実際のジャッジメントシステムと異なるジャッジが下される可能性のある例

- 小数(float型)による解答を行う問題の場合
  - 実際には正答として許容される誤差内の誤差であっても、このプログラムでは値が異なればWAと判定されます
- 複数の解が存在する問題である場合
  - たとえば「10以上20未満の整数値のうち、素数であるものを一つ出力しなさい」といったような問題の場合、{11, 13, 17, 19}の4つの正答例が存在しますが、このプログラムでは、サンプル出力と出力した値が異なれば、それはWAと判定されます

## 開発・動作確認環境

- Windows10 Pro 21H2
- 自作マシン (intel Core i5-10400F, Z490 Mainboard, DDR4-2933 48GB)
- Python (v3.8.4)
- VSCode (v.1.6.5)
