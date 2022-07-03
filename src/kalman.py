import  numpy   as np
import  pandas  as pd
import  matplotlib
matplotlib.use('Agg')
import  numpy.linalg        as la
import  matplotlib.pyplot   as plt


###
### 読み込み
###
df  = pd.read_csv('../data/input_data.csv')
# print(df)

k   = df['k'].values
z   = df['z'].values

#
# print(k)
'''
[-15 -14 -13 -12 -11 -10  -9  -8  -7  -6  -5  -4  -3  -2  -1   0   1   2
   3   4   5   6   7   8   9  10  11  12  13  14  15]
'''

#
# print(z)
'''
[162.1746 139.5805 113.8133  94.3372  74.7258  59.3817  41.4117  26.5951
  20.1832   8.8816   1.8636  -5.0213  -5.8861  -5.7711  -4.9332  -1.9845
   2.0593  12.3849  17.9044  30.1826  41.1677  55.7128  74.2944  93.7607
 112.6638 134.9818 162.7143 188.961  219.6236 248.9036 281.3082]
'''

# k = [odd, even]
w_aves = np.array([0, 0])
w_vars = np.array([1, 4])



###
### 状態方程式
### x' = A x + B u + v~
### x(k+1) = F(k) x(k) + G(k) u(k) + v(k)
###

def show(obj):
    print(f'type:{type(obj)}\nshape:{obj.shape}')

def init_H(k, detail=False):
    H = []
    ls = k.tolist()

    for n in ls:
        tmp = [1, n, n**2]
        H.append(tmp)

    H = np.array(H)

    if detail:
        show(H)

    return H

def init_R(k, w_vars, detail=False):
    ls  = k.tolist()
    R   = []

    for n in ls:
        tmp = 0
        if (n % 2) != 0:
            tmp = w_vars[0]
        else:
            tmp = w_vars[1]
        
        R.append(tmp)

    R = np.diag(np.array(R))

    if detail:
        show(R)

    return R

###
### A @ B       := 行列積演算子
### la.inv(A)   := 逆行列計算
### A.T         := 転置行列計算
###


###
### カルマンフィルタ
###
def kalman(k, z, w_vars, i=6, j=6):
    
    ans = []

    # 初期化
    # X : 推定値
    X = np.zeros((3,1))
    # P : 推定値誤差共分散行列
    P = np.eye(3) * (10**i)
    # Q : プラント雑音の共分散行列
    Q = np.eye(3) / (10**j)
    # F(k)
    F = np.eye(3)
    # G(k)
    G = np.eye(3)
    # u(k)
    u = np.zeros((3, 1))

    h = init_H(k)
    # print(h)
    r = init_R(k, w_vars)
    # print(r)

    for i in range(len(k)):
        # H(k+1)
        H = h[i].reshape(-1,3)

        # R(k+1)
        R = r[i][i]

        ###
        ### 予測
        ###
        # \hat{x}(k+1|k) 
        # = F(k) * \hat{x}(k|k) + G(k) * u(k)
        X = F @ X + G @ u

        # P(k+1|k) 
        # = F(k) * P(k|k) * F(k).T + Q(k)
        P = F @ P @ F.T + Q

        ###
        ### 更新
        ###
        # \hat{z}(k+1|k) 
        # = H(k+1) * \hat{x}(k+1|k)
        Z = H @ X

        # v(k+1) 
        # = z(k+1) - \hat{z}(k+1|k)
        V = z[i] - Z
        # print(f'{V},{z[i]},{Z}')


        # S(k+1)
        # = H(k+1) * P(k+1|k) * H(k+1).T + R(k+1) 
        S = H @ P @ H.T + R
        # print(f'{S},{R}')


        # W(k+1) 
        # = P(k+1|k) * H(k+1).T * inv(S(k+1))
        W = P @ H.T @ la.inv(S)

        # \hat{x}(k+1|k+1) 
        # = \hat{x}(k+1|k) + W(k+1) * v(k+1) 
        X = X + W @ V

        # P(k+1|k+1) 
        # = P(k+1|k) - W(k+1) * S(k+1) * W(k+1).T
        P = P - W @ S @ W.T

        ans.append(X.reshape(3,))

    return ans


def implot(ans, i=6, j=6):
    
    ### 初期化
    plt.figure()
    plt.ylim(-5, 5)

    ### 真値
    plt.hlines(4, 0, 31, color="black")
    plt.hlines(1, 0, 31, color="black")
    plt.hlines(-3, 0, 31, color="black")

    ### 予測値
    plt.plot(ans)
    plt.xticks([i for i in range(0, 30+2, 2)], \
                [i for i in range(-15, 15+1, 2)])
    plt.grid()
    plt.title(f'i={i}, j=-{j}')
    plt.legend(['x0^', 'x1^', 'x2^', 'x0', 'x1', 'x2'])
    plt.xlabel("k")
    plt.ylabel("Predicted")
    plt.savefig(f'../result/kalman_P_{pow(10, i)}_Q_{pow(10, j)}.png')

###
### (1) 実行と出力
###
ans = kalman(k, z, w_vars)
print(f'ans={ans[-1]}')
implot(ans)


###
### (2) 初期共分散の値の変更
###

### P(0)の値を変更
for i in range(-1, 8):
    ans = kalman(k, z, w_vars, i=i)
    print(f'ans({i}, -6) = {ans[-1]}')
    implot(ans, i=i)

### Qの値を変更
for j in range(-1, 8):
    ans = kalman(k, z, w_vars, j=j)
    print(f'ans(6, {-j}) = {ans[-1]}')
    implot(ans, j=j)