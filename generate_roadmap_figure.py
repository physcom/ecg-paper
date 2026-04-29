"""
Build a one-page visual Gantt-style roadmap for the 12-month future-work
plan documented in Future_Work_Plan.md.

Output: Figure_future_work_roadmap.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(r"C:\Users\enazarkulov\Documents\Мастер")
FIG = OUT / "Figure_future_work_roadmap.png"

# ---------------------------------------------------------------------------
# Tracks and tasks
# ---------------------------------------------------------------------------

# Each task: (track_label, task_label, start_week, end_week, colour, deliverable)
TRACKS = ["Path A · Multi-lead", "Path B · Multi-modal", "Path C · Edge / Pilot",
          "Cross-cutting"]

TASKS = [
    # Path A
    ("Path A · Multi-lead", "Lock baseline · num_leads CLI", 1, 2,  "#3b82f6",
     "v1.0-singlelead-97.34"),
    ("Path A · Multi-lead", "Train m1, m3, m6, m12",         3, 4,  "#3b82f6",
     "lead-ablation table"),
    ("Path A · Multi-lead", "Paper #2 (lead ablation)",      5, 8,  "#1d4ed8",
     "MJEN journal draft"),

    # Path B (multi-modal)
    ("Path B · Multi-modal", "PPG-DaLiA + WESAD ingest",     9, 10, "#10b981",
     "aligned multimodal data"),
    ("Path B · Multi-modal", "Two-stream fusion CNN",       11, 12, "#10b981",
     "ECG+PPG model"),
    ("Path B · Multi-modal", "Multimodal ablation + paper #3", 13, 16, "#047857",
     "paper #3 draft"),

    # Path C (edge / pilot)
    ("Path C · Edge / Pilot", "PTB-XL cross-dataset eval",   5, 6,  "#f59e0b",
     "external validation #s"),
    ("Path C · Edge / Pilot", "ONNX export · INT8 quantise", 7, 7,  "#f59e0b",
     "edge model bundle"),
    ("Path C · Edge / Pilot", "Pi 4 / phone benchmark",      8, 8,  "#f59e0b",
     "edge benchmark"),
    ("Path C · Edge / Pilot", "Hospital partner · IRB",     17, 24, "#dc2626",
     "ethics approval"),
    ("Path C · Edge / Pilot", "Bishkek pilot — shadow",     25, 28, "#dc2626",
     "concordance baseline"),
    ("Path C · Edge / Pilot", "Bishkek pilot — assisted",   29, 32, "#dc2626",
     "go/no-go decision"),
    ("Path C · Edge / Pilot", "Pilot analysis · paper #4",  33, 40, "#b91c1c",
     "paper #4 draft"),

    # Cross-cutting
    ("Cross-cutting", "Respiration multi-task head",         3, 4,  "#a855f7",
     "free EDR output"),
    ("Cross-cutting", "Thesis assembly · defence prep",     41, 48, "#7c3aed",
     "defence package"),
]

# Decision points
MILESTONES = [
    (4,  "1→12 sweep · ≥ +1 pp ?",        "#0ea5e9"),
    (8,  "PTB-XL holds up?",              "#0ea5e9"),
    (16, "Multimodal +1pp ?",             "#0ea5e9"),
    (32, "Pilot go / no-go",              "#10b981"),
    (48, "Defence",                       "#dc2626"),
]


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

def render() -> Path:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.edgecolor": "#cbd5e1",
        "axes.linewidth": 0.8,
    })

    fig, ax = plt.subplots(figsize=(14.5, 6.4))
    fig.subplots_adjust(left=0.16, right=0.985, top=0.88, bottom=0.10)

    # y = task index from top
    n_tasks = len(TASKS)
    y_positions = list(range(n_tasks, 0, -1))  # top is highest y

    track_colours = {
        "Path A · Multi-lead":   "#dbeafe",
        "Path B · Multi-modal":  "#d1fae5",
        "Path C · Edge / Pilot": "#fee2e2",
        "Cross-cutting":         "#ede9fe",
    }

    # Background bands per track
    for i, (track_label, task_label, sw, ew, colour, deliverable) in enumerate(TASKS):
        y = y_positions[i]
        ax.add_patch(patches.Rectangle((0.5, y - 0.45), 49, 0.9,
                                       facecolor=track_colours[track_label],
                                       alpha=0.35, edgecolor="none"))

    # Bars
    for i, (track_label, task_label, sw, ew, colour, deliverable) in enumerate(TASKS):
        y = y_positions[i]
        ax.barh(y, ew - sw + 1, left=sw, height=0.55, color=colour,
                edgecolor="white", linewidth=1.2, zorder=3)
        # Right-side deliverable label (in italics, light)
        ax.text(ew + 0.7, y, f"→ {deliverable}", va="center", ha="left",
                fontsize=9, color="#475569", fontstyle="italic", zorder=4)

    # Milestones
    for week, label, mcol in MILESTONES:
        ax.axvline(week, color=mcol, linestyle=":", linewidth=1.2, alpha=0.7,
                   zorder=2)
        ax.plot(week, n_tasks + 0.7, marker="v", color=mcol, markersize=12,
                markeredgecolor="white", markeredgewidth=1.5, zorder=5,
                clip_on=False)
        ax.text(week, n_tasks + 1.4, label, ha="center", va="bottom",
                fontsize=9, color=mcol, fontweight="bold", clip_on=False)

    # y-tick labels = task names
    ax.set_yticks(y_positions)
    ax.set_yticklabels([t[1] for t in TASKS], fontsize=10, color="#1e293b")

    # x-axis: weeks 1..48 with phase markers
    ax.set_xlim(0.5, 49)
    ax.set_ylim(0.3, n_tasks + 0.8)
    ax.set_xlabel("Week (Week 1 = 2026-04-29)", fontsize=11, color="#1e293b")

    # x ticks every 4 weeks
    ax.set_xticks(np.arange(0, 49, 4))

    # Phase backgrounds (top)
    phase_spans = [
        (1,  4,  "Phase 1 — Lock baseline + Path A start", "#bfdbfe"),
        (5,  8,  "Phase 2 — Cross-dataset + Edge",         "#fde68a"),
        (9,  16, "Phase 3 — Multi-modal",                  "#bbf7d0"),
        (17, 48, "Phase 4 — Pilot + Defence",              "#fecaca"),
    ]
    for sw, ew, label, col in phase_spans:
        ax.text((sw + ew) / 2, n_tasks + 2.4, label, ha="center",
                va="center", fontsize=10, color="#0f172a", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.45", facecolor=col,
                          edgecolor="none"),
                clip_on=False)

    # Legend (track colours)
    handles = [
        patches.Patch(facecolor="#3b82f6", label="A · Multi-lead"),
        patches.Patch(facecolor="#10b981", label="B · Multi-modal"),
        patches.Patch(facecolor="#dc2626", label="C · Edge / Pilot"),
        patches.Patch(facecolor="#a855f7", label="Cross-cutting"),
        patches.Patch(facecolor="#0ea5e9", label="Decision point"),
    ]
    ax.legend(handles=handles, loc="lower right", ncol=5, fontsize=9,
              frameon=False)

    ax.set_title(
        "Future-Work Roadmap — 12 months · Single-lead baseline → "
        "multi-lead study + multimodal fusion + Bishkek clinical pilot",
        fontsize=12, color="#0f172a", fontweight="bold", pad=24,
    )

    # Light grid
    ax.grid(True, axis="x", linestyle=":", color="#e2e8f0", linewidth=0.5)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    fig.savefig(FIG, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return FIG


if __name__ == "__main__":
    out = render()
    print(f"Saved: {out.name}  ({out.stat().st_size:,} bytes)")
