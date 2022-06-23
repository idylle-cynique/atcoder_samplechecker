import os
import json

class SampleCheckerSettings:
    '''サンプルチェックプログラムに関する設定情報のパッケージ'''
    # 現状個別に扱っても大して手間はないが、将来的な設定情報の増大の可能性も考慮してこのようにしておく
    readme_path = r"./readme.md"
    settings = r"./settings.json"

    '''
        サンプル入力・サンプル出力データのディレクトリパス
        解答コードの出力結果・エラー出力結果のディレクトリパス
        解答コードが格納されたディレクトリのパス
    '''

    answercode_dirpath = { # 解答コードの格納されたサンプルコードのディレクトリパス情報
        "ABC": r".",
        "ARC": r".",
        "AGC": r"."
    }

    sampleio_dirpath = {   # サンプル入出力の格納されたディレクトリのパス情報
        "ABC": r".",
        "ARC": r".",
        "AGC": r"."
    }

    def __init__(self):
        # 解答コードの格納されたパスに関する情報を./settings.jsonから取得
        exist = os.path.exists(self.settings)

        if not(exist):
            return 

        with open(os.path.abspath(self.settings), 'r', encoding='UTF-8') as jsf:
            json_data = json.load(jsf)

        for key,v in json_data.items():
            if "abc" in key:
                self.answercode_dirpath["ABC"] = v
            if "arc" in key:
                self.answercode_dirpath["ARC"] = v
            if "agc" in key:
                self.answercode_dirpath["AGC"] = v
        return


def main()-> int:
    scs = SampleCheckerSettings()
    print(scs.readme_path)
    print(scs.answercode_dirpath["ABC"])
    return 0

if __name__ == '__main__':
    main()
    