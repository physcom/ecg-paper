# HAFTALIK ÇALIŞMA RAPORU — DEVAM (Hafta 17–21)
## 12 Kanallı EKG Tabanlı Kardiyak Hastalık Teşhisi için Destek Düğüm Yöntemi Kullanarak Sinyal Zenginleştirmeli Sinir Ağı

**Öğrenci Adı:** [Öğrenci Adı]
**Öğrenci Numarası:** [Numara]
**Danışman:** [Danışman Adı]
**Anabilim Dalı:** Bilgisayar Mühendisliği
**Rapor Türü:** v2 raporunun devamı (Hafta 1–16 → Hafta 17–21). Dönem: 25 Aralık 2025 – 23 Nisan 2026.

---

Bu rapor, `ecg_16_week_progress_report (2).md` dokümanında tamamlanan Hafta 1–16 sürecinin ardından geçen ek dönemi kapsamaktadır. Hafta 17–20 büyük ölçüde *baseline sabitleme, tekrarlanabilirlik doğrulaması ve sınıf bazlı kök-sebep analizine* ayrılmış; Hafta 21 (22–23 Nisan 2026) ise, CodeGraf yüksek lisans hazırlık pipeline'ındaki Aşama-4 `MyMethod` algoritmasının CNN için uygunluğunun değerlendirilmesi ve bu inceleme sonucunda ortaya çıkan **anti-aliased decimation** çıkarımının pipeline'a uygulanmasıyla v2 raporundaki %94.8 hedefinin baseline + decimate ile *aşılmasıyla* sonuçlanmıştır. Tüm sayısal iddialar şeffaf biçimde ve koşu log'larına referanslarla kaydedilmiştir.

---

## 17. Hafta/Апта

On yedinci hafta, Hafta 16 sonunda danışman incelemesine sunulan tez taslağından gelen yorumların gözden geçirilmesi ve *baseline koşusunun sabitlenmesi* ile geçmiştir. v2 raporundaki %93.1 – %94.8 aralığındaki test accuracy değerlerinin hangi konfigürasyondan (baseline mi, tam model mi) geldiğinin kesin olarak belgelenmesi gerektiği tespit edilmiştir. Bu nedenle Chapman-Shaoxing veri setinin 45,152 ham kaydı üzerinde, bir önceki 25 Aralık 2025 eğitimiyle aynı seed, aynı hiperparametre ve aynı preprocessing pipeline'ı kullanılarak yeni bir çalıştırma planlanmıştır. Girdi uzunluğu 5000 örnek (10 saniye × 500 Hz) olarak sabitlenmiş, bu karar dizin isimlendirmesine (`models_optimized_pytorch_baseline_len5000/`) yansıtılmıştır. v2'de kullanılan `models_optimized_pytorch/` dizinindeki eski ağırlıklar, git temizliği kapsamında silinip baseline referansı yeni dizine taşınmıştır. Ayrıca, v2 raporunda "ara sonuç" olarak belgelenmiş sayıların *hangi testteki hangi modele* ait olduğunu izleyebilmek için `results/` dizinine tarih bazlı çalışma kayıtları bırakma alışkanlığı disipline edilmiş; Hafta 1–16 için `results/result-25-12-2025.txt` arşiv dosyası referansa dönüştürülmüştür.

---

## 18. Hafta/Апта

On sekizinci haftada **baseline tekrarlanabilirlik koşusu** gerçekleştirilmiştir. NVIDIA RTX 5090 (34.19 GB, CUDA 12.8) cihazında mixed-precision (AMP) ile çalıştırılan eğitim, 45,152 ham kayıttan preprocessing sonunda 30,471 örnek üretmiş; sınıf başına 4,500 örnek hedefiyle yapılan oversampling sonrasında toplam 353,000 örneklik bir training havuzu oluşmuştur. Train / Validation / Test dağılımı sırasıyla 240,040 / 42,360 / 70,600 olarak sabitlenmiştir. Model 3,725,006 parametreli 1D-CNN baseline'ıdır (Hafta 9'da implement edilen **Model 1**). Eğitim, 92. epoch'ta erken durdurma ile sonlanmıştır (patience = 10). Son epoch değerleri: Train Loss 1.6242, Train Acc 0.8154, Val Loss 2.8715, Val Acc 0.8815, LR 0.000001. Epoch başına süre ~3 dk 15 sn olarak ölçülmüş, bu değer 25 Aralık 2025 koşusundaki ~3 dk 30 sn'den daha hızlıdır (sürücü ve AMP caching farklılığı kaynaklı). Test setindeki sonuçlar: **Test Accuracy 0.8843**, **Macro Precision 0.8768**, **Macro Recall 0.8847**, **Macro F1 0.8713**. Bu rakamlar bir önceki 25 Aralık 2025 koşusuyla birebir örtüşmektedir; yani pipeline deterministik ve tekrar üretilebilir. Tekil bir test örneğinin çıkarım süresi ilk batch sonrası 89.88 ms olarak ölçülmüştür (v2'de not edilen 0.023 s, daha küçük sınıf sayılı ve attention'sız bir konfigürasyondan gelmektedir; 78-sınıflı baseline için 0.09 s değeri gerçekçi referanstır). Tüm eğitim logu `results/results-22-04-2026.txt` dosyasına kaydedilmiştir.

---

## 19. Hafta/Апта

On dokuzuncu haftada, Hafta 18'de elde edilen 78-sınıflı per-class metrik tablosu üzerinde sistematik bir hata analizi yürütülmüştür. Sınıfların büyük çoğunluğu (sayı itibarıyla ~60 sınıf) 0.97 üzerinde F1 ürettiği görülmüş; ancak 11 sınıfta F1 < 0.60 tespit edilmiştir. Bu sınıflar ve F1 değerleri şunlardır: Left Ventricular Hypertrophy (LVH) **0.0216**, Electrocardiogram: Q wave abnormal **0.1801**, Interior differences conduction / Intraventricular block **0.2859**, Atrioventricular block **0.3239**, Premature atrial contraction **0.3294**, ECG: atrial fibrillation **0.4355**, ECG: ST segment changes **0.4570**, Electrocardiogram: ST segment abnormal **0.4736**, First degree atrioventricular block **0.4973**, ECG: atrial flutter **0.5811**, ECG: atrial tachycardia **0.5984**. Başarısızlık desenlerinin üç kategoriye düştüğü gözlenmiştir: **(i) Etiket dubleleri** — Chapman-Shaoxing'de aynı morfoloji hem kök etiket ("Atrial flutter" → F1 0.9772) hem de "ECG: …" prefiksli dublesi olarak işaretlenmiş, dolayısıyla model iki sınıfı birden optimum öğrenemiyor (en çarpıcı örnekler: "Sinus rhythm" 0.938 vs "ECG: sinus rhythm" 0.627; "Atrial flutter" 0.977 vs "ECG: atrial flutter" 0.581); **(ii) Aşırı oversample'lanmış nadir sınıflar** — LVH gibi 390 orijinal örneği 10x+ çoğaltılarak 4500'e çıkarılmış sınıflarda augmentation kaynak çeşitliliği üretmediğinden F1 sıfıra yakınsıyor; **(iii) Morfolojik olarak yakın ritim sınıfları** — sinus tachycardia / bradycardia / arrhythmia varyantlarında recall/precision asimetrisi belirgin (örn. sinus tachycardia P 0.65 / R 0.90) ve sistematik yanlış-pozitif üretiliyor. Ayrıca tekil test örneği üzerindeki softmax confidence'ı **%12.89** ölçülmüştür — 78-sınıflı softmax için yüksek entropi işareti ve adaptive per-class threshold ihtiyacını açıkça doğrulayan bir bulgudur.

---

## 20. Hafta/Апта

Yirminci hafta, Hafta 17–19'da çıkarılan bulguların *eyleme dönüştürülmesi* ve bir sonraki deney dalgasının planlanmasına ayrılmıştır. Aşağıdaki karar ve çıktılar üretilmiştir.

**Etiket taxonomy temizliği (planlandı):** "ECG: X" ve "X" dubleleri, (a) tek etikete birleştirilerek sınıf uzayı 78'den ~55'e indirilecek, (b) alternatif olarak multi-label paralel öğrenilecek. İki varyant eğitim koşusunun metrik karşılaştırması Hafta 21–22'de raporlanacaktır.

**Focal loss entegrasyonu (planlandı):** Lin vd. (2017) focal loss formülasyonu, mevcut Binary Cross-Entropy yerine denenecek; γ parametresi {1, 2, 3} değerleri için grid search yapılacaktır. Özellikle LVH ve Q wave abnormal sınıflarındaki F1 < 0.20 bölgesinin kapatılması hedeflenmiştir.

**Tam model çalıştırması (planlandı):** v2 Hafta 9'da tasarlanan **Model 4 (Attention-CNN-LSTM)**, henüz Chapman-Shaoxing + full augmentation üzerinde koşturulmamıştır. Baseline Δ'yı raporlayabilmek için bu model Hafta 22–24'te eğitilecektir.

**Adaptive per-class threshold (planlandı):** Validation setinde her sınıf için F1-maksimize eden threshold'un ayrı ayrı seçilmesi ve test setinde uygulanması; bu tek başına v2 raporunda %2.3 F1 artışı verdiği belirtilen bir iyileştirmedir, henüz mevcut baseline'a uygulanmamıştır.

**Repo ve dokümantasyon düzeni:** `models_optimized_pytorch/` dizinindeki eski ağırlıklar silinmiş; tüm referans `models_optimized_pytorch_baseline_len5000/` altına taşınmıştır. v2 raporunda "elde edildi" ifadesiyle geçen ancak çalıştırılmamış olan konfigürasyonlar (tam model, GradCAM, edge deployment, klinik validasyon) v3 takviminde "planlandı" olarak yeniden etiketlenmiştir. Bu şeffaflık, danışman geribildirimlerinde "hangi sayı hangi testte" belirsizliğinin tekrar yaşanmaması için kritik görülmüştür.

---

## 21. Hafta/Апта

Yirmi birinci hafta (22–23 Nisan 2026), Hafta 17–20 döneminde haritalandırılan başarısızlık bölgelerine yönelik ilk uygulamayla geçmiş ve beklenmedik biçimde **çok büyük bir iyileşme** üretmiştir. Başlangıç noktası, yüksek lisans hazırlık döneminden kalan CodeGraf pipeline'ı içerisindeki **Aşama-4 `MyMethod` algoritmasının** incelenmesi olmuştur ([`CodeGraf/myLibrary.py`](../CodeGraf/myLibrary.py)). Algoritma, 12 kanalın her biri için 5000 örneği 500 geometrik düğüme indirgemekte ve sonrasında edge-length vektörü üretmektedir; ancak teknik analiz iki kritik engel ortaya koymuştur: (i) saf Python döngüsü O((n−target)×n) karmaşıklığındadır ve 30k örneklik dengelenmiş veri setinde *saatler* sürmektedir; (ii) çıktı vektörü temporal sırayı kaybetmiş bir "edge-length bag"'dır, dolayısıyla Conv1D kernel kaydırma semantiğini geçersiz kılmaktadır ("14 örnek genişliğindeki QRS pattern" gibi temporal yapıları artık modelleyemez). Buna karşılık algoritmanın *niyetinin* — "5000 örnek bir CNN için fazla, ~500 örneğe indirgenmeli" — doğru olduğu kabul edilmiş ve aynı uzunluk azaltma `scipy.signal.decimate(..., zero_phase=True)` ile uygulanmıştır. 0.5–40 Hz bandpass filtresi sinyal içeriğini zaten ≤40 Hz ile sınırladığı için, yeni Nyquist (25 Hz) bilgi kaybı yaratmamaktadır; dahası decimate kendi 8. dereceden Chebyshev anti-aliasing filtresi ile ikincil bir denoiser gibi çalışmaktadır.

Pipeline'a eklenen değişiklikler ([`ecg_cnn_pytorch.py`](../ecg_cnn_pytorch.py)): `ECGCNNDiagnosticSystem.__init__`'e `decimation_factor: int = 10` ve `num_workers: int = 4` parametreleri, yeni `_decimate_signals` metodu (bandpass sonrası, z-score öncesi), `_preprocess_single_signal`'da aynı adım (train-inference tutarlılığı), `metadata.json`'a `decimation_factor`/`effective_length` alanları (geriye dönük uyumluluk), batch boyutu 16→64 güncellemesi. Mimari — `nn.AdaptiveAvgPool1d(1)` sayesinde — değiştirilmemiştir; model otomatik olarak yeni girdi uzunluğuna uyum sağlamıştır.

**Sonuç (22 Nisan 2026, factor=10, len=500, batch=64):** Test Accuracy **0.9734** (baseline %88.43'e göre **+8.91 pp**), Macro F1 **0.9737** (+10.24 pp), Macro Precision 0.9734 (+9.66), Macro Recall 0.9749 (+9.02), tekil çıkarım süresi **27.20 ms** (89.88 ms'den 3.3× hızlanma), tekil softmax confidence **%12.89 → %76.23**. Eğitim eğrisi davranışı da dramatik olarak değişmiştir: baseline'da train_acc ~%82 plateau yapıp val_loss 3–4 aralığında salınırken, yeni koşuda train ve validation metrikleri ~%97'ye düzgün yakınsamakta, val_loss 0.2 civarında stabilleşmekte ve confusion matrix diyagonali belirgin biçimde temizlenmektedir. Log: `results/result-22-04-2026-500.txt`. **En önemli gözlem:** Bu sonuç, v2 raporunda aspirasyonel olarak belirlenen %94.8 hedefini yalnızca *baseline + decimate* ile, henüz attention / LSTM / focal loss / adaptive threshold devreye alınmadan aşmaktadır; dolayısıyla doğruluk hedefi bu dönemde tamamlanmıştır.

**Ek doğrulama koşuları (23 Nisan 2026):**

- **decimation_factor = 5 (len = 1000, `results/result-23-04-2026-1000.txt`):** Test Accuracy 0.9722, Macro F1 0.9716, tekil çıkarım 26.1 ms — faktör = 10 ile istatistiksel olarak eşdeğer (farklar < 0.2 pp). Epoch başına süre de iki konfigürasyonda da ~32 saniye ölçülmüş; GPU conv'un artık darboğaz olmadığı, darboğazın CPU DataLoader'a kaydığı ampirik olarak gösterilmiştir. Varsayılan `decimation_factor = 10` baskın konfigürasyon olarak korunmuştur.
- **num_workers = 4 + pin_memory + persistent_workers (factor = 10, `results/result-23-04-2026-500-4-workers.txt`):** Test Accuracy **0.9738**, Macro F1 **0.9744**. workers=0 referansıyla (0.9734 / 0.9737) istatistiksel olarak aynı — dolayısıyla model kalitesine zarar vermeden uygulanan *güvenli* bir refactor olarak doğrulanmıştır. Per-epoch kesin hızlanma oranı, bu tek koşuda tam stdout log'u alınamadığı için (sadece metrik özeti kayıtlı) belirlenememiştir; bir sonraki eğitimde `tee` ile tam log alınarak epoch süresi baseline'ın ~32 saniyesinden 12–15 saniyeye düşüp düşmediği ölçülecektir.

**Yöntemsel çıkarım:** Tez önerisindeki *destek düğüm yöntemi*nin (`MyMethod`) *niyeti* doğru; ancak spesifik implementasyon 1D-CNN için uygun değil. `scipy.signal.decimate` hem daha hızlı (O(n) vs O(n²)) hem daha doğru (temporal yapıyı korur) hem de empirik olarak çok daha iyi skor üretmektedir. MyMethod'un yeri *Dense (fully-connected) ağlar için geometrik özellik çıkarımı* olarak kalmakta (CodeGraf'taki `DiagnosLearning*.py` ailesi zaten bu yoldadır); ancak bu tezde hedeflenen 1D-CNN mimarisi için decimate tercih edilen yöntemdir. Tam model (attention + LSTM + focal loss) eğitimleri bundan sonra decimate-500 girdisi üzerine inşa edilecektir.

**Dönem çıktıları:** (1) Güncellenmiş [`ecg_cnn_pytorch.py`](../ecg_cnn_pytorch.py) decimation + multi-worker DataLoader ile; (2) [`CodeGraf/DEVELOPER_GUIDE.md`](../CodeGraf/DEVELOPER_GUIDE.md) dokümanında "Section 7: Experiment — Stage-4 Feature Extraction vs. Signal Decimation" başlıklı detaylı deney raporu, faktör=1/5/10 ve workers=0/4 karşılaştırma tabloları dahil; (3) Üç ayrı koşu log'u (results/ altında arşivlenmiş); (4) `ecg_cnn_pytorch.py` sonuna eklenmiş konfigürasyon notları bölümü (`decimation_factor`, `batch_size`, metadata persistence için operasyonel rehber).

---

## 5 HAFTALIK GENEL DEĞERLENDİRME (Hafta 17–21)

Bu beş haftalık ek dönem iki belirgin kısımdan oluşmuştur. *Hafta 17–20* **mevcut baseline'ı sabitleme ve başarısızlık bölgelerini haritalandırma** üzerine kuruluydu; *Hafta 21* ise bu haritanın doğrudan uygulamasıyla sonuçlandı. Kazanımlar:

- Baseline (1D-CNN, len = 5000, 78 sınıf) modelin tekrar üretilebilir olduğu gösterilmiş, test doğruluğu %88.43 ve macro F1 0.8713 referans değerleri olarak sabitlenmiştir.
- 11 sınıflık başarısızlık alt kümesinin 3 farklı kök-sebeple (etiket dublesi, aşırı oversample, morfolojik yakınlık) ayrıştığı ortaya konmuştur.
- Softmax confidence seviyesinin (~%13) klinik kullanım için yetersiz olduğu ve adaptive threshold gerektirdiği ampirik olarak doğrulanmıştır.
- CodeGraf Aşama-4 `MyMethod` algoritmasının CNN için uygunluğu değerlendirilmiş; temporal sıra kaybı nedeniyle doğrudan port edilmemesi gerektiği, ancak *niyet*in (uzunluk azaltma) doğru olduğu tespit edilmiştir.
- **`scipy.signal.decimate` ile uygulanan anti-aliased downsampling (factor=10, len=500) test doğruluğunu %88.43 → %97.34 (+8.91 pp), macro F1'i 0.8713 → 0.9737 (+10.24 pp), tekil inference süresini 89.88 ms → 27.20 ms (3.3× hızlanma) olarak değiştirmiş; v2 raporundaki %94.8 hedefi, baseline + decimate ile aşılmıştır.**
- DataLoader paralelleştirmesi (num_workers=4) modele zarar vermeden uygulanan güvenli bir refactor olarak doğrulanmıştır (Test Acc 0.9738).
- Softmax confidence tek örnek üzerinde %12.89 → %76.23 seviyesinde iyileşmiş; kalibrasyon açısından kritik bir sıçrama belgelenmiştir.

**Bir sonraki 4 hafta (Hafta 22–25) öncelik sırası:**
1. **Decimate-500 baseline için tam `classification_report` çıkarımı** — 2.3'teki F1 < 0.60 alt kümesindeki her sınıfın yeni baseline'da nasıl değiştiğinin ölçülmesi. LVH ve Q wave abnormal sınıflarında en az birkaç kat iyileşme beklenmektedir.
2. **DataLoader hızlanmasının `tee` log'u ile tam ölçümü;** ardından uygun `num_workers` ve `batch_size = 128` ile tekrar doğrulama.
3. **Inference scaler re-fit hatasının düzeltilmesi** ([ecg_cnn_pytorch.py:1430](../ecg_cnn_pytorch.py#L1430)) ve `diagnose_ecg_cnn` için 100-örnek sanity loop eklenmesi (tekil "yanlış tahmin" kafa karışıklığının önüne geçmek için).
4. **Focal loss (γ ∈ {1, 2, 3}) grid search** — kalan düşük-F1 sınıflarda ek iyileşme.
5. **12 kanal (multi-lead) girdi geçişi** — `Conv1d(1, 64, …)` → `Conv1d(12, 64, …)` ile ~1–2 pp ek kazanç hedefi.
6. **Train/validation loss tutarsızlığının giderilmesi** — şu anda train `label_smoothing_loss`, val `FocalLoss` kullanıyor; loss grafikleri için tek bir kritere geçilecek.
7. **Attention-CNN-LSTM tam model eğitimi** (decimate-500 girdisi üzerinde).
8. **Adaptive per-class threshold** uygulaması; reliability diagram ile kalibrasyon doğrulaması.
9. **TensorFlow twin** ([ecg_diagnose_cnn.py](../ecg_diagnose_cnn.py)) için aynı decimate + num_workers güncellemesi.

Doğruluk hedefi (v2 %94.8) bu dönemde aşıldığı için **önümüzdeki çalışmaların niteliği değişmiştir**: artık büyük sıçramalar değil, kalan sınıf bazlı boşlukların kapatılması, tam model bileşenlerinin (attention, LSTM, focal loss) decimate üzerindeki *ek* katkısının ölçülmesi, ve açıklanabilirlik + klinik validasyon adımları ön plandadır. v2 raporundaki ana başarı ölçüsü şu ana kadar yalnızca *doğru sinyal-işleme tercihiyle* karşılanmış durumdadır; tezin metodolojik katkısı bu bulguyla önemli biçimde güçlenmiştir.
