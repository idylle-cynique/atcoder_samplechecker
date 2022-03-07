'''
    起動用プログラムです。一連のプログラムファイルとダウンロードファイルおよび
    それらの動作に必要なPythonインストール後、このファイルを起動することでプログラムを利用することができます
'''

import atcoder_systemwindow

def main():
    system = atcoder_systemwindow.AtCoderMainWindow()
    system.startup()

if __name__ == "__main__":
    main()