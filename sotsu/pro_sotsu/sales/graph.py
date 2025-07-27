import matplotlib.pyplot as plt
import base64
from io import BytesIO
import math
import pandas as pd
import numpy as np

def Output_Graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=150) # 解像度を少し上げる
    buffer.seek(0)
    img = buffer.getvalue()
    graph = base64.b64encode(img).decode("utf-8")
    buffer.close()
    return graph

def Plot_Enhanced_Graph(x_dates, y_values):
    # スタイルを適用して見た目をリッチに
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.switch_backend("AGG")
    fig, ax = plt.subplots(figsize=(12, 6)) # fig, ax を使うとより細かい設定が可能

    # --- DataFrameを作成して移動平均を計算 ---
    df = pd.DataFrame({'Date': pd.to_datetime(x_dates), 'Revenue': y_values})
    df = df.sort_values('Date')
    # 3日移動平均を計算 (窓のサイズはデータ量に応じて調整)
    df['Moving_Average_3D'] = df['Revenue'].rolling(window=3).mean()

    # --- グラフの描画 ---
    # グラデーションカラーの棒グラフ
    colors = plt.cm.Blues(np.linspace(0.4, 1, len(df['Revenue'])))
    bars = ax.bar(df['Date'], df['Revenue'], color=colors, width=0.6, label='Daily Sales')

    # 棒の上に数値を表示
    ax.bar_label(bars, fmt='¥{:,}', padding=3, fontsize=9, color='dimgray')

    # 移動平均線をプロット
    ax.plot(df['Date'], df['Moving_Average_3D'], color='crimson', marker='o', 
            linestyle='--', linewidth=2, markersize=5, label='3-Day Moving Average')
    
    # --- デザインとラベルの設定 ---
    ax.set_title("Daily Sales Performance", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Revenue (JPY)", fontsize=12)

    # Y軸のフォーマットを3桁区切りに
    ax.yaxis.set_major_formatter('{x:,.0f}')
    
    # X軸の日付の表示を調整
    fig.autofmt_xdate(rotation=45) 
    
    ax.legend()
    ax.grid(axis='y', linestyle=':', alpha=0.7)
    plt.tight_layout()

    graph = Output_Graph()
    plt.close()
    return graph
