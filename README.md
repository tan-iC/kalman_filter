
# カルマンフィルタの実装

- カルマンフィルタの観測値推定
- 定数値のベクトル$\boldsymbol{x} = [x_0, x_1, ...x_n]^T$を推定する

## k番目の観測方程式

$$ z(k) = \boldsymbol{H}(k)\boldsymbol{x} + w(k) $$

## k番目の誤差共分散

$$R(k) = E[w(k)w(k)^T]$$

今回は特に $$ \boldsymbol{H}(k) = [1, k, k^2]$$,$$\boldsymbol{x} = [x_0, x_1, x_2]^T $$

## カルマンフィルタ

- k番目の推定値をもとにk+1番目の推定値を求める
- 初期化
  $$\boldsymbol{\hat{x}}(0) = [0, 0, ..., 0]^T$$
  $$\boldsymbol{P}(0) = \mathbf{diag}[10^a, 10^a, ..., 10^a]$$
  $$\boldsymbol{Q} = \mathbf{diag}[10^{-a}, 10^{-a}, ..., 10^{-a}]$$

1. 観測予測誤差共分散

1. 観測予測値

1. 観測予測誤差共分散 $$\boldsymbol{S}(k+1) = \boldsymbol{H}(k+1)\boldsymbol{P}(k)\boldsymbol{H}^T(k+1)+\boldsymbol{R}(k+1)$$

1. フィルタゲイン $$\boldsymbol{W}(k+1) = \boldsymbol{P}(k)\boldsymbol{H}^T(k+1)\boldsymbol{S}^{-1}(k+1)$$

1. 推定値 $$\boldsymbol{\hat{x}}(k+1) = \boldsymbol{\hat{x}}(k) + \boldsymbol{W}(k+1) [z(k+1) - \boldsymbol{H}(k+1) \boldsymbol{\hat{x}} (k)]$$

1. 推定誤差共分散 $$\boldsymbol{P}(k+1) = \boldsymbol{P}(k)-\boldsymbol{W}(k+1)\boldsymbol{S}(k+1)\boldsymbol{W}^T(k+1)$$

## リポジトリ内容

- ```src```: ソースコード

- ```data```: 観測データ

- ```result```: カルマンフィルタでの推定値の推移をプロットしたグラフ

- ```README.md```: このファイル
