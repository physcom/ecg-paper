"""Generate three explanatory figures contrasting naive downsampling vs
anti-aliased decimation for a synthetic ECG signal at 500 Hz, q=10.

Outputs in C:/Users/enazarkulov/Documents/Мастер/:
  - Figure_aliasing_time_domain.png      side-by-side time domain
  - Figure_aliasing_freq_domain.png      spectrum with aliased fold-in
  - Figure_aliasing_filter_response.png  Chebyshev-I order-8 response
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import decimate, freqz, cheby1

OUT = Path(r"C:\Users\enazarkulov\Documents\Мастер")

FS = 500
DUR_S = 1.6
N = int(FS * DUR_S)
t = np.linspace(0, DUR_S, N, endpoint=False)


def gauss(t, mu, sigma, amp):
    return amp * np.exp(-0.5 * ((t - mu) / sigma) ** 2)


def synthetic_ecg(t):
    sig = np.zeros_like(t)
    beat_starts = [0.10, 0.90]
    for b0 in beat_starts:
        sig += gauss(t, b0 + 0.10, 0.025, 0.12)
        sig += gauss(t, b0 + 0.30, 0.008, -0.20)
        sig += gauss(t, b0 + 0.32, 0.006, 1.10)
        sig += gauss(t, b0 + 0.34, 0.008, -0.30)
        sig += gauss(t, b0 + 0.55, 0.040, 0.36)
    sig += 0.05 * np.sin(2 * np.pi * 0.5 * t)
    rng = np.random.default_rng(11)
    sig += rng.normal(0, 0.008, size=N)
    return sig


sig = synthetic_ecg(t)
sig_naive = sig[::10]
sig_aa = decimate(sig, 10, ftype="iir", n=8, zero_phase=True)
t_down = np.linspace(0, DUR_S, len(sig_naive), endpoint=False)

PRIMARY = "#1f77b4"
NAIVE = "#dc2626"
AA = "#16a34a"
TEXT = "#1f2937"
GRID = "#e5e7eb"


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, linestyle=":", color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)


def figure_time_domain():
    fig, axes = plt.subplots(3, 1, figsize=(11.5, 7.2), sharex=True)
    fig.subplots_adjust(left=0.07, right=0.985, top=0.92, bottom=0.08, hspace=0.45)

    axes[0].plot(t, sig, color=PRIMARY, linewidth=1.0)
    axes[0].set_title("(A)  Original — 500 Hz, 800 samples", fontsize=11,
                      fontweight="bold", color=TEXT)
    axes[0].set_ylabel("Amplitude (mV)", fontsize=9, color=TEXT)
    axes[0].set_ylim(-0.6, 1.3)

    axes[1].plot(t_down, sig_naive, color=NAIVE, linewidth=1.4,
                 marker="o", markersize=3.0, alpha=0.95)
    axes[1].plot(t, sig, color=PRIMARY, linewidth=0.6, alpha=0.25, label="original")
    axes[1].set_title("(B)  Naive strided pool  x[::10] — 50 Hz, 80 samples",
                      fontsize=11, fontweight="bold", color=NAIVE)
    axes[1].set_ylabel("Amplitude (mV)", fontsize=9, color=TEXT)
    axes[1].set_ylim(-0.6, 1.3)
    axes[1].legend(loc="upper right", fontsize=8, frameon=False)

    axes[2].plot(t_down, sig_aa, color=AA, linewidth=1.4,
                 marker="o", markersize=3.0, alpha=0.95)
    axes[2].plot(t, sig, color=PRIMARY, linewidth=0.6, alpha=0.25, label="original")
    axes[2].set_title("(C)  Anti-aliased  scipy.signal.decimate(x, 10) — 50 Hz, 80 samples",
                      fontsize=11, fontweight="bold", color=AA)
    axes[2].set_ylabel("Amplitude (mV)", fontsize=9, color=TEXT)
    axes[2].set_xlabel("Time (s)", fontsize=9, color=TEXT)
    axes[2].set_ylim(-0.6, 1.3)
    axes[2].legend(loc="upper right", fontsize=8, frameon=False)

    for ax in axes:
        style_axes(ax)

    fig.suptitle(
        "Time-domain: naive strided pool corrupts QRS amplitudes; "
        "anti-aliased decimation preserves them",
        fontsize=12, fontweight="bold", color=TEXT, y=0.985,
    )
    out = OUT / "Figure_aliasing_time_domain.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_freq_domain():
    def spectrum(x, fs):
        n = len(x)
        X = np.abs(np.fft.rfft(x)) / n * 2
        f = np.fft.rfftfreq(n, 1.0 / fs)
        return f, X

    f_orig, S_orig = spectrum(sig, FS)
    f_naive, S_naive = spectrum(sig_naive, FS // 10)
    f_aa, S_aa = spectrum(sig_aa, FS // 10)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.0))
    fig.subplots_adjust(left=0.07, right=0.985, top=0.86, bottom=0.13, wspace=0.22)

    ax = axes[0]
    ax.plot(f_orig, S_orig, color=PRIMARY, linewidth=1.0)
    ax.axvline(25, color="#94a3b8", linestyle="--", linewidth=1.0)
    ax.text(25.5, ax.get_ylim()[1] * 0.7, "Nyquist of\nq=10 decimated\nsignal  (25 Hz)",
            fontsize=9, color="#475569", va="top")
    ax.fill_betweenx([0, S_orig.max() * 1.05], 25, 250,
                     color="#fee2e2", alpha=0.55,
                     label="Content that ALIASES under naive ::10")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, S_orig.max() * 1.05)
    ax.set_xlabel("Frequency (Hz)", fontsize=10, color=TEXT)
    ax.set_ylabel("Magnitude", fontsize=10, color=TEXT)
    ax.set_title("(A)  Spectrum of 500 Hz original — content above 25 Hz folds back",
                 fontsize=11, fontweight="bold", color=TEXT)
    ax.legend(loc="upper right", fontsize=8, frameon=False)
    style_axes(ax)

    ax = axes[1]
    ax.plot(f_naive, S_naive, color=NAIVE, linewidth=1.4, label="Naive x[::10]")
    ax.plot(f_aa, S_aa, color=AA, linewidth=1.4, label="Anti-aliased decimate")
    ax.set_xlim(0, 25)
    ymax = max(S_naive.max(), S_aa.max()) * 1.1
    ax.set_ylim(0, ymax)
    ax.set_xlabel("Frequency (Hz)", fontsize=10, color=TEXT)
    ax.set_ylabel("Magnitude", fontsize=10, color=TEXT)
    ax.set_title("(B)  Decimated spectra (50 Hz) — naive shows phantom energy",
                 fontsize=11, fontweight="bold", color=TEXT)
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    style_axes(ax)

    fig.suptitle(
        "Frequency-domain: anti-alias filter removes >25 Hz content "
        "before downsampling, blocking the alias fold-in",
        fontsize=12, fontweight="bold", color=TEXT, y=0.985,
    )
    out = OUT / "Figure_aliasing_freq_domain.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_filter_response():
    b, a = cheby1(8, 0.05, 0.8)
    w, h = freqz(b, a, worN=2048)
    freq_hz = w / np.pi * (FS / 2 / 10)
    mag_db = 20 * np.log10(np.abs(h) + 1e-12)

    fig, ax = plt.subplots(figsize=(11, 5.0))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.85, bottom=0.14)

    ax.plot(freq_hz, mag_db, color=AA, linewidth=1.7)
    ax.axvline(25, color="#94a3b8", linestyle="--", linewidth=1.0)
    ax.axhline(-3, color="#94a3b8", linestyle=":", linewidth=0.8)
    ax.fill_between(freq_hz, -120, mag_db,
                    where=(freq_hz > 22) & (freq_hz < 26),
                    color="#dcfce7", alpha=0.5)

    ax.text(26.5, -3, "−3 dB", fontsize=9, color="#475569", va="center")
    ax.text(25.5, -90, "Nyquist of q=10\n decimated signal\n  (25 Hz)",
            fontsize=9, color="#475569", va="bottom")
    ax.annotate("passband (DC-25 Hz):\nQRS / P / T energy preserved",
                xy=(8, -2), xytext=(8, -25), fontsize=9, color=AA,
                ha="left",
                arrowprops=dict(arrowstyle="->", color=AA, lw=0.7))
    ax.annotate("stopband (>25 Hz):\nremoved before downsampling",
                xy=(45, -80), xytext=(45, -50), fontsize=9, color=NAIVE,
                ha="left",
                arrowprops=dict(arrowstyle="->", color=NAIVE, lw=0.7))

    ax.set_xlim(0, 50)
    ax.set_ylim(-120, 5)
    ax.set_xlabel("Frequency (Hz)", fontsize=10, color=TEXT)
    ax.set_ylabel("Magnitude (dB)", fontsize=10, color=TEXT)
    ax.set_title("Chebyshev-I order-8 low-pass — zero-phase (forward–backward).  "
                 "Used by scipy.signal.decimate with ftype='iir'.",
                 fontsize=11, fontweight="bold", color=TEXT)
    style_axes(ax)

    out = OUT / "Figure_aliasing_filter_response.png"
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return out


if __name__ == "__main__":
    for fn in (figure_time_domain, figure_freq_domain, figure_filter_response):
        path = fn()
        print(f"  {path.name}  ({path.stat().st_size:,} bytes)")
