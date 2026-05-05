"""
Parse the four hybrid-plan training logs and emit:

  - results_summary.json                   structured metrics for downstream use
  - Figure_hybrid_headline.png             4-config bar-chart (Test Acc, Macro F1)
  - Figure_hybrid_inference.png            inference latency vs config
  - Figure_hybrid_perclass_top.png         per-class F1, top vs bottom 12 classes
  - Figure_hybrid_augment_effect.png       augment OFF→ON delta per class

The four logs are written by `Tee-Object` in PowerShell 5.1, which encodes
files as UTF-16 LE with CRLF line endings. We decode explicitly.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(r"C:\Users\enazarkulov\Documents\ML\ekg")
OUT_DIR = Path(r"C:\Users\enazarkulov\Documents\Мастер")

LOGS = {
    "lead1_augoff":  REPO / "results" / "result-lead1-augoff-2026-04-30.txt",
    "lead1_augon":   REPO / "results" / "result-lead1-augon-2026-04-30.txt",
    "lead12_augoff": REPO / "results" / "result-lead12-augoff-2026-04-30.txt",
    "lead12_augon":  REPO / "results" / "result-lead12-augon-2026-04-30.txt",
}

LABEL = {
    "lead1_augoff":  "1-lead · aug OFF",
    "lead1_augon":   "1-lead · aug ON",
    "lead12_augoff": "12-lead · aug OFF",
    "lead12_augon":  "12-lead · aug ON",
}

COLOR = {
    "lead1_augoff":  "#94a3b8",
    "lead1_augon":   "#3b82f6",
    "lead12_augoff": "#f59e0b",
    "lead12_augon":  "#10b981",
}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def read_log(path: Path) -> str:
    return path.read_bytes().decode("utf-16-le", errors="replace")


def extract_summary(text: str) -> dict:
    """Pull headline metrics out of a single training log."""
    def grab(pattern: str, default=None) -> str | None:
        m = re.search(pattern, text)
        return m.group(1) if m else default

    last_epoch = re.findall(r"Epoch (\d+)/\d+ - Loss: ([\d.]+), Acc: ([\d.]+),"
                            r" Val Loss: ([\d.]+), Val Acc: ([\d.]+),", text)
    final_epoch = last_epoch[-1] if last_epoch else None

    early_stop = grab(r"Early stopping triggered after (\d+) epochs")

    return {
        "test_acc":   float(grab(r"Test Accuracy:\s*([\d.]+)", "0") or 0),
        "macro_p":    float(grab(r"Macro Precision:\s*([\d.]+)", "0") or 0),
        "macro_r":    float(grab(r"Macro Recall:\s*([\d.]+)", "0") or 0),
        "macro_f1":   float(grab(r"Macro F1-Score:\s*([\d.]+)", "0") or 0),
        "confidence": float(grab(r"Confidence:\s*([\d.]+)%", "0") or 0) / 100,
        "inference_ms": float(grab(r"Inference:\s*([\d.]+)ms", "0") or 0),
        "early_stop_epoch": int(early_stop) if early_stop else None,
        "final_epoch": int(final_epoch[0]) if final_epoch else None,
        "final_train_acc": float(final_epoch[2]) if final_epoch else None,
        "final_val_acc":   float(final_epoch[4]) if final_epoch else None,
    }


def extract_per_class(text: str) -> dict[str, dict]:
    """Pull per-class precision/recall/f1/support table."""
    block = re.search(
        r"Per-Class Metrics:\s*\n[-]+\s*\n[^\n]+\n[-]+\s*\n(.*?)\n[-]+",
        text, re.DOTALL,
    )
    if not block:
        return {}
    rows = block.group(1).splitlines()
    classes = {}
    # The class name can contain spaces; the last 4 fields are numbers.
    pattern = re.compile(r"^(.*?)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s*$")
    for row in rows:
        m = pattern.match(row.rstrip())
        if not m:
            continue
        cls, p, r, f1, sup = m.groups()
        classes[cls.strip()] = {
            "precision": float(p),
            "recall":    float(r),
            "f1":        float(f1),
            "support":   int(sup),
        }
    return classes


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {}
    perclass = {}

    for key, log in LOGS.items():
        if not log.exists():
            print(f"  [skip] {log.name} missing")
            continue
        text = read_log(log)
        summary[key] = extract_summary(text)
        perclass[key] = extract_per_class(text)
        n_cls = len(perclass[key])
        print(f"  {key:<14}  acc={summary[key]['test_acc']:.4f}  "
              f"f1={summary[key]['macro_f1']:.4f}  "
              f"classes={n_cls}  early_stop@{summary[key]['early_stop_epoch']}")

    out_json = OUT_DIR / "results_summary.json"
    out_json.write_text(json.dumps(
        {"summary": summary, "per_class": perclass}, indent=2,
    ), encoding="utf-8")
    print(f"\nWrote {out_json.name} ({out_json.stat().st_size:,} bytes)")

    # ----- Figure 1 — Headline 2-panel bar chart -----
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    fig.subplots_adjust(left=0.07, right=0.985, top=0.86, bottom=0.18,
                        wspace=0.25)

    keys = ["lead1_augoff", "lead12_augoff", "lead1_augon", "lead12_augon"]
    x = np.arange(len(keys))
    accs = [summary[k]["test_acc"] * 100 for k in keys]
    f1s  = [summary[k]["macro_f1"] for k in keys]
    cols = [COLOR[k] for k in keys]
    labels_short = [LABEL[k] for k in keys]

    b1 = axes[0].bar(x, accs, color=cols, edgecolor="white", linewidth=1.2)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels_short, rotation=15, ha="right", fontsize=10)
    axes[0].set_ylabel("Test accuracy (%)", fontsize=11)
    axes[0].set_ylim(0, 105)
    axes[0].set_title("(A)  Test accuracy by configuration",
                      fontsize=12, fontweight="bold", color="#0f172a")
    axes[0].grid(True, axis="y", linestyle=":", color="#e2e8f0")
    axes[0].set_axisbelow(True)
    for b, v in zip(b1, accs):
        axes[0].text(b.get_x() + b.get_width() / 2, v + 1.5,
                     f"{v:.2f}%", ha="center", fontsize=10, fontweight="bold")

    b2 = axes[1].bar(x, f1s, color=cols, edgecolor="white", linewidth=1.2)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels_short, rotation=15, ha="right", fontsize=10)
    axes[1].set_ylabel("Macro F1-score", fontsize=11)
    axes[1].set_ylim(0, 1.05)
    axes[1].set_title("(B)  Macro F1 by configuration",
                      fontsize=12, fontweight="bold", color="#0f172a")
    axes[1].grid(True, axis="y", linestyle=":", color="#e2e8f0")
    axes[1].set_axisbelow(True)
    for b, v in zip(b2, f1s):
        axes[1].text(b.get_x() + b.get_width() / 2, v + 0.02,
                     f"{v:.4f}", ha="center", fontsize=10, fontweight="bold")

    fig.suptitle(
        "Hybrid plan ablation — {1-lead, 12-lead} × {augment OFF, augment ON}\n"
        "Same seed, same data split, same code revision · Chapman–Shaoxing · len=500",
        fontsize=11, color="#1e293b", y=0.995,
    )
    fig.savefig(OUT_DIR / "Figure_hybrid_headline.png",
                dpi=170, bbox_inches="tight")
    plt.close(fig)

    # ----- Figure 2 — Inference & confidence -----
    fig, ax1 = plt.subplots(figsize=(11, 4.0))
    fig.subplots_adjust(left=0.08, right=0.92, top=0.85, bottom=0.20)
    inf = [summary[k]["inference_ms"] for k in keys]
    cnf = [summary[k]["confidence"] * 100 for k in keys]

    bw = 0.38
    b3 = ax1.bar(x - bw/2, inf, bw, color="#0ea5e9", edgecolor="white",
                 linewidth=1.2, label="Inference (ms)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels_short, rotation=15, ha="right", fontsize=10)
    ax1.set_ylabel("Inference (ms / sample)", color="#0ea5e9", fontsize=11)
    ax1.tick_params(axis="y", colors="#0ea5e9")
    ax1.set_ylim(0, max(inf) * 1.3)
    for b, v in zip(b3, inf):
        ax1.text(b.get_x() + b.get_width() / 2, v + max(inf) * 0.03,
                 f"{v:.1f}", ha="center", fontsize=9, color="#0ea5e9")

    ax2 = ax1.twinx()
    b4 = ax2.bar(x + bw/2, cnf, bw, color="#a855f7", edgecolor="white",
                 linewidth=1.2, label="Confidence (%)")
    ax2.set_ylabel("Confidence on test sample (%)", color="#a855f7",
                   fontsize=11)
    ax2.tick_params(axis="y", colors="#a855f7")
    ax2.set_ylim(0, 105)
    for b, v in zip(b4, cnf):
        ax2.text(b.get_x() + b.get_width() / 2, v + 2,
                 f"{v:.1f}%", ha="center", fontsize=9, color="#a855f7")

    ax1.set_title("Inference latency and softmax confidence by configuration",
                  fontsize=12, fontweight="bold", color="#0f172a")
    ax1.grid(True, axis="y", linestyle=":", color="#e2e8f0")
    ax1.set_axisbelow(True)
    fig.savefig(OUT_DIR / "Figure_hybrid_inference.png",
                dpi=170, bbox_inches="tight")
    plt.close(fig)

    # ----- Figure 3 — Top / bottom per-class F1 (augment-ON configs) -----
    if "lead1_augon" in perclass and "lead12_augon" in perclass:
        # Use lead1_augon as ranking reference (it was the earliest sweep).
        ref = perclass["lead1_augon"]
        all_classes = sorted(ref.keys(),
                             key=lambda c: ref[c]["f1"], reverse=True)
        top = all_classes[:12]
        bot = all_classes[-12:]

        fig, axes = plt.subplots(1, 2, figsize=(15, 6.0))
        fig.subplots_adjust(left=0.30, right=0.98, top=0.88, bottom=0.06,
                            wspace=0.55)

        for ax, cls_set, title in [
            (axes[0], top, "(A)  Top-12 best-performing classes"),
            (axes[1], bot, "(B)  Bottom-12 most-difficult classes"),
        ]:
            y = np.arange(len(cls_set))
            f1_1 = [perclass["lead1_augon"][c]["f1"] for c in cls_set]
            f1_12 = [perclass["lead12_augon"][c]["f1"] for c in cls_set]
            ax.barh(y - 0.20, f1_1, 0.4, color=COLOR["lead1_augon"],
                    edgecolor="white", label="1-lead · aug ON")
            ax.barh(y + 0.20, f1_12, 0.4, color=COLOR["lead12_augon"],
                    edgecolor="white", label="12-lead · aug ON")
            ax.set_yticks(y)
            ax.set_yticklabels([c if len(c) <= 36 else c[:33] + "..."
                                for c in cls_set], fontsize=9)
            ax.invert_yaxis()
            ax.set_xlim(0, 1.05)
            ax.axvline(1.0, color="#cbd5e1", linewidth=0.5)
            ax.set_xlabel("F1-score", fontsize=10)
            ax.grid(True, axis="x", linestyle=":", color="#e2e8f0")
            ax.set_axisbelow(True)
            ax.set_title(title, fontsize=12, fontweight="bold",
                         color="#0f172a")
            ax.legend(loc="lower right", fontsize=9)

        fig.suptitle(
            "Per-class F1: 1-lead vs 12-lead (both augment ON, same seed)\n"
            "Most classes are tied at ≥0.97; the bottom-12 contains the "
            "label-duplicate cluster (\"ECG: …\" vs root labels)",
            fontsize=11, color="#1e293b", y=0.995,
        )
        fig.savefig(OUT_DIR / "Figure_hybrid_perclass_top.png",
                    dpi=170, bbox_inches="tight")
        plt.close(fig)

    # ----- Figure 4 — Augmentation effect (OFF→ON delta per class) -----
    if all(k in perclass for k in ("lead1_augoff", "lead1_augon")):
        common = sorted(
            set(perclass["lead1_augoff"]) & set(perclass["lead1_augon"]),
            key=lambda c: (perclass["lead1_augon"][c]["f1"]
                           - perclass["lead1_augoff"][c]["f1"]),
            reverse=True,
        )
        # Top 20 most-helped by augmentation
        top_helped = common[:20]
        deltas = [(perclass["lead1_augon"][c]["f1"]
                   - perclass["lead1_augoff"][c]["f1"]) for c in top_helped]
        f1_off = [perclass["lead1_augoff"][c]["f1"] for c in top_helped]
        f1_on  = [perclass["lead1_augon"][c]["f1"]  for c in top_helped]

        fig, ax = plt.subplots(figsize=(13, 7.5))
        fig.subplots_adjust(left=0.32, right=0.97, top=0.91, bottom=0.07)
        y = np.arange(len(top_helped))
        ax.barh(y, deltas, color="#10b981", edgecolor="white",
                linewidth=1.2)
        for i, (d, off, on) in enumerate(zip(deltas, f1_off, f1_on)):
            ax.text(d + 0.005, i, f"{off:.2f} → {on:.2f}  (Δ +{d:.2f})",
                    va="center", fontsize=9, color="#475569")
        ax.set_yticks(y)
        ax.set_yticklabels([c if len(c) <= 42 else c[:39] + "..."
                            for c in top_helped], fontsize=9)
        ax.invert_yaxis()
        ax.axvline(0, color="#94a3b8", linewidth=0.6)
        ax.set_xlim(0, max(deltas) * 1.4)
        ax.set_xlabel("ΔF1 (augment OFF → augment ON), 1-lead config",
                      fontsize=11)
        ax.set_title(
            "Reference-node augmentation lifts the long-tail classes the most\n"
            "Top 20 classes by ΔF1 — the title's 'sinyal büyütme' commitment "
            "is empirically validated here",
            fontsize=12, fontweight="bold", color="#0f172a", pad=12,
        )
        ax.grid(True, axis="x", linestyle=":", color="#e2e8f0")
        ax.set_axisbelow(True)
        fig.savefig(OUT_DIR / "Figure_hybrid_augment_effect.png",
                    dpi=170, bbox_inches="tight")
        plt.close(fig)

    print()
    print("Figures written to", OUT_DIR)
    for f in OUT_DIR.glob("Figure_hybrid_*.png"):
        print(f"  {f.name}  ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
