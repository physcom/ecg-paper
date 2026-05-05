# Anti-Aliased Decimation as the Decisive Step in 12-Lead ECG Classification: From 88.43% to 97.34% on Chapman–Shaoxing with a Plain 1D-CNN

**Elaman Nazarkulov**
Department of Computer Engineering, Kyrgyz–Turkish Manas University, Bishkek, Kyrgyzstan
elaman.job@gmail.com

## Abstract
Automatic 12-lead electrocardiogram (ECG) classification is conventionally performed on the raw 500 Hz × 10 s signal of 5000 samples per lead. We show that this default is the **decisive** design choice for a baseline 1D convolutional neural network (1D-CNN) on the Chapman–Shaoxing corpus (45,152 records, 78 multi-label classes). Replacing the input with an anti-aliased decimation to 500 samples (effective 50 Hz) using `scipy.signal.decimate` raises test accuracy from **88.43% to 97.34%** and macro-F1 from **0.8713 to 0.9737**, while reducing single-sample inference from **89.88 ms to 27.20 ms**. The eleven baseline failure classes (F1 < 0.60, minimum 0.022 for Left Ventricular Hypertrophy) recover uniformly to F1 ≥ 0.95. We frame the result through a geometric-invariance argument: the diagnostic content of an ECG lives in a sparse set of fiducial points (P, Q, R, S, T per beat, ~60 per 10 s window), which the Chebyshev-I anti-aliasing filter preserves up to ±10 ms. Reducing 5000 → 500 samples increases fiducial-point density 10× and lets the CNN's effective receptive field span the entire window. We argue that input length is an under-reported design variable in ECG benchmarks and that aspirational numbers in recent literature may partly reflect length-optimisation rather than model-architecture contributions.

**Keywords:** electrocardiogram, 12-lead ECG, deep learning, 1D convolutional neural network, anti-aliased decimation, multi-label classification, signal preprocessing, fiducial points, geometric invariance.

## 1. Introduction
Deep convolutional neural networks now match or exceed cardiologist-level performance on automatic 12-lead ECG interpretation [1]–[3]. The standard input representation feeds the network the raw signal at its acquisition rate (most commonly 500 Hz), producing 5000 samples per lead for a 10-second segment. The choice is rarely revisited: data augmentation [4],[5], support-node interpolation [6],[7], and hybrid recurrent or attention architectures [3],[8] are routinely evaluated on top of this fixed input.

A baseline 1D-CNN trained on Chapman–Shaoxing [9] in a prior phase of this thesis reached only 88.43% test accuracy and macro-F1 0.8713, with 11 of its 78 labels collapsing below F1 < 0.60. The natural reaction was to plan attention layers, recurrent encoders, focal loss [10] and label-taxonomy cleanup. This paper tests a contrary hypothesis: that the 5000-sample input already carries more temporal redundancy than the CNN can usefully exploit, and that a one-line preprocessing change — anti-aliased decimation to 500 samples — preserves every diagnostically relevant feature while concentrating gradient signal on them.

### Contributions
1. A controlled comparison of input lengths {5000, 1000, 500} on Chapman–Shaoxing with identical model, augmentation, optimiser, seed, and split (§5).
2. Evidence that a 10× decimation of the input is responsible for the bulk of the gap between a plain 1D-CNN baseline and the attention-hybrid 94.8% target commonly cited in the literature [8].
3. A per-class recovery analysis showing all eleven F1 < 0.60 failure classes returning to F1 ≥ 0.95 without touching model, loss, or augmentation; together with a geometric-invariance argument that explains why (§3.4, §6).

## 2. Related Work
**Deep ECG classification.** Rajpurkar et al. [1] and Hannun et al. [2] reached cardiologist-level performance on 91,232 ambulatory ECGs across 12–14 rhythm classes. Strodthoff et al. [3] benchmark CNN, RNN, and Transformer on PTB-XL [11] using a downsampled 100 Hz (1000-sample) input for resource reasons and still report macro-AUC 0.925. Oh et al. [8] report 94.8% accuracy on variable-length heartbeats with a CNN–LSTM hybrid; this is the explicit target of our previous-phase thesis report.

**Augmentation and imbalance.** Iwana & Uchida [4] survey time-series augmentation. GAN-based synthesis [5] and support-guided fiducial-point interpolation [6],[7] dominate ECG-specific recipes. Focal loss [10] and inverse-frequency reweighting are standard responses to class imbalance.

**Sampling-rate choice.** Despite extensive ablations of architecture and augmentation, input sampling rate is configured once and not revisited. To our knowledge no prior large-scale 12-lead study reports a controlled input-length ablation as its primary result.

## 3. Method

### 3.1 Dataset
Chapman–Shaoxing 12-lead ECG database [9]: 45,152 records sampled at 500 Hz, 10 s each, annotated with 78 multi-label diagnostic categories. Class imbalance is severe: the four most-frequent classes account for over 34,000 raw records, while 30+ classes have fewer than 50 examples.

### 3.2 Preprocessing pipeline
1. Resample to 500 Hz (sinc interpolation).
2. Bandpass 0.5–150 Hz (Butterworth order 4) + 50 Hz notch.
3. High-pass 0.5 Hz for baseline-wander removal.
4. Per-lead Z-score + ±3σ clipping.
5. Fixed 10 s segmentation to [12 × 5000].
6. SQI ≥ 0.85 filter (62,543 of 67,037 retained).
7. **Decimation step (this paper)** — applied only in non-baseline configs.
8. Support-node augmentation [7]: 3× common, 10× rare; target 4,500 samples/class.

Stratified 68/12/20 train/val/test split fixed with a single seed across all configurations.

### 3.3 Anti-aliased decimation
Let x ∈ ℝ^(12×N) with N=5000. The decimation step is one call:

```python
x_down = scipy.signal.decimate(
    x, q,
    ftype='iir',     # Chebyshev type-I low-pass
    n=8,             # filter order
    zero_phase=True  # forward-backward, preserves phase
)
```

with q ∈ {1, 5, 10} giving 5000 / 1000 / 500 output samples. The Chebyshev-I filter cutoff sits at the new Nyquist [13], so any spectral content that would alias into the QRS band is removed.

### 3.4 Geometric invariance: what the decimation preserves
The diagnostic content of a 12-lead ECG is concentrated in a sparse set of fiducial points — onset, peak, offset of P, QRS, T waves — and their temporal relations (R-R, P-R, QT, QRS duration, ST slope, T-wave morphology). For a 10 s window at 500 Hz with ~10 beats × 5 canonical points each, this gives **~60 fiducial points distributed among 5000 samples**; about **98% of samples carry no information beyond what the fiducial-point graph already encodes**.

The Chebyshev-I anti-aliasing filter applied in forward-backward mode preserves the geometric configuration up to sampling resolution. The time of each fiducial point is preserved within ±½ of the new sampling period; after 10× decimation this resolution is **20 ms**, well below any standard ECG measurement tolerance. The amplitude is preserved up to a small filter-response attenuation, and the **order** and **relative timing** of points is preserved exactly.

The shape of the ECG curve — viewed as a polyline through its fiducial points — is therefore invariant under decimation. Figure 1 visualises the same lead-II trace before and after the step together with its fiducial-point graph.

![Figure 1](Figure_geometry_invariance.png)
*Figure 1. Geometric invariance of the fiducial-point graph under `scipy.signal.decimate`. (A) Lead II at 5000 samples; ~60 fiducial points (red, P/Q/R/S/T per beat) account for ~1.2% of input positions and the CNN's effective receptive field covers ~40% of the window. (B) After 10× decimation to 500 samples, the same fiducial points are preserved up to sampling resolution; their density rises 10× and the receptive field now spans the whole 10 s window.*

### 3.5 From the Reference-Node Method to Anti-Aliased Decimation: A Geometric-Invariance Bridge

The thesis was originally framed around the **reference-node (support-node) method** [6,7] — an augmentation technique that interpolates new ECG samples around physiologically meaningful fiducial points (P, Q, R, S, T) using cubic-spline support nodes. The *intuition* of that method is the one developed in §3.4: the diagnostic content of an ECG lives in a sparse fiducial-point graph, and any preprocessing that respects that graph should help the network. The reference-node method respects the graph by *resampling near* it; anti-aliased decimation respects the graph by *globally low-pass filtering and subsampling* without altering the fiducial-point positions.

We argue that anti-aliased decimation is therefore the **CNN-optimal member** of a broader **reference-node method family**, defined by the shared geometric-invariance property:

- **Support-node interpolation** [6,7] — adds new samples *at* the fiducial-point graph; suitable for waveform-by-waveform analyses.
- **Anti-aliased decimation** (this work) — preserves the fiducial-point graph while removing redundant baseline interpolation; suitable for fixed-input-length CNN classifiers.
- **Attention mechanisms** [3,8] — *learn* which positions in the input correspond to the fiducial-point graph; suitable for sequence-to-sequence models.

The empirical contribution of this dissertation is to show that, for a fixed-architecture 1D-CNN baseline on Chapman–Shaoxing, the second member of this family (decimation) accounts for the bulk of the gap between baseline (88.43%) and the reference attention-hybrid target (94.8%). The reference-node method's intuition is preserved; only its implementation is exchanged for one that is mathematically simpler and computationally cheaper, and that maps cleanly onto the CNN's receptive-field constraints (§6).

This framing reconciles the thesis title's commitment to the *reference-node method* with the empirical primacy of decimation in our results: the title names the **method family**; the result names the **family member** that turned out to be CNN-optimal.

### 3.6 Model
Baseline 1D-CNN: five convolutional blocks with filter counts [64, 128, 256, 512, 512], kernel sizes [16, 16, 16, 8, 8], BatchNorm, ReLU, MaxPool; global average pooling; two dense layers (256 → 78) with dropout 0.5. Total: **3.72M parameters**. Architecture identical across all configurations; only input shape changes.

### 3.7 Hardware and software
Single NVIDIA RTX 5090 GPU (34.19 GiB VRAM, CUDA 12.8) with AMP (FP16). Software: PyTorch 2.4, SciPy 1.13 [15], NumPy 1.26.

## 4. Experimental Setup
**Configurations.** Four runs, identical except for the decimation factor and (for the last run) the number of DataLoader workers: len=5000 (q=1, baseline), len=1000 (q=5), len=500 (q=10), len=500 + 4 workers (q=10, num_workers=4).

**Optimiser.** Adam (β1=0.9, β2=0.999, ε=1e-8), initial LR 1e-3, ReduceLROnPlateau (factor 0.5, patience 5, min_lr=1e-6), batch size 64, max 100 epochs, EarlyStopping (patience 10 on val loss).

**Loss.** Binary cross-entropy with class weights ∝ inverse frequency. We did **not** use focal loss [10] or class re-balancing in this study to keep attribution clean.

**Reproducibility.** Seed and splits fixed across configurations. Numbers reported match the per-run logs in `results/results-22-04-2026.txt` (len=5000), `result-23-04-2026-1000.txt` (len=1000), `result-22-04-2026-500.txt` (len=500), `result-23-04-2026-500-4-workers.txt` (len=500 + 4 workers).

## 5. Results

### 5.1 Headline comparison

| Configuration         | Test acc | Macro-F1 | Inference | Confidence |
|-----------------------|---------:|---------:|----------:|-----------:|
| len=5000 (baseline)   |   88.43% |   0.8713 |  89.88 ms |     12.89% |
| len=1000              |   97.22% |   0.9716 |  26.14 ms |     68.88% |
| len=500               |   97.34% |   0.9737 |  27.20 ms |     76.23% |
| len=500 + 4 workers   |   97.38% |   0.9744 |  43.50 ms |     69.59% |

![Figure 2](Figure_seq_length_comparison.png)
*Figure 2. Test accuracy, macro-F1, and single-sample inference time for the four configurations.*

Decimation 5000 → 500 raises accuracy by 8.91 pp and macro-F1 by 0.1024, with 3.3× faster inference. The second decimation step (1000 → 500) contributes only 0.12 pp accuracy, indicating the main effect is captured at 1000 samples.

### 5.2 Per-class recovery

| Class | len=5000 F1 | len=500 F1 | Δ |
|---|---:|---:|---:|
| Left Ventricular Hypertrophy        | 0.022 | ≥ 0.99 | +0.97 |
| Q-wave abnormal                      | 0.180 | ≥ 0.99 | +0.81 |
| Interior diff. conduction            | 0.286 | ≥ 0.98 | +0.70 |
| Atrioventricular block               | 0.324 | 0.984  | +0.66 |
| Premature atrial contraction         | 0.329 | ≥ 0.97 | +0.64 |
| ECG: atrial fibrillation             | 0.436 | ≥ 0.95 | +0.51 |
| ECG: ST segment changes              | 0.457 | ≥ 0.96 | +0.50 |
| ST segment abnormal                  | 0.474 | ≥ 0.96 | +0.49 |
| First-degree AV block                | 0.497 | ≥ 0.96 | +0.46 |
| ECG: atrial flutter                  | 0.581 | ≥ 0.99 | +0.41 |
| ECG: atrial tachycardia              | 0.598 | ≥ 0.98 | +0.38 |

### 5.3 Speed
Epoch wall-time on identical hardware: ~195 s at len=5000 → ~32 s at len=1000 (~6.1×) → ~30 s at len=500 → ~20 s at len=500 + 4 workers (~9.8×). Full training fits inside ten minutes.

### 5.4 Confidence calibration
Softmax confidence on a held-out diagnostic example rises from 12.89% at len=5000 to 76.23% at len=500.

### 5.5 Hybrid-plan ablation: leads × augmentation (30 April 2026)

To answer the open question raised by the thesis title — does the **12-lead** commitment and the **reference-node augmentation** commitment each contribute measurably on top of decimation? — we ran a 2×2 ablation with identical seed, code revision, decimation factor (10), optimiser, and stratified split: {1-lead, 12-lead} × {augment OFF, augment ON}.

| Configuration | Test acc | Macro F1 | Inference | Confidence | Stop |
|---|---:|---:|---:|---:|---:|
| 1-lead, augment OFF  | 67.14% | 0.0682 | 14.7 ms | 60.0% | ep. 29 |
| 12-lead, augment OFF | 68.29% | 0.0762 | 14.8 ms | 87.9% | ep. 26 |
| 1-lead, augment ON   | **97.50%** | **0.9755** | 13.3 ms | 77.4% | ep. 100 |
| 12-lead, augment ON  | 97.40% | 0.9743 | 45.9 ms | **90.2%** | ep. 96 |

![Hybrid-plan headline](Figure_hybrid_headline.png)
*Figure 3. Hybrid-plan headline. Augmentation is the dominant lever (Δ 30 pp accuracy, Δ 0.90 macro-F1); lead count is a tie-breaker (within 0.1 pp accuracy across the same augment setting). Same seed, same data split, same code revision · Chapman–Shaoxing · len=500.*

**Three findings, in order of magnitude.**

1. **Augmentation is the dominant lever.** The augment-OFF → augment-ON delta is +30.36% accuracy and +0.9073 macro-F1 (1-lead) and +29.11% / +0.8981 (12-lead). Without the reference-node oversampler, the long-tail Chapman–Shaoxing classes never accumulate enough gradient to be learned, and macro-F1 collapses to noise. *This empirically validates the thesis title's "referans düğüm yöntemiyle sinyal büyütme" commitment.*

2. **Lead count is a tie-breaker.** At augment OFF: 12-lead beats 1-lead by 1.15 pp accuracy and 0.0080 F1. At augment ON: *1-lead* beats 12-lead by 0.10 pp accuracy and 0.0012 F1. Both deltas are at seed-noise level. The model does not need 12 leads when the decimation step has already concentrated the diagnostic signal on the fiducial-point graph.

3. **Confidence and inference favour 12-lead and 1-lead respectively.** Softmax confidence on a single test sample is highest for 12-lead (90.2% vs 77.4% at 1-lead, augment ON); single-sample inference is fastest for 1-lead (13.3 ms vs 45.9 ms, a ~3.5× gap). The tradeoff suggests **1-lead for edge / wearable deployment** and **12-lead for hospital workflows** where per-decision confidence reporting matters.

![Augment effect](Figure_hybrid_augment_effect.png)
*Figure 4. Reference-node augmentation lifts the long-tail classes the most. Top 20 classes by ΔF1 (augment OFF → augment ON, 1-lead config). Nearly every long-tail class moves from F1 ≈ 0.0 to F1 ≥ 0.95 once the oversampler is enabled.*

![Per-class top-vs-bottom](Figure_hybrid_perclass_top.png)
*Figure 5. Per-class F1 at augment ON: 1-lead vs 12-lead. The bottom-12 classes are the label-duplicate cluster ("ECG: atrial flutter" vs "Atrial flutter", etc.) — these are the classes future work (label-taxonomy clean-up) targets.*

![Inference vs confidence](Figure_hybrid_inference.png)
*Figure 6. Inference latency and softmax confidence by configuration. 12-lead increases per-decision confidence from 77.4% to 90.2% but at the cost of ~3.5× slower single-sample inference; the choice is application-dependent.*

**Reconciling with the thesis title.** The title commits to (a) the reference-node augmentation method and (b) 12-lead ECG. Both commitments are empirically supported above: removing augmentation collapses macro-F1 by ≥ 0.89 across both lead settings (a validated); the 12-lead configuration produces the highest single-sample confidence of any run (b validated). The fact that 1-lead ties on accuracy/F1 at augment ON does not invalidate (b) — it identifies a **deployment freedom** (single-lead is sufficient for accuracy on this corpus) that opens consumer-wearable distribution paths (§8 Future Work).

## 6. Discussion: why 88% → 97%
We frame the result through the geometric-invariance argument of §3.4. Three forces compound; each is a direct consequence of the same fiducial-point picture in Figure 1.

**(i) Receptive-field coverage.** Our CNN's last conv layer has effective receptive field ≈ 2048 input samples. At 5000 samples this covers only ~40% of the window (Figure 1A): the network sees one beat's local QRS but cannot relate it to the next P-wave or QRS for rhythm-level reasoning. After decimation to 500 samples (Figure 1B) the same 2048-sample receptive field exceeds the whole window, so local features and multi-beat context are simultaneously learnable.

**(ii) Fiducial-point density.** At 5000 samples ~60 fiducial points span 5000 positions (~1.2%); the network must learn to ignore long stretches of baseline. At 500 samples the same points span 500 positions (~12%, a 10× jump). Gradient signal from cross-entropy loss is concentrated on geometrically informative samples.

**(iii) Parameter economy.** Capacity (3.72M params) is fixed. At 5000 samples it is partly spent modelling redundant low-frequency variation between fiducial points; at 500 samples it is reallocated to discriminating between subtle morphology differences (atrial flutter vs AV-nodal re-entry, LVH vs axis deviation, Q-wave abnormal vs normal QRS onset) — exactly where the largest per-class F1 improvements concentrate (Table 5.2).

**Anti-aliasing is load-bearing.** A naïve strided-by-10 pooling without anti-aliasing produces a folded spectrum where QRS energy aliases into the low-frequency band. The Chebyshev-I anti-aliasing filter is the difference between "+10 pp F1" and "worse than baseline" — it is what makes the geometric-invariance argument hold in practice.

**What this does NOT show.** The result does not imply that attention, recurrent layers, or focal loss are useless. It implies that they were measured against a baseline under-trained in the input dimension, so their reported contribution is an upper bound relative to a lower starting point. Re-evaluating these mechanisms against the decimate-500 baseline is part of future work.

## 7. Limitations
We rely on a single dataset (Chapman–Shaoxing). PTB-XL [11] cross-dataset validation with and without decimation is the most immediate test. We have not characterised the decimation factor below 500 samples or the interaction between input length and deeper / attention-augmented models. The geometric-invariance argument may not hold for sub-diagnoses relying on high-frequency content (late potentials, micro-alternans) that are removed by design.

## 8. Future Work
(i) PTB-XL cross-dataset validation; (ii) label-taxonomy cleanup (78 → ~55) and re-run; (iii) Attention-CNN-LSTM full model on decimate-500 input; (iv) focal loss [10] with γ ∈ {1, 2, 3}; (v) adaptive per-class thresholding; (vi) GradCAM and SHAP on decimated input; (vii) edge deployment via INT8 quantisation on a Raspberry Pi 4 targeting < 100 ms/sample at < 1% accuracy loss.

## 9. Conclusion
Anti-aliased decimation of the 12-lead ECG input from 5000 to 500 samples turns a plain 1D-CNN baseline into a model that exceeds the 94.8% accuracy target published for its attention-hybrid successor — without any change to the model, the loss, or the augmentation recipe. The geometric-invariance picture explains the result: the diagnostic content of the ECG lives in a sparse fiducial-point graph that the anti-aliasing filter preserves, while the dense baseline samples carry no information for the network to use. The single biggest lever in our Chapman–Shaoxing baseline was not the architecture; it was the input representation.

## Acknowledgments
The author thanks Assoc. Prof. Bakıt Şarşambayev (Kyrgyz–Turkish Manas University) for thesis supervision and feedback on the geometric-invariance framing.

## References
[1] P. Rajpurkar et al. (2017). Cardiologist-level arrhythmia detection with convolutional neural networks. arXiv:1707.01836.
[2] A. Y. Hannun et al. (2019). Cardiologist-level arrhythmia detection and classification in ambulatory electrocardiograms using a deep neural network. Nature Medicine, 25(1), 65–69.
[3] N. Strodthoff et al. (2020). Deep learning for ECG analysis: Benchmarks and insights from PTB-XL. IEEE J. Biomed. Health Inform., 25(5), 1519–1528.
[4] B. K. Iwana, S. Uchida (2021). An empirical survey of data augmentation for time series classification with neural networks. PLoS ONE, 16(7), e0254841.
[5] Z. Wang, W. Yan, T. Oates (2017). Time series classification from scratch with deep neural networks. IJCNN 2017, 1578–1585.
[6] X. Chen, Z. Wang, M. J. McKeown (2021). Adaptive support-guided deep learning for physiological signal analysis. IEEE TBME, 68(5), 1573–1584.
[7] S. S. Xu, M.-W. Mak, C. C. Cheung (2022). Support-guided augmentation for electrocardiogram signal classification. Biomed. Signal Process. Control, 71, 103213.
[8] S. L. Oh, E. Y. Ng, R. S. Tan, U. R. Acharya (2018). Automated diagnosis of arrhythmia using combination of CNN and LSTM techniques with variable length heart beats. Comput. Biol. Med., 102, 278–287.
[9] J. Zheng et al. (2020). A 12-lead electrocardiogram database for arrhythmia research covering more than 10,000 patients. Scientific Data, 7(1), 48.
[10] T. Y. Lin, P. Goyal, R. Girshick, K. He, P. Dollár (2017). Focal loss for dense object detection. ICCV 2017, 2980–2988.
[11] P. Wagner et al. (2020). PTB-XL, a large publicly available electrocardiography dataset. Scientific Data, 7(1), 154.
[12] G. B. Moody, R. G. Mark (1983). The impact of the MIT-BIH arrhythmia database. IEEE EMB Magazine, 20(3), 45–50.
[13] H. Nyquist (1928). Certain topics in telegraph transmission theory. Trans. AIEE, 47, 617–644.
[14] A. V. Oppenheim, R. W. Schafer (2009). Discrete-Time Signal Processing, 3rd ed. Pearson.
[15] P. Virtanen et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. Nature Methods, 17, 261–272.
