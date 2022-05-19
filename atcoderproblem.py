import os

class AtCoderProblem:
    '''AtCoderの問題パッケージ'''
    oldabc_dict = { # 古いコンテストのURL文字列解決用
            "a":"1", "b":"2", "c":"3",
            "d":"4", "e":"5", "f":"6",
            "g":"7", "h":"8"
    }
    contests = {   # コンテストの種類
        "ABC", "ARC", "AGC"
    }

    ''' 必要なもの
    メソッド
        URL解決メソッド
        サンプル入出力の取得
    
    変数
        クラス変数
            URL解決用の辞書
        メンバ(インスタンス)変数
            ページタイトル文字列
            コンテスト名
            コンテスト番号
            問題番号文字列
            問題URL
            問題検知フラグ
        
    '''
    def __init__(self)-> None:
        self.pagetitle = str()          # 対象の問題のページタイトル
        self.contest_string = str()     # コンテスト名
        self.question_no = int()        # 問題番号
        self.question_string = str()    # コンテスト名＋問題番号
        self.url = str()                # 対象の問題のURL
        self.interativeflag = False     # インタラクティブ問題(サンプルケースの入出力テストが不可能)かどうかを真理値で保持
        self.flag = True                # 対象の問題が確かに存在していて、問題情報を取得可能かを真理値で保持
        self.sample_inputs = list()     # 対象の問題のサンプル入力
        self.sample_outputs = list()    # 対象の問題のサンプル出力
    
    def resolve_url(self):
        '''URLの解決'''
        return
    
    def set_url(self):
        '''対象の問題のURLを生成'''
        return 
    
    def get_samples(self):
        '''サンプル入出力を取得'''
        return 
    





def main()-> int:

    return 0

if __name__ == '__main__':
    main()