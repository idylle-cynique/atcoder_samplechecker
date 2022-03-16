# ABC161 - D

'''
 パッと思いつくのは10**5番目のルンルン数が含まれるくらいの大きな値Nを用意して
 1～Nまでの数を全探索してひとつひとつルンルン数であるかを判定していく、というものだが
 妥当なNの値を想起するのが容易ではないうえ、TLEになる可能性が極めて高い
 ルンルン数のパターンは規則的で、生成がそれほど難しくないことに着目して、
 ルンルン数にあたる数を10**5番目に当たる数が含まれるくらいまで生成していき、
 最後にソートしたルンルン数リストから、入力値に対応するインデックスに格納されたルンルン数を出力する、
 というようにすればよい。
 このルンルン数の生成には幅優先探索がおあつらえ向きで、出題意図もこの部分の実装を求めるものであると思われる
'''

from collections import deque

K = int(input())
LunLunNumbers = set([1,2,3,4,5,6,7,8,9]) # ルンルン数リストは集合型で管理。一桁のルンルン数は事前に格納しておく

def LunLun_BFS(k):
    search_queue = deque([1,2,3,4,5,6,7,8,9]) # 一桁目までのルンルン数を探索キューに格納
    cnt = 9 # ここまでで9個のルンルン数の探索を終えている

    while(cnt <= 10**5*2): # 10**5番目までのルンルン数の探索が終わるくらいまで探索を続ける
        v = search_queue.popleft()
        #print(search_queue)

        tmp = v*10 + v%10 # 取り出したルンルン数の一桁目との差が0であるルンルン数を生成してリストに格納
        search_queue.append(tmp)
        LunLunNumbers.add(tmp)
        cnt += 1  
        
        if v%10 != 0:     # 取り出したルンルン数の一桁目が0でない場合
            tmp = v*10 + v%10-1 # 取り出したルンルン数の一桁目との差が-1であるルンルン数を生成してリストに格納
            search_queue.append(tmp)
            LunLunNumbers.add(tmp)
            cnt += 1
            
        if v%10 != 9:     # 取り出したルンルン数の一桁目が9でない場合
            tmp = v*10 + v%10+1 # 取り出したルンルン数の一桁目との差が+1であるルンルン数を生成してリストに格納
            search_queue.append(tmp)
            LunLunNumbers.add(tmp)
            cnt += 1
    
    return True


ans = LunLun_BFS(K)
LunLunNumbers = sorted(LunLunNumbers) # リストに直してソート

print(LunLunNumbers[K-1]) # Kの値に対応するインデックスのルンルン数を出力