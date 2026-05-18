"""Render the ECGCNN architecture diagram with Kyrgyz labels.

Mirrors training/plot_ecg_cnn_architecture.py but emits Cyrillic strings.
Output: Figure_ecg_cnn_architecture_KG.png in the Мастер folder.
"""

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

OUT = Path(r"C:\Users\enazarkulov\Documents\Мастер") / "Figure_ecg_cnn_architecture_KG.png"
INPUT_LEN = 500

COLORS = {
    "conv": ("#A8C4F0", "#4A78C8"),
    "pool": ("#F4A6A6", "#D26464"),
    "fc":   ("#B7E4B7", "#5FB35F"),
    "gap":  ("#FFD580", "#D99A40"),
}

stages = [
    ("conv", "Conv-1",     1,  64,  INPUT_LEN,       f"{INPUT_LEN} x 64"),
    ("pool", "",           1,  64,  INPUT_LEN // 2,  ""),
    ("conv", "ResBlock-1", 2,  128, INPUT_LEN // 2,  f"{INPUT_LEN // 2} x 128"),
    ("pool", "",           1,  128, INPUT_LEN // 4,  ""),
    ("conv", "ResBlock-2", 2,  256, INPUT_LEN // 4,  f"{INPUT_LEN // 4} x 256"),
    ("pool", "",           1,  256, INPUT_LEN // 8,  ""),
    ("conv", "ResBlock-3", 2,  512, INPUT_LEN // 8,  f"{INPUT_LEN // 8} x 512"),
    ("pool", "",           1,  512, INPUT_LEN // 16, ""),
    ("conv", "ResBlock-4", 2,  512, INPUT_LEN // 16, f"{INPUT_LEN // 16} x 512"),
    ("gap",  "GAP",        1,  512, 1,               "1 x 512"),
    ("fc",   "FC-1",       1,  256, 1,               "1 x 256"),
    ("fc",   "FC-2",       1,  128, 1,               "1 x 128"),
    ("fc",   "FC-3",       1,  5,   1,               "1 x num_classes"),
]

fig, ax = plt.subplots(figsize=(20, 9))
ax.set_xlim(0, 110)
ax.set_ylim(0, 50)
ax.set_aspect("equal")
ax.axis("off")

sig_x0, sig_x1 = 1.5, 11.5
sig_y_center = 25
t = np.linspace(0, 1, 800)


def ecg_wave(t):
    y = np.zeros_like(t)
    for cycle in range(3):
        c = 0.15 + cycle * 0.3
        y += 0.15 * np.exp(-((t - c + 0.05) ** 2) / 0.0008)
        y += -0.25 * np.exp(-((t - c + 0.02) ** 2) / 0.00015)
        y += 1.4 * np.exp(-((t - c) ** 2) / 0.00008)
        y += -0.35 * np.exp(-((t - c - 0.018) ** 2) / 0.0002)
        y += 0.35 * np.exp(-((t - c - 0.08) ** 2) / 0.0015)
    return y


sig_y_plot = sig_y_center + ecg_wave(t) * 3.2
sig_x_plot = sig_x0 + t * (sig_x1 - sig_x0)
ax.plot(sig_x_plot, sig_y_plot, color="#C0392B", linewidth=1.4)
ax.add_patch(Polygon(
    [(sig_x0 - 0.3, sig_y_center - 8), (sig_x1 + 0.3, sig_y_center - 8),
     (sig_x1 + 0.3, sig_y_center + 8), (sig_x0 - 0.3, sig_y_center + 8)],
    closed=True, fill=False, edgecolor="#222", linewidth=1.0))
ax.text((sig_x0 + sig_x1) / 2, sig_y_center - 9.6,
        "Кириш ЭКГ\n1 канал, узундугу L = 500",
        ha="center", va="top", fontsize=10, color="#222")


def block_dims(channels, length):
    w = 0.6 + 1.6 * math.log2(max(length, 1) + 1) / math.log2(INPUT_LEN + 1) * 4
    h = 3 + 14 * (math.log2(channels) / math.log2(512))
    return w, h


def draw_block(ax, x, y_center, w, h, depth, fcolor, scolor, lw=0.9):
    front = [(x, y_center - h / 2), (x + w, y_center - h / 2),
             (x + w, y_center + h / 2), (x, y_center + h / 2)]
    ax.add_patch(Polygon(front, closed=True, facecolor=fcolor,
                         edgecolor="#222", linewidth=lw))
    top = [(x, y_center + h / 2), (x + w, y_center + h / 2),
           (x + w + depth, y_center + h / 2 + depth),
           (x + depth, y_center + h / 2 + depth)]
    ax.add_patch(Polygon(top, closed=True, facecolor=scolor,
                         edgecolor="#222", linewidth=lw))
    right = [(x + w, y_center - h / 2), (x + w + depth, y_center - h / 2 + depth),
             (x + w + depth, y_center + h / 2 + depth), (x + w, y_center + h / 2)]
    ax.add_patch(Polygon(right, closed=True, facecolor=scolor,
                         edgecolor="#222", linewidth=lw))


cursor_x = 13.5
y_center = sig_y_center
depth_3d = 0.9
stage_positions = []

for (group, label, repeats, ch, length, dims_label) in stages:
    w, h = block_dims(ch, length)
    fc, sc = COLORS[group]

    if group == "fc":
        bar_w = 1.6
        bar_h = max(2.0, h * 0.45)
        draw_block(ax, cursor_x, y_center, bar_w, bar_h, depth_3d, fc, sc)
        stage_positions.append((label, cursor_x + bar_w / 2,
                                y_center + bar_h / 2 + depth_3d))
        ax.text(cursor_x + bar_w / 2 + depth_3d / 2,
                y_center - bar_h / 2 - 1.8,
                dims_label, ha="center", va="top", fontsize=9, color="#222")
        cursor_x += bar_w + 2.8
        continue

    if group == "gap":
        bar_w = 1.4
        bar_h = h * 0.55
        draw_block(ax, cursor_x, y_center, bar_w, bar_h, depth_3d, fc, sc)
        stage_positions.append((label, cursor_x + bar_w / 2,
                                y_center + bar_h / 2 + depth_3d))
        ax.text(cursor_x + bar_w / 2 + depth_3d / 2,
                y_center - bar_h / 2 - 1.8,
                dims_label, ha="center", va="top", fontsize=9, color="#222")
        cursor_x += bar_w + 3.0
        continue

    spacing = 0.45
    stack_left = cursor_x
    for r in range(repeats):
        draw_block(ax, cursor_x, y_center, w, h, depth_3d, fc, sc)
        cursor_x += w + spacing
    stack_right = cursor_x - spacing

    if label:
        stage_positions.append((label, (stack_left + stack_right) / 2,
                                y_center + h / 2 + depth_3d))
    if dims_label:
        ax.text((stack_left + stack_right) / 2 + depth_3d / 2,
                y_center - h / 2 - 1.4,
                dims_label, ha="center", va="top", fontsize=9, color="#222")

    cursor_x += 0.4

for i, (label, cx, top_y) in enumerate(stage_positions):
    is_tail = label in ("GAP", "FC-1", "FC-2", "FC-3")
    if is_tail:
        offset = {"GAP": 1.4, "FC-1": 3.2, "FC-2": 5.0, "FC-3": 6.8}[label]
        y = top_y + offset
    else:
        y = top_y + 1.4 + (1.6 if i % 2 == 0 else 0.0)
    color = "#1F8C8C" if not label.startswith("FC") else "#2E7D32"
    ax.text(cx, y, label, ha="center", va="bottom",
            fontsize=11, color=color, fontweight="bold")
    ax.plot([cx, cx], [top_y, y - 0.2], color="#888", linewidth=0.6)

ax.text(55, 47, "ECGCNN архитектурасы",
        fontsize=22, fontweight="bold", ha="center", color="#222")
ax.text(55, 44.2,
        "4 калдыктык блогу бар 1Б-ЖНТ  ·  ecg_cnn_pytorch.py",
        fontsize=11, ha="center", color="#666")

legend_items = [
    ("конволюция + BN + ReLU", COLORS["conv"]),
    ("максимум пулинг",        COLORS["pool"]),
    ("глобалдык орточо пулинг", COLORS["gap"]),
    ("толук байланышкан + ReLU", COLORS["fc"]),
]
lx0, ly0 = 80, 8
for i, (text, (fc, sc)) in enumerate(legend_items):
    yy = ly0 - i * 2.2
    draw_block(ax, lx0, yy, 1.6, 1.4, 0.45, fc, sc)
    ax.text(lx0 + 2.6, yy, text, fontsize=10, va="center", color="#222")

plt.tight_layout()
plt.savefig(OUT, dpi=180, bbox_inches="tight", facecolor="white")
print(f"Saved diagram to {OUT}")
