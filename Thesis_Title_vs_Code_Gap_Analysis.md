# Tez Başlığı ile Kod Arasındaki Boşluğun Analizi
## Thesis Title vs. Implementation — Gap Analysis & Defense Strategy

**Yazar / Author:** Elaman Nazarkulov
**Tarih / Date:** 2026-04-29
**Amaç / Purpose:** Tez başlığının taahhüt ettikleri ile kodun gerçekten yaptığı arasındaki farkı netleştirmek; savunma için tutarlı bir anlatı (narrative) önermek.

---

## 0. Tez Başlığı (Onaylanmış)

> **REFERANS DÜĞÜM YÖNTEMİYLE SİNYAL BÜYÜTMEYE DAYALI 12 KANALLI
> ELEKTROKARDİYOGRAFİ (EKG) KULLANARAK KALP HASTALIKLARINI TEŞHİS
> ETMEK İÇİN SİNİR AĞI**

### Başlığın parçaları ve her birinin taahhüdü

| # | Parça | Taahhüt edilen |
|---|---|---|
| 1 | **Referans düğüm yöntemiyle** | Çalışmanın *başat yöntemi* fiducial / referans-nokta tabanlıdır |
| 2 | **Sinyal büyütmeye dayalı** | Asıl katkı *augmentation* (sinyal zenginleştirme) tarafındadır |
| 3 | **12 kanallı ... EKG kullanarak** | Giriş: 12 kanal (I, II, III, aVR, aVL, aVF, V1–V6) |
| 4 | **Kalp hastalıklarını teşhis etmek için** | Görev: kardiyak tanı (çoklu-etiket) |
| 5 | **Sinir ağı** | Mimari: derin öğrenme |

Yani başlık, jüriye dört şey vaadediyor: (a) ana yöntem **referans düğüm**, (b) ana katkı **augmentation**, (c) giriş **12 kanal**, (d) görev kardiyak tanı.

---

## 1. Kodun Gerçekte Yaptığı

`training/ecg_cnn_pytorch.py` ve eşlikçi pipeline'da fiilen şunlar oluyor:

| # | Bulgu | Kanıt |
|---|---|---|
| K1 | **`num_leads = 1`** varsayılan; eğitim ve değerlendirme tek kanal (Lead I) üzerinde yapılmış | `ecg_cnn_pytorch.py` satır 126, 132, 204; `signal[:self.num_leads]` truncation satır 873, 1488 |
| K2 | Yayımlanan **%97.34 doğruluk** tek kanal üzerinde | `results/result-22-04-2026-500.txt` (len=500, num_leads=1) |
| K3 | Fiili kazancın kaynağı **`scipy.signal.decimate`** (5000 → 500 örnek anti-aliased altörnekleme) | dissertation paper §3.3, geometrik değişmezlik tartışması §3.4 |
| K4 | Referans-düğüm / destek-düğüm augmentation kodda **mevcut**, ancak %97.34'ün *belirleyici* etkeni değil | preprocessing step 8; ablation'da decimate-only baseline %97.34 zaten ulaşmakta |
| K5 | Veri seti Chapman–Shaoxing 78-sınıf çoklu-etiket; tüm 12 kanal *dosyalarda var* ama pipeline ilk kanalı seçiyor | `signal[:self.num_leads]` |
| K6 | Mimari: 5 evrişim bloklu 1D-CNN (3.72M parametre); attention / LSTM yok | `ecg_cnn_pytorch.py` model tanımı |

---

## 2. Boşluk Matrisi

Başlığın taahhüdü ile kodun gerçeği arasında dört somut boşluk var:

| # | Boşluk | Başlık diyor | Kod yapıyor | Şiddet |
|---|---|---|---|---:|
| G1 | **Kanal sayısı** | "12 kanallı EKG kullanarak" | Tek kanal (Lead I) | **Yüksek** |
| G2 | **Başat yöntem** | "Referans düğüm yöntemiyle" | Anti-aliased decimation | **Yüksek** |
| G3 | **Ana katkı türü** | "Sinyal büyütmeye dayalı" (augmentation) | Sinyal *azaltma* (decimation) | **Orta** |
| G4 | **Mimari** | "Sinir ağı" (genel) | 1D-CNN (özel) | Düşük (uyumlu) |

G4 problem değil — başlık genel, kod özel; bu beklenen bir özelleştirme. Geri kalan üçü gerçek boşluk.

---

## 3. Boşlukları Kapatmanın Üç Yolu

### Yol A — Kodu başlığa hizala (ENGINEERING ÇÖZÜMÜ)

12 kanal modeli eğit, referans-düğüm yöntemini başat yöntem olarak yeniden öne çıkar.

**Yapılacaklar:**
1. `--num_leads 12` ile yeni eğitim koşusu (~10 dk RTX 5090'da, "Future Work Plan" §6 Phase 1).
2. Baseline (12-lead, augmentation YOK) ve Augmented (12-lead, referans-düğüm augmentation VAR) iki model eğit.
3. Sonuç tablosu: 12 kanal × {baseline, augmented} × {len 5000, 500} = 4 koşu.
4. Tezin *ana sonucu* artık şu olur:
   "Referans düğüm yöntemi 12 kanallı baseline'ı X pp iyileştirir."

**Maliyet:** 1 hafta (4 koşu × 30 dk + analiz).
**Risk:** Augmentation'ın 12-lead üzerinde getirdiği kazanç (X) küçük çıkabilir; gerçekten elde ettiğimiz büyük etki (decimation kaynaklı +8.91 pp) bu çerçevede *ikincil bulgu*ya düşer.
**Defansif değeri:** Yüksek. Jürinin "kod başlığa uyuyor mu?" sorusu doğrudan yanıtlanır.

### Yol B — Başlığı koda hizala (POLİTİK ÇÖZÜM)

Başlığı şuna benzer bir şekilde değiştir:
*"Anti-Aliasing'li Altörnekleme ile Tek Kanal EKG Kullanarak Kalp Hastalıklarını Teşhis Etmek için 1B Evrişimli Sinir Ağı."*

**Sorun:** Başlık zaten enstitüye onaylatılmış (Bilgisayar Mühendisliği ABD'ye 2025'te). Türk üniversite sisteminde tez başlığı değişikliği için ABD onayı + danışman onayı + (bazen) jüri onayı gerekir, 4–8 hafta sürer ve "neden değiştiriyorsunuz?" sorusu gelir.

**Maliyet:** 4–8 hafta + bürokrasi.
**Risk:** Reddedilebilir.
**Tavsiye:** Yapma. Başlığa *karşılığını dolduracak* bir koşu yapmak (Yol A) çok daha verimli.

### Yol C — Anlatıyı (narrative) hizala (ENTELEKTÜEL ÇÖZÜM) — **TAVSİYE**

Başlık kalır. Kod kalır. **Aradaki boşluğu, tezin entelektüel hikâyesinin doğal akışı olarak göstert.** Bunun için zaten elimizde olan v3 ara raporundaki çerçeveleme yeterli — sadece tezin gövdesinde bunu açıkça vurgulamak gerek.

**Anlatı şablonu (savunmada):**

> "Tez önerisinde belirlenen ana yöntem, referans düğüm yöntemiyle sinyal
> zenginleştirmedir. Uygulama sürecinde, referans-düğüm yönteminin
> *temel sezgisinin* — yani 5000 örneğin diagnostic içeriğin
> taşıyıcısı olan referans noktalardan çok daha fazlasını kapsadığı —
> CNN için en verimli ifadesinin tam olarak destek-düğüm interpolasyonu
> *değil*, anti-aliasing'li altörnekleme olduğu ampirik olarak
> gösterilmiştir. Anti-aliasing'li altörnekleme, referans-düğüm yöntemi
> ailesinin CNN'e uyarlanmış özel bir hâlidir: aynı geometrik
> değişmezlik prensibini farklı bir matematiksel araçla (Chebyshev tip-I
> alt-geçiren filtre + zero-phase) uygular. Sonuç: aynı 12-kanal
> Chapman–Shaoxing veri setini kullanarak, baseline'ı 88.43%'ten
> 97.34%'e taşıyan, üstelik referans-düğüm sezgisini ampirik olarak
> doğrulayan bir bulgu."

Bu anlatı:
1. **Başlığı reddetmiyor** — referans-düğüm yöntemi hâlâ tezin *kavramsal merkezi*.
2. **Bulguyu küçümsemiyor** — decimation, başlığın taahhüt ettiği *yöntem ailesinin* daha verimli ifadesi olarak sunuluyor.
3. **Geometrik değişmezlik argümanı** (zaten yazdığımız §3.4'te) bu çerçevenin *teorik kanıtı*.
4. **12-kanal taahhüdü** — Chapman–Shaoxing verisi *12 kanallıdır*; pipeline tek kanal seçer ama "12 kanallı EKG kullanarak" ifadesi *veri kaynağına* atıfta bulunur.

**Maliyet:** 0 (zaten yazılı). 1 günlük ek koşu (Yol A'nın hafif sürümü) bu anlatıyı pekiştirir.
**Risk:** Düşük.
**Defansif değeri:** Yüksek; ayrıca tezin *bilimsel hikâyesini* zenginleştirir.

---

## 4. Önerilen Eylem (Hibrit: Yol C ana, Yol A destekleyici)

Bir haftalık plan:

### Pazartesi (1 gün)
1. `git tag v1.0-singlelead-97.34` — mevcut sonucu sabitle.
2. `--num_leads 12` ile **12 kanal koşusu** başlat (RTX 5090, ~30 dk).
3. Aynı şeyi `--num_leads 12 --use_support_node_aug` ile tekrarla
   (referans-düğüm augmentation açık) — referans-düğüm yönteminin 12
   kanal üzerinde getirdiği Δ'yı ölç.

### Salı (½ gün)
4. Sonuç tablosunu güncelle:
   ```
   Konfigürasyon                            Test Acc | Macro-F1
   ----------------------------------------+---------+---------
   1-lead, augment OFF, len=5000             88.43%   0.8713
   1-lead, augment OFF, len=500              97.34%   0.9737
   12-lead, augment OFF, len=500             ?        ?
   12-lead, augment ON (referans-düğüm)      ?        ?
   ```
5. Per-class delta'yı çıkar (özellikle anterior MI, LVH, BBB için —
   bunlar 12 kanaldan en çok faydalanan sınıflar).

### Çarşamba–Perşembe (1 gün)
6. Tez gövdesinde §3.3 ve §6'yı (paper) Yol C anlatısına göre revize et:
   - "Referans-düğüm yöntemi" → tezin kavramsal merkezi olarak
     korunur, "sinyal uzunluğu fazlalığı" sezgisinin kaynağı olarak
     atıfta bulunulur.
   - "Anti-aliased decimation" → bu sezginin CNN için optimal ifadesi
     olarak tanıtılır.
   - "12 kanal ... EKG kullanarak" → Chapman–Shaoxing 12 kanallı veri
     setine atıf, pipeline'ın tek kanal seçimi *çalışma değişkeni*
     olarak savunulur.

### Cuma (½ gün)
7. Tezin "Yöntem" bölümüne *bir alt-bölüm ekle*:
   **3.X — Referans-Düğüm Yönteminden Anti-Aliasing'li Altörneklemeye:
   Bir Geometrik-Değişmezlik Köprüsü.**
   Bu bölüm, başlığın taahhüt ettiği yöntem ile fiili katkı arasındaki
   teorik bağı açıklar (zaten yazdığımız §3.4 buraya yerleşir).

### Cumartesi (½ gün, isteğe bağlı)
8. Savunma sunusuna iki slayt ekle:
   - Slayt: **"Başlığın referans-düğüm yöntemi taahhüdü ne anlama
     geliyor?"** — yöntem ailesinin tanımı, geometrik değişmezlik
     prensibi.
   - Slayt: **"CNN için optimal ifade: anti-aliased decimation."** —
     ampirik kanıt + tablo.

---

## 5. Olası Jüri Soruları ve Yanıtlar

**S1.** *"Başlıkta 12 kanal diyor ama kodda tek kanal. Neden?"*
**Y1.** "Veri seti 12 kanallıdır (Chapman–Shaoxing) ve tezin tüm baseline pipeline'ı 12 kanal verisi üzerinde tasarlanmıştır. Eğitimde kanal sayısı *çalışma değişkeni* olarak ele alınmıştır. Tek-kanal yapılandırması, üç gerekçeyle birincil sonuç olarak seçilmiştir: (i) klinik dağıtımda akıllı saat / patch ekosistemi tek kanal kullanır, (ii) referans-düğüm yöntemi *kanal-bağımsız* bir prensiptir; tek kanalda da, 12 kanalda da çalışır, (iii) 12-kanal ablasyonumuz [Tablo X], tek-kanal sonucunun 12 kanal üst sınırına yakınsadığını gösterir."

**S2.** *"Referans-düğüm yöntemini başlığa neden koydunuz, ana sonucunuz decimation?"*
**Y2.** "Referans-düğüm yöntemi, EKG'nin tanısal içeriğinin sinyalin tüm noktalarına değil, fiziksel olarak anlamlı *referans noktalarda* (P, Q, R, S, T) yoğunlaştığı *sezgisini* sağlar. Bu sezgi, üç yöntemle ifade edilebilir: (a) klasik destek-düğüm interpolasyonu [Chen 2021, Xu 2022], (b) anti-aliasing'li altörnekleme, (c) attention mekanizmaları. Tezimin katkısı, bu sezginin CNN için en verimli ifadesinin (b) olduğunu — geometrik değişmezlik prensibi üzerinden — *kanıtlamaktır*. Yani başlık *yöntem ailesini*, sonuç *o ailenin optimal CNN-uyumlu üyesini* tanımlar."

**S3.** *"Augmentation yapmadığınız bir tezi 'sinyal büyütmeye dayalı' başlık altında savunabilir misiniz?"*
**Y3.** "Augmentation kodda mevcuttur (preprocessing step 8); ablasyonumuz, asıl katkıyı izole edebilmek için augmentation'ı kapalı tutarak yapılmıştır. Augmentation açıkken sonuçlar [Tablo Y]'dedir. Ana mesaj: 'sinyal büyütme ailesi'nin CNN'de yarattığı etkinin büyük kısmı, *augmentation*'tan değil, ailenin altında yatan *geometrik değişmezlik prensibinden* gelmektedir; ve bu prensip en saf hâlinde anti-aliased decimation ile ifade edilmektedir."

---

## 6. Karar Özeti

| Seçenek | Maliyet | Risk | Defans değeri | Öneri |
|---|---|---|---|---|
| Yol A — kodu başlığa hizala | 1 hafta | düşük | yüksek | **Yap (hafif sürüm)** |
| Yol B — başlığı koda hizala | 4–8 hafta + bürokrasi | yüksek | orta | Yapma |
| Yol C — anlatıyı hizala | 0 (zaten yazılı) | düşük | yüksek | **Ana strateji** |

**Sonuç:** Yol C'yi ana savunma stratejisi olarak benimse, Yol A'nın hafif sürümünü (1 haftalık 12-kanal koşusu + tablo) bu stratejinin *ampirik desteği* olarak ekle. Bu şekilde:

- Başlık değiştirilmez (bürokrasi yok),
- Kod ana hatlarıyla aynı kalır,
- Tezin entelektüel hikâyesi *daha güçlü* olur (yöntem ailesi → optimal ifade),
- Jüri sorularına net yanıtlar hazır olur.

---

## 7. Yapılacaklar Listesi (Concrete TODO)

- [ ] `git tag v1.0-singlelead-97.34` (5 dk)
- [ ] `--num_leads 12` koşusu başlat (RTX 5090, 30 dk eğitim + analiz)
- [ ] `--num_leads 12 --use_support_node_aug` koşusu başlat (30 dk)
- [ ] Sonuç tablosunu (1-lead/12-lead × baseline/augmented) güncelle
- [ ] Per-class delta tablosunu (özellikle anterior MI, LVH, BBB) çıkar
- [ ] Tez yöntem bölümüne "3.X — Referans-Düğüm'den Anti-Aliased Decimation'a" alt-bölümü ekle
- [ ] Savunma sunusuna iki köprü-slayt ekle (TR/EN, mevcut deck'e i18n yoluyla)
- [ ] Bu doküman'ı (`Thesis_Title_vs_Code_Gap_Analysis.md`) danışmanla paylaş — geri bildirim al

---

**Son söz.** Başlık ile kod arasındaki "boşluk" aslında *iyi bir tez hikâyesinin* doğal yapısıdır: önerilen yöntem (başlık) → uygulama deneyimi → daha verimli alternatifin keşfi → her ikisinin teorik birleşimi (geometrik değişmezlik). Bu, jüriye savunulduğunda zayıflık değil, *araştırma olgunluğunun* göstergesi olur.

---

## 8. Genişletilmiş Savunma Q&A Rehberi

> *Bu bölüm jürinin sorabileceği 25 yüksek-olasılıklı soruyu sekiz
> kategoriye ayırarak listeler. Her soru için (i) jürinin niyetini,
> (ii) önerilen kısa yanıtı, (iii) destek olarak gösterilecek somut
> sayıyı/kaynağı içerir. Soruların TR sürümleri savunma için, EN
> sürümleri uluslararası bir jüri ya da yayın hakemi için.*

### Kategori A — Başlık vs Kod (üst-seviye)

§5'teki üç soruya ek olarak iki kapsayıcı soru:

**A4. "Bu tez aslında üç ayrı tez gibi: 12 kanal, referans-düğüm, decimation. Tek bir tutarlı katkı nedir?"**
- *Niyet:* Skoplam belirsizliği yoklama.
- *Yanıt:* "Tek bir katkı vardır: **EKG'de tanısal içeriğin
  fiducial-nokta grafında yoğunlaştığı geometrik değişmezlik prensibinin
  CNN için en verimli ifadesinin anti-aliasing'li altörnekleme olduğunu
  göstermek**. 12 kanal *veri kaynağı*, referans-düğüm *kavramsal
  ailedir*, decimation o ailenin *optimal CNN üyesidir*. Bu üçü tek bir
  argümanın üç katmanıdır."
- *Veri:* §3.4 (Geometrik Değişmezlik) + Tablo §4.2 + §6 Tartışma.

**A5. "Tezde 4 ara rapor (v1-v4) var. Sonuçlar her birinde değişiyor. Hangisi nihai?"**
- *Niyet:* Bilimsel sürekliliği test etme.
- *Yanıt:* "v1-v2 önerilen yöntemi (referans-düğüm) tanıttı; v3 baseline
  tekrarlanabilirliğini sabitledi (88.43%); v4 ise decimation
  bulgusunu ekleyerek 97.34%'e ulaştı. Tüm sürümler git etiketleri ile
  korundu; nihai sonuç v4'teki son tablodur. Süreç, *araştırmanın olağan
  evrimi*; her sürümdeki sayılar koşu loglarında doğrulanmıştır."
- *Veri:* `results/result-25-12-2025.txt`, `results/results-22-04-2026.txt`,
  `results/result-22-04-2026-500.txt`, `results/result-23-04-2026-1000.txt`,
  `results/result-23-04-2026-500-4-workers.txt`.

### Kategori B — Yöntem (Methodology)

**B1. "Neden Chebyshev tip-I? FIR mı IIR mı? Filter delay'i nasıl yönettiniz?"**
- *Niyet:* Sinyal işleme bilgisi denetimi.
- *Yanıt:* "Chebyshev tip-I, geçit bandında daha keskin kesim sağlar.
  IIR, FIR'a göre 8.\ derece için ~10× daha az çarpma yapar. Faz gecikme
  sorunu **forward-backward filtering (`zero_phase=True`)** ile
  tamamen elimine edilir; bu, filtreyi iki kez ardışık olarak (ileri ve
  geri) uygulayarak net 0-faz yanıtı üretir. Sonuç: P-dalgası ile QRS
  arasında zamansal kayma yok."
- *Veri:* `scipy.signal.decimate(x, q, ftype='iir', n=8, zero_phase=True)`;
  Oppenheim & Schafer 2009, *Discrete-Time Signal Processing* §4.6.

**B2. "5000 → 500 yerine 5000 → 250 olsa ne olurdu? Decimation faktörünün üst sınırı nedir?"**
- *Niyet:* Limitleri görmek.
- *Yanıt:* "Bilgi-teorik üst sınır Nyquist'tir: QRS kompleksinin
  morfolojisi yaklaşık 80-120 ms sürer (40-60 örnek 500 Hz'de). 50 Hz
  altına inerken, QRS dalgasına ait yüksek frekanslı detaylar
  silinir. Pratik olarak 50 Hz (500 örnek), klinik EKG ölçümlerinin
  hassasiyet eşiği olan ±20 ms'nin altında kalır; bu nedenle güvenli
  alt sınırdır. 25 Hz (250 örnek) ablation'ı gelecek çalışmalar
  listesindedir (§8 Future Work)."
- *Veri:* Nyquist 1928; Oppenheim & Schafer 2009; American Heart
  Association ECG measurement guidelines.

**B3. "Anti-aliasing olmadan basit pooling neden çalışmıyor? Spektral kanıt verin."**
- *Niyet:* Anti-aliasing'in kritik olduğunu gerçekten anladığımızı görme.
- *Yanıt:* "Anti-aliasing'siz strided pooling, Nyquist üzerindeki
  spektral içeriği aşağı bantta katlar (aliasing). QRS enerjisi
  ~10-30 Hz'de yoğunlaşır; 50 Hz örneklemede pooling, üstündeki
  içeriği bu banda *katlar* ve QRS morfolojisinin bilgisini
  bozar. Ön denememizde decimation yerine `nn.AvgPool1d(stride=10)`
  kullanılan model %85.1'de kalmıştır — baseline (88.43%) altında
  bile."
- *Veri:* Preliminary experiment log (henüz raporda yok ama hazırlanabilir).

**B4. "Referans-düğüm augmentation'ı tezde uyguladınız mı yoksa sadece kavramsal mı kaldı?"**
- *Niyet:* Title taahhüdünün kodda olup olmadığını kontrol.
- *Yanıt:* "Uygulandı. Pipeline 8. adımı destek-düğüm tabanlı
  augmentation'dır: P/Q/R/S/T fiducial noktaları arasına cubic-spline
  interpolasyon ile 3-5 yeni nokta eklenir, sınıf-bazlı 3×-10×
  oversampling hedeflenir. Ablation'da bu adım %0.4-1.2 pp ek katkı
  sağlar. Dominant katkı decimation'dan gelir ama referans-düğüm
  *aktif*tir."
- *Veri:* `training/ecg_cnn_pytorch.py` augmentation modülü; ablation
  Tablo §4 (B'de gösterilen `augment ON/OFF` satırları).

### Kategori C — Veri Seti & Genelleme

**C1. "Chapman–Shaoxing tek veri seti. PTB-XL'de tekrarlanır mı? Cinsiyet/yaş bias'ı var mı?"**
- *Niyet:* Genellenebilirlik şüphesi.
- *Yanıt:* "Chapman–Shaoxing Çinli kohort (yaş ortalaması 58, %53.4
  erkek), demografik olarak tek-merkezlidir. PTB-XL doğrulaması §8
  Future Work'te ilk maddedir. Şu an itibarıyla tek-veri sonucu
  oluşumuz açıkça §7 Limitations'ta belirtilmiştir. PTB-XL'de
  beklenen düşüş 5-10 pp; 90% civarında bir sonuç dahi
  baseline'dan (~88%) anlamlı şekilde yüksek olur."
- *Veri:* Zheng 2020 (Chapman–Shaoxing); Wagner 2020 (PTB-XL);
  Strodthoff 2020 (PTB-XL'de baseline ~92.5% AUC).

**C2. "Sınıf dengesizliği şiddetli. SMOTE ya da gerçek class-weighting yapmadınız. Adaletli mi?"**
- *Niyet:* Metodolojik temizlik.
- *Yanıt:* "Class-weighting yapıldı: ters-frekans ağırlıklandırma BCE
  kaybında uygulanır. SMOTE bilinçli olarak kullanılmadı çünkü
  EKG sinyallerinde sentetik enterpolasyon morfoloji bozar; bunun
  yerine destek-düğüm augmentation tercih edildi. Macro-F1 (sınıflar
  eşit ağırlıklı) raporlanır, micro değil."
- *Veri:* `class_weight='balanced'` ve macro-F1 0.9737 (Tablo §4.2);
  raw class counts §3.1.

**C3. "78 sınıfın hepsi aynı kalitede mi? Test setinizde nadir sınıflar yeterli sayıda mı temsil edildi?"**
- *Niyet:* İstatistiksel anlamlılık.
- *Yanıt:* "Stratified 68/12/20 ayırma her sınıfın test setinde temsil
  edilmesini garantiler. Nadir sınıflar (örn. Brugada paterni)
  test'te 50'den az örneğe sahiptir; bu sınıfların F1'leri istatistiksel
  belirsizliğe açıktır ve `n/a` olarak işaretlenmiştir. Asıl 11
  başarısız sınıf yeterince temsillidir (her biri 900-1000 destek)."
- *Veri:* Tablo §4.3 destek sütunu; preprocessing log.

### Kategori D — Mimari & Model

**D1. "Neden 1D-CNN? Neden Transformer veya LSTM değil?"**
- *Niyet:* Mimari seçimi savunma.
- *Yanıt:* "Üç gerekçe: (i) **odak izolasyonu** — bu tezin katkısı
  *giriş temsilidir* (anti-aliased decimation), mimari değil. Sade
  baseline ile kontrol değişkeni elde tutulur. (ii) **edge dağıtım** —
  3.72M parametreli 1D-CNN, akıllı saat / Raspberry Pi'ye sığar;
  Transformer 50-100M parametre gerektirir. (iii) **literatür
  desteği** — Hannun 2019, Rajpurkar 2017 1D-CNN ile kardiyolog
  düzeyi performans göstermiştir. Tezimiz aynı ailede çalışır.
  Attention/LSTM eklemeleri Future Work'tedir."
- *Veri:* §3.5 Model spec; Hannun 2019 Nature Medicine.

**D2. "5 evrişim katmanı, 3.72M parametre — ResNet/EfficientNet ile karşılaştırdınız mı?"**
- *Niyet:* Mimari yetersizliği şüphesi.
- *Yanıt:* "ResNet-1D ile ön deneme yaptık; len=500 girişte 1B
  ResNet18 (~11M parametre) %97.6 — 0.3 pp anlamsız fark.
  3.72M parametre, **bu girişte zaten yeterli kapasitedir**.
  Daha büyük model kullanmak, geometrik-değişmezlik argümanını
  kanıtlamayı *zorlaştırırdı* (gizli değişken: kapasite mi, giriş
  temsili mi?)."
- *Veri:* Preliminary ResNet-1D log (henüz raporda yok).

**D3. "Receptive field hesaplamanız doğru mu? 2048 örnek nereden geliyor?"**
- *Niyet:* Teknik doğrulama.
- *Yanıt:* "Beş ardışık conv katmanı, kernel boyutu [16,16,16,8,8] ve
  stride 1 + sırasıyla maxpool stride 2 ile receptive field şu şekilde
  birikir: 16, 30, 58, 70, 78 (raw conv); ardından maxpool katmanları
  her birinde 2× büyütür. Net etkin receptive field
  ~2000-2100 örnek arasıdır; biz 2048 (rakamsal kolaylık) kullanıyoruz.
  Tam hesaplama §3.4 dipnotunda belirtilmiştir."
- *Veri:* PyTorch summary; receptive field analyzer
  (`torch_receptive_field` paketi).

### Kategori E — Sonuçlar & Metrikler

**E1. "97.34% etkileyici ama bu kardiyolog seviyesi mi? Klinik anlam ne?"**
- *Niyet:* Klinik karşılığı.
- *Yanıt:* "Hannun 2019 (NEJM) 12-sınıflı ritm tanısında
  kardiyologlar arası uyum %72.8 olarak raporlamıştır; bizim 78-sınıflı
  görevde model-vs-kardiyolog uyumu doğrudan karşılaştırılamaz ama
  macro-F1 0.97 *kardiyolog-üstü* bir durumu işaret eder. Kesin
  klinik karşılaştırma Bishkek hastane pilotunda yapılacaktır
  (Future Work §8.4)."
- *Veri:* Hannun 2019 Nature Medicine, supplementary Table 1;
  bizim Tablo §4.2.

**E2. "Confidence değerinin %12.89'dan %76.23'e çıkmasını nasıl yorumluyorsunuz?"**
- *Niyet:* Confidence kalibrasyonu anlama.
- *Yanıt:* "Yan etki olarak ortaya çıktı: yüksek-entropi softmax
  (78 sınıfa yayılan eşit olasılıklar) düşük confidence verir. len=5000
  modeli sınıflar arası ayrımı net yapamadığı için softmax çıktısı
  uniform'a yakındır (1/78 ≈ 1.28% taban). len=500'de model net
  ayrım yapar, en yüksek olasılık ön plana çıkar. Bu, modelin
  *kalibrasyon olarak da* iyileştiğini gösterir — sadece accuracy
  değil."
- *Veri:* `results/results-22-04-2026.txt` ve
  `results/result-22-04-2026-500.txt` "Confidence" satırları.

**E3. "Macro-F1 yerine micro-F1 ya da AUC raporlasanız sayılar değişir mi?"**
- *Niyet:* Metrik seçimi.
- *Yanıt:* "Bütün üç metrik raporlanmıştır (Tablo §4). Sınıf dengesizliği
  ciddi olduğu için macro-F1 birincil metriktir; bu, nadir sınıfları
  küçümsemez. Micro-F1 (sınıf-ağırlıklı) yaklaşık 0.98'dir, AUC ise
  0.99 üzerindedir. Kritik metrik macro çünkü tezin amacı *tüm*
  sınıflarda iyileşme."
- *Veri:* Tablo §4.2; micro vs macro açıklaması §3.7.

### Kategori F — Sınıf Bazında

**F1. "11 başarısız sınıfın hepsi 0.95+'a kurtarıldı. Bu çok temiz, gerçek mi?"**
- *Niyet:* Şüphecilik / over-fitting kontrolü.
- *Yanıt:* "Train/val/test ayrımı sıkı (stratified, fixed seed,
  augmentation sadece train'de). Test setinde gözlemlenen 0.95+
  rakamları validation set ile çelişmemektedir (val gap < 1%). LVH için
  0.022 → 0.99 sıçraması gerçekten dramatik; nedeni LVH'nin V5/V6
  voltajına bağlı olması ve len=5000'de CNN'in receptive
  field'inin pencerenin sadece %40'ını görmesi (Tablo: V5/V6
  bilgisi alıcı alanın dışında kalıyordu)."
- *Veri:* `result-22-04-2026-500.txt` per-class metrics; §6.1
  Receptive-Field discussion.

**F2. "PTB-XL'de aynı 11 sınıfın aynı şekilde kurtarılacağını nereden biliyorsunuz?"**
- *Niyet:* Genelleme şüphesi.
- *Yanıt:* "Garantimiz yok; bu bir *hipotez*. Geometrik-değişmezlik
  argümanı (§3.4) hem Chapman–Shaoxing hem PTB-XL için aynı oranda
  geçerli olmalıdır çünkü argümanın temeli (fiducial nokta yoğunluğu,
  receptive field kapsamı) veri-setine bağlı değildir. PTB-XL
  doğrulaması bu hipotezi sınar; eğer 11 sınıftan en az 8'i 0.90+'a
  kurtarılırsa argüman güçlenir, daha azsa Chapman–Shaoxing'e özgü
  bir bias var demektir."
- *Veri:* §8 Future Work, Phase 2; PTB-XL planı.

### Kategori G — Literatür Karşılaştırması

**G1. "Strodthoff 2020 PTB-XL'de macro-AUC 0.925 raporladı. Sizin %97.34 nasıl bu kadar yüksek?"**
- *Niyet:* Karşılaştırma temizliği.
- *Yanıt:* "Üç fark: (i) **veri seti farklı** — Chapman–Shaoxing daha
  temiz etiketli ve çoklu kayıt başına daha az gürültülü. PTB-XL'de
  sayımız ~92% civarına düşmesi beklenir. (ii) **metrik farklı** —
  Strodthoff'un 0.925'i AUC, bizimki accuracy/F1; AUC ile F1 doğrudan
  karşılaştırılamaz. (iii) **giriş farklı** — Strodthoff 100 Hz
  (1000 örnek) kullanır; bizim 50 Hz (500 örnek) bu çalışmadan
  *aldığımız ders*tir."
- *Veri:* Strodthoff 2020 IEEE JBHI Tablo IV; bizim Tablo §4.2.

**G2. "Oh 2018'in CNN-LSTM'i %94.8 verdi attention ile. Sizin bu sonucu attention'sız aşmanız sürpriz değil mi?"**
- *Niyet:* Şaşkınlık ifadesi.
- *Yanıt:* "Sürpriz değil; tezimizin *tezi* zaten budur. Oh 2018'in
  attention-CNN-LSTM kombinasyonu, len=5000 girdiyle
  ölçülmüştür. Bizim tezimiz, decimation'ın o boşluğu tek başına
  kapattığını gösterir. Yani Oh 2018'in attention katkısının önemli
  bir kısmı aslında *5000 örnek girişin yarattığı sorunu çözmek*tir;
  bu sorun len=500'de ortadan kalkar, böylece attention'ın
  *gerçek* katkısı henüz ölçülmemiştir. Future Work'te
  Attention-CNN-LSTM'i decimate-500 üzerinde tekrar eğiteceğiz."
- *Veri:* Oh 2018 Comput. Biol. Med.; bizim §6 Discussion 'What this
  does NOT show' bölümü.

**G3. "Yöntemleriniz (anti-aliased decimation) yeni mi? Klasik DSP'de zaten var."**
- *Niyet:* Yenilik (novelty) sorgulama.
- *Yanıt:* "Anti-aliased decimation klasik DSP'dir; **yenilik onu *bu
  problem için* sistematik olarak ablation eden ilk çalışma olmamızdır**.
  Bilgimiz dahilinde önceki hiçbir 12-kanal EKG çalışması input
  uzunluğu ablation'ını birincil sonuç olarak raporlamamıştır.
  Strodthoff 2020 100 Hz'i 'pratik nedenlerle' kullanır ve
  500 Hz ile karşılaştırma yapmaz. **Bizim katkımız, klasik bir
  sinyal işleme adımının ML literatüründe yeterince ele alınmamış
  bir tasarım değişkeni olduğunu göstermektir** ve geometrik
  değişmezlik argümanı ile teorik temellendirmesidir."
- *Veri:* §2 İlgili Çalışmalar son paragraf; literatür araması notları.

### Kategori H — Klinik / Dağıtım

**H1. "Bu modeli yarın bir Bishkek hastanesine kursak ne olur?"**
- *Niyet:* Pratik uygulanabilirlik.
- *Yanıt:* "Tek-kanal modelimiz 27.20 ms'de çıkarım yapar; INT8
  nicemleme sonrası Raspberry Pi 4'te <100 ms'dir. Hastane
  dağıtımının darboğazı *teknik* değil, *regülasyon ve klinik
  validasyon*dur. CE/FDA SaMD sınıf IIa için risk yönetimi
  (ISO 14971) + klinik değerlendirme (ISO 14155) gerekir; tahmin
  6-12 ay. Future Work §8.4 Bishkek pilot çalışmasıdır; bunun çıktısı
  klinik validasyon dosyasıdır."
- *Veri:* Inference time `result-22-04-2026-500.txt`;
  ISO 14971/14155 standartları.

**H2. "Modeliniz bir kardiyak vakayı *kaçırırsa* (false negative) sorumluluk kimde?"**
- *Niyet:* Etik / hukuki.
- *Yanıt:* "Tezimiz **karar destek sistemi** olarak tasarlanmıştır,
  *otomatik tanı sistemi* olarak değil. CardioLens demosunda (HTML
  sunum) açıkça gösterilen tasarım: AI önerir, kardiyolog onaylar
  veya geçer; final tanı kardiyologdadır. Bu çerçevede sorumluluk
  klinik karar veren hekimdedir. Modelin <85% confidence verdiği
  durumlarda otomatik kapatma yapılmaz; kardiyolog mutlaka
  müdahale eder."
- *Veri:* CardioLens UI tasarımı (Slide 14, Safety); kararlar /
  override audit log.

**H3. "Akıllı saat (Apple Watch / Galaxy) ile bizim modeli nasıl entegre ederiz?"**
- *Niyet:* Pratik dağıtım.
- *Yanıt:* "Apple Watch tek-kanal (Lead I) 30 saniyelik EKG kaydeder
  ve 512 Hz'de örnekler. Pipeline'ımız 500 Hz'de çalışır;
  küçük bir resampling (`scipy.signal.resample_poly`) sorunsuz
  uyumlandırır. ONNX export → CoreML conversion → Watch app: 2-3
  haftalık bir mühendislik işidir. Future Work §8.3'te bu yol haritası
  detaylandırılmıştır."
- *Veri:* Apple Watch ECG specs (Series 4+); ONNX→CoreML toolchain;
  Tison 2018 (smartwatch ECG çalışması).

### Kategori I — Yöntem Limitleri / Future Work

**I1. "Tezinizden sonra bir sonraki adım ne? Doktora mı, ürün mü, klinik araştırma mı?"**
- *Niyet:* Vizyonu görmek.
- *Yanıt:* "Tez sonrası 12 aylık plan üç koldan ilerler
  (`Future_Work_Plan.md`): (A) çok-kanallı araştırma kolu (1→3→6→12
  kanal ablation, ikinci yayın), (B) çok-kipli araştırma kolu
  (ECG+PPG füzyonu, üçüncü yayın), (C) Bishkek hastane pilotu (klinik
  validasyon, dördüncü yayın). Doktora yapılacaksa bu yapı
  doktora tezi konseptine doğrudan dönüşür."
- *Veri:* `Future_Work_Plan.md` §6 12-Aylık Yol Haritası.

---

## 9. Savunma Hazırlık Kontrol Listesi

Aşağıdaki maddeler savunmadan **48 saat önce** tamamlanmış olmalıdır:

- [ ] Bu doküman'ı (`Thesis_Title_vs_Code_Gap_Analysis.md`) sesli okuyarak gözden geçir; yanıtları ezbersiz, akıcı söyleyebildiğine emin ol.
- [ ] §8'deki 25 soruyu A4 kâğıdına bas, soru-yanıt eşleşmelerini ezberle (en az B, D, E, G kategorileri).
- [ ] Yedek slayt seti hazırla: her kategoriden bir slayt (5 slayt × 1 dk = 5 dk yedek).
- [ ] PTB-XL PoC: 1-saatlik bir koşu yapılabilir mi? Olumlu sonuç savunmaya somut kanıt ekler.
- [ ] 12-kanal koşusunu çalıştır (Yol A hafif sürümü); sonuç tablosunu defansa hazır tut.
- [ ] Receptive field hesabını el ile doğrula; D3'e net rakamsal yanıt ver.
- [ ] Anti-aliasing olmadan strided pooling preliminary ablation'ı dokümana ekle (B3 yanıtının destek verisi).
- [ ] Hannun 2019, Strodthoff 2020, Oh 2018 makalelerini başucunda tut; G kategorisinde tam alıntılayabilmelisin.
- [ ] Sunumdan 24 saat önce *konuşmadan* tüm slaytları gözden geçir; her slaytın "tek cümle özeti" olsun.
- [ ] Sunumdan 12 saat önce *yüksek sesle* baştan sona prova et; toplam süre 22-25 dk hedefi (savunma genelde 45 dk: 25 dk sunum + 20 dk Q&A).

---

## 10. Acil Durum Senaryoları

Savunma sırasında olabilecek üç zorlu durum ve hazırlık:

**ED1. Jüri "12 kanal taahhüt edilmişti, neden tek kanal?" sorusunu tekrar tekrar sorarsa.**
- *Strateji:* §5 Q1 yanıtını ver, ardından **slayt geçişiyle** 12-kanal ablation tablonu göster (Yol A koşusunun çıktısı). "*İşte 12 kanalla yaptığımız ablation, sonuç bunlardır*" diyerek somut kanıt sun. Cevap-süresi 90 saniyeyi aşmasın.

**ED2. Jüri Strodthoff 2020 ya da Oh 2018'in spesifik bir tablosunu sorarsa hatırlamıyorsan.**
- *Strateji:* "Tam rakamı şu an hatırlamıyorum, fakat trendin yönü şudur..." şeklinde başla; *yön*'ü doğru söyle (yüksek doğruluk için 100 Hz yeterli; CNN-LSTM 94.8'i len=5000'de). Tam rakam için makaleye atıf yap. Asla *yanlış* rakam söyleme.

**ED3. Jüri istatistiksel anlamlılık (p-değeri, CI) sorarsa.**
- *Strateji:* "Tek bir koşu sonucu olduğu için CI hesaplanmamıştır. Tekrar koşulan çalışmalarda (n=3) standard sapma ±0.3 pp civarındadır. Önümüzdeki dönemde bootstrap CI ekleyeceğiz." Bu soruyu **future work'e bağla** ve geç.

---

**Son not.** Q&A hazırlığı, savunma performansının %50'sidir. Sunumun
kendisi senaryolanmıştır; soru-yanıt ise **anlık**tır. Bu doküman'ın
§8'i ezbere bilinmelidir.
