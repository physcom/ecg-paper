"""
Build the geometry-invariance figure in two languages.

Outputs in C:/Users/enazarkulov/Documents/Мастер/:
  Figure_geometry_invariance.png      (English — for EN paper / HTML EN deck)
  Figure_geometry_invariance_TR.png   (Turkish — for TR paper / Manas docx / HTML TR deck)

Two-panel figure that visually argues why anti-aliased decimation from 5000
to 500 samples lifts a baseline 1D-CNN from 88.43% to 97.34% on
Chapman-Shaoxing:

  Panel A (top)    — synthetic 10 s lead-II ECG sampled at 500 Hz
                     (5000 samples). The diagnostic content lives in a
                     sparse set of fiducial points (P, Q, R, S, T) per beat;
                     ~98% of the samples are baseline interpolation. The
                     translucent band shows the CNN's effective receptive
                     field (≈40% of the window).
  Panel B (bottom) — the same signal after scipy.signal.decimate(x, 10).
                     Fiducial points are preserved up to sampling
                     resolution; their density jumps 10x, the receptive
                     field now spans the whole window.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import decimate

OUT = Path(r"C:\Users\enazarkulov\Documents\Мастер")

# ---------------------------------------------------------------------------
# Strings per language
# ---------------------------------------------------------------------------

STRINGS = {
    "en": {
        "out": OUT / "Figure_geometry_invariance.png",
        "label_5000": "Lead II, 5000 samples (500 Hz × 10 s)",
        "label_5000_rf": "CNN receptive field (~2048 samples ≈ 40% of window)",
        "rf_text_5000": "CNN receptive field ≈ 40% of window",
        "label_500": "Lead II, 500 samples (50 Hz × 10 s) — anti-aliased",
        "label_500_rf": "CNN receptive field (~2048 samples > full window)",
        "rf_text_500": "CNN receptive field covers 100% of window",
        "xlabel": "Time (s)",
        "ylabel": "Amplitude (mV)",
        "title_a": ("(A)  Input length = 5000 samples — fiducial points are "
                    "sparse (≈ 60 / 5000 ≈ 1.2 % of positions)"),
        "title_b": ("(B)  Input length = 500 samples — same fiducial points, "
                    "10× denser (≈ 60 / 500 ≈ 12 % of positions)"),
        "suptitle": (
            "Geometric invariance under anti-aliased decimation. "
            "Diagnostic content lives in the fiducial-point graph "
            "(P, Q, R, S, T per beat), which scipy.signal.decimate "
            "preserves up to sampling resolution. Reducing "
            "5000 → 500 samples increases fiducial-point density 10× "
            "and lets the 1D-CNN's receptive field span the entire "
            "10 s window."
        ),
    },
    "tr": {
        "out": OUT / "Figure_geometry_invariance_TR.png",
        "label_5000": "Lead II, 5000 örnek (500 Hz × 10 s)",
        "label_5000_rf": "CNN alıcı alanı (~2048 örnek ≈ pencerenin %40'ı)",
        "rf_text_5000": "CNN alıcı alanı ≈ pencerenin %40'ı",
        "label_500": "Lead II, 500 örnek (50 Hz × 10 s) — anti-aliased",
        "label_500_rf": "CNN alıcı alanı (~2048 örnek > tüm pencere)",
        "rf_text_500": "CNN alıcı alanı pencerenin %100'ünü kapsar",
        "xlabel": "Zaman (s)",
        "ylabel": "Genlik (mV)",
        "title_a": ("(A)  Giriş uzunluğu = 5000 örnek — referans noktalar "
                    "seyrek (≈ 60 / 5000 ≈ %1.2)"),
        "title_b": ("(B)  Giriş uzunluğu = 500 örnek — aynı referans noktalar, "
                    "10× daha yoğun (≈ 60 / 500 ≈ %12)"),
        "suptitle": (
            "Anti-aliasing'li altörnekleme altında geometrik değişmezlik. "
            "Tanısal içerik, atım başına P, Q, R, S, T olmak üzere referans "
            "nokta grafında yaşar ve scipy.signal.decimate bu noktaları "
            "örnekleme çözünürlüğüne kadar korur. 5000 → 500 örneğe "
            "indirgemek referans nokta yoğunluğunu 10× artırır ve "
            "1D-CNN'in alıcı alanının tüm 10 s pencereyi kapsamasını "
            "sağlar."
        ),
    },
}

# ---------------------------------------------------------------------------
# ECG synthesis (shared across languages)
# ---------------------------------------------------------------------------
RNG = np.random.default_rng(7)
FS = 500
DUR_S = 10
N = FS * DUR_S  # 5000

t = np.linspace(0, DUR_S, N, endpoint=False)


def gauss(t, mu, sigma, amp):
    return amp * np.exp(-0.5 * ((t - mu) / sigma) ** 2)


def beat(t, t0, hr_factor=1.0):
    p_t = t0 + 0.10 * hr_factor
    q_t = t0 + 0.30 * hr_factor
    r_t = t0 + 0.32 * hr_factor
    s_t = t0 + 0.34 * hr_factor
    t_t = t0 + 0.55 * hr_factor

    p = gauss(t, p_t, 0.025, 0.12)
    q = gauss(t, q_t, 0.010, -0.18)
    r = gauss(t, r_t, 0.012, 1.00)
    s = gauss(t, s_t, 0.012, -0.28)
    tw = gauss(t, t_t, 0.040, 0.34)

    fid = {"P": p_t, "Q": q_t, "R": r_t, "S": s_t, "T": t_t}
    return p + q + r + s + tw, fid


beat_starts = np.arange(0.10, DUR_S - 0.85, 0.80)
sig = np.zeros_like(t)
fid_points: list[tuple[float, float, str]] = []
for k, b0 in enumerate(beat_starts):
    w, fid = beat(t, b0)
    sig += w
    if 0.05 < b0 < DUR_S - 0.65:
        for name, ft in fid.items():
            idx = int(np.clip(ft * FS, 0, N - 1))
            fid_points.append((ft, sig[idx], name))

sig += 0.04 * np.sin(2 * np.pi * 0.3 * t)
sig += RNG.normal(0, 0.012, size=N)

sig_500 = decimate(sig, 10, ftype="iir", n=8, zero_phase=True)
t_500 = np.linspace(0, DUR_S, 500, endpoint=False)

fid_points_500 = []
for ft, _amp, name in fid_points:
    idx = int(np.clip(ft * 50, 0, 500 - 1))
    fid_points_500.append((ft, sig_500[idx], name))


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

PRIMARY = "#2563eb"
ACCENT = "#0891b2"
RED = "#dc2626"
BG_RF = (0.15, 0.51, 0.92, 0.13)
TEXT = "#0f172a"


def render(strings: dict) -> Path:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.edgecolor": "#cbd5e1",
        "axes.linewidth": 0.8,
        "axes.titleweight": "bold",
    })

    fig, axes = plt.subplots(2, 1, figsize=(13.5, 7.4), sharex=False)
    fig.subplots_adjust(hspace=0.55, top=0.88, bottom=0.08, left=0.06, right=0.985)

    # --- Panel A ---
    axA = axes[0]
    axA.plot(t, sig, color=PRIMARY, linewidth=1.0, label=strings["label_5000"])
    for ft, amp, _name in fid_points:
        axA.plot(ft, amp, "o", markersize=4.5, color=RED,
                 markeredgecolor="white", markeredgewidth=0.6)
    demo_b0 = beat_starts[1]
    demo = [pt for pt in fid_points if abs(pt[0] - (demo_b0 + 0.32)) < 0.5][:5]
    for ft, amp, name in demo:
        dy = -0.20 if name in ("Q", "S") else 0.18
        axA.annotate(name, xy=(ft, amp), xytext=(ft, amp + dy),
                     ha="center", fontsize=10, color=RED, fontweight="bold",
                     arrowprops=dict(arrowstyle="-", color=RED, lw=0.6, alpha=0.6))

    rf_start, rf_end = 0.6, 4.7
    axA.axvspan(rf_start, rf_end, color=BG_RF, label=strings["label_5000_rf"])
    axA.text((rf_start + rf_end) / 2, 1.20, strings["rf_text_5000"],
             ha="center", fontsize=10, color=PRIMARY, fontweight="bold")

    axA.set_xlim(0, DUR_S)
    axA.set_ylim(-0.7, 1.45)
    axA.set_xlabel(strings["xlabel"], fontsize=10, color=TEXT)
    axA.set_ylabel(strings["ylabel"], fontsize=10, color=TEXT)
    axA.set_title(strings["title_a"], fontsize=12, color=TEXT, pad=10)
    axA.grid(True, linestyle=":", color="#e2e8f0", linewidth=0.6)
    axA.legend(loc="upper right", fontsize=9, frameon=False)

    # --- Panel B ---
    axB = axes[1]
    axB.plot(t_500, sig_500, color=ACCENT, linewidth=1.4, marker="o",
             markersize=2.2, markerfacecolor=ACCENT, markeredgecolor=ACCENT,
             alpha=0.85, label=strings["label_500"])
    for ft, amp, _name in fid_points_500:
        axB.plot(ft, amp, "o", markersize=5.2, color=RED,
                 markeredgecolor="white", markeredgewidth=0.7)
    demo500 = [pt for pt in fid_points_500 if abs(pt[0] - (demo_b0 + 0.32)) < 0.5][:5]
    for ft, amp, name in demo500:
        dy = -0.22 if name in ("Q", "S") else 0.20
        axB.annotate(name, xy=(ft, amp), xytext=(ft, amp + dy),
                     ha="center", fontsize=10, color=RED, fontweight="bold",
                     arrowprops=dict(arrowstyle="-", color=RED, lw=0.6, alpha=0.6))

    axB.axvspan(0, DUR_S, color=BG_RF, label=strings["label_500_rf"])
    axB.text(DUR_S / 2, 1.25, strings["rf_text_500"],
             ha="center", fontsize=10, color=PRIMARY, fontweight="bold")

    axB.set_xlim(0, DUR_S)
    axB.set_ylim(-0.7, 1.45)
    axB.set_xlabel(strings["xlabel"], fontsize=10, color=TEXT)
    axB.set_ylabel(strings["ylabel"], fontsize=10, color=TEXT)
    axB.set_title(strings["title_b"], fontsize=12, color=TEXT, pad=10)
    axB.grid(True, linestyle=":", color="#e2e8f0", linewidth=0.6)
    axB.legend(loc="upper right", fontsize=9, frameon=False)

    fig.suptitle(strings["suptitle"], fontsize=10, color=TEXT,
                 x=0.5, y=0.985, wrap=True)

    fig.savefig(strings["out"], dpi=170, bbox_inches="tight")
    plt.close(fig)
    return strings["out"]


for lang, s in STRINGS.items():
    out = render(s)
    print(f"  {lang}: {out.name}  ({out.stat().st_size:,} bytes)")
