# ARC005 - C

# 01-BFSと呼ばれるBFSの発展アルゴリズムを用いて解く問題
# グリッド上の各マスへ到達するための最小コストを求め、ゴールに当たるマスがコスト要件を満たすならYES, そうでないならNOを返すというもの
# 通常の迷路などと異なり、ただの道マスに遷移するだけならコストは0、壁マスに遷移する場合はコストは1、というふうに定められている
# すると、道だけを経由して到達できる場所には可能な限り道だけで行き、そうせざるを得ないときだけ壁マスを破壊する、というふうにしたい
# パッとは思いつきにくいが、幅優先探索(BFS)を行うにあたって
# 1) 遷移コスト0のマス(道)を発見した時は、探索用両端キューの先頭に加え、優先的に探索を行えるようにする
# 2) 遷移コスト1のマス(壁)を発見した時は、探索用両端キューの末尾に加え、遷移コスト0のマスの探索が全て終わり次第探索を行うようにする
# とすることで、最小コストで各マスの探索を行うことができる

# 公式な解説が存在しないので、今回は以下の解説サイトを参考にした
# https://betrue12.hateblo.jp/entry/2018/12/08/000020

from collections import deque
from copy import deepcopy

H,W = map(int,input().split())
GridMap = []
CostMap = [[-1 for x in range(W+2)] for y in range(H+2)]

dy = [-1, 0,+1, 0]
dx = [ 0,+1, 0,-1]

for i in range(H+2): # グリッド情報を受取
    if i == 0 or i == H+1:
        GridMap.append(list("x"*(W+2)))
    else:
        GridMap.append(list("x" + input() + "x"))
        
for j in range(H+2): # グリッド情報をもとにコストマップとスタート・ゴール地点の情報を得る
    for i in range(W+2):
        if GridMap[j][i] == "x":   # 壁なら大きな値を入れておく
            CostMap[j][i] = H*W
        elif GridMap[j][i] == "s": # スタート地点の座標を得る
            sy,sx = j,i
            GridMap[j][i] = "."
        elif GridMap[j][i] == "g": # ゴール地点の座標を得る
            gy,gx = j,i
            GridMap[j][i] = "."

def view_grid(field):      # グリッド情報を出力
    for row in field:
        print("".join(row))
    return True
 
def view_distmap(distmap): # コストマップの情報を出力
    for row in distmap:
        print(row)
    return True
 
def ZeroOne_BFS(field):
    CostMap[sy][sx] = 0
    
    search_queue = deque() # 探索用両端キューを生成
    search_queue.append([sy,sx])
    
    while(len(search_queue) != 0):
        #view_distmap(CostMap); print(search_queue)
        ny,nx = search_queue.popleft() # 先頭の要素を取り出す

        for k in range(len(dx)):
            y,x = ny+dy[k],nx+dx[k]
            
            if CostMap[y][x] != -1: 
                pass
            elif field[y][x] == "#": 
                search_queue.append([y,x])      # 壁マスなら両端キューの末尾に追加
                CostMap[y][x] = CostMap[ny][nx]+1 # 最小コスト + 壁遷移(破壊)コスト が最小コストになる
            elif field[y][x] == ".":
                search_queue.appendleft([y,x])  # 道マスなら両端キューの先頭に追加
                CostMap[y][x] = CostMap[ny][nx]   # 最小コスト + 道遷移(0)コスト が最小コストになる
            else:
                pass

    return True

#view_grid(GridMap)#; view_distmap(DistMap)
Field = deepcopy(GridMap)
ZeroOne_BFS(GridMap) # 01-BFSで各マスへ遷移するための最小コストを計算したマップを生成
#view_distmap(CostMap)

if CostMap[gy][gx] < 3: # ゴール地点への到達最小コストが2以下ならYES
    print("YES")
else:                   # 3以上ならNO
    print("NO")