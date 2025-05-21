import matplotlib.pyplot as plt
import base64
from io import BytesIO
import math

def Output_Graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img = buffer.getvalue()
    graph = base64.b64encode(img).decode("utf-8")
    buffer.close()
    return graph

def Plot_Graph(x, y):
    plt.switch_backend("AGG")
    plt.figure(figsize=(10, 5))
    plt.bar(x, y, color='skyblue')

    plt.xticks(rotation=45)
    plt.title("Daily Sales")
    plt.xlabel("Date")
    plt.ylabel("Revenue")

    # 数値の精度を保証し、Y軸の範囲を適切に設定
    y_int = [int(value) for value in y] 
    max_y = max(y_int) if y_int else 0

    # 1000円単位で丸めてY軸を調整
    plt.ylim(0, math.ceil(max_y / 1000) * 1000)

    # Y軸の目盛りを強調
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    graph = Output_Graph()
    plt.close()
    return graph