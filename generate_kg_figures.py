"""
Generate Kyrgyz-labeled variants of the five non-geometry result figures.

The Turkish/English originals are produced by:
  - generate_v4_reports.py    -> Figure_seq_length_comparison.png    (TR)
  - parse_results.py          -> Figure_hybrid_*.png                 (EN)

This script does NOT modify those originals; it only writes:
  - Figure_seq_length_comparison_KG.png
  - Figure_hybrid_headline_KG.png
  - Figure_hybrid_inference_KG.png
  - Figure_hybrid_perclass_top_KG.png
  - Figure_hybrid_augment_effect_KG.png

Data sources are the same:
  - Hybrid figures read results_summary.json (written by parse_results.py).
  - Seq-length figure uses the hardcoded RESULTS dict mirrored from
    generate_v4_reports.py (4 configs: len=5000 / 1000 / 500 / 500+4w).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(r"C:\Users\enazarkulov\Documents\Мастер")

# ---------------------------------------------------------------------------
# Sequence-length comparison (mirrors generate_v4_reports.py.RESULTS)
# ---------------------------------------------------------------------------
SEQ_RESULTS = [
    ("len=5000",          88.43, 87.13, 89.88),
    ("len=1000",          97.22, 97.16, 26.14),
    ("len=500",           97.34, 97.37, 27.20),
    ("len=500 + 4 жип",   97.38, 97.44, 43.50),
]


def build_seq_length_comparison_kg() -> Path:
    keys = [r[0] for r in SEQ_RESULTS]
    test_acc = [r[1] for r in SEQ_RESULTS]
    f1 = [r[2] for r in SEQ_RESULTS]
    inf = [r[3] for r in SEQ_RESULTS]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    x = np.arange(len(keys))
    colors = ["#c0392b", "#2980b9", "#27ae60", "#16a085"]

    bars0 = axes[0].bar(x, test_acc, color=colors)
    axes[0].set_ylim(80, 100)
    axes[0].set_ylabel("Тест тактык (%)")
    axes[0].set_title("Тест тактык")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(keys, rotation=20, ha="right")
    for b, v in zip(bars0, test_acc):
        axes[0].text(b.get_x() + b.get_width() / 2, v + 0.3,
                     f"{v:.2f}", ha="center", fontsize=9)

    bars1 = axes[1].bar(x, f1, color=colors)
    axes[1].set_ylim(80, 100)
    axes[1].set_ylabel("Макро F1 (%)")
    axes[1].set_title("Макро F1-баа")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(keys, rotation=20, ha="right")
    for b, v in zip(bars1, f1):
        axes[1].text(b.get_x() + b.get_width() / 2, v + 0.3,
                     f"{v:.2f}", ha="center", fontsize=9)

    bars2 = axes[2].bar(x, inf, color=colors)
    axes[2].set_ylabel("Чыгаруу убактысы (мс/үлгү)")
    axes[2].set_title("Бир үлгү чыгаруу убактысы")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(keys, rotation=20, ha="right")
    for b, v in zip(bars2, inf):
        axes[2].text(b.get_x() + b.get_width() / 2, v + max(inf) * 0.02,
                     f"{v:.2f}", ha="center", fontsize=9)

    fig.suptitle(
        "Кириш сигналдын узундугунун негизги 1Б-ЖНТ көрсөткүчүнө таасири\n"
        "Чапман–Шаосин, 78 класс, NVIDIA RTX 5090, AMP",
        fontsize=11,
    )
    fig.tight_layout()
    out = OUT / "Figure_seq_length_comparison_KG.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Hybrid-plan figures (data from results_summary.json)
# ---------------------------------------------------------------------------
LABEL_KG = {
    "lead1_augoff":  "1-канал · ауг. ӨЧҮК",
    "lead1_augon":   "1-канал · ауг. КОСУЛ",
    "lead12_augoff": "12-канал · ауг. ӨЧҮК",
    "lead12_augon":  "12-канал · ауг. КОСУЛ",
}

COLOR = {
    "lead1_augoff":  "#94a3b8",
    "lead1_augon":   "#3b82f6",
    "lead12_augoff": "#f59e0b",
    "lead12_augon":  "#10b981",
}


def build_hybrid_kg(summary: dict, perclass: dict) -> list[Path]:
    written: list[Path] = []
    keys = ["lead1_augoff", "lead12_augoff", "lead1_augon", "lead12_augon"]
    x = np.arange(len(keys))
    accs = [summary[k]["test_acc"] * 100 for k in keys]
    f1s = [summary[k]["macro_f1"] for k in keys]
    cols = [COLOR[k] for k in keys]
    labels_short = [LABEL_KG[k] for k in keys]

    # ----- Figure 1: headline -----
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    fig.subplots_adjust(left=0.07, right=0.985, top=0.86, bottom=0.18,
                        wspace=0.25)

    b1 = axes[0].bar(x, accs, color=cols, edgecolor="white", linewidth=1.2)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels_short, rotation=15, ha="right", fontsize=10)
    axes[0].set_ylabel("Тест тактык (%)", fontsize=11)
    axes[0].set_ylim(0, 105)
    axes[0].set_title("(A)  Конфигурация боюнча тест тактык",
                      fontsize=12, fontweight="bold", color="#0f172a")
    axes[0].grid(True, axis="y", linestyle=":", color="#e2e8f0")
    axes[0].set_axisbelow(True)
    for b, v in zip(b1, accs):
        axes[0].text(b.get_x() + b.get_width() / 2, v + 1.5,
                     f"{v:.2f}%", ha="center", fontsize=10, fontweight="bold")

    b2 = axes[1].bar(x, f1s, color=cols, edgecolor="white", linewidth=1.2)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels_short, rotation=15, ha="right", fontsize=10)
    axes[1].set_ylabel("Макро F1-баа", fontsize=11)
    axes[1].set_ylim(0, 1.05)
    axes[1].set_title("(B)  Конфигурация боюнча макро F1",
                      fontsize=12, fontweight="bold", color="#0f172a")
    axes[1].grid(True, axis="y", linestyle=":", color="#e2e8f0")
    axes[1].set_axisbelow(True)
    for b, v in zip(b2, f1s):
        axes[1].text(b.get_x() + b.get_width() / 2, v + 0.02,
                     f"{v:.4f}", ha="center", fontsize=10, fontweight="bold")

    fig.suptitle(
        "Гибрид-план аблациясы — {1-канал, 12-канал} × {ауг. ӨЧҮК, ауг. КОСУЛ}\n"
        "Бирдей seed, бирдей маалымат бөлүшүү, бирдей код версиясы · Чапман–Шаосин · len=500",
        fontsize=11, color="#1e293b", y=0.995,
    )
    out = OUT / "Figure_hybrid_headline_KG.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)
    written.append(out)

    # ----- Figure 2: inference + confidence -----
    fig, ax1 = plt.subplots(figsize=(11, 4.0))
    fig.subplots_adjust(left=0.08, right=0.92, top=0.85, bottom=0.20)
    inf = [summary[k]["inference_ms"] for k in keys]
    cnf = [summary[k]["confidence"] * 100 for k in keys]

    bw = 0.38
    b3 = ax1.bar(x - bw / 2, inf, bw, color="#0ea5e9", edgecolor="white",
                 linewidth=1.2, label="Чыгаруу (мс)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels_short, rotation=15, ha="right", fontsize=10)
    ax1.set_ylabel("Чыгаруу (мс / үлгү)", color="#0ea5e9", fontsize=11)
    ax1.tick_params(axis="y", colors="#0ea5e9")
    ax1.set_ylim(0, max(inf) * 1.3)
    for b, v in zip(b3, inf):
        ax1.text(b.get_x() + b.get_width() / 2, v + max(inf) * 0.03,
                 f"{v:.1f}", ha="center", fontsize=9, color="#0ea5e9")

    ax2 = ax1.twinx()
    b4 = ax2.bar(x + bw / 2, cnf, bw, color="#a855f7", edgecolor="white",
                 linewidth=1.2, label="Ишеним (%)")
    ax2.set_ylabel("Тест үлгүсүндөгү ишеним (%)", color="#a855f7", fontsize=11)
    ax2.tick_params(axis="y", colors="#a855f7")
    ax2.set_ylim(0, 105)
    for b, v in zip(b4, cnf):
        ax2.text(b.get_x() + b.get_width() / 2, v + 2,
                 f"{v:.1f}%", ha="center", fontsize=9, color="#a855f7")

    ax1.set_title(
        "Конфигурация боюнча чыгаруу күтүүсү жана softmax ишеними",
        fontsize=12, fontweight="bold", color="#0f172a")
    ax1.grid(True, axis="y", linestyle=":", color="#e2e8f0")
    ax1.set_axisbelow(True)
    out = OUT / "Figure_hybrid_inference_KG.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)
    written.append(out)

    # ----- Figure 3: per-class top/bottom F1 -----
    if "lead1_augon" in perclass and "lead12_augon" in perclass:
        ref = perclass["lead1_augon"]
        all_classes = sorted(ref.keys(), key=lambda c: ref[c]["f1"], reverse=True)
        top = all_classes[:12]
        bot = all_classes[-12:]

        fig, axes = plt.subplots(1, 2, figsize=(15, 6.0))
        fig.subplots_adjust(left=0.30, right=0.98, top=0.88, bottom=0.06,
                            wspace=0.55)

        for ax, cls_set, title in [
            (axes[0], top, "(A)  Эң мыкты 12 класс"),
            (axes[1], bot, "(B)  Эң кыйын 12 класс"),
        ]:
            y = np.arange(len(cls_set))
            f1_1 = [perclass["lead1_augon"][c]["f1"] for c in cls_set]
            f1_12 = [perclass["lead12_augon"][c]["f1"] for c in cls_set]
            ax.barh(y - 0.20, f1_1, 0.4, color=COLOR["lead1_augon"],
                    edgecolor="white", label="1-канал · ауг. КОСУЛ")
            ax.barh(y + 0.20, f1_12, 0.4, color=COLOR["lead12_augon"],
                    edgecolor="white", label="12-канал · ауг. КОСУЛ")
            ax.set_yticks(y)
            ax.set_yticklabels([c if len(c) <= 36 else c[:33] + "..."
                                for c in cls_set], fontsize=9)
            ax.invert_yaxis()
            ax.set_xlim(0, 1.05)
            ax.axvline(1.0, color="#cbd5e1", linewidth=0.5)
            ax.set_xlabel("F1-баа", fontsize=10)
            ax.grid(True, axis="x", linestyle=":", color="#e2e8f0")
            ax.set_axisbelow(True)
            ax.set_title(title, fontsize=12, fontweight="bold", color="#0f172a")
            ax.legend(loc="lower right", fontsize=9)

        fig.suptitle(
            "Класс боюнча F1: 1-канал vs 12-канал (экөө тең ауг. КОСУЛ, бирдей seed)\n"
            "Көпчүлүк класстар ≥0.97 деңгээлинде; төмөнкү 12 — этикет дубликаттарынын кластери",
            fontsize=11, color="#1e293b", y=0.995,
        )
        out = OUT / "Figure_hybrid_perclass_top_KG.png"
        fig.savefig(out, dpi=170, bbox_inches="tight")
        plt.close(fig)
        written.append(out)

    # ----- Figure 4: augmentation effect -----
    if all(k in perclass for k in ("lead1_augoff", "lead1_augon")):
        common = sorted(
            set(perclass["lead1_augoff"]) & set(perclass["lead1_augon"]),
            key=lambda c: (perclass["lead1_augon"][c]["f1"]
                           - perclass["lead1_augoff"][c]["f1"]),
            reverse=True,
        )
        top_helped = common[:20]
        deltas = [(perclass["lead1_augon"][c]["f1"]
                   - perclass["lead1_augoff"][c]["f1"]) for c in top_helped]
        f1_off = [perclass["lead1_augoff"][c]["f1"] for c in top_helped]
        f1_on = [perclass["lead1_augon"][c]["f1"] for c in top_helped]

        fig, ax = plt.subplots(figsize=(13, 7.5))
        fig.subplots_adjust(left=0.32, right=0.97, top=0.91, bottom=0.07)
        y = np.arange(len(top_helped))
        ax.barh(y, deltas, color="#10b981", edgecolor="white", linewidth=1.2)
        for i, (d, off, on) in enumerate(zip(deltas, f1_off, f1_on)):
            ax.text(d + 0.005, i, f"{off:.2f} → {on:.2f}  (Δ +{d:.2f})",
                    va="center", fontsize=9, color="#475569")
        ax.set_yticks(y)
        ax.set_yticklabels([c if len(c) <= 42 else c[:39] + "..."
                            for c in top_helped], fontsize=9)
        ax.invert_yaxis()
        ax.axvline(0, color="#94a3b8", linewidth=0.6)
        ax.set_xlim(0, max(deltas) * 1.4)
        ax.set_xlabel("ΔF1 (ауг. ӨЧҮК → ауг. КОСУЛ), 1-канал конфигурациясы",
                      fontsize=11)
        ax.set_title(
            "Таяныч түйүн менен аугментациялоо узун куйруктуу класстарды эң жогору тартат\n"
            "ΔF1 боюнча эң үстүнкү 20 класс — иш темасынын 'сигналды аугментациялоо' коммитменти ушул жерде ырасталат",
            fontsize=12, fontweight="bold", color="#0f172a", pad=12,
        )
        ax.grid(True, axis="x", linestyle=":", color="#e2e8f0")
        ax.set_axisbelow(True)
        out = OUT / "Figure_hybrid_augment_effect_KG.png"
        fig.savefig(out, dpi=170, bbox_inches="tight")
        plt.close(fig)
        written.append(out)

    return written


def main() -> None:
    seq_path = build_seq_length_comparison_kg()
    print(f"  {seq_path.name}  ({seq_path.stat().st_size:,} bytes)")

    summary_path = OUT / "results_summary.json"
    if not summary_path.exists():
        print(f"  results_summary.json not found at {summary_path} — "
              f"skipping hybrid figures.")
        return
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    summary = data["summary"]
    perclass = data.get("per_class", {})

    for p in build_hybrid_kg(summary, perclass):
        print(f"  {p.name}  ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
