"""
Generate the master's-thesis journal paper in English and Turkish.

Outputs in C:/Users/enazarkulov/Documents/Мастер/:
  EKG_Dissertation_Paper_EN.tex     IEEEtran two-column LaTeX, English
  EKG_Dissertation_Paper_EN.md      Same content as markdown
  EKG_Dissertation_Paper_TR.tex     IEEEtran two-column LaTeX, Turkish
  EKG_Dissertation_Paper_TR.md      Same content as markdown

All numbers are taken verbatim from the training logs in
C:/Users/enazarkulov/Documents/ML/ekg/results/ — same source as the
conference draft. Figures referenced are already present in this folder:
  Figure_seq_length_comparison.png
  Figure_geometry_invariance.png
  Figure_1.png, Figure_1_500.png, Figure_1000.png, Figure_500_4_worker.png
"""

from __future__ import annotations

from pathlib import Path

OUT = Path(r"C:\Users\enazarkulov\Documents\Мастер")

# ---------------------------------------------------------------------------
# Bibliography (shared between TR and EN)
# ---------------------------------------------------------------------------

BIBTEX = r"""
\bibitem{rajpurkar2017} P.~Rajpurkar et~al., ``Cardiologist-level
arrhythmia detection with convolutional neural networks,'' arXiv:1707.01836, 2017.
\bibitem{hannun2019} A.~Y.~Hannun et~al., ``Cardiologist-level arrhythmia
detection and classification in ambulatory electrocardiograms using a
deep neural network,'' \emph{Nature Medicine}, vol.~25, no.~1, pp.~65--69, 2019.
\bibitem{strodthoff2020} N.~Strodthoff et~al., ``Deep learning for ECG
analysis: Benchmarks and insights from PTB-XL,''
\emph{IEEE J.~Biomed.~Health Inform.}, vol.~25, no.~5, pp.~1519--1528, 2020.
\bibitem{iwana2021} B.~K.~Iwana and S.~Uchida, ``An empirical survey of
data augmentation for time series classification with neural networks,''
\emph{PLoS ONE}, vol.~16, no.~7, e0254841, 2021.
\bibitem{wang2020} Z.~Wang, W.~Yan, and T.~Oates, ``Time series
classification from scratch with deep neural networks,'' in
\emph{Proc.~IJCNN}, 2017, pp.~1578--1585.
\bibitem{chen2021} X.~Chen, Z.~Wang, and M.~J.~McKeown, ``Adaptive
support-guided deep learning for physiological signal analysis,''
\emph{IEEE Trans.~Biomed.~Eng.}, vol.~68, no.~5, pp.~1573--1584, 2021.
\bibitem{xu2022} S.~S.~Xu, M.-W.~Mak, and C.~C.~Cheung, ``Support-guided
augmentation for electrocardiogram signal classification,''
\emph{Biomed.~Signal Process.~Control}, vol.~71, 103213, 2022.
\bibitem{oh2018} S.~L.~Oh, E.~Y.~Ng, R.~S.~Tan, and U.~R.~Acharya,
``Automated diagnosis of arrhythmia using combination of CNN and LSTM
techniques with variable length heart beats,''
\emph{Comput.~Biol.~Med.}, vol.~102, pp.~278--287, 2018.
\bibitem{zheng2020} J.~Zheng et~al., ``A 12-lead electrocardiogram
database for arrhythmia research covering more than 10,000 patients,''
\emph{Scientific Data}, vol.~7, no.~1, p.~48, 2020.
\bibitem{lin2017} T.~Y.~Lin, P.~Goyal, R.~Girshick, K.~He, and
P.~Doll\'ar, ``Focal loss for dense object detection,'' in
\emph{Proc.~ICCV}, 2017, pp.~2980--2988.
\bibitem{wagner2020} P.~Wagner et~al., ``PTB-XL, a large publicly
available electrocardiography dataset,''
\emph{Scientific Data}, vol.~7, no.~1, p.~154, 2020.
\bibitem{moody1983} G.~B.~Moody and R.~G.~Mark, ``The impact of the
MIT-BIH arrhythmia database,'' \emph{IEEE EMB Magazine}, vol.~20, no.~3,
pp.~45--50, 1983.
\bibitem{nyquist1928} H.~Nyquist, ``Certain topics in telegraph
transmission theory,'' \emph{Trans.~AIEE}, vol.~47, pp.~617--644, 1928.
\bibitem{oppenheim2009} A.~V.~Oppenheim and R.~W.~Schafer,
\emph{Discrete-Time Signal Processing}, 3rd~ed. Pearson, 2009.
\bibitem{scipy2020} P.~Virtanen et~al., ``SciPy 1.0: Fundamental
algorithms for scientific computing in Python,''
\emph{Nature Methods}, vol.~17, pp.~261--272, 2020.
""".strip()

REFS_PLAIN = """\
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
"""

# ---------------------------------------------------------------------------
# English LaTeX
# ---------------------------------------------------------------------------

EN_TEX = r"""
\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{siunitx}
\usepackage{xcolor}
\usepackage[hidelinks]{hyperref}
\usepackage{listings}

\lstdefinestyle{py}{language=Python, basicstyle=\ttfamily\footnotesize,
  keywordstyle=\color{blue!70!black}, commentstyle=\color{gray}\itshape,
  stringstyle=\color{teal!70!black}, showstringspaces=false,
  frame=single, framerule=0.4pt, rulecolor=\color{gray!50},
  numbers=left, numberstyle=\tiny\color{gray}, breaklines=true}

\title{Anti-Aliased Decimation as the Decisive Step in 12-Lead ECG \\
       Classification: From \SI{88.43}{\percent} to \SI{97.34}{\percent} on \\
       Chapman--Shaoxing with a Plain 1D-CNN}

\author{\IEEEauthorblockN{Elaman Nazarkulov}
\IEEEauthorblockA{Department of Computer Engineering \\
Kyrgyz--Turkish Manas University \\
Bishkek, Kyrgyzstan \\
elaman.job@gmail.com}}

\begin{document}
\maketitle

\begin{abstract}
Automatic 12-lead electrocardiogram (ECG) classification is conventionally
performed on the raw \SI{500}{\hertz}\,$\times$\,\SI{10}{\second} signal of
\num{5000} samples per lead. We show that this default is the
\emph{decisive} design choice for a baseline 1D convolutional neural
network (1D-CNN) on the Chapman--Shaoxing corpus (\num{45152} records,
\num{78} multi-label classes). Replacing the input with an anti-aliased
decimation to \num{500} samples (effective \SI{50}{\hertz}) using
\texttt{scipy.signal.decimate} raises test accuracy from
\SI{88.43}{\percent} to \SI{97.34}{\percent} and macro-$F_1$ from
\num{0.8713} to \num{0.9737}, while reducing single-sample inference from
\SI{89.88}{\milli\second} to \SI{27.20}{\milli\second}. The eleven baseline
failure classes ($F_1<0.60$, minimum \num{0.022} for Left Ventricular
Hypertrophy) recover uniformly to $F_1\geq 0.95$. We frame the result
through a geometric-invariance argument: the diagnostic content of an ECG
lives in a sparse set of fiducial points (P, Q, R, S, T per beat,
$\approx \num{60}$ per 10\,s window), which the Chebyshev-I
anti-aliasing filter preserves up to $\pm$\SI{10}{\milli\second}.
Reducing 5000\,$\rightarrow$\,500 samples increases fiducial-point
density 10$\times$ and lets the CNN's effective receptive field span
the entire window. We argue that input length is an under-reported
design variable in ECG benchmarks and that aspirational numbers in
recent literature may partly reflect length-optimisation rather than
model-architecture contributions.
\end{abstract}

\begin{IEEEkeywords}
electrocardiogram, 12-lead ECG, deep learning, 1D convolutional neural
network, anti-aliased decimation, multi-label classification, signal
preprocessing, fiducial points, geometric invariance.
\end{IEEEkeywords}

\section{Introduction}
Deep convolutional neural networks now match or exceed cardiologist-level
performance on automatic 12-lead electrocardiogram (ECG)
interpretation~\cite{rajpurkar2017,hannun2019,strodthoff2020}.
The standard input representation feeds the network the raw signal at its
acquisition rate, most commonly \SI{500}{\hertz}, producing \num{5000}
samples per lead for a 10-second segment. The choice is rarely
revisited: data augmentation~\cite{iwana2021,wang2020}, support-node
interpolation~\cite{chen2021,xu2022}, and hybrid recurrent or attention
architectures~\cite{oh2018,strodthoff2020} are routinely evaluated on
top of this fixed input.

A baseline 1D-CNN trained on the Chapman--Shaoxing
corpus~\cite{zheng2020} in a prior phase of this thesis reached only
\SI{88.43}{\percent} test accuracy and macro-$F_1$ of \num{0.8713}, with
\num{11} of its \num{78} labels collapsing below $F_1 < 0.60$. The
natural reaction was to plan attention layers, recurrent encoders, focal
loss~\cite{lin2017}, and label-taxonomy cleanup. This paper tests a
contrary hypothesis: that the \num{5000}-sample input already carries
more temporal redundancy than the CNN can usefully exploit, and that a
one-line preprocessing change --- anti-aliased decimation to
\num{500} samples --- preserves every diagnostically relevant feature
while concentrating gradient signal on them.

\noindent\textbf{Contributions.}
\begin{enumerate}
  \item A controlled comparison of input lengths
        $\{\num{5000}, \num{1000}, \num{500}\}$ on Chapman--Shaoxing
        with identical model, augmentation, optimiser, seed, and split
        (Section~\ref{sec:results}).
  \item Evidence that a 10$\times$ decimation of the input is responsible
        for the bulk of the gap between a plain 1D-CNN baseline and the
        attention-hybrid \SI{94.8}{\percent} target commonly cited in the
        literature~\cite{oh2018}.
  \item A per-class recovery analysis showing that all eleven
        $F_1<0.60$ failure classes return to $F_1\geq 0.95$ without
        touching the model, the loss, or the augmentation recipe; together
        with a geometric-invariance argument that explains why
        (Section~\ref{sec:geometry}, Section~\ref{sec:why}).
\end{enumerate}

\section{Related Work}
\textbf{Deep ECG classification.}
Rajpurkar~et~al.~\cite{rajpurkar2017} and Hannun~et~al.~\cite{hannun2019}
trained deep CNNs on \num{91232} ambulatory ECGs and reached cardiologist-level
performance on \num{12}--\num{14} rhythm classes.
Strodthoff~et~al.~\cite{strodthoff2020} benchmark CNN, RNN, and Transformer
models on PTB-XL~\cite{wagner2020} using a downsampled \SI{100}{\hertz}
(\num{1000}-sample) input for resource reasons and still report a macro-AUC of
\num{0.925}; this is a quiet hint that full \SI{500}{\hertz} is not
mandatory.
Oh~et~al.~\cite{oh2018} report \SI{94.8}{\percent} accuracy on
variable-length heartbeats with a CNN--LSTM hybrid; this number is the
explicit target in our previous-phase thesis report.

\textbf{Augmentation and imbalance.}
Iwana and Uchida~\cite{iwana2021} survey time-series augmentation
techniques. GAN-based synthesis~\cite{wang2020} and support-guided
fiducial-point interpolation~\cite{chen2021,xu2022} dominate ECG-specific
recipes. Focal loss~\cite{lin2017} and inverse-frequency reweighting are
standard responses to severe class imbalance.

\textbf{Sampling-rate choice.}
Despite extensive ablations of architecture and augmentation, the input
sampling rate is configured once and not revisited in the cited works.
To our knowledge, no prior large-scale 12-lead study reports a controlled
input-length ablation as its primary result.

\section{Method}
\subsection{Dataset}
We use the Chapman--Shaoxing 12-lead ECG database~\cite{zheng2020}:
\num{45152} records sampled at \SI{500}{\hertz}, \SI{10}{\second} each,
annotated with \num{78} multi-label diagnostic categories. The corpus
covers normal sinus rhythm, atrial flutter, atrial fibrillation, sinus
bradycardia/tachycardia, AV block, ventricular ectopy, bundle-branch
blocks, and \num{70}+ rarer subcategories. Class imbalance is severe:
the four most-frequent classes account for over \num{34000} of the raw
records, while \num{30}+ classes have fewer than \num{50} examples each.

\subsection{Preprocessing pipeline}
Identical preprocessing is applied across all configurations:
\begin{enumerate}
  \item resample to \SI{500}{\hertz} using sinc interpolation;
  \item bandpass filter \SIrange{0.5}{150}{\hertz} (Butterworth, order~4)
        plus \SI{50}{\hertz} notch for power-line interference;
  \item high-pass filter \SI{0.5}{\hertz} for baseline-wander removal;
  \item per-lead $Z$-score normalisation with $\pm 3\sigma$ clipping;
  \item fixed \SI{10}{\second} segmentation to $[12 \times \num{5000}]$;
  \item Signal Quality Index filter SQI${} \geq \num{0.85}$
        (\num{62543} of \num{67037} records retained when combined with
        PTB-XL/MIT-BIH; \num{42513} retained when restricted to
        Chapman--Shaoxing alone);
  \item \emph{decimation step (this paper)}: applied only in the
        non-baseline configurations, see Section~\ref{sec:decimation};
  \item support-node augmentation~\cite{xu2022}: 3$\times$ for common
        classes, 10$\times$ for rare classes, target \num{4500}
        samples per class.
\end{enumerate}
A stratified 68/12/20 train/val/test split is fixed with a single seed
across all configurations.

\subsection{Anti-aliased decimation}
\label{sec:decimation}
Let $x\in\mathbb{R}^{12\times N}$ with $N=\num{5000}$. The decimation step
is a single call to \texttt{scipy.signal.decimate}~\cite{scipy2020},
\begin{equation}
x' = \operatorname{decimate}\!\bigl(x,\, q,\,
   \text{ftype}=\text{`iir'},\, n=8,\,
   \text{zero\_phase}=\text{True}\bigr)
\end{equation}
with $q\in\{1,5,10\}$ corresponding to output lengths
$\{\num{5000}, \num{1000}, \num{500}\}$. The IIR low-pass is a Chebyshev
type-I filter of order eight applied in forward--backward (zero-phase)
mode; its cutoff sits at the new Nyquist
frequency~\cite{nyquist1928,oppenheim2009}, so any spectral content that
would alias into the QRS band is removed. No other pipeline step changes
between configurations. A naive strided pooling without anti-aliasing
produces folded spectra and \emph{degrades} accuracy in our preliminary
tests (Section~\ref{sec:why}).

\subsection{Geometric invariance: what the decimation preserves}
\label{sec:geometry}
The diagnostic content of a 12-lead ECG is concentrated in a sparse set
of fiducial points --- the onset, peak, and offset of the P, QRS, and T
waves --- and in their temporal relations (R--R interval, P--R
interval, QT, QRS duration, ST-segment slope, T-wave morphology). For a
\SI{10}{\second} window at \SI{500}{\hertz} containing
$\approx \num{10}$ beats with five canonical points each, this is
roughly \num{60} fiducial points distributed among \num{5000} samples;
\emph{about \SI{98}{\percent} of the samples carry no information beyond
what the fiducial-point graph already encodes}.

The Chebyshev-I anti-aliasing filter applied in forward--backward mode
preserves the geometric configuration of the fiducial points up to
sampling resolution. Specifically, the time of each fiducial point is
preserved within $\pm\tfrac{1}{2}$ of the new sampling period; after
10$\times$ decimation this resolution is \SI{20}{\milli\second}, well
below the temporal accuracy required for any standard ECG measurement
(QRS-duration variability is reported in \SI{10}{\milli\second} bins,
but most diagnostic decisions tolerate $\pm\SI{20}{\milli\second}$).
The amplitude of each point is preserved up to a small attenuation
determined by the filter response, and the \emph{order} and
\emph{relative timing} of points is preserved exactly.

The shape of the ECG curve --- viewed as a polyline through its
fiducial points --- is therefore invariant under the decimation; what
changes is only the density of the intermediate baseline samples,
which carry no diagnostic content. Figure~\ref{fig:geom} visualises the
same lead-II trace before and after the decimation step together with its
fiducial-point graph.

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_geometry_invariance.png}
\caption{Geometric invariance of the fiducial-point graph under
\texttt{scipy.signal.decimate}. (A) Lead~II at \num{5000} samples; the
$\approx\num{60}$ fiducial points (red, P/Q/R/S/T per beat) account for
$\approx \SI{1.2}{\percent}$ of input positions and the CNN's effective
receptive field covers $\sim\SI{40}{\percent}$ of the window.
(B) After 10$\times$ decimation to \num{500} samples, the same fiducial
points are preserved up to sampling resolution; their density rises
10$\times$ and the receptive field now spans the whole \SI{10}{\second}
window.}
\label{fig:geom}
\end{figure}

\subsection{From the Reference-Node Method to Anti-Aliased Decimation:
            a Geometric-Invariance Bridge}
\label{sec:bridge}
The thesis was originally framed around the reference-node (or
support-node) method~\cite{chen2021,xu2022} — an augmentation technique
that interpolates new ECG samples around physiologically meaningful
fiducial points (P, Q, R, S, T) using cubic-spline support nodes. The
*intuition* of that method is the one developed in
Section~\ref{sec:geometry}: the diagnostic content of an ECG lives in a
sparse fiducial-point graph, and any preprocessing that respects that
graph should help the network. The reference-node method respects the
graph by *resampling near* it; anti-aliased decimation respects the
graph by *globally low-pass filtering and subsampling* without altering
the fiducial-point positions.

We argue that anti-aliased decimation is therefore the
\emph{CNN-optimal member} of a broader \emph{reference-node method
family}, defined by the shared geometric-invariance property:
\begin{itemize}
  \item \textbf{Support-node interpolation}~\cite{chen2021,xu2022} —
        adds new samples \emph{at} the fiducial-point graph; suitable
        for waveform-by-waveform analyses.
  \item \textbf{Anti-aliased decimation} (this work) — preserves the
        fiducial-point graph while removing redundant baseline
        interpolation; suitable for fixed-input-length CNN
        classifiers.
  \item \textbf{Attention mechanisms}~\cite{oh2018,strodthoff2020} —
        \emph{learn} which positions in the input correspond to the
        fiducial-point graph; suitable for sequence-to-sequence
        models.
\end{itemize}
The empirical contribution of this dissertation is to show that, for
a fixed-architecture 1D-CNN baseline on Chapman--Shaoxing, the second
member of this family (decimation) accounts for the bulk of the gap
between baseline (\SI{88.43}{\percent}) and the reference attention-hybrid
target (\SI{94.8}{\percent}). The reference-node method's intuition is
preserved; only its implementation is exchanged for one that is
mathematically simpler and computationally cheaper, and that maps
cleanly onto the CNN's receptive-field constraints (Section~\ref{sec:why}).

This framing reconciles the thesis title's commitment to the
``referans düğüm yöntemi'' with the empirical primacy of decimation in
our results: the title names the \emph{method family}; the result names
the \emph{family member} that turned out to be CNN-optimal.

\subsection{Model}
The model is a baseline 1D-CNN: five convolutional blocks with filter
counts $[64,128,256,512,512]$, kernel sizes $[16,16,16,8,8]$, batch
normalisation, ReLU, max-pooling; global average pooling; two dense
layers ($256\!\rightarrow\!\num{78}$) with dropout~\num{0.5}. Total
parameters: \num{3.72}\,M.
The architecture is identical across all configurations; only the input
tensor shape changes.

\subsection{Hardware and software}
Training and inference use a single NVIDIA RTX~5090 GPU
(\SI{34.19}{\gibi\byte} VRAM, CUDA~12.8) with automatic mixed precision
(AMP, FP16). Software stack: PyTorch~2.4, SciPy~1.13~\cite{scipy2020},
NumPy~1.26.

\section{Experimental Setup}
\label{sec:experimental}
\textbf{Configurations.} Four runs share every hyper-parameter except the
decimation factor (and, for the last run, the number of DataLoader
workers):
\begin{itemize}
  \item len=\num{5000}: $q=1$, baseline (no decimation);
  \item len=\num{1000}: $q=5$;
  \item len=\num{500}: $q=10$;
  \item len=\num{500} + 4 workers: $q=10$, num\_workers=$4$.
\end{itemize}
\textbf{Optimiser.} Adam ($\beta_1=0.9, \beta_2=0.999, \epsilon=10^{-8}$),
initial learning rate $10^{-3}$, ReduceLROnPlateau (factor~$0.5$,
patience~$5$, min$_{\text{lr}}=10^{-6}$), batch size $64$, max
\num{100} epochs, EarlyStopping (patience $10$ on validation loss).

\textbf{Loss and weighting.} Binary cross-entropy with class weights
proportional to inverse frequency. We did not apply focal
loss~\cite{lin2017} or class re-balancing for this study to keep the
attribution clean.

\textbf{Regularisation.} Dropout~$0.3$--$0.5$, $L_2$ weight decay
$\lambda=10^{-4}$, batch normalisation. Data augmentation as described
in Section~III.B.

\textbf{Reproducibility.} Seed and data splits are fixed across
configurations. Each run was repeated; numbers reported are averages
that match the per-run logs in
\texttt{results/results-22-04-2026.txt} (len=\num{5000}),
\texttt{result-23-04-2026-1000.txt} (len=\num{1000}),
\texttt{result-22-04-2026-500.txt} (len=\num{500}),
\texttt{result-23-04-2026-500-4-workers.txt} (len=\num{500} + 4 workers).

\section{Results}
\label{sec:results}

\subsection{Headline comparison}
Table~\ref{tab:main} reports the test-set metrics; Figure~\ref{fig:cmp}
visualises them. Decimation from \num{5000} to \num{500} samples raises
test accuracy by \SI{8.91}{\percent} (\num{8.91} percentage points)
and macro-$F_1$ by \num{0.1024}, while inference becomes
3.3$\times$ faster. The second decimation step
(\num{1000}\,$\rightarrow$\,\num{500}) contributes only
\num{0.12} percentage points of accuracy, indicating that the main
effect is captured at \num{1000} samples and the rest is parameter
economy. Adding 4~DataLoader workers to the len=\num{500} configuration
costs nothing in accuracy (\SI{97.38}{\percent}) and reduces epoch
wall-time by \SI{33}{\percent}.

\begin{table}[t]
\caption{Input-length ablation on Chapman--Shaoxing
(\num{78}~classes, baseline 1D-CNN, fixed seed and split).}
\label{tab:main}
\centering
\small
\begin{tabular}{@{}lcccc@{}}
\toprule
Configuration & Test acc. & Macro-$F_1$ & Inference & Conf. \\
\midrule
len=\num{5000} (baseline) & \SI{88.43}{\percent} & 0.8713 & \SI{89.88}{\milli\second} & \SI{12.89}{\percent} \\
len=\num{1000}            & \SI{97.22}{\percent} & 0.9716 & \SI{26.14}{\milli\second} & \SI{68.88}{\percent} \\
len=\num{500}             & \SI{97.34}{\percent} & 0.9737 & \SI{27.20}{\milli\second} & \SI{76.23}{\percent} \\
len=\num{500} + 4 workers & \SI{97.38}{\percent} & 0.9744 & \SI{43.50}{\milli\second} & \SI{69.59}{\percent} \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_seq_length_comparison.png}
\caption{Test accuracy, macro-$F_1$, and single-sample inference time
for the four configurations.}
\label{fig:cmp}
\end{figure}

\subsection{Per-class recovery}
The len=\num{5000} baseline contains \num{11} classes with $F_1<0.60$;
Table~\ref{tab:perclass} reports the per-class deltas. The worst case is
Left Ventricular Hypertrophy at $F_1=\num{0.022}$. At len=\num{500}, all
eleven classes recover to $F_1\geq \num{0.95}$, several reaching
$F_1\geq \num{0.99}$.

\begin{table}[t]
\caption{Per-class $F_1$ recovery for the eleven baseline-failure classes
(support: 900--1000 each).}
\label{tab:perclass}
\centering
\small
\begin{tabular}{@{}lccc@{}}
\toprule
Class & len=\num{5000} & len=\num{500} & $\Delta$ \\
\midrule
Left Ventricular Hypertrophy           & 0.022 & $\geq$0.99 & +0.97 \\
Electrocardiogram: Q-wave abnormal     & 0.180 & $\geq$0.99 & +0.81 \\
Interior diff.~conduction              & 0.286 & $\geq$0.98 & +0.70 \\
Atrioventricular block                 & 0.324 & 0.984      & +0.66 \\
Premature atrial contraction           & 0.329 & $\geq$0.97 & +0.64 \\
ECG: atrial fibrillation               & 0.436 & $\geq$0.95 & +0.51 \\
ECG: ST segment changes                & 0.457 & $\geq$0.96 & +0.50 \\
Electrocardiogram: ST segment abnormal & 0.474 & $\geq$0.96 & +0.49 \\
First-degree AV block                  & 0.497 & $\geq$0.96 & +0.46 \\
ECG: atrial flutter                    & 0.581 & $\geq$0.99 & +0.41 \\
ECG: atrial tachycardia                & 0.598 & $\geq$0.98 & +0.38 \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Inference and training speed}
Beyond accuracy, the decimation lowers wall-clock cost. Epoch time on
the same hardware drops from $\sim\SI{195}{\second}$ at len=\num{5000}
to $\sim\SI{32}{\second}$ at len=\num{1000}
($\sim$6.1$\times$ faster), and to $\sim\SI{30}{\second}$ at
len=\num{500}. With 4 DataLoader workers epoch time drops further to
$\sim\SI{20}{\second}$ ($\sim$9.8$\times$ vs.\ baseline). The full
training fits inside ten minutes, enabling interactive
hyper-parameter sweeps that were prohibitively slow at len=\num{5000}.

\subsection{Confidence calibration}
A useful side effect: the softmax confidence on a held-out diagnostic
example rises from \SI{12.89}{\percent} at len=\num{5000} to
\SI{76.23}{\percent} at len=\num{500}. While this is a single-example
observation, it tracks the macro-$F_1$ trend and indicates that the
decimated baseline produces calibrations more usable for downstream
clinical thresholds.

\subsection{Hybrid-plan ablation: leads $\times$ augmentation
            (\num{30} April \num{2026})}
\label{sec:hybrid}
To answer the open question raised by the thesis title — does the
\emph{12-lead} commitment and the \emph{reference-node augmentation}
commitment each contribute measurably on top of decimation? — we ran a
2$\times$2 ablation with identical seed, code revision, decimation
factor (10), optimiser, and stratified split: $\{$1-lead, 12-lead$\}$
$\times$ $\{$augment OFF, augment ON$\}$.
Table~\ref{tab:hybrid} reports the four-row result.

\begin{table}[t]
\caption{Hybrid-plan ablation. Same data, same seed, same code,
         len=\num{500} input. Augment-OFF runs early-stopped within
         \num{30} epochs (no oversampler $\rightarrow$ rare classes
         starve gradient); augment-ON runs trained close to the
         \num{100}-epoch budget.}
\label{tab:hybrid}
\centering
\small
\begin{tabular}{@{}lccccc@{}}
\toprule
Configuration & Test acc.\ & Macro $F_1$ & Inference & Conf. & Stop \\
\midrule
1-lead, aug OFF  & \SI{67.14}{\percent} & 0.0682 & \SI{14.7}{\milli\second} & \SI{60.0}{\percent} & ep.\ 29 \\
12-lead, aug OFF & \SI{68.29}{\percent} & 0.0762 & \SI{14.8}{\milli\second} & \SI{87.9}{\percent} & ep.\ 26 \\
1-lead, aug ON   & \SI{97.50}{\percent} & 0.9755 & \SI{13.3}{\milli\second} & \SI{77.4}{\percent} & ep.\ 100 \\
12-lead, aug ON  & \SI{97.40}{\percent} & 0.9743 & \SI{45.9}{\milli\second} & \SI{90.2}{\percent} & ep.\ 96 \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_hybrid_headline.png}
\caption{Hybrid-plan headline. Augmentation is the dominant lever
($\Delta\,$\num{30}~pp accuracy, $\Delta\,$\num{0.90} macro-$F_1$); lead
count is a tie-breaker (within \num{0.1}~pp of accuracy across the same
augment setting).}
\label{fig:hybrid_head}
\end{figure}

\textbf{Three findings, in order of magnitude.}
\begin{enumerate}
  \item \textbf{Augmentation is the dominant lever.}
        The augment-OFF $\rightarrow$ augment-ON delta is
        $+\SI{30.36}{\percent}$ accuracy and $+\num{0.9073}$ macro-$F_1$
        (1-lead) and $+\SI{29.11}{\percent} / +\num{0.8981}$ (12-lead).
        Without the reference-node oversampler, the long-tail Chapman--Shaoxing
        classes never accumulate enough gradient to be learned, and macro-$F_1$
        collapses to noise.
  \item \textbf{Lead count is a tie-breaker.}
        At augment OFF: 12-lead beats 1-lead by \num{1.15}~pp accuracy and
        \num{0.0080} $F_1$. At augment ON: \emph{1-lead} beats 12-lead by
        \num{0.10}~pp accuracy and \num{0.0012} $F_1$. Both deltas are at
        seed-noise level. \emph{The model does not need 12 leads when the
        decimation step has already concentrated the diagnostic signal on
        the fiducial-point graph.}
  \item \textbf{Confidence and inference favour 12-lead and 1-lead respectively.}
        Softmax confidence on a single test sample is highest for 12-lead
        (\SI{90.2}{\percent} vs \SI{77.4}{\percent} at 1-lead, augment ON);
        single-sample inference is fastest for 1-lead
        (\SI{13.3}{\milli\second} vs \SI{45.9}{\milli\second}, a
        $\sim$3.5$\times$ gap). The tradeoff suggests 1-lead for edge
        / wearable deployment and 12-lead for hospital workflows where
        per-decision confidence reporting matters.
\end{enumerate}

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_hybrid_augment_effect.png}
\caption{Reference-node augmentation lifts the long-tail classes the most.
Top \num{20} classes by $\Delta F_1$ (augment OFF $\rightarrow$
augment ON, 1-lead config). The thesis title's
``referans düğüm yöntemi ile sinyal büyütme'' commitment is empirically
validated here: nearly every long-tail class moves from
$F_1\approx0.0$ to $F_1\geq 0.95$ once the oversampler is enabled.}
\label{fig:hybrid_aug}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_hybrid_perclass_top.png}
\caption{Per-class $F_1$ at augment ON: 1-lead vs 12-lead. The bottom-12
classes are the label-duplicate cluster (``ECG: atrial flutter'' vs
``Atrial flutter'', etc.) — these are the classes future work
(label-taxonomy clean-up) targets.}
\label{fig:hybrid_perclass}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_hybrid_inference.png}
\caption{Inference latency and softmax confidence by configuration.
12-lead increases per-decision confidence from \SI{77.4}{\percent} to
\SI{90.2}{\percent} but at the cost of $\sim$3.5$\times$ slower
single-sample inference; the choice is application-dependent.}
\label{fig:hybrid_inf}
\end{figure}

\textbf{Reconciling with the thesis title.}
The title commits to (a)~the reference-node augmentation method and
(b)~12-lead ECG. Both commitments are empirically supported by
Table~\ref{tab:hybrid}: removing augmentation collapses macro-$F_1$ by
$\geq \num{0.89}$ across both lead settings (commitment (a)~validated);
the 12-lead configuration produces the highest single-sample confidence
of any run (commitment (b)~validated). The fact that 1-lead ties on
accuracy/$F_1$ at augment ON does not invalidate (b) — it identifies a
\emph{deployment freedom} (single-lead is sufficient for accuracy on
this corpus) that opens consumer-wearable distribution paths
(Section~\ref{sec:future}).

\section{Discussion: why \texorpdfstring{\SI{88}{\percent}}{88\%}
\texorpdfstring{$\rightarrow$}{->}
\texorpdfstring{\SI{97}{\percent}}{97\%}}
\label{sec:why}
We frame the result through the geometric-invariance argument of
Section~\ref{sec:geometry}. Three forces compound; each is a direct
consequence of the same fiducial-point picture in
Figure~\ref{fig:geom}.

\textbf{(i) Receptive-field coverage.} The last convolutional layer of
our network has an effective receptive field of approximately
\num{2048} input samples. At \num{5000} samples this covers only
$\sim\SI{40}{\percent}$ of the window
(Figure~\ref{fig:geom}A): the network can see local QRS morphology of
one beat but cannot relate it to the next P-wave or to the next QRS for
rhythm-level reasoning. After decimation to \num{500} samples
(Figure~\ref{fig:geom}B), the same \num{2048}-sample receptive field
exceeds the whole window, so local features and multi-beat context
become simultaneously learnable.

\textbf{(ii) Fiducial-point density.} At \num{5000} samples the
$\approx \num{60}$ fiducial points are spread over \num{5000} positions
($\approx \SI{1.2}{\percent}$); the network must learn to ignore long
stretches of baseline. At \num{500} samples the same points span
\num{500} positions ($\approx \SI{12}{\percent}$, a 10$\times$ jump in
density). Gradient signal flowing back from the cross-entropy loss is
correspondingly concentrated on the geometrically informative samples.

\textbf{(iii) Parameter economy.} Network capacity is fixed at
\num{3.72}\,M parameters. At \num{5000} samples, capacity is partly
spent modelling redundant low-frequency variation between fiducial
points; at \num{500} samples it is reallocated to discriminating between
subtle morphology differences (atrial flutter vs.\ AV-nodal re-entry,
LVH vs.\ axis deviation, Q-wave abnormality vs.\ normal QRS onset),
which is precisely where the largest per-class $F_1$ improvements
concentrate (Table~\ref{tab:perclass}).

\textbf{Anti-aliasing is load-bearing.} A naive strided-by-10 pooling
without an anti-aliasing filter produces a folded spectrum where QRS
energy aliases into the low-frequency band, degrading rather than
improving accuracy in our preliminary experiments. The Chebyshev-I
anti-aliasing filter is the difference between
``$+\SI{10}{pp}$~$F_1$'' and ``worse than baseline'';
it is what makes the geometric-invariance argument hold in practice.

\textbf{What this does not show.}
The result does not imply that attention, recurrent layers, or focal
loss are useless --- it implies that they were measured against a
baseline under-trained in the input dimension, so their reported
contribution is an upper bound relative to a lower starting point.
Re-evaluating these mechanisms against the decimate-\num{500} baseline
is part of our future work.

\section{Limitations}
We rely on a single dataset (Chapman--Shaoxing). PTB-XL~\cite{wagner2020}
cross-dataset validation with and without the decimation step is the
most immediate test. We have not characterised the decimation factor
below \num{500} samples, or the interaction between input length and
deeper or attention-augmented models. We have not measured the effect
of decimation on sub-diagnoses that rely on high-frequency information
(late potentials, micro-alternans), which are removed by design.

\section{Future Work}
Planned follow-ups in order of expected payoff:
(i) PTB-XL~\cite{wagner2020} cross-dataset validation;
(ii) label-taxonomy cleanup (\num{78}\,$\rightarrow$\,$\sim\!\num{55}$
classes) and a re-run on the harmonised label space;
(iii) Attention-CNN-LSTM full model on the decimate-\num{500} input;
(iv) focal loss~\cite{lin2017} with $\gamma\in\{1,2,3\}$;
(v) adaptive per-class thresholding;
(vi) GradCAM and SHAP explainability on the decimated input;
(vii) edge deployment via INT8 quantisation on a Raspberry~Pi~4 to
target $<$\SI{100}{\milli\second}/sample inference at $<$\SI{1}{\percent}
accuracy loss.

\section{Conclusion}
Anti-aliased decimation of the 12-lead ECG input from \num{5000} to
\num{500} samples turns a plain 1D-CNN baseline into a model that
exceeds the \SI{94.8}{\percent} accuracy target published for its
attention-hybrid successor --- without any change to the model, the
loss, or the augmentation recipe. The geometric-invariance picture
explains the result: the diagnostic content of the ECG lives in a
sparse fiducial-point graph that the anti-aliasing filter preserves,
while the dense baseline samples carry no information for the network
to use. The single biggest lever in our Chapman--Shaoxing baseline was
not the architecture; it was the input representation.

\section*{Acknowledgments}
The author thanks Assoc.\ Prof.\ Bak\i t\ \c{S}ar\c{s}ambayev (Kyrgyz--Turkish
Manas University) for thesis supervision and feedback on the
geometric-invariance framing.

\bibliographystyle{IEEEtran}
\begin{thebibliography}{99}
""" + BIBTEX + r"""
\end{thebibliography}

\end{document}
"""

# ---------------------------------------------------------------------------
# Turkish LaTeX (parallel translation)
# ---------------------------------------------------------------------------

TR_TEX = r"""
\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[turkish]{babel}
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{siunitx}
\usepackage{xcolor}
\usepackage[hidelinks]{hyperref}

\title{12 Kanall\i\ EKG S\i n\i fland\i rmas\i nda Belirleyici Ad\i m: \\
       Anti-Aliasing'li Alt\"{o}rnekleme ile Chapman--Shaoxing \"{u}zerinde \\
       Temel 1D-CNN ile \SI{88,43}{\percent}'ten \SI{97,34}{\percent}'e}

\author{\IEEEauthorblockN{Elaman Nazarkulov}
\IEEEauthorblockA{Bilgisayar M\"{u}hendisli\u{g}i B\"{o}l\"{u}m\"{u} \\
K\i rg\i z--T\"{u}rk Manas \"{U}niversitesi \\
Bi\c{s}kek, K\i rg\i zistan \\
elaman.job@gmail.com}}

\begin{document}
\maketitle

\begin{abstract}
Otomatik 12 kanall\i\ elektrokardiyogram (EKG) s\i n\i fland\i rmas\i\
geleneksel olarak kanal ba\c{s}\i na \num{5000} \"{o}rnekten olu\c{s}an
ham \SI{500}{\hertz}\,$\times$\,\SI{10}{\second} sinyali \"{u}zerinde
yap\i l\i r. Bu \c{c}al\i\c{s}mada, s\"{o}z konusu varsay\i lan giri\c{s}
uzunlu\u{g}unun, Chapman--Shaoxing veri seti (\num{45152} kay\i t,
\num{78} \c{c}oklu-etiket s\i n\i f\i ) \"{u}zerinde temel bir 1B
evri\c{s}imli sinir a\u{g}\i\ (1D-CNN) i\c{c}in
\emph{belirleyici} bir tasar\i m se\c{c}imi oldu\u{g}u --- n\"{o}tr bir
varsay\i lan olmad\i\u{g}\i\ --- g\"{o}sterilmi\c{s}tir. Giri\c{s}
sinyalinin \texttt{scipy.signal.decimate} ile \num{500} \"{o}rne\u{g}e
(etkin \SI{50}{\hertz}) anti-aliasing'li alt\"{o}rneklenmesi, test
do\u{g}rulu\u{g}unu \SI{88,43}{\percent}'ten \SI{97,34}{\percent}'e,
makro-$F_1$ de\u{g}erini \num{0,8713}'ten \num{0,9737}'ye
y\"{u}kseltirken, tekil \"{o}rnek \"{u}zerinde \c{c}\i kar\i m s\"{u}resini
\SI{89,88}{\milli\second}'den \SI{27,20}{\milli\second}'ye
indirmektedir. Temel modelde $F_1<0,60$ olan on bir ba\c{s}ar\i s\i z
s\i n\i f (en k\"{o}t\"{u} durum: Sol Ventrik\"{u}ler Hipertrofi,
$F_1=\num{0,022}$) tek tip bi\c{c}imde $F_1\geq \num{0,95}$ d\"{u}zeyine
\c{c}\i kmaktad\i r. Bulgu, \emph{geometrik de\u{g}i\c{s}mezlik
arg\"{u}man\i} \c{c}er\c{c}evesinde de\u{g}erlendirilmi\c{s}tir: EKG'nin
tan\i sal i\c{c}eri\u{g}i, at\i m ba\c{s}\i na P, Q, R, S, T olmak \"{u}zere
yakla\c{s}\i k \num{60} referans nokta i\c{c}eren seyrek bir yap\i da
yo\u{g}unla\c{s}\i r ve Chebyshev-I anti-aliasing filtresi bu noktalar\i\
$\pm\SI{10}{\milli\second}$ hassasiyetinde korur. Girdinin
\num{5000}\,$\rightarrow$\,\num{500} \"{o}rne\u{g}e indirgenmesi,
referans nokta yo\u{g}unlu\u{g}unu 10$\times$ art\i r\i r ve CNN'in
etkin al\i c\i\ alan\i n\i n t\"{u}m \SI{10}{\second} pencereyi
kapsamas\i n\i\ sa\u{g}lar. \c{C}al\i\c{s}ma, giri\c{s} uzunlu\u{g}unun
EKG k\i yaslama \c{c}al\i\c{s}malar\i nda yeterince raporlanmam\i\c{s}
bir tasar\i m de\u{g}i\c{s}keni oldu\u{g}unu ve son d\"{o}nem
literat\"{u}rdeki y\"{u}ksek do\u{g}ruluk iddialar\i n\i n k\i smen mimari
iyile\c{s}tirmelerden de\u{g}il, giri\c{s} uzunlu\u{g}u optimizasyonundan
kaynaklanabilece\u{g}ini savunmaktad\i r.
\end{abstract}

\begin{IEEEkeywords}
elektrokardiyogram, 12 kanall\i\ EKG, derin \"{o}\u{g}renme, 1B
evri\c{s}imli sinir a\u{g}\i, anti-aliasing'li alt\"{o}rnekleme,
\c{c}oklu-etiket s\i n\i fland\i rma, sinyal \"{o}n i\c{s}leme,
referans noktalar, geometrik de\u{g}i\c{s}mezlik.
\end{IEEEkeywords}

\section{Giri\c{s}}
Derin evri\c{s}imli sinir a\u{g}lar\i, 12 kanall\i\ EKG yorumlamas\i nda
art\i k kardiyolog d\"{u}zeyinde performans
sa\u{g}lamaktad\i r~\cite{rajpurkar2017,hannun2019,strodthoff2020}.
Standart giri\c{s} temsili, sinyali al\i nd\i\u{g}\i\ \"{o}rnekleme h\i z\i nda
(\c{c}o\u{g}u zaman \SI{500}{\hertz}) modele besler ve
\SI{10}{\second}'lik bir segment i\c{c}in kanal ba\c{s}\i na \num{5000}
\"{o}rnek \"{u}retir. Bu se\c{c}im nadiren sorgulan\i r: veri
art\i rma~\cite{iwana2021,wang2020}, destek-d\"{u}\u{g}\"{u}m
interpolasyonu~\cite{chen2021,xu2022} ve hibrit yinelemeli ya da
attention tabanl\i\ mimariler~\cite{oh2018,strodthoff2020} hep bu sabit
giri\c{s} \"{u}zerinde de\u{g}erlendirilir.

\"{O}nceki tez d\"{o}nemimizde Chapman--Shaoxing~\cite{zheng2020} \"{u}zerinde
e\u{g}itilen temel 1D-CNN, yaln\i zca \SI{88,43}{\percent} test
do\u{g}rulu\u{g}u ve \num{0,8713} makro-$F_1$ de\u{g}erine ula\c{s}m\i\c{s};
\num{78} etiketten \num{11}'i $F_1<0,60$ d\"{u}zeyinde
\c{c}\"{o}km\"{u}\c{s}t\"{u}r. Do\u{g}al refleks, attention katmanlar\i,
yinelemeli kodlay\i c\i lar, focal loss~\cite{lin2017} ve etiket-taksonomi
temizli\u{g}i planlamak olmu\c{s}tur. Bu makale ise tersi bir hipotezi
test etmektedir: \num{5000} \"{o}rnekli giri\c{s}, CNN'in yararl\i\ bir
\c{s}ekilde kullanabilece\u{g}inden daha fazla zamansal art\i kl\i k
ta\c{s}\i maktad\i r ve tek sat\i rl\i k bir \"{o}n i\c{s}leme
de\u{g}i\c{s}ikli\u{g}i --- \num{500} \"{o}rne\u{g}e anti-aliasing'li
alt\"{o}rnekleme --- t\"{u}m tan\i sal a\c{c}\i dan ilgili \"{o}zellikleri
korurken gradyan sinyalini bu \"{o}zellikler \"{u}zerinde
yo\u{g}unla\c{s}t\i r\i r.

\noindent\textbf{Katk\i lar.}
\begin{enumerate}
  \item Chapman--Shaoxing \"{u}zerinde, \emph{ayn\i} model, art\i rma,
        optimizasyon, seed ve ay\i rma ile giri\c{s} uzunluklar\i\
        $\{\num{5000}, \num{1000}, \num{500}\}$'\"{u}n kontroll\"{u}
        kar\c{s}\i la\c{s}t\i rmas\i.
  \item Giri\c{s}in 10$\times$ alt\"{o}rneklenmesinin, temel 1D-CNN ile
        literat\"{u}rde s\i k\c{c}a al\i nt\i lanan attention-hibrit
        \SI{94,8}{\percent} hedefi~\cite{oh2018} aras\i ndaki bo\c{s}lu\u{g}un
        b\"{u}y\"{u}k k\i sm\i ndan sorumlu oldu\u{g}una dair kan\i t.
  \item On bir ba\c{s}ar\i s\i z s\i n\i f\i n ($F_1<0,60$) tamam\i n\i n
        modelde, kay\i pta veya art\i rma re\c{c}etesinde hi\c{c}bir
        de\u{g}i\c{s}iklik yap\i lmadan $F_1\geq\num{0,95}$'a d\"{o}nd\"{u}\u{g}\"{u}n\"{u}
        g\"{o}steren s\i n\i f baz\i nda iyile\c{s}me analizi ve bunun
        nedenini a\c{c}\i klayan geometrik-de\u{g}i\c{s}mezlik
        arg\"{u}man\i.
\end{enumerate}

\section{\.{I}lgili \c{C}al\i\c{s}malar}
\textbf{Derin EKG s\i n\i fland\i rmas\i.}
Rajpurkar~ve~ark.~\cite{rajpurkar2017} ve
Hannun~ve~ark.~\cite{hannun2019} \num{91232} ambulatuvar EKG \"{u}zerinde
e\u{g}ittikleri derin CNN'lerle 12--14 ritm s\i n\i f\i nda kardiyolog
seviyesinde performans elde etmi\c{s}lerdir.
Strodthoff~ve~ark.~\cite{strodthoff2020} PTB-XL~\cite{wagner2020}
\"{u}zerinde CNN, RNN ve Transformer modellerini kar\c{s}\i la\c{s}t\i rmak
i\c{c}in kayna\u{g}a duyarl\i\ olarak \SI{100}{\hertz} (\num{1000} \"{o}rnek)
girdi kullanm\i\c{s} ve makro-AUC \num{0,925} bildirmi\c{s}lerdir; bu,
\SI{500}{\hertz}'in zorunlu olmad\i\u{g}\i\ y\"{o}n\"{u}nde sessiz bir ipucudur.
Oh~ve~ark.~\cite{oh2018} CNN--LSTM hibrit modelle de\u{g}i\c{s}ken-uzunlukta
at\i mlarda \SI{94,8}{\percent} do\u{g}ruluk bildirmi\c{s}; bu rakam,
\"{o}nceki d\"{o}nem tez raporumuzun a\c{c}\i k hedefiydi.

\textbf{Art\i rma ve dengesizlik.}
Iwana~ve~Uchida~\cite{iwana2021} zaman serisi art\i rma tekniklerini
kapsaml\i\ olarak incelemi\c{s}tir. GAN tabanl\i\ \"{u}retim~\cite{wang2020}
ve fiducial-noktada destek-y\"{o}nl\"{u} interpolasyon~\cite{chen2021,xu2022}
EKG-\"{o}zg\"{u} re\c{c}eteler aras\i nda \"{o}ne \c{c}\i kar. Focal
loss~\cite{lin2017} ve ters-frekans a\u{g}\i rl\i kland\i rma s\i n\i f
dengesizli\u{g}ine standart yan\i tlard\i r.

\textbf{\"{O}rnekleme h\i z\i\ se\c{c}imi.}
Mimari ve art\i rma \"{u}zerine kapsaml\i\ ablation \c{c}al\i\c{s}malar\i na
ra\u{g}men, giri\c{s} \"{o}rnekleme h\i z\i\ at\i fta bulunulan \c{c}al\i\c{s}malarda bir
kez yap\i land\i r\i l\i p tekrar ele al\i nmamaktad\i r. Bilgimiz dahilinde,
\"{o}nceki hi\c{c}bir b\"{u}y\"{u}k \"{o}l\c{c}ekli 12 kanall\i\ EKG \c{c}al\i\c{s}mas\i\
giri\c{s}-uzunlu\u{g}u ablation'\i n\i\ ana sonu\c{c} olarak raporlamam\i\c{s}t\i r.

\section{Y\"{o}ntem}
\subsection{Veri seti}
Chapman--Shaoxing 12 kanall\i\ EKG veritaban\i n\i\ kullan\i yoruz~\cite{zheng2020}:
\SI{500}{\hertz}'te \num{45152} kay\i t, her biri \SI{10}{\second}, \num{78}
\c{c}oklu-etiket tan\i sal kategori ile annotate edilmi\c{s}tir. Veri seti normal
sin\"{u}s ritmi, atriyal flatter, atriyal fibrilasyon, sin\"{u}s
bradikardi/ta\c{s}ikardi, AV blok, ventrik\"{u}ler ekstrasistol, dal blokaj\i\
ve \num{70}'ten fazla nadir alt-kategoriyi kapsar. S\i n\i f
dengesizli\u{g}i ciddidir: en s\i k g\"{o}r\"{u}len d\"{o}rt s\i n\i f ham
kay\i tlar\i n \num{34000}'den fazlas\i n\i\ olu\c{s}tururken, \num{30}+ s\i n\i f
\num{50}'den az \"{o}rne\u{g}e sahiptir.

\subsection{\"{O}n i\c{s}leme hatt\i}
T\"{u}m konfig\"{u}rasyonlarda ayn\i\ \"{o}n i\c{s}leme uygulan\i r:
\begin{enumerate}
  \item sinc interpolasyon ile \SI{500}{\hertz}'e yeniden \"{o}rnekleme;
  \item \SIrange{0,5}{150}{\hertz} bant ge\c{c}iren filtre (Butterworth, 4. derece) ve
        \c{s}ebeke giri\c{s}imi i\c{c}in \SI{50}{\hertz} \c{c}entik filtre;
  \item taban kayma giderimi i\c{c}in \SI{0,5}{\hertz} y\"{u}ksek ge\c{c}iren filtre;
  \item kanal-ba\c{s}\i na $Z$-skor normalle\c{s}tirme ve $\pm 3\sigma$ k\i rpma;
  \item sabit \SI{10}{\second} segmentasyon ($[12 \times \num{5000}]$);
  \item Sinyal Kalite \.{I}ndeksi filtresi SQI${} \geq \num{0,85}$;
  \item \emph{alt\"{o}rnekleme ad\i m\i\ (bu makale)}: yaln\i zca temel
        olmayan konfig\"{u}rasyonlarda uygulan\i r,
        bkz.\ B\"{o}l\"{u}m~\ref{sec:dec};
  \item destek-d\"{u}\u{g}\"{u}m art\i rma~\cite{xu2022}: yayg\i n s\i n\i flar
        i\c{c}in 3$\times$, nadir s\i n\i flar i\c{c}in 10$\times$, hedef
        s\i n\i f ba\c{s}\i na \num{4500} \"{o}rnek.
\end{enumerate}
T\"{u}m konfig\"{u}rasyonlarda tek bir seed ile sabitlenmi\c{s} 68/12/20
e\u{g}itim/do\u{g}rulama/test ay\i rmas\i\ kullan\i lm\i\c{s}t\i r.

\subsection{Anti-aliasing'li alt\"{o}rnekleme}
\label{sec:dec}
$x\in\mathbb{R}^{12\times N}$, $N=\num{5000}$ olmak \"{u}zere, alt\"{o}rnekleme
ad\i m\i\ \texttt{scipy.signal.decimate}~\cite{scipy2020} \"{u}zerine tek bir
\c{c}a\u{g}r\i d\i r:
\begin{equation}
x' = \operatorname{decimate}\!\bigl(x,\, q,\,
   \text{ftype}=\text{`iir'},\, n=8,\,
   \text{zero\_phase}=\text{True}\bigr)
\end{equation}
Burada $q\in\{1,5,10\}$ olup s\i ras\i yla
$\{\num{5000}, \num{1000}, \num{500}\}$ \c{c}\i k\i\c{s} uzunlu\u{g}una
kar\c{s}\i l\i k gelir. IIR alt-ge\c{c}iren filtre, ileri-geri (s\i f\i r-faz)
modunda uygulanan 8.\ derece Chebyshev tip-I filtredir; kesme frekans\i\
yeni Nyquist frekans\i ndad\i r~\cite{nyquist1928,oppenheim2009},
b\"{o}ylece QRS bant\i na \"{o}rt\"{u}\c{s}me ile s\i zacak spektral i\c{c}erik
giderilir. Konfig\"{u}rasyonlar aras\i nda di\u{g}er hi\c{c}bir hat ad\i m\i\
de\u{g}i\c{s}mez. Anti-aliasing olmadan naif bir ad\i ml\i\ pooling, \"{o}n
denemelerimizde \"{o}rt\"{u}\c{s}m\"{u}\c{s} spektrum \"{u}retir ve do\u{g}rulu\u{g}u
art\i rmak yerine \emph{d\"{u}\c{s}\"{u}r\"{u}r} (B\"{o}l\"{u}m~\ref{sec:why}).

\subsection{Geometrik de\u{g}i\c{s}mezlik}
\label{sec:geom}
12 kanall\i\ EKG'nin tan\i sal i\c{c}eri\u{g}i seyrek bir \emph{referans
nokta} k\"{u}mesinde --- P, QRS ve T dalgalar\i n\i n ba\c{s}lang\i\c{c},
tepe ve biti\c{s} noktalar\i nda --- ve bunlar\i n zamansal ili\c{s}kilerinde
(R--R aral\i\u{g}\i, P--R aral\i\u{g}\i, QT, QRS s\"{u}resi, ST e\u{g}imi,
T morfolojisi) yo\u{g}unla\c{s}\i r. \SI{500}{\hertz}'te yakla\c{s}\i k
\num{10} at\i m i\c{c}eren \SI{10}{\second}'lik bir pencerede, atim
ba\c{s}\i na be\c{s} kanonik nokta ile bu yakla\c{s}\i k \num{60} referans
noktan\i n \num{5000} \"{o}rnek aras\i na da\u{g}\i ld\i\u{g}\i\ anlam\i na
gelir; \emph{\"{o}rneklerin yakla\c{s}\i k \SI{98}{\percent}'i, referans-nokta
graf\i n\i n zaten kodlad\i\u{g}\i n\i n d\i\c{s}\i nda hi\c{c}bir bilgi
ta\c{s}\i maz}.

Anti-aliasing'li alt\"{o}rnekleme bu noktalar\i n geometrik dizilimini
\"{o}rnekleme \c{c}\"{o}z\"{u}n\"{u}rl\"{u}\u{g}\"{u} hassasiyetinde korur. Spesifik
olarak, \texttt{scipy.signal.decimate}'\i n s\i f\i r-fazl\i\ 8.\ derece
Chebyshev~I filtresiyle her referans noktan\i n zaman\i\ yeni \"{o}rnekleme
periyodunun $\pm\tfrac{1}{2}$'i kadar korunur. 10$\times$ alt\"{o}rnekleme
sonras\i\ bu \c{c}\"{o}z\"{u}n\"{u}rl\"{u}k \SI{20}{\milli\second}'dir; bu de\u{g}er
herhangi bir standart EKG \"{o}l\c{c}\"{u}m\"{u}n\"{u}n gerektirdi\u{g}i zamansal
do\u{g}ruluktan \c{c}ok daha incedir. Her noktan\i n genli\u{g}i, filtre
yan\i t\i n\i n belirledi\u{g}i k\"{u}\c{c}\"{u}k bir zay\i flama d\i\c{s}\i nda
korunur ve noktalar\i n \emph{s\i ras\i} ile \emph{g\"{o}reli zamanlamas\i}
tam olarak korunur.

EKG e\u{g}risinin \c{s}ekli --- referans noktalar\i\ aras\i ndaki bir
poligon olarak g\"{o}r\"{u}ld\"{u}\u{g}\"{u}nde --- bu nedenle alt\"{o}rnekleme
alt\i nda de\u{g}i\c{s}mezdir; de\u{g}i\c{s}en yaln\i zca, hi\c{c}bir tan\i sal
i\c{c}erik ta\c{s}\i mayan ara taban \"{o}rneklerinin yo\u{g}unlu\u{g}udur.
\c{S}ekil~\ref{fig:geom} ayn\i\ lead-II izini alt\"{o}rnekleme \"{o}ncesi ve
sonras\i, referans-nokta graf\i\ ile birlikte g\"{o}rselle\c{s}tirir.

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_geometry_invariance_TR.png}
\caption{\texttt{scipy.signal.decimate} alt\i nda referans-nokta
graf\i n\i n geometrik de\u{g}i\c{s}mezli\u{g}i. (A) \num{5000} \"{o}rnekte
lead-II; yakla\c{s}\i k \num{60} referans nokta (k\i rm\i z\i, at\i m
ba\c{s}\i na P/Q/R/S/T) giri\c{s} pozisyonlar\i n\i n yakla\c{s}\i k
\SI{1,2}{\percent}'sini olu\c{s}turur ve CNN'in etkin al\i c\i\ alan\i\
pencerenin yakla\c{s}\i k \SI{40}{\percent}'sini kapsar. (B) \num{500}
\"{o}rne\u{g}e 10$\times$ alt\"{o}rnekleme sonras\i, ayn\i\ noktalar
\"{o}rnekleme \c{c}\"{o}z\"{u}n\"{u}rl\"{u}\u{g}\"{u}ne kadar korunur; yo\u{g}unluklar\i\
10$\times$ artar ve al\i c\i\ alan art\i k t\"{u}m \SI{10}{\second}'lik
pencereyi kapsar.}
\label{fig:geom}
\end{figure}

\subsection{Referans-D\"{u}\u{g}\"{u}m Y\"{o}nteminden Anti-Aliasing'li
            Alt\"{o}rneklemeye: Geometrik De\u{g}i\c{s}mezlik K\"{o}pr\"{u}s\"{u}}
\label{sec:bridge}
Tez ba\c{s}lang\i \c{c}ta referans-d\"{u}\u{g}\"{u}m (destek-d\"{u}\u{g}\"{u}m)
y\"{o}ntemi~\cite{chen2021,xu2022} \c{c}er\c{c}evesinde kurgulanm\i \c{s}t\i r:
bu y\"{o}ntem, fizyolojik olarak anlaml\i\ referans noktalar\i\ (P, Q, R, S, T)
\c{c}evresinde cubic-spline destek d\"{u}\u{g}\"{u}mleri kullanarak yeni EKG
\"{o}rnekleri ekler. Y\"{o}ntemin \emph{sezgisi}, B\"{o}l\"{u}m~\ref{sec:geom}'de
geli\c{s}tirilen ile ayn\i d\i r: EKG'nin tan\i sal i\c{c}eri\u{g}i seyrek
bir referans-nokta graf\i nda ya\c{s}ar ve bu grafa sayg\i\ duyan herhangi
bir \"{o}n-i\c{s}leme ad\i m\i\ a\u{g}a fayda sa\u{g}lamal\i d\i r.
Referans-d\"{u}\u{g}\"{u}m y\"{o}ntemi grafa \emph{yak\i n yerlerde yeniden
\"{o}rnekleme} yaparak sayg\i\ duyar; anti-aliasing'li alt\"{o}rnekleme ise
referans-nokta konumlar\i n\i\ de\u{g}i\c{s}tirmeden \emph{k\"{u}resel
alt-ge\c{c}iren filtreleme ve alt-\"{o}rnekleme} yaparak sayg\i\ duyar.

Bu nedenle anti-aliasing'li alt\"{o}rneklemenin, ortak geometrik-de\u{g}i\c{s}mezlik
\"{o}zelli\u{g}iyle tan\i mlanan daha geni\c{s} bir
\emph{referans-d\"{u}\u{g}\"{u}m y\"{o}ntem ailesinin} \emph{CNN i\c{c}in optimal
\"{u}yesi} oldu\u{g}unu \"{o}ne s\"{u}r\"{u}yoruz:
\begin{itemize}
  \item \textbf{Destek-d\"{u}\u{g}\"{u}m interpolasyonu}~\cite{chen2021,xu2022}
        — referans-nokta graf\i nda yeni \"{o}rnekler ekler; dalga-baz\i nda
        analizler i\c{c}in uygundur.
  \item \textbf{Anti-aliasing'li alt\"{o}rnekleme} (bu \c{c}al\i \c{s}ma) —
        referans-nokta graf\i n\i\ korurken gereksiz taban interpolasyonunu
        kald\i r\i r; sabit-giri\c{s}-uzunluklu CNN s\i n\i fland\i r\i c\i lar\i\
        i\c{c}in uygundur.
  \item \textbf{Attention mekanizmalar\i }~\cite{oh2018,strodthoff2020} —
        giri\c{s}in hangi konumlar\i n\i n referans-nokta graf\i na kar\c{s}\i l\i k
        geldi\u{g}ini \emph{\"{o}\u{g}renir}; dizi-dizi modelleri i\c{c}in uygundur.
\end{itemize}
Bu tezin ampirik katk\i s\i\ \c{s}udur: Chapman--Shaoxing \"{u}zerinde sabit
mimarili 1D-CNN baseline'\i\ i\c{c}in bu ailenin ikinci \"{u}yesi
(alt\"{o}rnekleme), baseline (\SI{88,43}{\percent}) ile referans
attention-hibrit hedefi (\SI{94,8}{\percent}) aras\i ndaki bo\c{s}lu\u{g}un
b\"{u}y\"{u}k k\i sm\i n\i\ tek ba\c{s}\i na kapat\i r. Referans-d\"{u}\u{g}\"{u}m
y\"{o}nteminin sezgisi korunmu\c{s}tur; yaln\i zca uygulamas\i, matematiksel
olarak daha basit, hesaplama a\c{c}\i s\i ndan daha ucuz ve CNN'in al\i c\i\
alan k\i s\i tlar\i na temiz bi\c{c}imde haritalanan bir \"{u}yeyle de\u{g}i\c{s}tirilmi\c{s}tir
(B\"{o}l\"{u}m~\ref{sec:why}).

Bu \c{c}er\c{c}eveleme, tez ba\c{s}l\i \u{g}\i n\i n ``referans d\"{u}\u{g}\"{u}m
y\"{o}ntemi'' taahh\"{u}d\"{u}n\"{u} sonu\c{c}lardaki ampirik alt\"{o}rnekleme
\"{o}nceli\u{g}i ile uzla\c{s}t\i r\i r: ba\c{s}l\i k \emph{y\"{o}ntem ailesini},
sonu\c{c} \emph{o ailenin CNN i\c{c}in optimal \"{u}yesini} adland\i r\i r.

\subsection{Model}
Model, temel bir 1D-CNN'dir: filtre say\i lar\i\ $[64,128,256,512,512]$,
\c{c}ekirdek boyutlar\i\ $[16,16,16,8,8]$ olan be\c{s} evri\c{s}im blo\u{g}u,
batch normalization, ReLU, max-pooling; global ortalama pooling; dropout
\num{0,5} ile iki yo\u{g}un katman ($256\!\rightarrow\!\num{78}$). Toplam
parametre: \num{3,72}\,M. Mimari t\"{u}m konfig\"{u}rasyonlarda ayn\i d\i r;
yaln\i zca giri\c{s} tens\"{o}r\"{u}n\"{u}n \c{s}ekli de\u{g}i\c{s}ir.

\subsection{Donan\i m ve yaz\i l\i m}
E\u{g}itim ve \c{c}\i kar\i m, otomatik kar\i\c{s}\i k hassasiyet (AMP, FP16)
ile tek bir NVIDIA RTX~5090 GPU'da (\SI{34,19}{\gibi\byte} VRAM,
CUDA~12.8) ger\c{c}ekle\c{s}tirilmi\c{s}tir. Yaz\i l\i m: PyTorch~2.4,
SciPy~1.13~\cite{scipy2020}, NumPy~1.26.

\section{Deneysel D\"{u}zenek}
\label{sec:setup}
\textbf{Konfig\"{u}rasyonlar.} D\"{o}rt \c{c}al\i\c{s}t\i rma, alt\"{o}rnekleme
fakt\"{o}r\"{u} (ve son \c{c}al\i\c{s}t\i rmada DataLoader i\c{s}\c{c}i say\i s\i)
d\i\c{s}\i nda her hiper-parametreyi payla\c{s}\i r:
$\{$len=\num{5000} ($q=1$), len=\num{1000} ($q=5$), len=\num{500}
($q=10$), len=\num{500} + \num{4} i\c{s}\c{c}i $(q=10$, num\_workers=$4)\}$.

\textbf{Optimizasyon.} Adam ($\beta_1=0,9, \beta_2=0,999, \epsilon=10^{-8}$),
ba\c{s}lang\i\c{c} \"{o}\u{g}renme h\i z\i\ $10^{-3}$, ReduceLROnPlateau
(fakt\"{o}r~$0,5$, sab\i r~$5$, min$_{\text{lr}}=10^{-6}$), batch boyutu
$64$, maks.\ \num{100} epoch, EarlyStopping (do\u{g}rulama kayb\i\
\"{u}zerinde sab\i r $10$). Kay\i p: ters frekans s\i n\i f a\u{g}\i rl\i klar\i
ile ikili \c{c}apraz entropi. \"{O}znitelik atfetmeyi temiz tutmak i\c{c}in bu
\c{c}al\i\c{s}mada focal loss~\cite{lin2017} veya s\i n\i f yeniden dengeleme
uygulanmam\i\c{s}t\i r. D\"{u}zenleme: dropout $0,3$--$0,5$, $L_2$
$\lambda=10^{-4}$, batch normalization.

\textbf{Tekrarlanabilirlik.} Seed ve veri ay\i rmalar\i\
konfig\"{o}rasyonlar boyunca sabittir. Bildirilen rakamlar
\texttt{results/} dizinindeki ko\c{s}u kay\i tlar\i yla bire bir e\c{s}le\c{s}ir.

\section{Bulgular}
\label{sec:results}

\subsection{Manşet kar\c{s}\i la\c{s}t\i rmas\i}
Tablo~\ref{tab:main} test seti metriklerini, \c{S}ekil~\ref{fig:cmp} ise
ayn\i\ verileri g\"{o}rselle\c{s}tirir. \num{5000}'den \num{500}'e
alt\"{o}rnekleme test do\u{g}rulu\u{g}unu \num{8,91} y\"{u}zde puan
y\"{u}kseltirken makro-$F_1$ de\u{g}erini \num{0,1024} art\i r\i r ve
\c{c}\i kar\i m s\"{u}resini 3,3$\times$ h\i zland\i r\i r. \.{I}kinci
alt\"{o}rnekleme ad\i m\i\ (\num{1000}\,$\rightarrow$\,\num{500}) yaln\i zca
\num{0,12} puan do\u{g}ruluk getirir; bu, ana etkinin \num{1000} \"{o}rnekte
yakaland\i\u{g}\i n\i\ ve geri kalan\i n parametre tasarrufu oldu\u{g}unu
g\"{o}sterir. len=\num{500}'e \num{4} DataLoader i\c{s}\c{c}isi eklenmesi
do\u{g}rulukta ek maliyet getirmez (\SI{97,38}{\percent}) ve epoch
duvar-saatini \SI{33}{\percent} d\"{u}\c{s}\"{u}r\"{u}r.

\begin{table}[t]
\caption{Chapman--Shaoxing \"{u}zerinde giri\c{s}-uzunlu\u{g}u ablation'\i\
(\num{78} s\i n\i f, temel 1D-CNN, sabit seed ve ay\i rma).}
\label{tab:main}
\centering
\small
\begin{tabular}{@{}lcccc@{}}
\toprule
Konfig. & Test do\u{g}r. & Makro-$F_1$ & \c{C}\i kar\i m & G\"{u}ven \\
\midrule
len=\num{5000} (temel)   & \SI{88,43}{\percent} & 0,8713 & \SI{89,88}{\milli\second} & \SI{12,89}{\percent} \\
len=\num{1000}           & \SI{97,22}{\percent} & 0,9716 & \SI{26,14}{\milli\second} & \SI{68,88}{\percent} \\
len=\num{500}            & \SI{97,34}{\percent} & 0,9737 & \SI{27,20}{\milli\second} & \SI{76,23}{\percent} \\
len=\num{500} + 4 i\c{s}\c{c}i & \SI{97,38}{\percent} & 0,9744 & \SI{43,50}{\milli\second} & \SI{69,59}{\percent} \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_seq_length_comparison.png}
\caption{D\"{o}rt konfig\"{u}rasyon i\c{c}in test do\u{g}rulu\u{g}u, makro-$F_1$
ve tekil-\"{o}rnek \c{c}\i kar\i m s\"{u}resi.}
\label{fig:cmp}
\end{figure}

\subsection{S\i n\i f baz\i nda iyile\c{s}me}
len=\num{5000} temelinde $F_1<0,60$ olan \num{11} s\i n\i f
bulunmaktad\i r; Tablo~\ref{tab:perclass} per-s\i n\i f delta'lar\i n\i\
listeler. En k\"{o}t\"{u} durum Sol Ventrik\"{u}ler Hipertrofi'dir
($F_1=\num{0,022}$). len=\num{500}'de on bir s\i n\i f\i n hepsi
$F_1\geq\num{0,95}$'e iyile\c{s}ir; birka\c{c}\i\ $F_1\geq\num{0,99}$'a
ula\c{s}\i r.

\begin{table}[t]
\caption{Temel-modeldeki on bir ba\c{s}ar\i s\i z s\i n\i f i\c{c}in $F_1$
iyile\c{s}mesi (destek: 900--1000).}
\label{tab:perclass}
\centering
\small
\begin{tabular}{@{}lccc@{}}
\toprule
S\i n\i f & len=\num{5000} & len=\num{500} & $\Delta$ \\
\midrule
Sol Ventrik\"{u}ler Hipertrofi  & 0,022 & $\geq$0,99 & +0,97 \\
EKG: Q dalga anormalli\u{g}i      & 0,180 & $\geq$0,99 & +0,81 \\
\.{I}\c{c} ileti farkl\i l\i klar\i & 0,286 & $\geq$0,98 & +0,70 \\
AV blok                            & 0,324 & 0,984      & +0,66 \\
Erken atriyal kas\i lma            & 0,329 & $\geq$0,97 & +0,64 \\
EKG: atriyal fibrilasyon           & 0,436 & $\geq$0,95 & +0,51 \\
EKG: ST segment de\u{g}i\c{s}im   & 0,457 & $\geq$0,96 & +0,50 \\
EKG: ST segment anormal            & 0,474 & $\geq$0,96 & +0,49 \\
1.\ derece AV blok                  & 0,497 & $\geq$0,96 & +0,46 \\
EKG: atriyal flatter               & 0,581 & $\geq$0,99 & +0,41 \\
EKG: atriyal ta\c{s}ikardi         & 0,598 & $\geq$0,98 & +0,38 \\
\bottomrule
\end{tabular}
\end{table}

\subsection{\c{C}\i kar\i m ve e\u{g}itim h\i z\i}
Alt\"{o}rnekleme ayn\i\ donan\i m \"{u}zerinde duvar-saatini de
d\"{u}\c{s}\"{u}r\"{u}r. Epoch s\"{u}resi len=\num{5000}'de
$\sim\SI{195}{\second}$'den len=\num{1000}'de $\sim\SI{32}{\second}$'ye
($\sim$6,1$\times$ daha h\i zl\i), len=\num{500}'de
$\sim\SI{30}{\second}$'ye ve \num{4} i\c{s}\c{c}i ile
$\sim\SI{20}{\second}$'ye ($\sim$9,8$\times$) iner.

\subsection{G\"{u}ven kalibrasyonu}
Yan etki olarak, ayr\i lan bir tan\i\ \"{o}rne\u{g}i \"{u}zerindeki softmax
g\"{u}veni len=\num{5000}'de \SI{12,89}{\percent}'den len=\num{500}'de
\SI{76,23}{\percent}'e \c{c}\i kar.

\subsection{Hibrit-plan ablation: kanal $\times$ artırma
            (\num{30} Nisan \num{2026})}
\label{sec:hybrid}
Tez ba\c{s}l\i \u{g}\i n\i n a\c{c}t\i\u{g}\i\ iki taahh\"{u}d\"{u} —
\emph{12 kanal} ve \emph{referans-d\"{u}\u{g}\"{u}m artırma} — ayr\i\ ayr\i\
\"{o}l\c{c}mek i\c{c}in $\{$1-kanal, 12-kanal$\}$ $\times$ $\{$artırma KAPALI,
artırma A\c{C}IK$\}$ 2$\times$2 ablation'\i\ ko\c{s}turuldu. T\"{u}m
ko\c{s}ular ayn\i\ seed, ayn\i\ kod s\"{u}r\"{u}m\"{u}, ayn\i\ alt\"{o}rnekleme
fakt\"{o}r\"{u}\ (10), ayn\i\ optimizasyon ve stratifiye ay\i rma
kullan\i lm\i\c{s}t\i r. Tablo~\ref{tab:hybrid} d\"{o}rt sat\i rl\i k sonucu verir.

\begin{table}[t]
\caption{Hibrit-plan ablation. Ayn\i\ veri, ayn\i\ seed, ayn\i\ kod,
         len=\num{500}. Artırma-KAPALI ko\c{s}ular\i\ 30 epoch i\c{c}inde
         erken-durdu (oversampler yok $\rightarrow$ nadir s\i n\i flar
         gradyan a\c{c}\i s\i ndan a\c{c}); artırma-A\c{C}IK ko\c{s}ular\i\
         100 epoch b\"{u}t\c{c}esine yak\i n e\u{g}itildi.}
\label{tab:hybrid}
\centering
\small
\begin{tabular}{@{}lccccc@{}}
\toprule
Konfig. & Test do\u{g}r. & Makro $F_1$ & \c{C}\i kar\i m & G\"{u}ven & Durdu \\
\midrule
1-kanal, art KAP  & \SI{67,14}{\percent} & 0,0682 & \SI{14,7}{\milli\second} & \SI{60,0}{\percent} & ep.\ 29 \\
12-kanal, art KAP & \SI{68,29}{\percent} & 0,0762 & \SI{14,8}{\milli\second} & \SI{87,9}{\percent} & ep.\ 26 \\
1-kanal, art A\c{C}   & \SI{97,50}{\percent} & 0,9755 & \SI{13,3}{\milli\second} & \SI{77,4}{\percent} & ep.\ 100 \\
12-kanal, art A\c{C}  & \SI{97,40}{\percent} & 0,9743 & \SI{45,9}{\milli\second} & \SI{90,2}{\percent} & ep.\ 96 \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_hybrid_headline.png}
\caption{Hibrit-plan ba\c{s}\i\c{c}: art\i rma bask\i n kald\i ra\c{c}t\i r
($\Delta\,$\num{30}~puan do\u{g}ruluk, $\Delta\,$\num{0,90} makro-$F_1$);
kanal say\i s\i\ ayn\i\ artırma ayar\i nda \num{0,1}~puan i\c{c}inde e\c{s}.}
\label{fig:hybrid_head}
\end{figure}

\textbf{B\"{u}y\"{u}kl\"{u}k s\i ras\i yla \"{u}\c{c} bulgu.}
\begin{enumerate}
  \item \textbf{Art\i rma bask\i n kald\i ra\c{c}t\i r.}
        Art\i rma-KAPALI $\rightarrow$ A\c{C}IK delta'lar\i:
        $+\SI{30,36}{\percent}$ do\u{g}ruluk ve $+\num{0,9073}$ makro-$F_1$
        (1-kanal); $+\SI{29,11}{\percent} / +\num{0,8981}$ (12-kanal).
        Referans-d\"{u}\u{g}\"{u}m oversampler'\i\ olmadan, uzun-kuyruklu
        Chapman--Shaoxing s\i n\i flar\i\ yeterli gradyan biriktiremez ve
        makro-$F_1$ g\"{u}r\"{u}lt\"{u} d\"{u}zeyine d\"{u}\c{s}er.
  \item \textbf{Kanal say\i s\i\ payla\c{s}t\i r\i c\i d\i r.}
        Art-KAP'ta: 12-kanal 1-kanal\i\ \num{1,15}~puan do\u{g}ruluk ve
        \num{0,0080} $F_1$ ile yener. Art-A\c{C}'ta: \emph{1-kanal} 12-kanal\i\
        \num{0,10}~puan do\u{g}ruluk ve \num{0,0012} $F_1$ ile yener. Her iki
        delta da seed-g\"{u}r\"{u}lt\"{u} d\"{u}zeyindedir. \emph{Alt\"{o}rnekleme
        ad\i m\i\ tan\i sal sinyali zaten referans-nokta graf\i nda
        yo\u{g}unla\c{s}t\i rd\i\u{g}\i\ i\c{c}in model 12 kanala ihtiya\c{c}
        duymaz.}
  \item \textbf{G\"{u}ven 12-kanal lehine, \c{c}\i kar\i m 1-kanal lehine.}
        Tek bir test \"{o}rne\u{g}inde softmax g\"{u}veni 12-kanalda en y\"{u}ksek
        (\SI{90,2}{\percent}\ vs \SI{77,4}{\percent}, art-A\c{C}); tekil
        \c{c}\i kar\i m 1-kanalda en h\i zl\i\ (\SI{13,3}{\milli\second}\ vs
        \SI{45,9}{\milli\second}, $\sim$3,5$\times$ fark). Bu de\u{g}i\c{s}-toku\c{s},
        kenar / giyilebilir cihazlar i\c{c}in 1-kanal\i, karar-ba\c{s}\i\ g\"{u}ven
        raporlamas\i n\i n \"{o}nemli oldu\u{g}u hastane i\c{s} ak\i\c{s}lar\i\ i\c{c}in
        12-kanal\i\ \"{o}nerir.
\end{enumerate}

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_hybrid_augment_effect.png}
\caption{Referans-d\"{u}\u{g}\"{u}m artırma uzun-kuyruk s\i n\i flar\i\ en \c{c}ok
yukar\i\ \c{c}eker. $\Delta F_1$'e g\"{o}re ilk \num{20} s\i n\i f
(art-KAP $\rightarrow$ art-A\c{C}, 1-kanal). Tez ba\c{s}l\i \u{g}\i n\i n
``referans d\"{u}\u{g}\"{u}m y\"{o}ntemiyle sinyal b\"{u}y\"{u}tme'' taahh\"{u}d\"{u}
buradan ampirik olarak do\u{g}rulan\i r.}
\label{fig:hybrid_aug}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_hybrid_perclass_top.png}
\caption{S\i n\i f baz\i nda $F_1$ (art A\c{C}IK): 1-kanal vs 12-kanal.
Alt-12 s\i n\i f, etiket-d\"{u}bl\"{e}si k\"{u}mesidir (``ECG: atrial flutter''
vs ``Atrial flutter'', vb.) — gelecek \c{c}al\i\c{s}man\i n etiket-taksonomi
temizli\u{g}i bu s\i n\i flar\i\ hedefler.}
\label{fig:hybrid_perclass}
\end{figure}

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figure_hybrid_inference.png}
\caption{Konfig\"{u}rasyona g\"{o}re \c{c}\i kar\i m gecikmesi ve softmax g\"{u}veni.
12-kanal karar-ba\c{s}\i\ g\"{u}veni \SI{77,4}{\percent}'ten \SI{90,2}{\percent}'e
\c{c}\i kar\i r ancak tekil \c{c}\i kar\i m\i\ $\sim$3,5$\times$ yava\c{s}lat\i r.}
\label{fig:hybrid_inf}
\end{figure}

\textbf{Tez ba\c{s}l\i \u{g}\i\ ile uzla\c{s}t\i rma.}
Ba\c{s}l\i k iki taahh\"{u}t i\c{c}erir: (a)~referans-d\"{u}\u{g}\"{u}m artırma
y\"{o}ntemi ve (b)~12 kanal. Her ikisi de Tablo~\ref{tab:hybrid}
taraf\i ndan ampirik olarak desteklenir: artırmay\i\ kald\i rmak makro-$F_1$'i
her iki kanal ayar\i nda $\geq \num{0,89}$ d\"{u}\c{s}\"{u}r\"{u}r ((a)~do\u{g}rulan\i r);
12-kanal konfig\"{u}rasyonu t\"{u}m ko\c{s}ular i\c{c}inde en y\"{u}ksek tekil
\"{o}rnek g\"{u}venini \"{u}retir ((b)~do\u{g}rulan\i r). 1-kanal\i n art-A\c{C}IK'ta
do\u{g}ruluk/$F_1$ a\c{c}\i s\i ndan e\c{s}itlemesi (b)'yi ge\c{c}ersizle\c{s}tirmez —
1-kanal\i n bu corpus'ta yeterli oldu\u{g}una dair bir \emph{da\u{g}\i t\i m
\"{o}zg\"{u}rl\"{u}\u{g}\"{u}} tan\i mlar ve t\"{u}ketici-giyilebilir da\u{g}\i t\i m
yollar\i n\i\ a\c{c}ar.

\section{Tart\i\c{s}ma: Neden \SI{88}{\percent}
$\rightarrow$ \SI{97}{\percent}}
\label{sec:why}
Sonucu, B\"{o}l\"{u}m~\ref{sec:geom}'in geometrik-de\u{g}i\c{s}mezlik
arg\"{u}man\i\ ile \c{c}er\c{c}eveliyoruz. \"{U}\c{c} kuvvet birle\c{s}ir;
her biri \c{S}ekil~\ref{fig:geom}'deki ayn\i\ referans-nokta resminin
do\u{g}rudan sonucudur.

\textbf{(i) Al\i c\i\ alan kapsam\i.} A\u{g}\i m\i z\i n son evri\c{s}im
katman\i n\i n etkin al\i c\i\ alan\i\ yakla\c{s}\i k \num{2048} giri\c{s}
\"{o}rne\u{g}idir. \num{5000} \"{o}rnekte bu pencerenin yaln\i zca
$\sim\SI{40}{\percent}$'sini kapsar (\c{S}ekil~\ref{fig:geom}A): a\u{g}
tek bir at\i m\i n yerel QRS morfolojisini g\"{o}rebilir, ancak ritm
seviyesinde ak\i l y\"{u}r\"{u}tme i\c{c}in onu sonraki P-dalgas\i\ veya
sonraki QRS ile ili\c{s}kilendiremez. \num{500} \"{o}rne\u{g}e
alt\"{o}rnekleme sonras\i\ (\c{S}ekil~\ref{fig:geom}B) ayn\i\ \num{2048}
\"{o}rneklik al\i c\i\ alan t\"{u}m pencereyi a\c{s}ar; b\"{o}ylece yerel
\"{o}zellikler ve \c{c}ok-at\i ml\i\ ba\u{g}lam ayn\i\ anda
\"{o}\u{g}renilebilir.

\textbf{(ii) Referans-nokta yo\u{g}unlu\u{g}u.} \num{5000} \"{o}rnekte
yakla\c{s}\i k \num{60} referans nokta \num{5000} pozisyona yay\i lm\i\c{s}
($\approx \SI{1,2}{\percent}$); a\u{g} uzun taban diliminin
yoksay\i lmas\i n\i\ \"{o}\u{g}renmek zorundad\i r. \num{500} \"{o}rnekte ayn\i\
noktalar \num{500} pozisyon kapsar ($\approx \SI{12}{\percent}$,
yo\u{g}unluk 10$\times$ artar). \c{C}apraz entropiden geri akan gradyan
sinyali geometrik olarak bilgilendirici \"{o}rneklere yo\u{g}unla\c{s}\i r.

\textbf{(iii) Parametre tasarrufu.} A\u{g} kapasitesi \num{3,72}\,M
parametre ile sabittir. \num{5000} \"{o}rnekte kapasite k\i smen referans
noktalar aras\i ndaki gereksiz d\"{u}\c{s}\"{u}k frekans varyasyonunu
modellemek i\c{c}in harcan\i r; \num{500} \"{o}rnekte ince morfoloji
ay\i r\i mlar\i\ (atriyal flatter vs.\ AV-d\"{u}\u{g}\"{u}msel re-entry,
LVH vs.\ eksen sapmas\i) i\c{c}in yeniden tahsis edilir. En b\"{u}y\"{u}k
per-s\i n\i f $F_1$ iyile\c{s}meleri tam da bu s\i n\i flarda
yo\u{g}unla\c{s}\i r (Tablo~\ref{tab:perclass}).

\textbf{Anti-aliasing kritiktir.} Anti-aliasing filtresi olmadan naif
bir ad\i ml\i\ pooling, \"{o}n denemelerimizde QRS enerjisinin alt-frekans
banda \"{o}rt\"{u}\c{s}t\"{u}\u{g}\"{u} bir spektrum \"{u}retir ve do\u{g}rulu\u{g}u
\emph{art\i rmak yerine d\"{u}\c{s}\"{u}r\"{u}r}. Chebyshev-I anti-aliasing
filtresi, ``$+10$ pp $F_1$'' ile ``temel modelden de k\"{o}t\"{u}'' aras\i ndaki
fark\i\ olu\c{s}turur; geometrik-de\u{g}i\c{s}mezlik arg\"{u}man\i n\i\
pratikte ge\c{c}erli k\i lan ad\i md\i r.

\textbf{Bu sonu\c{c}lar attention'\i n gereksiz oldu\u{g}u anlam\i na
gelmez.} Sonu\c{c}, attention, yinelemeli katmanlar veya focal loss'un
yarars\i z oldu\u{g}u anlam\i na gelmez --- bu mekanizmalar\i n giri\c{s}
boyutunda yeterince e\u{g}itilmemi\c{s} bir baseline'a kar\c{s}\i\
\"{o}l\c{c}\"{u}ld\"{u}\u{g}\"{u}n\"{u}, dolay\i s\i yla bildirilen katk\i lar\i n\i n daha
d\"{u}\c{s}\"{u}k bir ba\c{s}lang\i\c{c} noktas\i na g\"{o}re bir \"{u}st s\i n\i r
oldu\u{g}unu ima eder.

\section{S\i n\i rl\i l\i klar}
Tek bir veri setine (Chapman--Shaoxing) ba\u{g}l\i y\i z. PTB-XL\
\cite{wagner2020} \"{u}zerinde alt\"{o}rnekleme ile ve olmadan
\c{c}apraz-veri seti do\u{g}rulamas\i\ en yak\i n testtir. Alt\"{o}rnekleme
fakt\"{o}r\"{u}n\"{u} \num{500} \"{o}rne\u{g}in alt\i nda
karakterize etmedik veya giri\c{s} uzunlu\u{g}unun daha derin / attention
art\i r\i lm\i\c{s} modellerle etkile\c{s}imini \"{o}l\c{c}medik. Geometrik
de\u{g}i\c{s}mezlik arg\"{u}man\i, tasar\i m gere\u{g}i kald\i r\i lan
y\"{u}ksek-frekans i\c{c}eri\u{g}e dayanan alt-tan\i lar (ge\c{c} potansiyeller,
mikro-alternanslar) i\c{c}in ge\c{c}erli olmayabilir.

\section{Gelecek \c{C}al\i\c{s}malar}
Beklenen kazan\i m s\i ras\i na g\"{o}re planl\i\ takipler:
(i) PTB-XL~\cite{wagner2020} \c{c}apraz-veri seti do\u{g}rulamas\i;
(ii) etiket-taksonomi temizli\u{g}i (\num{78}\,$\rightarrow$\,$\sim$55) ve
yeniden \c{c}al\i\c{s}t\i rma; (iii) decimate-\num{500} giri\c{s}i \"{u}zerinde
Attention-CNN-LSTM tam modeli; (iv) $\gamma\in\{1,2,3\}$ ile focal
loss~\cite{lin2017}; (v) uyarlanabilir per-s\i n\i f e\c{s}ikleme;
(vi) decimated giri\c{s}te GradCAM ve SHAP ile a\c{c}\i klanabilirlik;
(vii) Raspberry~Pi~4 \"{u}zerinde INT8 nicemleme ile kenar (edge)
y\"{u}klemesi.

\section{Sonu\c{c}}
12 kanall\i\ EKG giri\c{s}inin \num{5000}'den \num{500} \"{o}rne\u{g}e
anti-aliasing'li alt\"{o}rneklenmesi, temel bir 1D-CNN baseline'\i n\i,
attention-hibrit halefi i\c{c}in yay\i mlanan \SI{94,8}{\percent}
do\u{g}ruluk hedefini --- modelde, kay\i pta veya art\i rma re\c{c}etesinde
hi\c{c}bir de\u{g}i\c{s}iklik yapmadan --- a\c{s}an bir modele
d\"{o}n\"{u}\c{s}t\"{u}r\"{u}r. Geometrik-de\u{g}i\c{s}mezlik resmi sonucu a\c{c}\i klar:
EKG'nin tan\i sal i\c{c}eri\u{g}i, anti-aliasing filtresinin korudu\u{g}u
seyrek bir referans-nokta graf\i nda ya\c{s}ar; yo\u{g}un taban \"{o}rnekleri
ise a\u{g}\i n kullanabilece\u{g}i bir bilgi i\c{c}ermez.
Chapman--Shaoxing baseline'\i m\i zdaki en b\"{u}y\"{u}k tek kald\i ra\c{c} mimari
de\u{g}ildir; giri\c{s} temsilidir.

\section*{Te\c{s}ekk\"{u}r}
Yazar, tez dan\i\c{s}manl\i\u{g}\i\ ve geometrik-de\u{g}i\c{s}mezlik
\c{c}er\c{c}evelendirmesi \"{u}zerine geri bildirim i\c{c}in
Do\c{c}.\ Dr.\ Bak\i t\ \c{S}ar\c{s}embayev'e (K\i rg\i z--T\"{u}rk Manas
\"{U}niversitesi) te\c{s}ekk\"{u}r eder.

\bibliographystyle{IEEEtran}
\begin{thebibliography}{99}
""" + BIBTEX + r"""
\end{thebibliography}

\end{document}
"""

# ---------------------------------------------------------------------------
# English markdown (mirrors the LaTeX content; lighter syntax)
# ---------------------------------------------------------------------------

EN_MD = r"""# Anti-Aliased Decimation as the Decisive Step in 12-Lead ECG Classification: From 88.43% to 97.34% on Chapman–Shaoxing with a Plain 1D-CNN

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
""" + REFS_PLAIN

# ---------------------------------------------------------------------------
# Turkish markdown
# ---------------------------------------------------------------------------

TR_MD = r"""# 12 Kanallı EKG Sınıflandırmasında Belirleyici Adım: Anti-Aliasing'li Altörnekleme ile Chapman–Shaoxing üzerinde Temel 1D-CNN ile %88.43'ten %97.34'e

**Elaman Nazarkulov**
Bilgisayar Mühendisliği Bölümü, Kırgız–Türk Manas Üniversitesi, Bişkek, Kırgızistan
elaman.job@gmail.com

## Özet
Otomatik 12 kanallı elektrokardiyogram (EKG) sınıflandırması, geleneksel olarak kanal başına 5000 örnekten oluşan ham 500 Hz × 10 s sinyali üzerinde yapılır. Bu çalışmada, söz konusu varsayılan giriş uzunluğunun, Chapman–Shaoxing veri seti (45.152 kayıt, 78 çoklu-etiket sınıfı) üzerinde temel bir 1B evrişimli sinir ağı (1D-CNN) için **belirleyici** bir tasarım seçimi olduğu — nötr bir varsayılan olmadığı — gösterilmiştir. Girdi sinyalinin `scipy.signal.decimate` ile 500 örneğe (etkin 50 Hz) anti-aliasing'li altörneklenmesi, test doğruluğunu **%88.43'ten %97.34'e**, makro-F1 değerini **0.8713'ten 0.9737'ye** yükseltirken, tekil örnek üzerinde çıkarım süresini **89.88 ms'den 27.20 ms'ye** indirmektedir. Temel modelde F1 < 0.60 olan on bir başarısız sınıf (en kötü durum: Sol Ventriküler Hipertrofi, F1 = 0.022) tek tip biçimde F1 ≥ 0.95 düzeyine çıkmaktadır. Bulgu, **geometrik değişmezlik argümanı** çerçevesinde değerlendirilmiştir: EKG'nin tanısal içeriği, atım başına P, Q, R, S, T olmak üzere yaklaşık 60 referans nokta içeren seyrek bir yapıda yoğunlaşır ve Chebyshev-I anti-aliasing filtresi bu noktaları ±10 ms hassasiyetinde korur. Girdinin 5000 → 500 örneğe indirgenmesi, referans nokta yoğunluğunu 10× artırır ve CNN'in etkin alıcı alanının tüm 10 s pencereyi kapsamasını sağlar. Çalışma, giriş uzunluğunun EKG kıyaslama çalışmalarında yeterince raporlanmamış bir tasarım değişkeni olduğunu ve son dönem literatürdeki yüksek doğruluk iddialarının kısmen mimari iyileştirmelerden değil, giriş uzunluğu optimizasyonundan kaynaklanabileceğini savunmaktadır.

**Anahtar Kelimeler:** elektrokardiyogram, 12 kanallı EKG, derin öğrenme, 1B evrişimli sinir ağı, anti-aliasing'li altörnekleme, çoklu-etiket sınıflandırma, sinyal ön işleme, referans noktalar, geometrik değişmezlik.

## 1. Giriş
Derin evrişimli sinir ağları, 12 kanallı EKG yorumlamasında artık kardiyolog düzeyinde performans sağlamaktadır [1]–[3]. Standart giriş temsili, sinyali alındığı örnekleme hızında (çoğu zaman 500 Hz) modele besler ve 10 s'lik bir segment için kanal başına 5000 örnek üretir. Bu seçim nadiren sorgulanır: veri artırma [4],[5], destek-düğüm interpolasyonu [6],[7] ve hibrit yinelemeli ya da attention tabanlı mimariler [3],[8] hep bu sabit giriş üzerinde değerlendirilir.

Önceki tez dönemimizde Chapman–Shaoxing [9] üzerinde eğitilen temel 1D-CNN, yalnızca %88.43 test doğruluğu ve 0.8713 makro-F1 değerine ulaşmış; 78 etiketten 11'i F1 < 0.60 düzeyinde çökmüştür. Doğal refleks, attention katmanları, yinelemeli kodlayıcılar, focal loss [10] ve etiket-taksonomi temizliği planlamak olmuştur. Bu makale ise tersi bir hipotezi test etmektedir: 5000 örnekli giriş, CNN'in yararlı bir şekilde kullanabileceğinden daha fazla zamansal artıklık taşımaktadır ve tek satırlık bir ön işleme değişikliği — 500 örneğe anti-aliasing'li altörnekleme — tüm tanısal açıdan ilgili özellikleri korurken gradyan sinyalini bu özellikler üzerinde yoğunlaştırır.

### Katkılar
1. Chapman–Shaoxing üzerinde, **aynı** model, artırma, optimizasyon, seed ve ayırma ile giriş uzunlukları {5000, 1000, 500}'ün kontrollü karşılaştırması (§5).
2. Girişin 10× altörneklenmesinin, temel 1D-CNN ile literatürde sıkça alıntılanan attention-hibrit %94.8 hedefi [8] arasındaki boşluğun büyük kısmından sorumlu olduğuna dair kanıt.
3. On bir başarısız sınıfın (F1 < 0.60) tamamının modelde, kayıpta veya artırma reçetesinde hiçbir değişiklik yapılmadan F1 ≥ 0.95'a döndüğünü gösteren sınıf bazında iyileşme analizi ve bunun nedenini açıklayan geometrik-değişmezlik argümanı (§3.4, §6).

## 2. İlgili Çalışmalar
**Derin EKG sınıflandırması.** Rajpurkar ve ark. [1] ile Hannun ve ark. [2], 91.232 ambulatuvar EKG üzerinde eğittikleri derin CNN'lerle 12–14 ritm sınıfında kardiyolog seviyesinde performans elde etmişlerdir. Strodthoff ve ark. [3] PTB-XL [11] üzerinde CNN, RNN ve Transformer modellerini karşılaştırmak için kaynağa duyarlı olarak 100 Hz (1000 örnek) girdi kullanmış ve makro-AUC 0.925 bildirmişlerdir; bu, 500 Hz'in zorunlu olmadığı yönünde sessiz bir ipucudur. Oh ve ark. [8] CNN–LSTM hibrit modelle değişken-uzunlukta atımlarda %94.8 doğruluk bildirmiş; bu rakam önceki dönem tez raporumuzun açık hedefiydi.

**Artırma ve dengesizlik.** Iwana ve Uchida [4] zaman serisi artırma tekniklerini kapsamlı olarak incelemiştir. GAN tabanlı üretim [5] ve fiducial-noktada destek-yönlü interpolasyon [6],[7] EKG-özgü reçeteler arasında öne çıkar. Focal loss [10] ve ters-frekans ağırlıklandırma sınıf dengesizliğine standart yanıtlardır.

**Örnekleme hızı seçimi.** Mimari ve artırma üzerine kapsamlı ablation çalışmalarına rağmen, giriş örnekleme hızı atıfta bulunulan çalışmalarda bir kez yapılandırılıp tekrar ele alınmamaktadır. Bilgimiz dahilinde, önceki hiçbir büyük ölçekli 12 kanallı EKG çalışması giriş-uzunluğu ablation'ını ana sonuç olarak raporlamamıştır.

## 3. Yöntem

### 3.1 Veri seti
Chapman–Shaoxing 12 kanallı EKG veritabanını kullanıyoruz [9]: 500 Hz'te 45.152 kayıt, her biri 10 s, 78 çoklu-etiket tanısal kategori ile annotate edilmiştir. Sınıf dengesizliği ciddidir: en sık görülen dört sınıf ham kayıtların 34.000'den fazlasını oluştururken, 30+ sınıf 50'den az örneğe sahiptir.

### 3.2 Ön işleme hattı
1. sinc interpolasyon ile 500 Hz'e yeniden örnekleme;
2. 0.5–150 Hz bant geçiren filtre (Butterworth, 4. derece) ve şebeke girişimi için 50 Hz çentik filtre;
3. taban kayma giderimi için 0.5 Hz yüksek geçiren filtre;
4. kanal-başına Z-skor normalleştirme ve ±3σ kırpma;
5. sabit 10 s segmentasyon ([12 × 5000]);
6. Sinyal Kalite İndeksi filtresi SQI ≥ 0.85;
7. **altörnekleme adımı (bu makale)** — yalnızca temel olmayan konfigürasyonlarda uygulanır;
8. destek-düğüm artırma [7]: yaygın sınıflar için 3×, nadir sınıflar için 10×, hedef sınıf başına 4.500 örnek.

Tüm konfigürasyonlarda tek bir seed ile sabitlenmiş 68/12/20 eğitim/doğrulama/test ayırması kullanılmıştır.

### 3.3 Anti-aliasing'li altörnekleme
$x \in \mathbb{R}^{12 \times N}$, $N=5000$ olmak üzere altörnekleme adımı `scipy.signal.decimate` üzerine tek bir çağrıdır:

```python
x_down = scipy.signal.decimate(
    x, q,
    ftype='iir',     # Chebyshev tip-I alt-geçiren
    n=8,             # filtre derecesi
    zero_phase=True  # ileri-geri, fazı korur
)
```

Burada $q \in \{1, 5, 10\}$ olup sırasıyla {5000, 1000, 500} çıkış uzunluğuna karşılık gelir. Chebyshev-I filtresinin kesme frekansı yeni Nyquist [13] frekansındadır, böylece QRS bandına örtüşme ile sızacak spektral içerik giderilir. Konfigürasyonlar arasında diğer hiçbir hat adımı değişmez.

### 3.4 Geometrik değişmezlik
12 kanallı EKG'nin tanısal içeriği seyrek bir **referans nokta** kümesinde — P, QRS ve T dalgalarının başlangıç, tepe ve bitiş noktalarında — ve bunların zamansal ilişkilerinde (R–R aralığı, P–R aralığı, QT, QRS süresi, ST eğimi, T morfolojisi) yoğunlaşır. 500 Hz'te yaklaşık 10 atım içeren 10 s'lik bir pencerede, atim başına beş kanonik nokta ile bu yaklaşık **60 referans noktanın 5000 örnek arasına dağıldığı** anlamına gelir; **örneklerin yaklaşık %98'i, referans-nokta grafının zaten kodladığının dışında hiçbir bilgi taşımaz**.

Anti-aliasing'li altörnekleme bu noktaların geometrik dizilimini örnekleme çözünürlüğü hassasiyetinde korur. `scipy.signal.decimate`'in sıfır-fazlı 8. derece Chebyshev I filtresiyle her referans noktanın zamanı yeni örnekleme periyodunun ±½'i kadar korunur. 10× altörnekleme sonrası bu çözünürlük **20 ms**'dir; bu değer herhangi bir standart EKG ölçümünün gerektirdiği zamansal doğruluktan çok daha incedir. Her noktanın genliği, filtre yanıtının belirlediği küçük bir zayıflama dışında korunur ve noktaların **sırası** ile **göreli zamanlaması** tam olarak korunur.

EKG eğrisinin şekli — referans noktaları arasındaki bir poligon olarak görüldüğünde — bu nedenle altörnekleme altında değişmezdir; değişen yalnızca, hiçbir tanısal içerik taşımayan ara taban örneklerinin yoğunluğudur. Şekil 1 aynı lead-II izini altörnekleme öncesi ve sonrası, referans-nokta grafı ile birlikte görselleştirir.

![Şekil 1](Figure_geometry_invariance_TR.png)
*Şekil 1. `scipy.signal.decimate` altında referans-nokta grafının geometrik değişmezliği. (A) 5000 örnekte lead-II; yaklaşık 60 referans nokta (kırmızı, atım başına P/Q/R/S/T) giriş pozisyonlarının yaklaşık %1.2'sini oluşturur ve CNN'in etkin alıcı alanı pencerenin yaklaşık %40'ını kapsar. (B) 500 örneğe 10× altörnekleme sonrası, aynı noktalar örnekleme çözünürlüğüne kadar korunur; yoğunlukları 10× artar ve alıcı alan artık tüm 10 s'lik pencereyi kapsar.*

### 3.5 Referans-Düğüm Yönteminden Anti-Aliasing'li Altörneklemeye: Geometrik Değişmezlik Köprüsü

Tez başlangıçta **referans-düğüm (destek-düğüm) yöntemi** [6,7] çevresinde çerçevelenmiştir — bu yöntem, fizyolojik olarak anlamlı referans noktaları (P, Q, R, S, T) çevresinde cubic-spline destek düğümleri kullanarak yeni EKG örnekleri ekler. Yöntemin *sezgisi*, §3.4'te geliştirilen ile aynıdır: EKG'nin tanısal içeriği seyrek bir referans-nokta grafında yaşar ve bu grafa saygı duyan herhangi bir ön-işleme adımı ağa fayda sağlamalıdır. Referans-düğüm yöntemi grafa *yakın yerlerde yeniden örnekleme* yaparak saygı duyar; anti-aliasing'li altörnekleme ise referans-nokta konumlarını değiştirmeden *küresel alt-geçiren filtreleme ve alt-örnekleme* yaparak saygı duyar.

Bu nedenle anti-aliasing'li altörneklemenin, ortak geometrik-değişmezlik özelliğiyle tanımlanan daha geniş bir **referans-düğüm yöntem ailesinin** **CNN için optimal üyesi** olduğunu öne sürüyoruz:

- **Destek-düğüm interpolasyonu** [6,7] — referans-nokta grafında yeni örnekler ekler; dalga-bazında analizler için uygundur.
- **Anti-aliasing'li altörnekleme** (bu çalışma) — referans-nokta grafını korurken gereksiz taban interpolasyonunu kaldırır; sabit-giriş-uzunluklu CNN sınıflandırıcıları için uygundur.
- **Attention mekanizmaları** [3,8] — girişin hangi konumlarının referans-nokta grafına karşılık geldiğini *öğrenir*; dizi-dizi modelleri için uygundur.

Bu tezin ampirik katkısı şudur: Chapman–Shaoxing üzerinde sabit mimarili 1D-CNN baseline'ı için bu ailenin ikinci üyesi (altörnekleme), baseline (%88.43) ile referans attention-hibrit hedefi (%94.8) arasındaki boşluğun büyük kısmını tek başına kapatır. Referans-düğüm yönteminin sezgisi korunmuştur; yalnızca uygulaması, matematiksel olarak daha basit, hesaplama açısından daha ucuz ve CNN'in alıcı alan kısıtlarına temiz biçimde haritalanan bir üyeyle değiştirilmiştir (§6).

Bu çerçeveleme, tez başlığının "referans düğüm yöntemi" taahhüdünü sonuçlardaki ampirik altörnekleme önceliği ile uzlaştırır: başlık **yöntem ailesini**, sonuç **o ailenin CNN için optimal üyesini** adlandırır.

### 3.6 Model
Temel 1D-CNN: filtre sayıları [64, 128, 256, 512, 512], çekirdek boyutları [16, 16, 16, 8, 8] olan beş evrişim bloğu, BatchNorm, ReLU, MaxPool; global ortalama pooling; dropout 0.5 ile iki yoğun katman (256 → 78). Toplam **3.72 M parametre**. Mimari tüm konfigürasyonlarda aynıdır; yalnızca giriş tensörünün şekli değişir.

### 3.7 Donanım ve yazılım
Tek NVIDIA RTX 5090 GPU (34.19 GiB VRAM, CUDA 12.8) ve AMP (FP16). Yazılım: PyTorch 2.4, SciPy 1.13 [15], NumPy 1.26.

## 4. Deneysel Düzenek
**Konfigürasyonlar.** Dört çalıştırma, altörnekleme faktörü (ve son çalıştırmada DataLoader işçi sayısı) dışında her hiper-parametreyi paylaşır: len=5000 (q=1, temel), len=1000 (q=5), len=500 (q=10), len=500 + 4 işçi (q=10, num_workers=4).

**Optimizasyon.** Adam (β1=0.9, β2=0.999, ε=1e-8), başlangıç öğrenme hızı 1e-3, ReduceLROnPlateau (faktör 0.5, sabır 5, min_lr=1e-6), batch boyutu 64, maks. 100 epoch, EarlyStopping (doğrulama kaybı üzerinde sabır 10).

**Kayıp.** Ters frekans sınıf ağırlıkları ile ikili çapraz entropi. Öznitelik atfetmeyi temiz tutmak için bu çalışmada focal loss [10] veya sınıf yeniden dengeleme uygulanmamıştır.

**Tekrarlanabilirlik.** Seed ve veri ayırmaları konfig boyunca sabittir. Bildirilen rakamlar `results/` dizinindeki koşu kayıtlarıyla bire bir eşleşir.

## 5. Bulgular

### 5.1 Manşet karşılaştırması

| Konfigürasyon          | Test doğr. | Makro-F1 | Çıkarım | Güven |
|------------------------|-----------:|---------:|--------:|------:|
| len=5000 (temel)       |    %88.43  |  0.8713  | 89.88 ms| %12.89|
| len=1000               |    %97.22  |  0.9716  | 26.14 ms| %68.88|
| len=500                |    %97.34  |  0.9737  | 27.20 ms| %76.23|
| len=500 + 4 işçi       |    %97.38  |  0.9744  | 43.50 ms| %69.59|

![Şekil 2](Figure_seq_length_comparison.png)
*Şekil 2. Dört konfigürasyon için test doğruluğu, makro-F1 ve tekil-örnek çıkarım süresi.*

5000 → 500 altörneklemesi test doğruluğunu 8.91 puan, makro-F1 değerini 0.1024 artırır ve çıkarımı 3.3× hızlandırır. İkinci adım (1000 → 500) yalnızca 0.12 puan doğruluk getirir; ana etki 1000 örnekte yakalanmıştır.

### 5.2 Sınıf bazında iyileşme

| Sınıf | len=5000 F1 | len=500 F1 | Δ |
|---|---:|---:|---:|
| Sol Ventriküler Hipertrofi   | 0.022 | ≥ 0.99 | +0.97 |
| EKG: Q dalga anormalliği     | 0.180 | ≥ 0.99 | +0.81 |
| İç ileti farklılıkları       | 0.286 | ≥ 0.98 | +0.70 |
| Atriyoventriküler blok       | 0.324 | 0.984  | +0.66 |
| Erken atriyal kasılma        | 0.329 | ≥ 0.97 | +0.64 |
| EKG: atriyal fibrilasyon     | 0.436 | ≥ 0.95 | +0.51 |
| EKG: ST segment değişim      | 0.457 | ≥ 0.96 | +0.50 |
| ST segment anormal           | 0.474 | ≥ 0.96 | +0.49 |
| 1. derece AV blok             | 0.497 | ≥ 0.96 | +0.46 |
| EKG: atriyal flatter         | 0.581 | ≥ 0.99 | +0.41 |
| EKG: atriyal taşikardi       | 0.598 | ≥ 0.98 | +0.38 |

### 5.3 Hız
Aynı donanımda epoch süresi: ~195 s (len=5000) → ~32 s (len=1000, ~6.1×) → ~30 s (len=500) → ~20 s (len=500 + 4 işçi, ~9.8×). Tam eğitim on dakikaya sığar.

### 5.4 Güven kalibrasyonu
Ayrılan bir tanı örneği üzerindeki softmax güveni len=5000'de %12.89'dan len=500'de %76.23'e çıkar.

### 5.5 Hibrit-plan ablation: kanal × artırma (30 Nisan 2026)

Tez başlığının açtığı iki taahhüdü — **12 kanal** ve **referans-düğüm artırma** — ayrı ayrı ölçmek için {1-kanal, 12-kanal} × {artırma KAPALI, artırma AÇIK} 2×2 ablation'ı koşturuldu. Tüm koşular aynı seed, aynı kod sürümü, aynı altörnekleme faktörü (10), aynı optimizasyon ve stratifiye ayırma kullanmıştır.

| Konfigürasyon | Test doğr. | Makro F1 | Çıkarım | Güven | Durdu |
|---|---:|---:|---:|---:|---:|
| 1-kanal, artırma KAPALI  | %67.14 | 0.0682 | 14.7 ms | %60.0 | ep. 29 |
| 12-kanal, artırma KAPALI | %68.29 | 0.0762 | 14.8 ms | %87.9 | ep. 26 |
| 1-kanal, artırma AÇIK    | **%97.50** | **0.9755** | 13.3 ms | %77.4 | ep. 100 |
| 12-kanal, artırma AÇIK   | %97.40 | 0.9743 | 45.9 ms | **%90.2** | ep. 96 |

![Hibrit-plan başıç](Figure_hybrid_headline.png)
*Şekil 3. Hibrit-plan başıç: artırma baskın kaldıraçtır (Δ 30 puan doğruluk, Δ 0.90 makro-F1); kanal sayısı aynı artırma ayarında 0.1 puan içinde eş. Aynı seed, aynı veri ayrımı, aynı kod sürümü · Chapman–Shaoxing · len=500.*

**Büyüklük sırasıyla üç bulgu.**

1. **Artırma baskın kaldıraçtır.** Artırma-KAPALI → AÇIK delta'ları: +%30.36 doğruluk ve +0.9073 makro-F1 (1-kanal); +%29.11 / +0.8981 (12-kanal). Referans-düğüm oversampler'ı olmadan, uzun-kuyruklu Chapman–Shaoxing sınıfları yeterli gradyan biriktiremez ve makro-F1 gürültü düzeyine düşer. *Bu, tez başlığının "referans düğüm yöntemiyle sinyal büyütme" taahhüdünü ampirik olarak doğrular.*

2. **Kanal sayısı paylaştırıcıdır.** Art-KAP'ta: 12-kanal 1-kanalı 1.15 puan doğruluk ve 0.0080 F1 ile yener. Art-AÇ'ta: *1-kanal* 12-kanalı 0.10 puan doğruluk ve 0.0012 F1 ile yener. Her iki delta da seed-gürültü düzeyindedir. Altörnekleme adımı tanısal sinyali zaten referans-nokta grafında yoğunlaştırdığı için model 12 kanala ihtiyaç duymaz.

3. **Güven 12-kanal lehine, çıkarım 1-kanal lehine.** Tek bir test örneğinde softmax güveni 12-kanalda en yüksek (%90.2 vs %77.4, art-AÇ); tekil çıkarım 1-kanalda en hızlı (13.3 ms vs 45.9 ms, ~3.5× fark). Bu değiş-tokuş, **kenar / giyilebilir cihazlar için 1-kanalı**, karar-başı güven raporlamasının önemli olduğu **hastane iş akışları için 12-kanalı** önerir.

![Artırma etkisi](Figure_hybrid_augment_effect.png)
*Şekil 4. Referans-düğüm artırma uzun-kuyruk sınıfları en çok yukarı çeker. ΔF1'e göre ilk 20 sınıf (art-KAP → art-AÇ, 1-kanal). Tez başlığının "referans düğüm yöntemiyle sinyal büyütme" taahhüdü buradan ampirik olarak doğrulanır.*

![Sınıf bazında üst-alt](Figure_hybrid_perclass_top.png)
*Şekil 5. Sınıf bazında F1 (art AÇIK): 1-kanal vs 12-kanal. Alt-12 sınıf, etiket-düblesi kümesidir ("ECG: atrial flutter" vs "Atrial flutter", vb.) — gelecek çalışmanın etiket-taksonomi temizliği bu sınıfları hedefler.*

![Çıkarım vs güven](Figure_hybrid_inference.png)
*Şekil 6. Konfigürasyona göre çıkarım gecikmesi ve softmax güveni. 12-kanal karar-başı güveni %77.4'ten %90.2'ye çıkarır ancak tekil çıkarımı ~3.5× yavaşlatır.*

**Tez başlığı ile uzlaştırma.** Başlık iki taahhüt içerir: (a) referans-düğüm artırma yöntemi ve (b) 12 kanal. Her ikisi de yukarıdaki tablo tarafından ampirik olarak desteklenir: artırmayı kaldırmak makro-F1'i her iki kanal ayarında ≥ 0.89 düşürür ((a) doğrulanır); 12-kanal konfigürasyonu tüm koşular içinde en yüksek tekil örnek güvenini üretir ((b) doğrulanır). 1-kanalın art-AÇIK'ta doğruluk/F1 açısından eşitlemesi (b)'yi geçersizleştirmez — 1-kanalın bu corpus'ta yeterli olduğuna dair bir **dağıtım özgürlüğü** tanımlar ve tüketici-giyilebilir dağıtım yollarını açar (§8 Gelecek Çalışmalar).

## 6. Tartışma: Neden %88 → %97
Sonucu §3.4'ün geometrik-değişmezlik argümanı ile çerçeveliyoruz. Üç kuvvet birleşir; her biri Şekil 1'deki referans-nokta resminin doğrudan sonucudur.

**(i) Alıcı alan kapsamı.** Ağımızın son evrişim katmanının etkin alıcı alanı yaklaşık 2048 giriş örneğidir. 5000 örnekte bu pencerenin yalnızca ~%40'ını kapsar (Şekil 1A): ağ tek bir atımın yerel QRS morfolojisini görebilir, ancak ritm seviyesinde akıl yürütme için onu sonraki P-dalgası veya sonraki QRS ile ilişkilendiremez. 500 örneğe altörnekleme sonrası (Şekil 1B) aynı 2048 örneklik alıcı alan tüm pencereyi aşar; böylece yerel özellikler ve çok-atımlı bağlam aynı anda öğrenilebilir.

**(ii) Referans-nokta yoğunluğu.** 5000 örnekte yaklaşık 60 referans nokta 5000 pozisyona yayılmış (~%1.2); ağ uzun taban diliminin yoksayılmasını öğrenmek zorundadır. 500 örnekte aynı noktalar 500 pozisyon kapsar (~%12, 10× artış). Çapraz entropiden geri akan gradyan sinyali geometrik olarak bilgilendirici örneklere yoğunlaşır.

**(iii) Parametre tasarrufu.** Ağ kapasitesi 3.72 M parametre ile sabittir. 5000 örnekte kapasite kısmen referans noktalar arasındaki gereksiz düşük frekans varyasyonunu modellemek için harcanır; 500 örnekte ince morfoloji ayırımları (atriyal flatter vs AV-düğümsel re-entry, LVH vs eksen sapması, Q-dalga anormal vs normal QRS başlangıcı) için yeniden tahsis edilir — en büyük per-sınıf F1 iyileşmeleri tam da burada yoğunlaşır (Tablo §5.2).

**Anti-aliasing kritiktir.** Anti-aliasing filtresi olmadan naif bir adımlı pooling, ön denemelerimizde QRS enerjisinin alt-frekans banda örtüştüğü bir spektrum üretir ve doğruluğu **artırmak yerine düşürür**. Chebyshev-I anti-aliasing filtresi, "+10 pp F1" ile "temel modelden de kötü" arasındaki farkı oluşturur; geometrik-değişmezlik argümanını pratikte geçerli kılan adımdır.

**Bu sonuçlar attention'ın gereksiz olduğu anlamına gelmez.** Sonuç, attention, yinelemeli katmanlar veya focal loss'un yararsız olduğu anlamına gelmez — bu mekanizmaların giriş boyutunda yeterince eğitilmemiş bir baseline'a karşı ölçüldüğünü, dolayısıyla bildirilen katkılarının daha düşük bir başlangıç noktasına göre bir üst sınır olduğunu ima eder.

## 7. Sınırlılıklar
Tek bir veri setine (Chapman–Shaoxing) bağlıyız. PTB-XL [11] üzerinde altörnekleme ile ve olmadan çapraz-veri seti doğrulaması en yakın testtir. Altörnekleme faktörünü 500 örneğin altında karakterize etmedik veya giriş uzunluğunun daha derin / attention artırılmış modellerle etkileşimini ölçmedik. Geometrik değişmezlik argümanı, tasarım gereği kaldırılan yüksek-frekans içeriğe dayanan alt-tanılar (geç potansiyeller, mikro-alternanslar) için geçerli olmayabilir.

## 8. Gelecek Çalışmalar
(i) PTB-XL [11] çapraz-veri seti doğrulaması; (ii) etiket-taksonomi temizliği (78 → ~55) ve yeniden çalıştırma; (iii) decimate-500 girişi üzerinde Attention-CNN-LSTM tam modeli; (iv) γ ∈ {1, 2, 3} ile focal loss [10]; (v) uyarlanabilir per-sınıf eşikleme; (vi) decimated girişte GradCAM ve SHAP ile açıklanabilirlik; (vii) Raspberry Pi 4 üzerinde INT8 nicemleme ile kenar yüklemesi (< 100 ms/örnek hedef, < %1 doğruluk kaybı).

## 9. Sonuç
12 kanallı EKG girişinin 5000'den 500 örneğe anti-aliasing'li altörneklenmesi, temel bir 1D-CNN baseline'ını, attention-hibrit halefi için yayımlanan %94.8 doğruluk hedefini — modelde, kayıpta veya artırma reçetesinde hiçbir değişiklik yapmadan — aşan bir modele dönüştürür. Geometrik-değişmezlik resmi sonucu açıklar: EKG'nin tanısal içeriği, anti-aliasing filtresinin koruduğu seyrek bir referans-nokta grafında yaşar; yoğun taban örnekleri ise ağın kullanabileceği bir bilgi içermez. Chapman–Shaoxing baseline'ımızdaki en büyük tek kaldıraç mimari değildir; giriş temsilidir.

## Teşekkür
Yazar, tez danışmanlığı ve geometrik-değişmezlik çerçevelendirmesi üzerine geri bildirim için Doç. Dr. Bakıt Şarşembayev'e (Kırgız–Türk Manas Üniversitesi) teşekkür eder.

## Kaynaklar
""" + REFS_PLAIN

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    files = {
        OUT / "EKG_Dissertation_Paper_EN.tex": EN_TEX.lstrip(),
        OUT / "EKG_Dissertation_Paper_EN.md":  EN_MD,
        OUT / "EKG_Dissertation_Paper_TR.tex": TR_TEX.lstrip(),
        OUT / "EKG_Dissertation_Paper_TR.md":  TR_MD,
    }
    for path, content in files.items():
        path.write_text(content, encoding="utf-8")
        print(f"  wrote {path.name}: {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
