import requests
import re
from bs4 import BeautifulSoup

class AtCoderProblem:
    '''AtCoderの問題パッケージ'''
    oldabc_dict = { # 古いコンテストのURL文字列解決用
            "a":"1", "b":"2", "c":"3",
            "d":"4", "e":"5", "f":"6",
            "g":"7", "h":"8"
    }
    contests = {    # コンテストの種類
        "ABC", "ARC", "AGC"
    }
    
    # コンテストURLの文字列様式が異なる回
    abc_edge_contest = 19  
    arc_edge_contest = 34
    base_url = r"https://atcoder.jp/contests/*/tasks/*"    # 問題URLの様式
    error_title = "404 Not Found"  # 不適正な問題リンクを踏んだ場合に与えられるページのタイトル 

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
        '''各種インスタンス変数を初期化'''
        self.pagetitle = str()          # 対象の問題のページタイトル
        self.contest_string = str()     # コンテスト名
        self.contest_no = str()         # コンテスト番号
        self.problem_no = str()         # 問題番号
        self.cat_string = str()         # コンテスト名 + コンテスト番号 + 問題番号
        self.url = str()                # 対象の問題のURL
        self.soup = BeautifulSoup()     # サンプル入出力取得に用いるsoupデータ
        self.interativeflag = False     # インタラクティブ問題(サンプルケースの入出力テストが不可能)かどうかを真理値で保持
        self.flag = True                # 対象の問題が確かに存在していて、問題情報を取得可能かを真理値で保持
        self.sample_inputs = list()     # 対象の問題のサンプル入力
        self.sample_outputs = list()    # 対象の問題のサンプル出力

    def get_sourse(self)-> None:
        '''ソースデータを取得してBeatufulSoupオブジェクトとして格納'''
        html = requests.get(self.url)
        soup = BeautifulSoup(html.content, "html.parser")
        self.soup = soup

        # タイトル情報を取得
        titletag_pattern = re.compile(r'(?<=<title>).*(?=</title>)')
        title_txt = str(soup.find("title"))
        title_txt = re.search(titletag_pattern,title_txt).group()
        self.pagetitle = title_txt

    def check_link_validation(self)-> bool:
        '''生成したURLが適正かどうか検査する'''
        self.flag = False if self.error_title in self.pagetitle else True
        return self.flag

    def set_url(self,problem)-> None:
        '''問題情報からURL文字列を生成し、インスタンス変数に格納する'''
        # 受けとった情報を成型
        conname,connum,conalp = problem
        connum = "{:0=3}".format(int(connum))
        self.contest_string = conname.lower()
        self.contest_no = connum
        self.problem_no = conalp.lower()

        # エッジケース(古いURL様式)の場合は訂正
        if   conname=="ABC".lower() and int(connum) <= self.abc_edge_contest:
            conalp = self.oldabc_dict[conalp]
        elif conname=="ARC".lower() and int(connum) <= self.arc_edge_contest:
            conalp = self.oldabc_dict[conalp]

        # URL生成
        url = self.base_url
        url = self.base_url.replace("*", conname.lower() + connum) + "_" + conalp
        self.url = url
        return
    
    def set_problem(self,problem: list)-> bool:
        '''問題情報を元に問題に関する一連の情報を取得'''
        self.set_url(problem)   # URLを取得 
        self.get_sourse()       # URLをもとにソースを取得
        
        if not(self.check_link_validation()):
            return False

        self.get_samples()      # ソースデータをもとにサンプル入出力データを取得

        return True
    
    def get_samples(self):
        '''サンプル入出力を取得'''
        soup = self.soup
        slice_pattern = re.compile(r"(?<=<pre>).*(?=</pre>)", re.DOTALL)
        split_pattern = r"\r\n"
        input_label = "入力例"
        output_label = "出力例"

        # サンプル入出力をブロックごとに分割して抜き出す
        sample_io_sources = soup.find_all('div', class_='part') 
        temp_sample = str()

        for i,blockdata in enumerate(sample_io_sources):
            #print(blockdata); print("\n\n")
            blockstring = str(blockdata)

            if (input_label not in blockstring) and (output_label not in blockstring):
                continue 

            temp_sample = re.findall(slice_pattern,blockstring) # ブロックから文字列部分のみを抜き出す
            sampledata = re.sub(split_pattern,'\n', temp_sample.pop())                                # 改行文字列を変換
            #print(sampledata)
            if input_label in blockstring:
                self.sample_inputs.append(sampledata)

            if output_label in blockstring:
                self.sample_outputs.append(sampledata)

        return 
    





def main()-> int:
    atp = AtCoderProblem()
    contest_string = ["ABC","65","a"]

    print(atp.set_problem(contest_string))
    print(atp.pagetitle,":",atp.url)
    print(atp.sample_inputs)
    print(atp.sample_outputs)


    return 0

if __name__ == '__main__':
    main()