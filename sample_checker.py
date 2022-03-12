import os, time, filecmp, json
import requests, webbrowser
import re
from bs4 import BeautifulSoup

import timechecker

class AtCoderSample:
    url = ""
    title = ""
    input_samples = []
    output_samples = []
    dirpath = ""
    codepath = ""
    contests = ["ABC", "ARC", "AGC"]

    def __init__(self): # 問題のリンクと基本情報を取得
        pass

    def resolve_string(self,contest,number,alphabet):
        '''
            AtCoderSampleクラスに必要な基本情報を生成
        '''
        if not(contest and number and alphabet): # いずれも空でないことを確認
            return False
        
        number = "{:0=3}".format(int(number)) # 0埋めした文字列に変換

        # 問題タイトルを用意
        self.title = contest+number + "-" + alphabet

        # 問題URLを用意
        url_stra = contest.lower() + number
        url_strb = contest.lower() + number + "_" + alphabet.lower()
        print(self.title, url_stra, url_strb)
        self.url = "https://atcoder.jp/contests/{:}/tasks/{:}".format(url_stra,url_strb)

        print(self.url)
        return self.resolve_url() # 更にURLリゾルバに潜らせてからメインプログラムに真理値を返す

    def resolve_url(self,recheck=False):
        '''
            現在のコンテストのURL表記と過去のコンテストのURL表記とが異なる場合があるので、別途URLの文字列解決を行う
        '''
        
        # 現在のコンテストではアルファベット表記の問題が、以前は数字で表記されているので置き換える必要がある
        oldabc_dict = {"a":"1", "b":"2", "c":"3", "d":"4", "e":"5", "f":"6", "g":"7", "h":"8"}

        html = requests.get(self.url)
        soup = BeautifulSoup(html.content, "html.parser")
        pagetitle = str(soup.find("title"))
        print(pagetitle)

        if "404 Not Found" in pagetitle and recheck == False:  # 再チェック処理でないなら修整処理を施す
            print("リンクを修正します")
            contestring = self.title.lower().split("-")
            contestring[-1] = oldabc_dict[contestring[-1][0]]
            self.url = "https://atcoder.jp/contests/{:}/tasks/{:}".format(contestring[0], "_".join(contestring))
            print(self.url)
            return self.resolve_url(recheck=True) # リンクが適正か再チェック
        elif "404 Not Found" in pagetitle and recheck == True: # 再チェックしてなおリンクが不正ならFalseを返す
            return False
        else:                                                  # 適切に修整された場合はTrueを返す
            return True

    def start_samplecheck(self):
        self.get_sample()
        self.make_dirs() # サンプル入出力データ格納用のディレクトリを生成してそのファイルパスを得る
        self.make_sampletext() # サンプル入出力データをテキストで出力
        
        return self.check_answer()

    def get_sample(self):
        ''' 
            サンプルデータを入力・出力別に取得
            事前にresolve_url()を用いて問題リンクが適正であることを確認しておくこと    
        '''

        html = requests.get(self.url)
        soup = BeautifulSoup(html.content, "html.parser")

        # 入出力例にあたる部分だけ抜き出す
        IOSamples = soup.find_all('div', class_='part') 
        SlicePattern = re.compile(r"(?<=<pre>).*(?=</pre>)", re.DOTALL)
        SplitPattern = r"\r\n"

        self.input_samples = []
        self.output_samples = []

        for element in IOSamples:
            element = str(element)

            if "入力例" in element:
                #print("HERE"); print(element,"\n")
                sample = re.findall(SlicePattern,element)
                self.input_samples.append(re.sub(SplitPattern, "\n", sample.pop()))
                continue

            if "出力例" in element:
                #print("here"); print(element,"\n\n\n")
                sample = re.findall(SlicePattern,element)
                self.output_samples.append(re.sub(SplitPattern, "\n", sample.pop()))
                continue

    def make_dirs(self): 
        # サンプルデータを格納するためのディレクトリを生成
        for contest in self.contests:
            if contest in self.title:
                dir_name = contest
        
        path = os.path.abspath(os.path.join(dir_name+'_Samples'))
        if not(os.path.exists(path)): # 保存用のディレクトリが存在しなければ新規作成
            os.mkdir(path)
        self.dirpath = path
        
        path = os.path.abspath(os.path.join(dir_name+'_Answers'))
        if not(os.path.exists(path)):
            os.mkdir(path)
        self.codepath = path
            
    def make_sampletext(self):
        filepath = self.dirpath
        length = len(self.input_samples)
        print(filepath)
        for No in range(length):
            # No番目のサンプルケースの入力例をテキストファイルで出力
            filename = self.title+'_{:0=2}i.txt'.format(No+1)
            samplepath = os.path.join(filepath, filename) # ソートしても順序が荒れないよう0埋め
            with open(samplepath, 'w', encoding='UTF-8') as inputdata:
                #print(self.input_samples[No])
                inputdata.write(self.input_samples[No].lstrip("\n"))

            # No番目のサンプルケースの入力例をテキストファイルで出力e
            filename = self.title+'_{:0=2}o.txt'.format(No+1)
            samplepath = os.path.join(filepath, filename) # ソートしても順序が荒れないよう0埋め
            with open(samplepath, 'w', encoding='UTF-8') as outputdata:
                #print(self.output_samples[No])
                outputdata.write(self.output_samples[No].lstrip("\n"))
    
    def check_answer(self):
        # ディレクトリから対象のファイルを抜き出して実行
        '''
            1) ファイルを実行・同時に処理時間を計測
            2) タイムオーバーならTLEを返す
            3) エラー出力の場合はREを返す
            4) つきあわせた二つのファイルが異なる場合にはWA、等しい場合にはACを返す
        '''

        with open("settings.json","r",encoding="UTF-8") as f:
            settings = json.load(f)

        if "ABC" in self.title:
            code_dirpath = settings["abc_dirpath"]
        elif "ARC" in self.title:
            code_dirpath = settings["arc_dirpath"]
        else:
            code_dirpath = settings["agc_dirpath"]

        print(code_dirpath,settings)
        codefile = os.path.join(code_dirpath,self.title+".py")

        if not(os.path.exists(codefile)):
            print("解答コードがありませんでした")
            return False


        return_data = {}
        for n in range(1,10**2):
            filename = f"{self.title}_{n:0=2}"
            sample = os.path.join(self.dirpath,filename+"i.txt")
            answer = os.path.join(self.codepath,filename+"answer.txt")
            error = os.path.join(self.codepath,filename+"error.txt")
            sample_o = os.path.join(self.dirpath,filename+"o.txt")
            temp_data = {}
            if os.path.exists(sample): # 同名のサンプル入力が存在するなら解答の出力を行う
                #print(codefile, sample, answer, error)
                temp_data["sample_i"] = sample
                temp_data["sample_o"] = sample_o
                temp_data["answer"] = answer
                temp_data["error" ] = error
                temp_data["judge"] = None

                language = "python"

                '''
                    {python 解答コード.py < サンプル入力.txt > 解答コード出力 2> 解答エラー出力}
                    また、スペース(空白)を含むパス文字列が入る可能性もあるので、
                    ダブルクオーテーションでファイル名を囲んでまとまった文字列であることを明示しておくこと
                '''
                commandline = f'{language} "{codefile}" < "{sample}" 1> "{answer}" 2> "{error}"'
                print(commandline)
                
                timer = timechecker.TimeChecker(os.system,commandline) # TimeCheckerクラスで解答時間をチェック
                timer.start_timer()

                if timer.elapsed_time > timer.set_time: # TLE判定
                    print(f"{filename}は処理に時間が掛かり過ぎている……")
                    temp_data["judge"] = "TLE"
                elif filecmp.cmp(answer,sample_o):      # AC判定
                    temp_data["judge"] = "AC"
                else:
                    with open(error,"r") as err:        # RE判定
                        string = err.read()
                        if len(string) > 0:
                            temp_data["judge"] = "RE"
                        else:                           # WA判定
                            temp_data["judge"] = "WA"
                return_data[n] = temp_data                
            else:
                return return_data

    
    def browse_question(self): # 問題内容を確認
        webbrowser.open(self.url)



def main():
    url = r"https://atcoder.jp/contests/arc012/tasks/arc012_b"
    
    temp = AtCoderSample(url)
    flag = temp.resolve_url()

    temp.make_dirs()
    temp.get_sample()
    print(temp.dirpath)

    print(temp.input_samples); print(temp.output_samples)

    temp.make_sampletext()



if __name__ == "__main__":
    main()

    