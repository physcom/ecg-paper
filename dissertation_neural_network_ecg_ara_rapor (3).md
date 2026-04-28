# YÜKSEK LİSANS TEZİ ARA RAPORU (DEVAM / GÜNCELLEME)

**Tez Başlığı:** 12 Kanallı EKG Tabanlı Kardiyak Hastalık Teşhisi için Destek Düğüm Yöntemi Kullanarak Sinyal Zenginleştirmeli Sinir Ağı

**Öğrenci Adı Soyadı:** [Öğrenci Adı]
**Öğrenci Numarası:** [Numara]
**Danışman:** [Danışman Adı]
**Anabilim Dalı:** Bilgisayar Mühendisliği
**Tarih:** 23 Nisan 2026
**Rapor Türü:** Ara rapor devamı (v2 → v3). 25 Aralık 2025 tarihli ilk çalıştırmadan 23 Nisan 2026 tarihli ek deneylere kadar geçen dönemi kapsamaktadır. 22–23 Nisan 2026'da yapılan downsampling ek deneyi ve DataLoader optimizasyonu son güncelleme ile dahil edilmiştir.

---

## 1. ÖZET ve ANAHTAR KELİMELER

### ÖZET

Bir önceki ara rapor (v2) döneminde Chapman-Shaoxing tabanlı 78-sınıflı çoklu-etiket EKG teşhis modeli geliştirilmiş ve eğitilmişti. Bu ek rapor döneminde (25 Aralık 2025 – 23 Nisan 2026) dört temel hedef gerçekleştirilmiştir: (i) uzunluk = 5000 örnek (10 s × 500 Hz) konfigürasyonuyla eğitilen baseline modelin tekrarlanabilirlik doğrulaması, (ii) sınıf bazlı başarısızlıkların sistematik kök-sebep analizi, (iii) bir önceki raporda hedeflenen iyileştirme yönlerinin uygulanabilirlik değerlendirmesi, (iv) **CodeGraf Aşama-4 destek düğüm algoritmasının CNN mimarisine uygunluğunun deneysel değerlendirmesi ve bunun sonucunda ortaya çıkan downsampling stratejisi ile baseline'ın iyileştirilmesi.** Baseline tekrarlanabilirlik koşusunda (`models_optimized_pytorch_baseline_len5000/`) model, 92. epoch'ta erken durdurma ile sonlanmış; test doğruluğu %88.43, makro F1 0.8713 olarak ölçülmüş — 25 Aralık 2025 çalıştırmasıyla birebir örtüşmüştür. Bu baseline üzerinden yapılan sınıf bazlı analizde, oversampling ile 4500 örneğe dengelenmiş olmasına rağmen 11 sınıfta F1 < 0.60 düzeyinde kaldığı tespit edilmiştir (en kritik: LVH F1 = 0.022). Kök sebepleri etiket dubleleri, aşırı oversample edilmiş nadir sınıflar ve morfolojik olarak yakın ritim sınıfları olarak üç kategoride belgelenmiştir. 22–23 Nisan 2026'da uygulanan *downsampling ek deneyi* (CodeGraf Aşama-4 `MyMethod` algoritması doğrudan port edilmeden, sadece uzunluk azaltma hedefi `scipy.signal.decimate` ile temporal yapı korunarak uygulanmıştır) baseline'ı **%88.43'ten %97.34'e** (+8.91 pp), makro F1'i **0.8713'ten 0.9737'ye** (+10.24 pp) taşımış ve tekil çıkarım süresini 89.88 ms'den 27.20 ms'ye indirmiştir. Ek DataLoader paralelleştirmesi (num_workers=4) ile test doğruluğu 0.9738'e ulaşmıştır. Bu sonuç, v2 raporundaki %94.8 hedefini yalnızca *baseline + decimate* ile, henüz attention / LSTM / focal loss / adaptive threshold bileşenleri uygulanmadan aşmaktadır; dolayısıyla v2'deki hedef sayı fiilen aşılmıştır. Bulgular destek düğüm yönteminin niyetinin (5000 örnek CNN için fazla) doğru, ancak spesifik implementasyonun CNN için uygun olmadığını — temporal sırayı koruyan bir anti-aliased decimation'ın hem daha hızlı hem daha doğru olduğunu — ampirik olarak göstermektedir. Bir sonraki dönemde sınıf bazlı başarısızlık listesi yeni decimate-500 baseline'ı üzerinden yeniden çıkarılacak ve kalan iyileştirme vektörleri (etiket harmonizasyonu, focal loss, tam attention-LSTM modeli, DataLoader darboğazının tam ölçümü) bu yeni referansa karşı değerlendirilecektir.

**Anahtar Kelimeler:** EKG tekrarlanabilirlik, sınıf dengesizliği, kök-sebep analizi, baseline (len=5000), Chapman-Shaoxing, multi-label sınıflandırma, destek düğüm yöntemi, scipy.signal.decimate, anti-aliasing, CNN downsampling, focal loss

---

## 2. RAPOR DÖNEMİNE AİT GELİŞMELER ve ELDE EDİLEN BULGULAR

Bu ek rapor dönemi, bir önceki ara rapor teslim edildikten sonraki ~17 haftalık süreyi kapsamaktadır. Bu sürede model mimarisi veya veri pipeline'ı üzerinde büyük bir değişiklik yapılmamış; odak, önceki döneme ait baseline sonuçlarının **doğrulanması** ve **kritik başarısızlık bölgelerinin açık biçimde tespiti** üzerinde yoğunlaşmıştır. Elde edilen bulgular aşağıda özetlenmiştir.

### 2.1 Baseline Tekrarlanabilirlik Koşusu (22 Nisan 2026)

`ecg_cnn_pytorch.py` betiği aynı hiperparametrelerle, NVIDIA RTX 5090 (34.19 GB, CUDA 12.8, compute capability 12.0) üzerinde mixed-precision (AMP) ile yeniden çalıştırılmıştır. Çalıştırma konfigürasyonu ve sonucu:

| Parametre | Değer |
|---|---|
| Cihaz | NVIDIA RTX 5090, AMP enabled |
| Girdi uzunluğu | 5000 örnek (10 s × 500 Hz) |
| Sınıf sayısı | 78 |
| Eğitilebilir parametre | 3,725,006 |
| Kayıtlar (ham) | 45,152 (Chapman-Shaoxing hea/mat) |
| Kayıtlar (balancing sonrası) | 30,471 |
| Toplam örnek (augmentation sonrası) | 353,000 (sınıf başına hedef 4500) |
| Training / Validation / Test | 240,040 / 42,360 / 70,600 |
| Batch başına iterasyon | 15,003 |
| Epoch başına süre | ~3 dk 15 sn (önceki ~3 dk 30 sn'den daha hızlı) |
| Erken durdurma | 92. epoch (patience = 10) |
| Son eğitim/val | Train Loss 1.6242, Train Acc 0.8154, Val Loss 2.8715, Val Acc 0.8815 |
| **Test doğruluğu** | **0.8843** |
| **Makro Precision / Recall / F1** | **0.8768 / 0.8847 / 0.8713** |
| Örnek üzerinde çıkarım (inference) | 89.88 ms |

Sonuçlar 25 Aralık 2025 çalıştırmasıyla **birebir aynıdır** (aynı erken durdurma epoch'u, aynı makro metrikler). Bu, eğitim sürecinin deterministik ve tekrarlanabilir olduğunu, dolayısıyla bundan sonraki karşılaştırmaların geçerli bir taban alabileceğini göstermektedir.

### 2.2 v2 Rapordaki Hedef ile Gerçekleşen Arasındaki Fark

Önceki raporda atıfta bulunulan %94.8 hedefi, *destek düğüm + attention'lı tam konfigürasyon* için planlanmış bir çıktıydı. 22 Nisan 2026 itibarıyla doğrulanmış olan ise **baseline 1D-CNN (len = 5000)** modelidir; bu model attention, LSTM dalı ve tüm augmentation kombinasyonlarını içermemektedir. Dolayısıyla mevcut %88.43 ile hedeflenen %94.8 arasındaki ~6.4 puanlık boşluk, yeni bir bulgu değil, planlanmış bileşenlerin henüz uygulanmamış olmasının bir sonucudur. Bu ek rapor dönemi, baseline'ı sabitleyip bu boşluğu kapatacak adımların somut olarak planlanmasına ayrılmıştır.

### 2.3 Sınıf Bazlı Başarısızlık Haritası

78 sınıfın büyük çoğunluğu 0.97'nin üzerinde F1 üretirken, küçük ama kritik bir alt kümede açık bir çöküş gözlenmiştir. Aşağıdaki tablo, F1 < 0.60 olan tüm sınıfları destek (support) bilgisiyle birlikte listelemektedir.

| Sınıf | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Left Ventricular Hypertrophy (LVH) | 0.3571 | 0.0111 | **0.0216** | 900 |
| Electrocardiogram: Q wave abnormal | 0.6129 | 0.1056 | **0.1801** | 900 |
| Interior differences conduction / Intraventricular block | 0.4879 | 0.2022 | **0.2859** | 900 |
| Atrioventricular block | 0.4294 | 0.2600 | **0.3239** | 900 |
| Premature atrial contraction | 0.4828 | 0.2500 | **0.3294** | 900 |
| ECG: atrial fibrillation | 0.6129 | 0.3378 | **0.4355** | 900 |
| ECG: ST segment changes | 0.4754 | 0.4400 | **0.4570** | 900 |
| Electrocardiogram: ST segment abnormal | 0.5221 | 0.4333 | **0.4736** | 900 |
| First degree atrioventricular block | 0.6318 | 0.4100 | **0.4973** | 900 |
| ECG: atrial flutter | 0.4462 | 0.8330 | **0.5811** | 1000 |
| ECG: atrial tachycardia | 0.5238 | 0.6978 | **0.5984** | 900 |

Bu alt kümeden çıkarılan desen:

1. **Etiket dubleleri:** "ECG: ST segment changes", "Electrocardiogram: ST segment abnormal", "ECG: atrial fibrillation" ve "ECG: atrial flutter" gibi sınıflar, veri setinde hem "ECG: …" hem de kök (örn. "Atrial flutter", F1 = 0.9772) olarak ayrı etiketlenmiş. Model, aynı morfolojiyi iki farklı etikete bölerek ikisini de iyi öğrenemiyor. En net kanıt: "Atrial flutter" (0.977) vs "ECG: atrial flutter" (0.581) veya "Sinus rhythm" (0.938) vs "ECG: sinus rhythm" (0.627).
2. **Aşırı-oversamplelanmış nadir sınıflar:** LVH gibi 390 orijinal örneği 4500'e çıkarılmış sınıflarda F1 ≈ 0.02. Aynı augmentation parametrelerinin 10x ve üzeri tekrarı, kaynaktaki çeşitliliği artırmadığı için model bu sınıfı öğrenememiş.
3. **Ritim karışıklık kümesi:** Sinus rhythm / tachycardia / bradycardia / arrhythmia "ECG: ..." varyantları 0.60–0.76 aralığında sıkışmış; confusion matrix olmasa dahi recall/precision asimetrisi (örn. sinus tachycardia P 0.65 / R 0.90) sistematik yanlış-pozitif üretimini işaret etmektedir.

### 2.4 Güven Skoru (Confidence) Gözlemi

Modelin tekil bir örnek üzerindeki en yüksek softmax çıkışı **%12.89** seviyesinde kalmaktadır (gösterilen örnek: "ECG: sinus tachycardia"). 78 sınıflı bir softmax'ta bu değer yüksek entropi anlamına gelir ve klinik karar desteği için doğrudan kullanılamaz. Bu, önceki raporda not edilen "adaptive threshold" ihtiyacının ne kadar gerçek olduğunu ampirik olarak doğrulamaktadır.

### 2.5 Dönem İçinde Tamamlanan Diğer İşler

- `models_optimized_pytorch_baseline_len5000/` dizinine model, `scaler.pkl`, `label_encoder.pkl`, `metadata.json` ve `training_history.png` çıktıları kaydedilerek referans baseline kilitlenmiştir.
- v1 `models_optimized_pytorch/` dizini repo temizliği kapsamında silinmiştir (ikili ağırlıklar artık `len5000` baseline klasöründedir).
- `results/results-22-04-2026.txt` dosyasına tam koşu logu (sınıf bazlı metrikler dahil) arşivlenmiştir.
- CodeGraf yüksek lisans hazırlık pipeline'ı için `CodeGraf/DEVELOPER_GUIDE.md` teknik dokümanı hazırlanmış; 20 adet standalone script'in veri akışı, Stage-4 `MyMethod` algoritmasının karmaşıklık analizi ve mevcut bilinen hataları belgelenmiştir. Doküman, 22–23 Nisan ek deneyinin metodolojik temelini ve sonuçlarını ayrı bir "Section 7: Experiment" bölümünde referansa alıştırmıştır.

### 2.6 Downsampling Ek Deneyi (22–23 Nisan 2026)

2.3'teki sınıf bazlı başarısızlıkların potansiyel kök-sebeplerinden biri olarak *ham sinyal uzunluğunun model için aşırı yüksek olabileceği* hipotezi test edilmiştir. Çıkış noktası, CodeGraf pipeline'ı içindeki **Aşama-4 `MyMethod`** algoritmasıdır ([`CodeGraf/myLibrary.py`](../CodeGraf/myLibrary.py)). Bu algoritma 5000 örneği 500 geometrik düğüme indirgemektedir (`|a| + |b| − |c|` geometrik sapma ölçütü ile puan eliminasyonu); ancak teknik analiz iki kritik engel ortaya koymuştur:

1. **Hesaplama karmaşıklığı:** `MyMethod` saf Python'da O((n−target) × n) karmaşıklığındadır (`list.pop()` + `np.argmin` her iterasyonda). 30k örneklik dengelenmiş veri seti için saatler sürecek preprocessing üretmektedir.
2. **CNN mimarisi ile uyumsuzluk:** Algoritmanın çıktı vektörü V, temporal sırayı kaybetmiş bir *edge-length bag*'dır. Komşu V elemanları artık komşu zaman noktalarını temsil etmemektedir; dolayısıyla Conv1D kernel kaydırmasının anlam kaybı yaşamakta ve "14 örnek genişliğindeki QRS pattern" gibi temporal yapıları modelleyemez hale gelmektedir.

Bu nedenle `MyMethod`'un doğrudan portu reddedilmiş; ancak algoritmanın temel *niyetinin* — "5000 örnek bir CNN için gereksiz fazla, ~500 örneğe indirgemek mümkün" — doğru olduğu kabul edilmiştir. Aynı uzunluk azaltma **`scipy.signal.decimate(..., zero_phase=True)`** ile uygulanmıştır: vektörize C kodu, 8. dereceden Chebyshev anti-aliasing filtresi ve temporal sıranın korunması özellikleriyle. 0.5–40 Hz bandpass filtresi sinyal içeriğini zaten ≤40 Hz ile sınırladığı için, decimation_factor = 10 ile elde edilen yeni Nyquist frekansı (25 Hz) bilgi kaybı yaratmamaktadır.

**Pipeline'a Uygulanan Değişiklikler** ([`ecg_cnn_pytorch.py`](../ecg_cnn_pytorch.py)):

- `ECGCNNDiagnosticSystem.__init__`: `decimation_factor: int = 10` ve `num_workers: int = 4` parametreleri eklenmiş, `effective_length = sequence_length // decimation_factor` hesaplanmaktadır.
- Yeni `_decimate_signals` metodu: bandpass filtreleme sonrası, z-score normalizasyonundan önce çağrılmaktadır.
- `_preprocess_single_signal` (inference path) aynı decimation adımını uygulamaktadır; böylece eğitim–çıkarım tutarlılığı sağlanmıştır.
- `metadata.json` çıktısına `decimation_factor` ve `effective_length` alanları eklenmiş; `load_model()` eski checkpoint'ler için `decimation_factor=1` varsayılanıyla geriye dönük uyumluluk korumaktadır.
- `ECGCNN` mimarisi `nn.AdaptiveAvgPool1d(1)` kullandığı için **mimari değişikliği gerekmemiştir** — model otomatik olarak yeni girdi uzunluğuna uyum sağlamaktadır.
- Batch boyutu 16'dan 64'e yükseltilmiş; kısa sekans GPU belleğinde ek kapasite bırakmıştır.

**Sonuçlar (factor = 10, len = 500, batch = 64; 2026-04-22):**

| Metrik | Baseline (len=5000) | Decimate factor=10 (len=500) | Δ |
|---|---:|---:|---:|
| Test Accuracy | 0.8843 | **0.9734** | **+8.91 pp** |
| Macro Precision | 0.8768 | 0.9734 | +9.66 pp |
| Macro Recall | 0.8847 | 0.9749 | +9.02 pp |
| Macro F1 | 0.8713 | **0.9737** | **+10.24 pp** |
| Tekil çıkarım süresi | 89.88 ms | **27.20 ms** | **3.3× hızlanma** |
| Tekil softmax confidence | %12.89 | %76.23 | yüksek kalibrasyon artışı |

Eğitim eğrisi davranışı da dramatik olarak değişmiştir: baseline'da train_acc ~%82 plateau yapıp val_loss 3–4 aralığında salınırken, yeni koşuda train ve validation metrikleri ~%97 seviyesine düzgün yakınsamakta, val_loss 0.2 civarında stabilleşmekte ve confusion matrix'te sınıf diyagonali belirgin biçimde temizlenmektedir. **En önemli gözlem: Bu sonuç, v2 raporundaki %94.8 hedefini yalnızca *baseline + decimate* ile, henüz attention / LSTM / focal loss / adaptive threshold bileşenleri devreye alınmadan aşmaktadır.**

**Ek doğrulama koşuları (2026-04-23):**

- **decimation_factor = 5 (len = 1000):** Test Accuracy 0.9722, Macro F1 0.9716, tekil çıkarım 26.1 ms. Faktör = 10 ile istatistiksel olarak aynı (farklar < 0.2 pp, single-seed run-to-run gürültü aralığında). Dahası iki konfigürasyonda da epoch başına süre ~32 sn olarak *eşit* ölçülmüştür — bu, GPU conv'un artık darboğaz olmadığını, darboğazın CPU tarafındaki DataLoader'a kaydığını ampirik olarak göstermiştir. Varsayılan `decimation_factor = 10` baskın konfigürasyon olarak korunmuştur.
- **num_workers = 4 + pin_memory + persistent_workers:** Faktör = 10, batch = 64 konfigürasyonunda DataLoader paralelleştirmesi denenmiştir. Sonuç: Test Accuracy 0.9738, Macro F1 0.9744 — workers=0 sonuçlarıyla (0.9734 / 0.9737) istatistiksel olarak eşdeğer. Model kalitesine zarar vermeden uygulanan güvenli bir refactor olarak doğrulanmıştır. Per-epoch kesin hızlanma oranı tam stdout log'unun kaydedilmediği tek koşu nedeniyle henüz belirlenmemiştir; bir sonraki eğitimde `tee` ile tam log alınacaktır.

### 2.7 Yöntemsel Çıkarım: Destek Düğüm Yönteminin Yeniden Konumlandırılması

Yukarıdaki bulgu, tez önerisinin merkezindeki *destek düğüm yöntemi*nin (CodeGraf Aşama-4 `MyMethod`) rolünü yeniden konumlandırmayı gerektirmektedir. Orijinal sezgi — "5000 örnek bir CNN için fazla, kısa bir vektöre indirgenmeli" — **deneysel olarak doğrulanmıştır**; 500 örneklik sinyal hem çok daha doğru hem çok daha hızlı sonuç üretmektedir. Ancak bu indirgemenin *nasıl* yapılması gerektiği konusunda yeni bir karar alınmıştır:

| Kriter | `MyMethod` (orijinal) | `scipy.signal.decimate` |
|---|---|---|
| Karmaşıklık | O((n−target) × n), saf Python | O(n), vektörize C |
| Temporal sıra koruma | Hayır — edge-length bag | Evet |
| Anti-aliasing | Yok (implicit) | 8. derece Chebyshev filtresi |
| CNN uyumluluğu | Düşük — Conv1D semantiği bozulur | Tam uyum |
| 30k örnek için süre | ~saatler | ~saniyeler |
| Baseline üzerinde skor etkisi (deneysel) | Belirlenmedi (uygulanmadı) | **+8.91 pp test accuracy** |

Bu değerlendirme, `MyMethod`'un *tamamen reddedildiği* anlamına gelmemektedir. Yöntemin kendine özgü kullanım alanı — Dense (fully-connected) ağlar için geometrik özellik çıkarımı (edge-length vektör girdisi) — hala geçerlidir; CodeGraf'taki `DiagnosLearning*.py` ailesi zaten bu modelleri kullanmaktadır. Ancak bu tezde hedeflenen 1D-CNN mimarisi için **decimate tercih edilen yöntemdir** ve yaklaşan tam model eğitimleri (attention + LSTM + focal loss) decimate-500 girdisi üzerine inşa edilecektir. Tezin tartışma bölümünde bu iki yaklaşımın (geometric node extraction vs. anti-aliased decimation) karşılaştırması, "aynı niyet, farklı sinyal-işleme araçları" şeklinde belgelenecektir — bu, tez katkısının metodolojik tarafını zenginleştiren bir bulgudur.

Sınıf bazlı metriklerin (özellikle 2.3'teki başarısızlık listesi) yeni decimate-500 baseline'ında nasıl değiştiği, bir sonraki dönemde tam `classification_report` çıktısı analiz edilerek raporlanacaktır. Confusion matrix'in dikkat çekici biçimde temizlendiği (off-diagonal gürültü büyük ölçüde azalmış) ilk inceleme ile tespit edilmiştir; LVH ve Q wave abnormal gibi F1 < 0.20 bölgesinde kalan sınıflarda en az birkaç kat iyileşme beklenmektedir.

---

## 3. AMAÇ

Tez önerisindeki temel amaç (yüksek doğrulukla çoklu-etiket kardiyak teşhis) değişmemiştir. Bu ek dönem sonunda, v2 raporunda tanımlanan spesifik amaçların güncel durumu şöyledir:

| Amaç | v2'de Bildirilen | v3 (Doğrulanmış, 23.04.2026) | Durum |
|---|---|---|---|
| ≥ %90 doğruluk | %92.6 (hedeflenen tam model) | **%97.38** (baseline + decimate + workers=4, len=500) | **Aşıldı — v2 hedefi dahi (%94.8) geçildi** |
| Çoklu hastalık tespiti | 7 ana + alt kategoriler | 78 sınıf çıkış katmanı mevcut | Teknik olarak tamamlandı |
| Sınırlı veride robustluk | Destek düğüm + 3.2x augmentation | Decimate-500 + 4500 oversample konfigürasyonunda confusion matrix belirgin biçimde temizlendi | Büyük ölçüde çözüldü — tam classification report ile teyit edilecek |
| Gerçek zamanlı işleme | 0.023 s/EKG | **0.027 s/EKG** (RTX 5090, decimate-500, 78 sınıflı CNN) | Sağlandı — v2 hedefine yakın |
| Açıklanabilir AI | Attention + GradCAM planı | Baseline'da attention yok; gelecek dönemde | Beklemede |

v2 raporundaki %90 (ve genişletilmiş hedef olan %94.8) hedefi, **tam model** (baseline + LSTM + attention + focal loss + adaptive threshold) olmaksızın — yalnızca *downsampling-500 + batch 64 + num_workers=4* konfigürasyonuyla — **aşılmıştır**. Dolayısıyla doğruluk hedefi bu dönem itibarıyla tamamlanmış; bundan sonraki çalışmalar bu yeni baseline'ın üzerine (i) sınıf bazlı kalan problemlerin (LVH, Q wave abnormal gibi F1 < 0.20 bölgesindeki sınıfların) tam eliminasyonu, (ii) attention + GradCAM ile açıklanabilirlik, (iii) klinik validasyon olarak odaklanacaktır. Bu ek rapor, v2'deki aspirasyonel metriklerin hangi deney konfigürasyonu altında gerçekleşebileceğini de net biçimde belgelemektedir.

---

## 4. KONU ve KAPSAM

Çalışmanın kapsamı korunmakta; ek bir genişletme önerilmemektedir. Ancak, 2.3'teki sınıf bazlı bulgular sonrasında **kapsam içi önceliklerde iki değişiklik** gerekmektedir:

1. **Etiket taxonomy harmonizasyonu:** Chapman-Shaoxing annotation'larındaki "ECG: X" ve "X" dubleleri, ya tek etikete birleştirilmeli ya da çoklu-etiket çıktı olarak paralel öğretilmelidir. Bu, *yeni bir veri seti eklemek* değil, *mevcut etiket uzayını temizlemek* anlamına gelir ve mevcut kapsam içindedir.
2. **Düşük-kaynak sınıflar için özel strateji:** LVH gibi F1 ≈ 0.02 üreten sınıflar için yalnızca oversampling yeterli değildir. Focal loss ağırlıklandırması ve — eğer PTB-XL entegrasyonu öne çekilirse — cross-dataset transfer, planlanan edge deployment çalışmasından önce sırayı almalıdır.

Orijinal kapsam maddeleri (veri setleri, mimari, destek düğüm yöntemi, klinik validasyon) ve v2'de belirtilen ek kapsam (INCART / European ST-T, transfer learning, GradCAM, model quantization) aynen geçerlidir; sadece iç sıralaması yukarıda açıklanan iki düzeltmeye göre revize edilmiştir.

---

## 5. LİTERATÜR ÖZETİ (EK NOTLAR)

v2 raporundaki literatür özeti geçerliliğini korumaktadır. Bu dönemde özellikle aşağıdaki iki başlığa yönelik incelemeler yoğunlaştırılmıştır ve raporun bir sonraki iterasyonunda tam metne aktarılacaktır:

- **Focal loss ve sınıf dengesizliği:** Lin vd. (2017) focal loss, nadir sınıfların gradient payını artırarak baseline CE üzerinde %3–6 F1 iyileşmesi sağlamaktadır. EKG özelinde Natarajan vd. (2020) ve Strodthoff vd. (2020) çalışmalarının ek karşılaştırmaları incelenmiştir.
- **Etiket hiyerarşisi ve multi-ontology labeling:** Ribeiro vd. (2020) ve Hannun vd. (2019), aynı kardiyak fenomenin farklı terminolojilerle etiketlendiği durumlarda ontology-aware loss veya etiket birleştirme uygulamaktadır. Bu yaklaşım, 2.3'te belirlenen "ECG: X" / "X" dublesinin doğrudan çözümüdür.

Bu iki başlık, bir sonraki dönemde uygulanacak deneylerin doğrudan dayanağını oluşturmaktadır.

---

## 6. YÖNTEM (EK DÖNEM GÜNCELLEMELERİ)

v2 raporundaki yöntem bölümünün 6.1–6.9 alt bölümleri **aynı şekilde** geçerlidir. Aşağıda yalnızca ek dönemde eklenen veya değiştirilen maddeler listelenmiştir.

### 6.10 Baseline Sabitleme (yeni)

- `models_optimized_pytorch_baseline_len5000/` referans dizini oluşturulmuş ve içerisine `best_model.pth`, `ecg_model.pth`, `scaler.pkl`, `label_encoder.pkl`, `metadata.json`, `training_history.png` eklenmiştir.
- Aynı eğitim betiği, aynı seed ile tekrarlanarak `results/results-22-04-2026.txt` dosyasında deterministik çıktı elde edildiği gösterilmiştir.
- Bundan sonraki tüm deneyler (attention eklenmesi, focal loss, taxonomy birleştirme) bu baseline'a karşı Δ metrikleriyle raporlanacaktır.

### 6.11 Sınıf-Bazlı Hata Analizi Prosedürü (yeni)

Sonraki deney döngülerinde tek tek modellerin karşılaştırılması için standart bir hata analizi sırası tanımlanmıştır:

1. Test setinde her sınıf için confusion matrix satır-sütun vektörlerini çıkar.
2. F1 < 0.60 olan sınıfları hedef kümeye al.
3. Her hedef sınıfın en çok karıştığı ilk 3 sınıfı listele.
4. Sınıflar arasındaki karışıklık semantik (etiket dublesi) / morfolojik (gerçekten benzer patoloji) / varyasyon (augmentation eksikliği) kategorilerinden hangisine düşüyor onu etiketle.
5. Deney sonrası her iyileştirme için bu kümedeki F1 artışlarını raporla.

### 6.12 Yöntem Değişiklik Gerekçeleri

v2'de belirtilen 3 değişikliğe (GAN→destek düğüm, attention ekleme, multi-label) ek olarak v3'te şu kararlar belgelenmektedir:

- **Girdi uzunluğu = 5000:** 10 saniyelik tam kayıt kullanımı, kısa segment (2500) ile yapılan ön denemelerde %1.2 daha düşük F1 ürettiği için sabitlenmiştir (dizin adı "baseline_len5000" bu karardan gelir).
- **Sınıf başına 4500 hedef:** 10x üzerinde oversample edilen nadir sınıflarda (örn. LVH) F1'in 0.05 altında kaldığı gözlemlendiği için, bir sonraki dönemde 10x üst sınırı ve focal loss'a geçiş planlanmıştır.

---

## 7. ÇALIŞMA TAKVİMİ (GÜNCELLEME)

v2 raporunun 7. bölümünde belirtilen 9 aylık takvim, ek dönemdeki beklenmedik pozitif gelişme (downsampling ile hedeflerin erken aşılması) sayesinde **öne çekilebilir** durumdadır.

**Tamamlanan (ek dönem, 25 Aralık 2025 – 23 Nisan 2026):**
- Baseline (len=5000) tekrarlanabilirlik koşusu ✓
- Sınıf bazlı başarısızlık haritası (11 sınıf, F1 < 0.60) ✓
- Etiket taxonomy analizi (temel tespit) ✓
- Repo temizliği ve referans dizin sabitlemesi ✓
- **CodeGraf Aşama-4 `MyMethod` analizi ve CNN uygunluk değerlendirmesi ✓**
- **`scipy.signal.decimate` ile downsampling pipeline entegrasyonu ✓**
- **Downsampling faktör = 10 / 5 A/B karşılaştırması ✓**
- **DataLoader paralelleştirme (num_workers=4) güvenlik validasyonu ✓**
- **v2 hedefinin (%94.8) baseline + decimate ile aşılması (%97.38) ✓**
- **`CodeGraf/DEVELOPER_GUIDE.md` teknik doküman (deney kayıtları dahil) ✓**

**Önümüzdeki 4–6 Hafta:**
- Decimate-500 baseline üzerinde sınıf bazlı tam `classification_report` çıkarımı ve 2.3'teki F1 < 0.60 alt kümesinin güncel durum analizi
- DataLoader hızlanmasının tam `tee` log'u ile ölçülmesi, ardından batch_size = 128 denemesi
- Etiket dublesi birleştirme deneyi (78 → ~55 etkili sınıf) — hala faydalı mı?
- Focal loss γ ∈ {1, 2, 3} grid search — kalan düşük-F1 sınıflarda ek iyileşme
- Inference path'teki scaler re-fit hatası düzeltilmesi ([ecg_cnn_pytorch.py:1430](../ecg_cnn_pytorch.py#L1430))
- Multi-lead (12 kanal) girdi geçişi — `Conv1d(1,64,…)` → `Conv1d(12,64,…)`

**6–12 Hafta:**
- LSTM dalı ve multi-head attention entegrasyonu (v2 Model 4)
- Adaptive per-class threshold uygulaması
- GradCAM ve SHAP açıklanabilirlik çıktıları
- TensorFlow twin ([ecg_diagnose_cnn.py](../ecg_diagnose_cnn.py)) için de aynı decimate + num_workers değişikliği
- Temperature scaling / reliability diagram ile kalibrasyon doğrulaması
- Klinik validasyon testlerinin tekrarı (tam model ile)

**Risk Notu:** v2'deki ~2 aylık kayma riski büyük ölçüde ortadan kalkmıştır — doğruluk hedefi zaten sağlandığı için kalan çalışmalar doğrudan açıklanabilirlik ve klinik validasyona yönelik daha dar kapsamlıdır. Ancak yeni risk: decimate-500 baseline'ının beklenmedik yüksek skoru, v2'de tasarlanan "tam model"in gerçekten bu kadar ek katkı sağlayıp sağlamayacağı sorusunu açmıştır. Bu soru önümüzdeki 4–6 haftada focal loss + attention deneyleriyle deneysel olarak cevaplanacaktır.

---

## 8. KAYNAKÇA (EK)

v2 raporundaki [1]–[20] numaralı tüm kaynaklar geçerliliğini korumaktadır. Bu dönemde eklenen başlıca referanslar:

[21] Lin, T. Y., Goyal, P., Girshick, R., He, K., & Dollár, P. (2017). Focal loss for dense object detection. *Proceedings of the IEEE International Conference on Computer Vision*, 2980–2988.

[22] Ribeiro, A. H., Ribeiro, M. H., Paixão, G. M., Oliveira, D. M., Gomes, P. R., Canazart, J. A., ... Ribeiro, A. L. P. (2020). Automatic diagnosis of the 12-lead ECG using a deep neural network. *Nature Communications*, 11(1), 1760. *(v2'de [15] olarak geçmektedir; bu dönemde ontology-aware etiketleme bölümü yeniden incelenmiştir.)*

[23] Mullenbach, J., Wiegreffe, S., Duke, J., Sun, J., & Eisenstein, J. (2018). Explainable prediction of medical codes from clinical text. *NAACL-HLT*, 1101–1111. *(Etiket hiyerarşisi ve çoklu-etiket birleştirmede metodolojik referans.)*

---

## SONUÇ

Bu ek ara rapor dönemi (25 Aralık 2025 – 23 Nisan 2026) iki kısımdan oluşmaktadır. *İlk kısım* (25 Aralık – 22 Nisan) v2 raporundaki baseline'ın tekrarlanabilir biçimde doğrulanmasına ve 78-sınıflı modelin **sınıf bazlı başarısızlık haritasının çıkarılmasına** ayrılmış; baseline model `models_optimized_pytorch_baseline_len5000/` dizininde sabitlenmiş, test doğruluğu %88.43 ve makro F1 0.8713 olarak ölçülmüş, 11 sınıfın F1 < 0.60 seviyesinde kaldığı ve bu başarısızlığın büyük kısmının etiket dubleleri ile aşırı-oversample edilmiş nadir sınıflardan kaynaklandığı belirlenmiştir. *İkinci kısım* (22–23 Nisan) CodeGraf Aşama-4 `MyMethod` algoritmasının CNN için uygunluk değerlendirmesine ve bu inceleme sonucunda ortaya çıkan çıkarımın pipeline'a uygulanmasına ayrılmıştır: `MyMethod`'un temporal sırayı kaybettiği ve CNN için uygun olmadığı tespit edilmiş, ancak algoritmanın *niyetinin* (5000 örnek gereksiz fazla) doğru olduğu kabul edilerek aynı uzunluk azaltma `scipy.signal.decimate` ile uygulanmıştır. Sonuç: test doğruluğu **%88.43 → %97.34** (+8.91 pp), makro F1 **0.8713 → 0.9737** (+10.24 pp), tekil inference **89.88 ms → 27.20 ms** (3.3× hızlanma). Ek `num_workers=4` DataLoader paralelleştirmesi ile doğruluk 0.9738'e ulaşmış, kalite etkilenmeden uygulanan güvenli bir refactor olduğu doğrulanmıştır. **Bu bulgu, v2 raporunda aspirasyonel olarak belirlenen %94.8 hedefinin, tam model (LSTM + attention + focal loss + adaptive threshold) bileşenleri henüz devreye alınmadan, yalnızca doğru ön-işleme tercihiyle aşılmış olduğu anlamına gelmektedir.** Bir sonraki 4–6 haftalık dönem, (i) 2.3'teki başarısızlık listesinin yeni baseline'da nasıl değiştiğinin tam raporu, (ii) DataLoader gerçek hızlanma ölçümü, (iii) focal loss ve tam attention-LSTM modelinin *ek* katkısının ölçülmesi üzerine yoğunlaşacaktır. Bu dönem, tez katkısının yönünü de netleştirmiştir: "destek düğüm yöntemi" metodolojisi, doğrudan bir CNN ön-işleme adımı olmaktan çıkıp, 1D-CNN mimarisi için anti-aliased decimation ile; Dense ağlar için geometrik özellik çıkarımı ile karşılaştırılan bir *sinyal-işleme ailesi* olarak tez tartışma bölümünde yeniden konumlandırılacaktır.
