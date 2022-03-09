
import os, json, re
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as st
import tkinter.font as font
import tkinter.messagebox as messagebox
import webbrowser

import sample_checker # 自前のプログラム

class AtCoderMainWindow:
    def __init__(self):
        self.make_objects()
        self.set_style()
        self.make_window()
        self.make_sampleframe()
        self.make_buttons()
        self.make_widgets()
    
    def set_style(self):
        framefontstyle = ttk.Style()
        framefontstyle.configure("Main.TRadioButton",font=("HackGen Console Regular",36))
        self.radiostyle = "Main.TRadiobutton"

    def make_objects(self):
        # メインウィンドウの設定
        self.root = tk.Tk()
        self.root.title("AtCoder Samplecheck Automater")
        self.root.resizable(width=False, height=False)

        # サンプルチェックのためのオブジェクトを生成
        self.checksystem = sample_checker.AtCoderSample()
            
    def make_window(self):
        # メインフレームの設定
        self.frame = ttk.Frame(self.root,)
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        self.frame.propagate(False) 

        self.sampleframe = ttk.Frame(self.root,)
        self.sampleframe.propagate(False)
        self.sampleframe.grid(row=1, column=0,
                              padx=10, pady=5,)

    def make_sampleframe(self):
        # スクロールテキストボックスの設定
        box_length=80
        box_height=12
        self.sample_input  = st.ScrolledText(self.sampleframe,    font=("HackGen Console Regular",12),
                                             width=box_length,    height=box_height*2//3)
        self.mycode_output = st.ScrolledText(self.sampleframe,    font=("HackGen Console Regular",12),
                                             width=box_length//2, height=box_height)
        self.sample_output = st.ScrolledText(self.sampleframe,    font=("HackGen Console Regular",12),
                                             width=box_length//2, height=box_height)
        
        height = 0
        self.sample_input.grid(row=1, column=0, columnspan=2,
                      padx=5, ipady=height*2//3,
                      sticky=tk.E+tk.W)
        self.mycode_output.grid(
                      row=3, column=0,
                      padx=5, ipady=height,)
        self.sample_output.grid(row=3, column=1, ipady=height)


        # 各テキストボックスのラベル
        label_sample_i = ttk.Label(self.sampleframe, text="・サンプル入力")
        label_mycode_o = ttk.Label(self.sampleframe, text="・自作コードによる出力")
        label_sample_o = ttk.Label(self.sampleframe, text="・サンプルによる出力")

        label_sample_i.grid(row=0, column=0, padx=16, pady=4, sticky=tk.W)
        label_mycode_o.grid(row=2, column=0, padx=16, pady=4, sticky=tk.W)
        label_sample_o.grid(row=2, column=1, padx=16, pady=4, sticky=tk.W)

        # 解答判定テキスト
        self.judgement = tk.StringVar()
        judge_label = ttk.Entry(self.sampleframe, text=self.judgement)
        judge_label.grid(row=4, column=1, padx=10, pady=5, sticky=tk.E)

    def make_buttons(self):
        # 各種ボタンの入力値を記録するウィジェット変数を生成
        self.contestname = tk.StringVar()
        self.question = tk.StringVar()

        
        # ラジオボタンの生成
        button_names = ["ABC", "ARC", "AGC"]
        buttons = []
        for i in range(len(button_names)):
            buttons.append(ttk.Radiobutton(
                self.frame, style=self.radiostyle,
                text=button_names[i],
                variable=self.contestname,
                value = button_names[i],
                command=lambda:self.get_value()))
            buttons[i].grid(row=i+1,padx=10, pady=5)
        
        # 問題ページへのアクセスボタン
        browse_question = ttk.Button(self.frame, text="❔ 問題を確認する",                                
                                     padding=(10,10,10,10),  command=self.browse_link)
        browse_question.grid(row=2, rowspan=1, column=4, padx=10, pady=5,)        

        # 設定ボタンの生成
        settings_button = ttk.Button(self.frame, text="⚙ ディレクトリ設定",                                
                                     padding=(10,10,10,10),  command=self.settings)
        settings_button.grid(row=1, rowspan=1, column=4, padx=10, pady=5,)
        
        # 実行ボタンの生成
        exe_button = ttk.Button(self.frame, text="チェック開始",                                
                                padding=(10,36,10,36), 
                                command=lambda:self.check_code(

                                ))
        exe_button.grid(row=1, rowspan=3, column=3, padx=10, pady=5,)

        # 終了ボタンの生成
        quit_button = ttk.Button(self.frame, text="終了",command=self.quit)
        quit_button.grid(row=4, column=3,
                         padx=10, pady=5, sticky=tk.E)
    
    def make_widgets(self):
        self.contest_numbers = []
        self.contest_alphs = []
        for i in range(3):
            self.contest_numbers.append(tk.StringVar())
            self.contest_alphs.append(tk.StringVar())

        # ラベルの生成(1)
        label_strs = ["コンテストの種類", "コンテスト番号", "問題番号"]
        labels = []
        for i in range(len(label_strs)):
            labels.append(ttk.Label(self.frame,
                                    text=label_strs[i]))
            labels[i].grid(row=0, column=i,
                           padx=10, pady=5)
        
        # コンテスト番号の入力
        ent_len = 3
        text_length = 12
        self.contest_numbers= []
        for i in range(ent_len):
            self.contest_numbers.append(ttk.Entry(self.frame,
                                             width=text_length,
                                             ))
            self.contest_numbers[i].grid(row=i+1, column=1,
                                    padx=10, pady=5)
        
        # 問題番号の入力
        q_len = 3
        question_numbers = ["A","B","C","D","E","F","G","H (Ex)"]
        self.question_boxies = []
        box_length = 10
        for i in range(q_len):
            self.question_boxies.append(ttk.Combobox(self.frame, values=question_numbers,
                                                width=box_length,))
            self.question_boxies[i].set(question_numbers[0])
            self.question_boxies[i].grid(row=i+1, column=2,
                                    padx=10, pady=5)

    def get_basicinfo(self):
        con = self.contestname.get()
        if con == "ABC":
            idx = 0
        elif con == "ARC":
            idx = 1
        else:
            idx = 2
        
        num = self.contest_numbers[idx].get()
        alph = self.question_boxies[idx].get()
        print(con,num,alph,":",idx)
        return con,num,alph
               
    def check_code(self):
        con, num, alph = self.get_basicinfo()

        print("解答チェックを開始します...")

        if not(self.checksystem.resolve_string(con,num,alph)):
            messagebox.showerror(
                "問題取得エラー", 
                "チェック対象となる問題が存在しませんでした\n 「問題を確認する」ボタンから対象の問題が確かに存在するか再度チェックしてください"
            )
            return False
            # メッセージボックスを出して入力値が不正であることを示すようにしておきたい

        self.mycode_output.delete(0., tk.END)
        self.sample_input.delete(0., tk.END)
        self.sample_output.delete(0., tk.END)

        dictdata = self.checksystem.start_samplecheck()
        judgements = {"WA":0, "AC":0, "TLE":0, "RE":0}

        if not(dictdata): # チェック後解答データではなくブール値(False)が返ってきた場合
            messagebox.showerror("ファイル検出エラー", 
                "チェック対象となるコードファイルがディレクトリ内に存在しませんでした")
            return False


        for k,v in dictdata.items():
            if k == 1:
                self.sample_input.insert(tk.END,  "-"*(len(f"Sample Case No.{k:0=2}  \n")))
                self.sample_output.insert(tk.END, "-"*(len(f"Sample Case No.{k:0=2}  \n")))
                self.mycode_output.insert(tk.END, "-"*(len(f"Sample Case No.{k:0=2}  \n")))

            self.sample_input.insert(tk.END,  f"\nSample Case No.{k:0=2}  \n")
            self.sample_output.insert(tk.END, f"\nSample Case No.{k:0=2}  \n")
            self.mycode_output.insert(tk.END, f"\nSample Case No.{k:0=2}  \n")

            for key,val in v.items():
                #print(key,val)
                if key == "sample_i":
                    with open(val, "r") as f:
                        data = f.read()
                        self.sample_input.insert(tk.END,data)
                elif key == "sample_o":
                    with open(val, "r") as f:
                        data = f.read()
                        self.sample_output.insert(tk.END,data)
                elif key == "answer":
                    if v["judge"] == "AC":
                        with open(val, "r") as f:
                            data = f.read()
                            self.mycode_output.insert(tk.END,data)
                elif key == "error":
                    if v["judge"] == "RE":
                        with open(val, "r") as f:
                            data = f.read()
                            self.mycode_output.insert(tk.END,data)
                elif key == "judge":
                    judgements[val] += 1 
            self.sample_input.insert(tk.END, f"")
            self.sample_input.insert(tk.END,  "\n"+("-"*len(f"\nSample Case No.{k:0=2}  \n")))
            self.sample_output.insert(tk.END, "\n"+("-"*len(f"\nSample Case No.{k:0=2}  \n")))
            self.mycode_output.insert(tk.END, "\n"+("-"*len(f"\nSample Case No.{k:0=2}  \n")))
        
        answer_data = f"AC:{judgements['AC']} WA:{judgements['WA']} TLE:{judgements['TLE']} RE:{judgements['RE']}"
        self.judgement.set(answer_data)
        print("チェックが終了しました")
        return True
            
    def browse_link(self):
        con, num, alph = self.get_basicinfo()
        self.checksystem.resolve_string(con, num, alph)
        url = self.checksystem.resolve_url()
        print("flag", url)
        if not(url):
            messagebox.showerror(
                "問題チェックエラー",
                "指定された問題が見つかりませんでした。\nブラウザから対象の問題が確かに存在するかチェックしてください")
        self.checksystem.browse_question() # リンク先にアクセス


    def settings(self):
        print("設定ボタン押下")
        self.option_window = AtCoderOptionWindow()
        self.option_window.startup()

    def get_value(self):
        contest = self.contestname.get()
        #print(contest, widget_name)

    def startup(self):
        self.root.mainloop()
    
    def quit(self):
        self.root.destroy()


class AtCoderOptionWindow:
    def __init__(self):
        self.edit_settings(command="r")
        self.make_window()
        self.make_frame()
        self.make_widgets()

    def edit_settings(self,command="r"): # jsonファイルから設定を読込・書込
        filename = "settings.json"
        if command == "r":
            with open(filename, command,) as settings:
                self.presetting = json.load(settings)
        elif command == "w":
            with open(filename, command,) as settings:
                setting_dict = dict()
                setting_dict["abc_dirpath"] = self.abcdirpath.get()              
                setting_dict["arc_dirpath"] = self.arcdirpath.get()
                setting_dict["agc_dirpath"] = self.agcdirpath.get()
                #print(setting_dict)
                json.dump(setting_dict, settings, indent=4)
        print(command,":",self.presetting)
        return 

    def make_window(self):  # ウィンドウの設定
        self.option_window = tk.Toplevel()
        self.option_window.title("ディレクトリの設定")
        self.option_window.resizable(height=False)

    def make_frame(self):   # フレームの設定
        self.frame = tk.Frame(self.option_window)
        self.frame.grid(padx=10, pady=10)

    def make_widgets(self): # 各種ウィジェットの設定・配置
        # ラベルの設定
        abc_label = ttk.Label(self.frame, text="AtCoder Beginner Contest")
        arc_label = ttk.Label(self.frame, text="AtCoder Regular Contest")
        agc_label = ttk.Label(self.frame, text="AtCoder Grand Contest")
        abc_label.grid(row=0 , column=0, padx=10, pady=5)
        arc_label.grid(row=1 , column=0, padx=10, pady=5)
        agc_label.grid(row=2 , column=0, padx=10, pady=5)

        # ディレクトリパスを格納するための変数の設定
        self.abcdirpath = tk.StringVar()
        self.arcdirpath = tk.StringVar()
        self.agcdirpath = tk.StringVar()
        self.abcdirpath.set(self.presetting["abc_dirpath"])
        self.arcdirpath.set(self.presetting["arc_dirpath"])
        self.agcdirpath.set(self.presetting["agc_dirpath"])

        # テキストボックスの設定
        box_length = 48
        self.abc_dirpath = ttk.Entry(self.frame, width=box_length, textvariable=self.abcdirpath)
        self.arc_dirpath = ttk.Entry(self.frame, width=box_length, textvariable=self.arcdirpath)
        self.agc_dirpath = ttk.Entry(self.frame, width=box_length, textvariable=self.agcdirpath)

        self.abc_dirpath.grid(row=0, column=1, pady=5)
        self.arc_dirpath.grid(row=1, column=1, pady=5)
        self.agc_dirpath.grid(row=2, column=1, pady=5)

        # 変更ボタン
        self.abc_dirask = ttk.Button(self.frame, text="変更", command=lambda:self.push_changebutton("abc_dirpath"))
        self.arc_dirask = ttk.Button(self.frame, text="変更", command=lambda:self.push_changebutton("arc_dirpath"))
        self.agc_dirask = ttk.Button(self.frame, text="変更", command=lambda:self.push_changebutton("agc_dirpath")) 

        self.abc_dirask.grid(row=0 ,column=2 ,padx=10 ,pady=5)
        self.arc_dirask.grid(row=1 ,column=2 ,padx=10 ,pady=5)
        self.agc_dirask.grid(row=2 ,column=2 ,padx=10 ,pady=5) 

        # ラベル
        msg_label = ttk.Label(self.frame, text="各種コンテストの解答コードが保存されたディレクトリのパスを入力してください")
        msg_label.grid(row=4, column=0, columnspan=2,
                       padx=10, pady=5, sticky=tk.W)
        
        # キャンセルボタン
        self.cancel_button = ttk.Button(self.frame, text="キャンセル", command=lambda:self.quit(False))
        self.cancel_button.grid(row=4, column=1,
                      padx=10, pady=5, sticky=tk.E)

        # 設定終了(OK)ボタン
        self.OKbutton = ttk.Button(self.frame, text="OK", command=lambda:self.quit(True))
        self.OKbutton.grid(row=4, column=2,
                      padx=5, pady=5, sticky=tk.E)


    def push_changebutton(self,contest):
        if contest == "abc_dirpath":
            self.abcdirpath.get()
        if contest == "arc_dirpath":
            self.arcdirpath.get()
        if contest == "agc_dirpath":
            self.agcdirpath.get()
        #print(data,":",type(data)); print(f"{contest}の変更ボタンが押された")
    
    def startup(self): # 起動
        self.option_window.mainloop()

    def quit(self,flag): # 終了時の保存処理
        if flag:
            self.edit_settings(command="w")
        self.option_window.destroy()


def main():
    window = AtCoderMainWindow()
    window.startup()


if __name__ == '__main__':
    main()

