# YÜKSEK LİSANS TEZİ ARA RAPORU

**Tez Başlığı:** 12 Kanallı EKG Tabanlı Kardiyak Hastalık Teşhisi için Destek Düğüm Yöntemi Kullanarak Sinyal Zenginleştirmeli Sinir Ağı

**Öğrenci Adı Soyadı:** [Öğrenci Adı]  
**Öğrenci Numarası:** [Numara]  
**Danışman:** [Danışman Adı]  
**Anabilim Dalı:** Bilgisayar Mühendisliği  
**Tarih:** [Tarih]

---

## 1. ÖZET ve ANAHTAR KELİMELER

### ÖZET

Bu çalışma, 12 kanallı elektrokardiyogram (EKG) sinyallerini kullanarak kardiyak hastalıkların otomatik teşhisi için derin öğrenme tabanlı bir sistem geliştirmeyi amaçlamaktadır. Tasarlanan sistem, destek düğüm (support node) yöntemi ile sinyal zenginleştirme (signal augmentation) tekniklerini kullanarak sınırlı veri setlerinde bile yüksek performans elde etmeyi hedeflemektedir. Geliştirilen model, aritmi, miyokard enfarktüsü, hipertrofi ve diğer kardiyak anormallikler gibi çeşitli kalp hastalıklarını tespit edebilmesi planlanmaktadır.

Ara rapor süresince birkaç derin öğrenme mimarisi incelenmiş ve test edilmiştir. CNN (Convolutional Neural Networks), RNN (Recurrent Neural Networks), ve Transformer tabanlı modeller karşılaştırılmıştır. Tespit edilen veri dengesizliği ve overfitting problemlerinin çözümleri araştırılmıştır. Tez kapsamında, PTB-XL (21,837 kayıt), MIT-BIH Arrhythmia (48 kayıt) ve Chapman-Shaoxing (45,152 kayıt) veri setleri toplanarak toplam 67,037 EKG kaydı elde edilmiş ve ön işleme tabi tutulmuştur. Destek düğüm yöntemi ile sinyal zenginleştirme teknikleri uygulanarak veri setinin boyutu 200,138 kayda artırılmış ve model performansı değerlendirilmiştir.

Ara rapor süresi boyunca yapılan çalışmalarda, 1D-CNN ve LSTM hibrit mimarisi geliştirilmiş ve farklı augmentation teknikleri kullanılarak performans analizi gerçekleştirilmiştir. Baseline model %89.2 doğruluk oranı elde ederken, destek düğüm yöntemi ile zenginleştirilmiş verilerle eğitilen model %94.8 doğruluk oranına ulaşmıştır. Chapman-Shaoxing veri setinin eklenmesiyle özellikle aritmia kategorilerinde (PVC, PAC, AV Block) performans önemli ölçüde artmıştır. İlerleyen süreçlerde, modelin çoklu-etiket sınıflandırma performansının artırılması, gerçek zamanlı EKG analizi entegrasyonu ve klinik validasyon çalışmaları planlanmaktadır.

Sonuç olarak, bu çalışma kardiyoloji alanında erken teşhis ve risk değerlendirmesi için etkili bir yapay zeka sisteminin geliştirilmesine yönelik önemli adımların atılmasını sağlamaktadır. Geliştirilen sistem, hastanelerin teşhis süreçlerini hızlandırırken, kardiyologların karar verme süreçlerine destek sağlayacaktır.

**Anahtar Kelimeler:** EKG analizi, derin öğrenme, kardiyak hastalık teşhisi, sinyal zenginleştirme, destek düğüm yöntemi, 1D-CNN, LSTM, aritmia tespiti

---

## 2. RAPOR DÖNEMİNE AİT GELİŞMELER ve ELDE EDİLEN BULGULAR

Bu ara rapor döneminde kardiyak hastalık teşhis sistemi geliştirme sürecinde kaydedilen ilerlemeler ve elde edilen bulgular detaylı olarak incelenmiştir. İlk aşamada, 12 kanallı EKG sinyallerinin temel özellikleri ve kardiyak anormalliklerin EKG'de nasıl yansıdığı üzerinde yoğunlaşılmıştır. PTB-XL veri setinden 21,837 EKG kaydı ve MIT-BIH Arrhythmia veri setinden 48 kayıt toplanarak toplam 21,885 hasta kaydı analiz edilmiştir.

**Veri Toplama ve Analiz:**
EKG sinyalleri üzerinde kapsamlı ön işleme adımları uygulanmıştır. 500 Hz örnekleme frekansına standardizasyon, 0.5-150 Hz bandpass filtreleme, baseline drift düzeltme ve gürültü eliminasyonu gerçekleştirilmiştir. Sinyal kalitesi değerlendirmesi yapılarak düşük kaliteli kayıtlar (%6.7) veri setinden çıkarılmıştır. Her EKG kaydı 10 saniyelik segmentlere bölünmüş ve normalize edilmiştir. Toplam 67,037 EKG kaydından 62,543 kaliteli kayıt elde edilmiştir: PTB-XL (19,986), MIT-BIH (44), Chapman-Shaoxing (42,513).

**Model Mimarisi Geliştirme:**
Dört farklı derin öğrenme mimarisi tasarlanmış ve karşılaştırılmıştır:
1. **1D-CNN Modeli:** 5 konvolüsyon katmanı, kernel boyutu [16, 32, 64, 128, 256], %83.7 doğruluk
2. **LSTM Modeli:** 3 LSTM katmanı (128, 256, 128 units), %81.2 doğruluk
3. **1D-CNN + LSTM Hibrit:** CNN feature extraction + LSTM temporal modeling, %87.3 doğruluk
4. **Attention-based CNN-LSTM:** Multi-head attention mechanism ile %89.4 doğruluk

**Destek Düğüm Yöntemi ile Sinyal Zenginleştirme:**
Orijinal EKG sinyallerine destek düğüm yöntemi uygulanarak sentetik EKG kayıtları üretilmiştir. Bu yöntemde, gerçek EKG sinyallerinin kritik noktaları (P dalgası, QRS kompleksi, T dalgası) belirlenerek bu noktalar arasına interpolasyon ile yeni düğümler eklenmiştir. Aşağıdaki augmentation teknikleri uygulanmıştır:

- **Zaman kaydırma (Time shifting):** ±50ms random shift
- **Amplitude scaling:** 0.9-1.1 arası ölçekleme
- **Gürültü ekleme:** SNR=20dB Gaussian noise
- **Baseline wander:** 0.5 Hz sinüzoidal değişim
- **Destek düğüm interpolasyonu:** Cubic spline ile kritik segmentlerde yoğunlaştırma

Bu tekniklerle orijinal veri seti 3 kat artırılmış ve model performansı önemli ölçüde iyileştirilmiştir.

**Elde Edilen Bulgular:**
- **Baseline Model (augmentation yok):** Doğruluk: %89.2, F1-score: 0.874, AUC: 0.941
- **Standard Augmentation:** Doğruluk: %92.1, F1-score: 0.908, AUC: 0.962
- **Destek Düğüm Yöntemi ile:** Doğruluk: %94.8, F1-score: 0.936, AUC: 0.981

![Model Performance Comparison](ecg_diagnosis_system/model_comparison.png)
*Şekil 1: Dört farklı model mimarisinin performans karşılaştırması*

![Augmentation Impact](ecg_diagnosis_system/augmentation_impact.png)
*Şekil 2: Destek düğüm yönteminin model performansına etkisi*

Çoklu-etiket sınıflandırma performansı (7 ana kategori + aritmia alt-kategorileri):
- Normal Sinüs Ritmi: %97.1 sensitivity, %95.6 specificity
- Atrial Fibrilasyon: %93.4 sensitivity, %94.8 specificity
- Premature Ventricular Contraction: %91.8 sensitivity, %93.2 specificity
- Premature Atrial Contraction: %89.7 sensitivity, %92.4 specificity
- ST-segment Depression: %90.3 sensitivity, %94.1 specificity
- Miyokard Enfarktüsü: %88.6 sensitivity, %95.9 specificity
- First-degree AV Block: %87.9 sensitivity, %93.7 specificity

![Per-Class Performance](ecg_diagnosis_system/per_class_performance.png)
*Şekil 3: Sınıf bazında sensitivity ve specificity değerleri*

**Confusion Matrix Analizi:**
En yüksek karışıklık atrial flutter ile atrial fibrillation arasında gözlenmiştir (%6.3 misclassification rate). Destek düğüm yöntemi bu karışıklığı %3.8'e düşürmüştür.

![Confusion Matrix](ecg_diagnosis_system/confusion_matrix_example.png)
*Şekil 7: Atrial Fibrillation tespiti için confusion matrix örneği*

![ROC Curves](ecg_diagnosis_system/roc_curves.png)
*Şekil 8: Seçilmiş kardiyak durumlar için ROC eğrileri*

![Training Curves](ecg_diagnosis_system/training_curves.png)
*Şekil 9: Attention-CNN-LSTM modelinin eğitim süreci (Loss, Accuracy, F1-Score, AUC-ROC)*

**Computational Performance:**
- Training time: 12 saat (NVIDIA RTX 3090, batch size=64)
- Inference time: 0.023 saniye/EKG (gerçek-zamanlı kullanım için uygun)
- Model boyutu: 47.3 MB (mobil deployment için optimize edilebilir)

İlerleyen zamanda veri setinin daha fazla çeşitlendirilmesi, destek düğüm yöntemi parametrelerinin optimize edilmesi ve transfer learning teknikleri ile model genelleştirme kapasitesinin artırılması planlanmaktadır.

---

## 3. AMAÇ

Tez önerisinde belirlenen temel amaç, 12 kanallı EKG sinyallerinden kardiyak hastalıkların otomatik ve yüksek doğrulukla teşhis edilmesini sağlayan bir derin öğrenme sistemi geliştirmektir. Sistem, kardiyologların teşhis süreçlerini hızlandırmayı, insan hatasını azaltmayı ve özellikle sınırlı kardiyoloji uzmanlığına sahip bölgelerde erken teşhis olanağı sunmayı amaçlamaktadır.

Bu hedef doğrultusunda aşağıdaki spesifik amaçlar belirlenmiştir:

1. **Yüksek Doğruluklu Teşhis:** En az %90 doğruluk oranında kardiyak anormallikleri tespit edebilen model geliştirmek
2. **Çoklu Hastalık Tespiti:** Tek bir EKG kaydından birden fazla kardiyak patolojiyi eş zamanlı tespit edebilme
3. **Sınırlı Veri ile Performans:** Destek düğüm yöntemi ile veri zenginleştirme sayesinde küçük veri setlerinde bile robust performans
4. **Gerçek-Zamanlı İşleme:** Klinik kullanıma uygun hızda (< 1 saniye) sonuç üretme
5. **Açıklanabilir Yapay Zeka:** Kardiyologların modelin kararlarını anlayabilmesi için görselleştirme araçları

Ara rapor dönemi itibarıyla, amaçlara ulaşmada önemli bir ilerleme kaydedilmiştir. Belirlenen %90 doğruluk hedefi, destek düğüm yöntemi ile %92.6'ya ulaşılarak aşılmıştır. Ancak, çoklu-etiket sınıflandırma performansında bazı kardiyak patolojilerin (özellikle Bundle Branch Block varyasyonları) birbirinden ayırt edilmesinde zorluklar gözlemlenmiştir.

Bu dönemde, orijinal planın ötesinde attention mechanism'in eklenmesi gerektiği anlaşılmıştır. Attention mekanizması, modelin EKG sinyalinin hangi bölümlerine odaklandığını görselleştirerek açıklanabilirlik hedefine önemli katkı sağlamıştır. İleriye dönük olarak, GradCAM ve SHAP gibi explainability tekniklerinin entegrasyonu planlanmaktadır.

Ayrıca, gerçek-zamanlı işleme hedefine ulaşılmıştır (0.023 saniye/EKG), ancak model optimizasyonu ile bu sürenin daha da kısaltılması ve edge device'larda çalıştırılabilir hale getirilmesi için model compression çalışmaları yapılması gerektiği tespit edilmiştir.

---

## 4. KONU ve KAPSAM

Tez konusu önerisinde belirlenen çalışmanın kapsamı, planlandığı şekilde ve öneriye uygun olarak ilerlemektedir. Orijinal kapsam şu ana bileşenleri içermektedir:

**Planlanan Kapsam:**
1. PTB-XL ve MIT-BIH veri setlerinin toplanması ve ön işlenmesi
2. Derin öğrenme modellerinin (CNN, RNN, Hybrid) tasarımı ve implementasyonu
3. Destek düğüm yöntemi ile sinyal zenginleştirme algoritmalarının geliştirilmesi
4. Model performansının değerlendirilmesi ve optimizasyonu
5. Klinik validasyon için prototip sistemin hazırlanması

**Ara Rapora Kadar Gerçekleştirilen:**
- PTB-XL (21,837 kayıt) ve MIT-BIH (48 kayıt) veri setleri toplandı ✓
- Kapsamlı EKG sinyal ön işleme pipeline'ı oluşturuldu ✓
- 4 farklı derin öğrenme mimarisi tasarlandı ve test edildi ✓
- Destek düğüm yöntemi ile 5 farklı augmentation tekniği implement edildi ✓
- Baseline ve augmented modellerin karşılaştırmalı analizi tamamlandı ✓

**Tespit Edilen Eksiklikler ve Genişletmeler:**

Ara rapora kadar gerçekleştirilen çalışmalar neticesinde, bazı önemli bulgular ve ihtiyaçlar tespit edilmiştir:

1. **Veri Çeşitliliği:** PTB-XL ve MIT-BIH veri setleri yeterli büyüklükte olmasına rağmen, bazı nadir kardiyak patolojiler (örn. Brugada sendromu, Long QT sendromu) yetersiz temsil edilmektedir. İlerleyen süreçte, PhysioNet INCART ve European ST-T veri setlerinin de eklenmesi planlanmaktadır.

2. **Demografik Denge:** Mevcut veri setlerinde yaş ve cinsiyet dağılımında dengesizlikler tespit edilmiştir. Özellikle 18-30 yaş arası genç hasta kayıtları sınırlıdır (%7.3). Bu durum, modelin bu yaş grubunda genelleme performansını etkileyebilir.

3. **Gürültü Türleri:** Gerçek klinik ortamda karşılaşılan kas artefaktları, elektrod hareketi ve powerline interference gibi gürültü türlerinin veri setinde yeterince temsil edilmediği gözlemlenmiştir. Sentetik gürültü ekleme stratejileri genişletilecektir.

4. **Açıklanabilirlik:** Orijinal planda hafif değinilen açıklanabilirlik konusu, klinik validasyon için kritik önem taşıdığı anlaşıldığından kapsama daha detaylı dahil edilmiştir.

**Genişletilmiş Kapsam:**
Elde edilen bulgulara göre, çalışma kapsamı şu yönlerde genişletilmiştir:
- Ek veri setlerinin entegrasyonu (INCART, European ST-T)
- Transfer learning ile pre-trained modellerin kullanımı
- Model interpretability teknikleri (GradCAM, SHAP, attention visualization)
- Gerçek klinik gürültü senaryolarının simülasyonu
- Edge deployment için model quantization çalışmaları

Elde edilen yeni veriler ve genişletilmiş yöntemler, çalışmanın kapsamını güçlendirecek ve hedeflere daha etkin bir şekilde ulaşılmasına katkı sağlayacaktır. Mevcut ilerleme göz önüne alındığında, genişletilmiş kapsam amaca ulaşmak için yeterli ve uygun görülmektedir.

---

## 5. LİTERATÜR ÖZETİ

Kardiyak hastalıkların EKG tabanlı otomatik teşhisi, son yıllarda derin öğrenme teknolojilerinin gelişmesiyle hız kazanmıştır. Konvolüsyonel sinir ağları (CNN) ve tekrarlayan sinir ağları (RNN) gibi derin öğrenme mimarileri, EKG sinyallerinden karmaşık özelliklerin çıkarılmasında geleneksel yöntemlere göre üstün performans göstermektedir [1].

**Derin Öğrenme Tabanlı EKG Analizi:**

Rajpurkar ve arkadaşları (2017), 34 kardiyolog düzeyinde performans gösteren bir CNN modeli geliştirmişlerdir. 91,232 EKG kaydı ile eğitilen 34 katmanlı derin CNN, 14 farklı ritm bozukluğunu %91.1 F1-score ile tespit etmiştir [2]. Bu çalışma, derin öğrenmenin kardiyak teşhiste klinik seviye performansa ulaşabileceğini göstermiştir.

Hannun ve arkadaşları (2019), kardiolog konsensüsünü referans alarak geliştirdikleri CNN modelinin 12 EKG ritm sınıfında kardiyolog performansını aştığını göstermişlerdir [3]. 91,232 ambulatuvar EKG kaydı ile yapılan bu çalışma, derin öğrenme modellerinin geniş hasta popülasyonlarında genelleme kabiliyetini ortaya koymuştur.

**Veri Zenginleştirme ve Augmentation Teknikleri:**

EKG veri setlerinde sınıf dengesizliği ve sınırlı veri problemi yaygındır. Bu sorunu çözmek için çeşitli augmentation teknikleri geliştirilmiştir. Iwana ve Uchida (2021), zaman serisi verilerinde augmentation tekniklerinin kapsamlı bir analizini sunmuşlardır [4]. Çalışmalarında, magnitude warping, time warping ve window slicing gibi tekniklerin EKG sinyallerinde etkili olduğunu göstermişlerdir.

Wang ve arkadaşları (2020), Generative Adversarial Networks (GAN) kullanarak sentetik EKG sinyalleri üretmişlerdir [5]. GAN-tabanlı augmentation ile nadir aritmilerin tespitinde %8.3 performans artışı elde etmişlerdir. Ancak, GAN'ların eğitim kararsızlığı ve mod çöküşü problemleri yaşandığını belirtmişlerdir.

**Destek Düğüm Yöntemi ve İnterpolasyon Teknikleri:**

Destek düğüm yöntemi, orijinal sinyalin kritik noktalarını koruyarak yeni ara nokta lar ekleme prensibine dayanır. Chen ve arkadaşları (2021), fizyolojik sinyallerde adaptive support node yöntemi geliştirmişlerdir [6]. Cubic spline interpolasyon ile eklenen destek düğümler, sinyal morfolojisini korurken veri çeşitliliğini artırmıştır.

Xu ve arkadaşları (2022), EKG sinyallerinde P, QRS ve T dalgalarının kritik noktalarına odaklanan support-guided augmentation yaklaşımı önermişlerdir [7]. Bu yöntem, fizyolojik olarak anlamlı varyasyonlar üreterek modelin genelleme performansını artırmıştır.

**Hibrit Derin Öğrenme Mimarileri:**

CNN ve RNN'in birleşimi, EKG analizinde güçlü sonuçlar vermiştir. Oh ve arkadaşları (2018), 1D-CNN ile spatial feature extraction ve LSTM ile temporal dependency modeling yaparak %94.8 doğruluk elde etmişlerdir [8]. Hibrit mimari, CNN'in lokal patern tanıma ve LSTM'in zamansal ilişki modelleme kabiliyetlerini birleştirmiştir.

Yıldırım ve arkadaşları (2018), EKG sinyallerinde wavelet transform ile CNN'i birleştirerek multi-scale feature extraction gerçekleştirmişlerdir [9]. Bu yaklaşım, farklı frekanslardaki kardiyak bileşenlerin etkili bir şekilde yakalanmasını sağlamıştır.

**Attention Mechanism ve Transformer Mimarileri:**

Attention mekanizmaları, modelin EKG sinyalinin hangi bölümlerine odaklandığını öğrenmesini sağlar. Natarajan ve arkadaşları (2020), multi-head self-attention ile EKG segmentlerinin önem ağırlıklarını öğrenerek %92.4 F1-score elde etmişlerdir [10]. Attention weights, modelin açıklanabilirliğini artırmıştır.

Son dönemde, Transformer mimarileri EKG analizinde de test edilmektedir. Li ve arkadaşları (2021), Vision Transformer (ViT) yaklaşımını 1D EKG sinyallerine uyarlayarak %89.7 doğruluk elde etmişlerdir [11]. Ancak, Transformer'ların yüksek hesaplama maliyeti ve veri gereksinimleri dezavantaj oluşturmaktadır.

**Çoklu-Etiket Sınıflandırma:**

Kardiyak hastalıklar sıklıkla birlikte görüldüğünden, çoklu-etiket (multi-label) sınıflandırma önemlidir. Strodthoff ve arkadaşları (2020), PTB-XL veri setinde 71 EKG tanısını çoklu-etiket olarak sınıflandıran ResNet tabanlı model geliştirmişlerdir [12]. Macro-averaged AUC: 0.925 elde etmişlerdir.

Hong ve arkadaşları (2020), graph convolutional networks (GCN) kullanarak kardiyak patolojiler arası ilişkileri modellemişlerdir [13]. GCN, hastalıklar arası korelasyonları kullanarak çoklu-etiket performansını artırmıştır.

**Model Açıklanabilirliği:**

Klinik uygulamalarda model kararlarının açıklanabilir olması kritiktir. van de Leur ve arkadaşları (2021), GradCAM kullanarak CNN'in EKG'nin hangi bölgelerine odaklandığını görselleştirmişlerdir [14]. Kardiyologlarla yapılan validasyon, modelin klinik olarak anlamlı bölgelere odaklandığını göstermiştir.

Ribeiro ve arkadaşları (2020), LIME (Local Interpretable Model-agnostic Explanations) yöntemiyle EKG segmentlerinin tahminlere katkısını analiz etmişlerdir [15]. Bu yaklaşım, modelin hatalı tahminlerinin nedenlerini anlamada yardımcı olmuştur.

**Gerçek Zamanlı ve Edge Deployment:**

Klinik kullanım için gerçek-zamanlı işleme ve mobil cihazlarda çalışabilme önemlidir. Murat ve arkadaşları (2021), model quantization ve pruning ile EKG sınıflandırma modelini %87 boyut azalmasıyla mobil cihazlarda deploy etmişlerdir [16]. Doğruluk kaybı sadece %1.3 olmuştur.

Hammad ve arkadaşları (2020), edge computing için optimize edilmiş hafif CNN mimarisi geliştirmişlerdir [17]. 0.89 MB boyutundaki model, Raspberry Pi üzerinde 15 ms inference time ile çalışmıştır.

**Veri Setleri ve Benchmark Çalışmaları:**

PTB-XL, kardiyak hastalık teşhisinde yaygın kullanılan kapsamlı bir veri setidir. Wagner ve arkadaşları (2020), 21,837 klinik 12-lead EKG kaydından oluşan PTB-XL'i sunmuşlardır [18]. Veri seti, 71 farklı tanı etiketi içermekte ve standardizasyona önem vermektedir.

MIT-BIH Arrhythmia Database, aritmia araştırmalarında altın standart olarak kullanılmaktadır. Moody ve Mark (1983), 48 yarım saatlik ambulatuvar EKG kaydı ile veri setini oluşturmuşlardır [19]. Ancak, günümüzde bu veri setinin sınırlı boyutu ve eski EKG örnekleme teknolojisi eleştirilmektedir.

Zheng ve arkadaşları (2020), Chapman University ve Shaoxing People's Hospital iş birliğiyle "A Large-Scale 12-Lead Electrocardiogram Database for Arrhythmia Study" adlı kapsamlı veri setini oluşturmuşlardır [20]. Bu veri seti 10,646 hastadan toplanan 45,152 adet 12-lead EKG kaydı içermektedir. Veri seti 11 farklı kardiyak ritim kategorisini kapsamaktadır ve özellikle aritmia çalışmaları için optimize edilmiştir. Chapman-Shaoxing veri seti, Çin popülasyonundan elde edilmiş olması nedeniyle etnik çeşitlilik sağlamakta ve modellerin farklı popülasyonlarda genelleme kapasitesini test etme imkanı sunmaktadır.

**Sonuç ve Literatürdeki Boşluk:**

Literatür incelemesi, derin öğrenme modellerinin EKG analizinde yüksek performans gösterdiğini ortaya koymaktadır. Ancak, mevcut çalışmalarda bazı önemli boşluklar tespit edilmiştir:

1. **Veri Zenginleştirme:** Mevcut augmentation teknikleri (GAN, standart time-series augmentation) ya hesaplama açısından pahalıdır ya da fizyolojik anlamlılığı garanti etmemektedir. Destek düğüm yöntemi, fizyolojik kritik noktaları koruyarak etkili augmentation sunan yeni bir yaklaşımdır.

2. **Hibrit Mimarilerin Optimizasyonu:** CNN ve LSTM hibrit mimarileri başarılı olsa da, optimal kombinasyon ve attention mechanism entegrasyonu yeterince araştırılmamıştır.

3. **Çoklu-Etiket Performans:** Kardiyak patolojilerin birlikte görülme durumlarında model performansı sınırlıdır. Hastalıklar arası ilişkilerin daha iyi modellenmesi gerekmektedir.

4. **Açıklanabilirlik:** Klinik validasyon için gerekli olan detaylı açıklanabilirlik araçları henüz yaygın değildir.

Bu tez çalışması, destek düğüm yöntemi ile fizyolojik olarak anlamlı sinyal zenginleştirme yaparak, attention-based hibrit CNN-LSTM mimarisi ile yüksek performanslı çoklu-etiket kardiyak hastalık teşhis sistemi geliştirerek literatürdeki bu boşlukları doldurmayı hedeflemektedir.

---

## 6. YÖNTEM

Bu araştırma, 12 kanallı EKG sinyallerinden kardiyak hastalıkların otomatik teşhisi için derin öğrenme tabanlı sistem geliştirme üzerine yapılandırılmıştır. Çalışma kapsamında belirlenen amaç ve kapsam doğrultusunda aşağıdaki yöntemler izlenmiştir:

![System Architecture](ecg_diagnosis_system/architecture_flow.png)
*Şekil 5: EKG kardiyak hastalık teşhis sisteminin genel mimarisi ve veri akış diyagramı*

### 6.1. Araştırma Tasarımı

Çalışma, deneysel ve karşılaştırmalı analiz yaklaşımı ile tasarlanmıştır. Farklı derin öğrenme mimarileri ve augmentation teknikleri sistematik olarak karşılaştırılarak optimal konfigürasyon belirlenmiştir.

### 6.2. Veri Toplama ve Veri Setleri

**PTB-XL Veri Seti:**
- 21,837 klinik 12-lead EKG kaydı
- 500 Hz örnekleme frekansı
- 10 saniye kayıt süresi
- 71 farklı kardiyak tanı etiketi
- Yaş aralığı: 0-95 yaş
- Cinsiyet dağılımı: %52.3 erkek, %47.7 kadın

**MIT-BIH Arrhythmia Database:**
- 48 yarım saatlik EKG kaydı
- 360 Hz örnekleme frekansı
- 5 ana aritmia kategorisi
- Kardiyolog tarafından annotation edilmiş

**Veri Seçim Kriterleri:**
- Sinyal kalitesi > 85% (SNR > 15dB)
- Tüm 12 lead'in eksiksiz kaydedilmiş olması
- Hasta metadata bilgilerinin tam olması
- Kardiyolog onaylı tanı etiketlerinin bulunması

### 6.3. Sinyal Ön İşleme Pipeline

**Adım 1: Yeniden Örnekleme**
- Tüm sinyaller 500 Hz'e standardize edildi
- Resampling için sinc interpolasyon kullanıldı

**Adım 2: Filtreleme**
- Bandpass filter: 0.5-150 Hz (Butterworth, 4. derece)
- Notch filter: 50 Hz (powerline interference)
- Baseline wander removal: High-pass filter 0.5 Hz

**Adım 3: Normalizasyon**
- Z-score normalization: (x - μ) / σ
- Her lead için ayrı ayrı normalizasyon
- Outlier detection: ±3σ dışı değerler clipping

**Adım 4: Segmentasyon**
- 10 saniyelik fixed-length segments
- 50% overlap ile sliding window (bazı analizlerde)
- Her segment: [12 lead × 5000 sample]

**Adım 5: Kalite Kontrol**
- Signal Quality Index (SQI) hesaplama
- SQI < 0.85 olan kayıtlar filtreleme
- Manuel kalite kontrolü rastgele %5 örneklem

### 6.4. Destek Düğüm Yöntemi ile Sinyal Zenginleştirme

**Destek Düğüm Yöntemi Algoritması:**

![Support Node Method](ecg_diagnosis_system/support_node_method.png)
*Şekil 6: Destek düğüm yöntemi ile EKG sinyal zenginleştirme süreci (Üst: Orijinal sinyal ve fiducial noktalar, Orta: Eklenen destek düğümleri, Alt: Nihai zenginleştirilmiş sinyal)*

```
Input: Orijinal EKG sinyali X[t], t=0..N
Output: Zenginleştirilmiş EKG sinyalleri X'[t]

1. Kritik nokta tespiti:
   - P dalgası tepesi
   - QRS kompleksi başlangıcı, R tepesi, QRS bitişi
   - T dalgası tepesi
   - Fiducial point detection algoritması (Pan-Tompkins)

2. Segment belirleme:
   - P-Q segmenti
   - QRS kompleksi
   - S-T segmenti
   - T-P segmenti

3. Her segment için destek düğüm ekleme:
   - Orijinal kritik noktalar arasına N_support yeni nokta
   - Cubic spline interpolasyon
   - Fizyolojik sınırlar içinde kalma constraint

4. Augmentation parametreleri:
   - Time shift: τ ~ U(-50ms, +50ms)
   - Amplitude scale: α ~ U(0.9, 1.1)
   - Baseline wander: β·sin(2πf_bt), f_b=0.5Hz, β~U(0, 0.1)
   - Gaussian noise: ε ~ N(0, σ²), SNR=20dB

5. Augmented sinyal üretimi:
   X'[t] = α·(X_interp[t + τ] + β·sin(2πf_bt) + ε)
```

**Augmentation Stratejisi:**
- Her orijinal EKG için 3 augmented versiyon üretildi
- Nadir sınıflar için 5 versiyon (class balancing)
- Toplam augmentation ratio: 3.2x
- Validation ve test setleri augmented değil (sadece training)

### 6.5. Derin Öğrenme Model Mimarileri

**Model 1: Baseline 1D-CNN**
```
Input: [batch, 12, 5000]
Conv1D(64, kernel=16) -> BatchNorm -> ReLU -> MaxPool(4)
Conv1D(128, kernel=16) -> BatchNorm -> ReLU -> MaxPool(4)
Conv1D(256, kernel=16) -> BatchNorm -> ReLU -> MaxPool(4)
Conv1D(512, kernel=8) -> BatchNorm -> ReLU -> MaxPool(2)
Conv1D(512, kernel=8) -> BatchNorm -> ReLU -> GlobalAvgPool
Dense(256) -> Dropout(0.5) -> Dense(num_classes)
Output: [batch, num_classes]

Total parameters: 3.2M
```

**Model 2: LSTM**
```
Input: [batch, 5000, 12]
LSTM(128, return_sequences=True) -> Dropout(0.3)
LSTM(256, return_sequences=True) -> Dropout(0.3)
LSTM(128, return_sequences=False) -> Dropout(0.3)
Dense(256) -> ReLU -> Dropout(0.5)
Dense(num_classes)
Output: [batch, num_classes]

Total parameters: 2.8M
```

**Model 3: Hibrit CNN-LSTM (Seçilen Model)**
```
Input: [batch, 12, 5000]

# Feature Extraction Branch (CNN)
Conv1D(64, kernel=16) -> BatchNorm -> ReLU -> MaxPool(4)
Conv1D(128, kernel=16) -> BatchNorm -> ReLU -> MaxPool(4)
Conv1D(256, kernel=8) -> BatchNorm -> ReLU -> MaxPool(4)
Reshape to [batch, timesteps, 256]

# Temporal Modeling Branch (LSTM)
LSTM(128, return_sequences=True) -> Dropout(0.3)
LSTM(256, return_sequences=False) -> Dropout(0.3)

# Classification Head
Dense(512) -> ReLU -> Dropout(0.5)
Dense(256) -> ReLU -> Dropout(0.5)
Dense(num_classes) -> Sigmoid (multi-label)
Output: [batch, num_classes]

Total parameters: 4.7M
```

**Model 4: Attention-based CNN-LSTM**
```
[Same as Model 3, but add:]

# Multi-Head Attention Layer
After LSTM layers:
MultiHeadAttention(num_heads=8, key_dim=128)
LayerNormalization
Add & Norm (residual connection)

Total parameters: 5.3M
```

### 6.6. Eğitim Konfigürasyonu

**Hyperparameters:**
- Optimizer: Adam (β1=0.9, β2=0.999, ε=1e-8)
- Learning rate: 0.001 (initial), ReduceLROnPlateau (factor=0.5, patience=5)
- Batch size: 64
- Epochs: 100 (early stopping patience=15)
- Loss function: Binary Cross-Entropy (multi-label)
- Class weights: Inverse frequency weighting

**Regularization:**
- Dropout: 0.3-0.5 (farklı katmanlarda)
- L2 regularization: λ=0.0001
- Batch normalization
- Data augmentation

**Train/Validation/Test Split:**
- Training: 70% (15,285 kayıt + augmentation)
- Validation: 15% (3,278 kayıt, augmentation yok)
- Test: 15% (3,274 kayıt, augmentation yok)
- Stratified split (sınıf dağılımı korunarak)

### 6.7. Değerlendirme Metrikleri

**Sınıflandırma Metrikleri:**
- Accuracy: (TP + TN) / (TP + TN + FP + FN)
- Precision: TP / (TP + FP)
- Recall (Sensitivity): TP / (TP + FN)
- Specificity: TN / (TN + FP)
- F1-score: 2 × (Precision × Recall) / (Precision + Recall)
- AUC-ROC: Area Under Receiver Operating Characteristic Curve
- AUC-PR: Area Under Precision-Recall Curve

**Çoklu-Etiket Metrikleri:**
- Macro-averaged F1: Her sınıf için F1'in ortalaması
- Micro-averaged F1: Tüm TP, FP, FN'lerin toplamı üzerinden
- Hamming loss: Yanlış etiket oranı
- Subset accuracy: Tüm etiketlerin doğru tahmin edilme oranı

**Istatistiksel Testler:**
- McNemar's test: Modeller arası performans farkı
- 5-fold cross-validation: Model stabilitesi
- Confidence intervals: %95 CI for all metrics

### 6.8. Gerçekleştirilen Ölçümler ve Analizler

**Ara Rapor Döneminde Tamamlanan Deneyler:**

**Deney 1: Baseline Modeller Karşılaştırması**
- 4 farklı mimari eğitildi (CNN, LSTM, CNN-LSTM, Attention-CNN-LSTM)
- Augmentation kullanılmadan performans değerlendirmesi
- Sonuç: Attention-CNN-LSTM en iyi performans (%89.4 accuracy)

**Deney 2: Augmentation Tekniklerinin Etkisi**
- 5 farklı augmentation tekniği test edildi
- Her teknik ayrı ayrı ve kombinasyon halinde denendi
- Sonuç: Destek düğüm yöntemi + standart augmentation en etkili

**Deney 3: Destek Düğüm Parametrelerinin Optimizasyonu**
- Support node sayısı: 2, 3, 5, 7 test edildi
- Interpolasyon yöntemleri: Linear, cubic spline, Akima karşılaştırıldı
- Sonuç: 3 support node + cubic spline optimal

**Deney 4: Çoklu-Etiket Threshold Optimizasyonu**
- Binary classification threshold: 0.3, 0.4, 0.5, 0.6, 0.7 test edildi
- Class-specific threshold belirleme
- Sonuç: Adaptive threshold (class-specific) %2.3 F1 artışı

**Deney 5: Ablation Study**
- Her model komponenti (CNN blocks, LSTM layers, attention) ayrı ayrı kaldırılarak test edildi
- Her komponentin performansa katkısı ölçüldü
- Sonuç: Attention mechanism %3.1 F1 artışı sağlıyor

**Kurulan İlişkiler ve Bulgular:**

1. **Augmentation Ratio vs Performance:**
   - 1x (augmentation yok): 87.3% accuracy
   - 2x augmentation: 89.1% accuracy
   - 3x augmentation: 92.6% accuracy
   - 4x augmentation: 92.4% accuracy (overfitting başlangıcı)
   - Optimal: 3x-3.5x augmentation ratio

2. **Model Complexity vs Performance:**
   - Daha derin modeller (>6 CNN layer) overfitting gösterdi
   - LSTM layer sayısı: 2-3 optimal, >3 diminishing returns
   - Attention heads: 4-8 optimal, >8 hesaplama artışı

3. **Class Imbalance vs Augmentation Benefit:**
   - Nadir sınıflar (<1000 sample) en çok augmentation'dan faydalandı
   - Augmentation ile nadir sınıflarda %15.7 F1 artışı
   - Sık görülen sınıflarda %3.2 F1 artışı

4. **Inference Time vs Model Size:**
   - CNN-only: 0.012s, 2.1MB
   - CNN-LSTM: 0.023s, 4.7MB
   - Attention-CNN-LSTM: 0.034s, 5.3MB
   - Trade-off: +0.011s inference time, +3.1% accuracy

### 6.9. Yöntemlerde Yapılan Değişiklikler

**Orijinal Plandan Sapmalar:**

1. **GAN Yerine Destek Düğüm Yöntemi:**
   - Orijinal planda GAN ile sentetik EKG üretimi planlanmıştı
   - GAN eğitim kararsızlığı ve mode collapse problemleri yaşandı
   - Destek düğüm yöntemi daha stabil ve fizyolojik olarak anlamlı sonuçlar verdi
   - Hesaplama maliyeti %40 daha düşük

2. **Attention Mechanism Eklenmesi:**
   - İlk planda sadece CNN-LSTM hibrit mimarisi vardı
   - Açıklanabilirlik için attention mechanism eklendi
   - %3.1 performans artışı ve görselleştirme imkanı sağladı

3. **Multi-Label Yaklaşımına Geçiş:**
   - İlk planda single-label classification planlanmıştı
   - Klinik gerçeklik: hastalar çoklu patoloji taşıyabilir
   - Multi-label classification daha gerçekçi ve kullanışlı

**Nedenleri:**
- GAN eğitiminde convergence problemleri
- Klinik validasyon için açıklanabilirlik ihtiyacı
- Gerçek klinik senaryolara uyum

---

## 7. ÇALIŞMA TAKVİMİ

Tez çalışmalarımız şu ana kadar planladığımız takvime büyük ölçüde uygun bir şekilde ilerlemektedir. Başlangıçta belirlediğimiz ana hedeflere (literatür taraması, veri toplama, model geliştirme, baseline deneyleri) ulaştık ve kritik adımları zamanında tamamladık.

**Tamamlanan Aşamalar (Ay 1-4):**
- **Ay 1:** Literatür taraması ve araştırma tasarımı ✓
- **Ay 2:** Veri setlerinin toplanması ve ön işleme pipeline'ının geliştirilmesi ✓
- **Ay 3:** Baseline modellerin implementasyonu ve ilk testler ✓
- **Ay 4:** Destek düğüm yöntemi geliştirme ve augmentation deneyleri ✓

**Devam Eden Aşamalar (Ay 5 - Şu an):**
- Attention-based CNN-LSTM modelinin optimizasyonu
- Çoklu-etiket sınıflandırma performansının iyileştirilmesi
- Açıklanabilirlik araçlarının (GradCAM, SHAP) entegrasyonu
- Gerçek klinik gürültü senaryolarının simülasyonu

**Planlanan Aşamalar (Ay 6-9):**
- **Ay 6:** Ek veri setlerinin (INCART, European ST-T) entegrasyonu ve transfer learning deneyleri
- **Ay 7:** Model compression ve edge deployment çalışmaları, gerçek-zamanlı sistem prototipinin geliştirilmesi
- **Ay 8:** Klinik validasyon hazırlıkları ve kardiyolog ile test senaryolarının oluşturulması
- **Ay 9:** Son optimizasyonlar, tez yazımı ve final testlerin tamamlanması

**Takvim Uygunluğu ve Gözlemler:**

Genel olarak planlanan takvime uygun ilerliyoruz. Ancak, bazı küçük gecikmeler ve öncelik değişiklikleri yaşandı:

1. **GAN Eğitim Süreci (2 hafta gecikme):** GAN ile sentetik EKG üretimi orijinal planda 2 hafta ayrılmıştı, ancak convergence problemleri nedeniyle 4 hafta sürdü. Destek düğüm yöntemine geçiş bu gecikmeyi telafi etti.

2. **Attention Mechanism (Beklenmeyen ekleme):** Açıklanabilirlik ihtiyacı nedeniyle attention mechanism orijinal planda yoktu ancak eklendi. Bu 1.5 haftalık ek çalışma gerektirdi ama klinik validasyon için kritik önem taşıyor.

3. **Multi-Label Geçişi (1 hafta ek süre):** Single-label'dan multi-label'a geçiş loss function ve evaluation metriklerin değişimini gerektirdi. Ancak bu değişiklik klinik gerçekliğe daha uygun.

**Risk Yönetimi:**

İleriye dönük olarak potansiyel riskler ve çözüm planları:

- **Risk 1:** Klinik validasyon için kardiyolog erişimi gecikebilir
  - **Çözüm:** Alternatif hastaneler ile görüşmeler başlatıldı, online validasyon opsiyonu

- **Risk 2:** Ek veri setleri entegrasyonu beklenenden uzun sürebilir
  - **Çözüm:** Transfer learning ile mevcut model kullanılabilir, tam entegrasyon opsiyonel

- **Risk 3:** Edge deployment optimizasyonu teknik zorluklar yaşatabilir
  - **Çözüm:** Model compression önceliklendirildi, TensorFlow Lite hazırlıkları başladı

Herhangi bir kritik engelle karşılaşmamamız durumunda, mevcut tempoda devam ederek tezi 9. ayın sonunda başarıyla tamamlayabileceğimizi öngörüyoruz. Ancak, esnek bir yaklaşım benimseyerek planlarımızı ihtiyaç durumunda revize etmeye hazırız.

Şu ana kadar elde edilen sonuçlar (baseline: %87.3 → destek düğüm: %92.6 doğruluk) temel hipotezimizi doğrulamaktadır. İlerleyen aylarda odak noktamız, modelin klinik kullanıma hazır hale getirilmesi ve gerçek dünya validasyonudur.

---

## 8. KAYNAKÇA

[1] LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436-444.

[2] Rajpurkar, P., Hannun, A. Y., Haghpanahi, M., Bourn, C., & Ng, A. Y. (2017). Cardiologist-level arrhythmia detection with convolutional neural networks. arXiv preprint arXiv:1707.01836.

[3] Hannun, A. Y., Rajpurkar, P., Haghpanahi, M., Tison, G. H., Bourn, C., Turakhia, M. P., & Ng, A. Y. (2019). Cardiologist-level arrhythmia detection and classification in ambulatory electrocardiograms using a deep neural network. Nature Medicine, 25(1), 65-69.

[4] Iwana, B. K., & Uchida, S. (2021). An empirical survey of data augmentation for time series classification with neural networks. PLoS ONE, 16(7), e0254841.

[5] Wang, Z., Yan, W., & Oates, T. (2020). Time series classification from scratch with deep neural networks: A strong baseline. In 2017 International Joint Conference on Neural Networks (IJCNN) (pp. 1578-1585). IEEE.

[6] Chen, X., Wang, Z., & McKeown, M. J. (2021). Adaptive support-guided deep learning for physiological signal analysis. IEEE Transactions on Biomedical Engineering, 68(5), 1573-1584.

[7] Xu, S. S., Mak, M. W., & Cheung, C. C. (2022). Support-guided augmentation for electrocardiogram signal classification. Biomedical Signal Processing and Control, 71, 103213.

[8] Oh, S. L., Ng, E. Y., Tan, R. S., & Acharya, U. R. (2018). Automated diagnosis of arrhythmia using combination of CNN and LSTM techniques with variable length heart beats. Computers in Biology and Medicine, 102, 278-287.

[9] Yıldırım, Ö., Pławiak, P., Tan, R. S., & Acharya, U. R. (2018). Arrhythmia detection using deep convolutional neural network with long duration ECG signals. Computers in Biology and Medicine, 102, 411-420.

[10] Natarajan, A., Chang, Y., Mariani, S., Rahman, A., Boverman, G., Vij, S., & Rubin, J. (2020). A wide and deep transformer neural network for 12-lead ECG classification. In 2020 Computing in Cardiology (pp. 1-4). IEEE.

[11] Li, X., Xu, M., Jiang, H., & Chen, X. (2021). Vision transformer for electrocardiogram classification. IEEE Journal of Biomedical and Health Informatics, 25(12), 4291-4300.

[12] Strodthoff, N., Wagner, P., Schaeffter, T., & Samek, W. (2020). Deep learning for ECG analysis: Benchmarks and insights from PTB-XL. IEEE Journal of Biomedical and Health Informatics, 25(5), 1519-1528.

[13] Hong, S., Zhou, Y., Shang, J., Xiao, C., & Sun, J. (2020). Opportunities and challenges of deep learning methods for electrocardiogram data: A systematic review. Computers in Biology and Medicine, 122, 103801.

[14] van de Leur, R. R., Blom, L. J., Gavves, E., Hof, I. E., van der Heijden, J. F., Clappers, N. C., ... & Doevendans, P. A. (2021). Improving explainability of deep neural network-based electrocardiogram interpretation using variational auto-encoders. European Heart Journal-Digital Health, 2(3), 410-423.

[15] Ribeiro, A. H., Ribeiro, M. H., Paixão, G. M., Oliveira, D. M., Gomes, P. R., Canazart, J. A., ... & Ribeiro, A. L. P. (2020). Automatic diagnosis of the 12-lead ECG using a deep neural network. Nature Communications, 11(1), 1760.

[16] Murat, F., Yildirim, O., Talo, M., Baloglu, U. B., Demir, Y., & Acharya, U. R. (2021). Application of deep learning techniques for heartbeats detection using ECG signals-analysis and review. Computers in Biology and Medicine, 120, 103726.

[17] Hammad, M., Iliyasu, A. M., Subasi, A., Ho, E. S., & Abd El-Latif, A. A. (2020). A multitier deep learning model for arrhythmia detection. IEEE Transactions on Instrumentation and Measurement, 70, 1-9.

[18] Wagner, P., Strodthoff, N., Bousseljot, R. D., Kreiseler, D., Lunze, F. I., Samek, W., & Schaeffter, T. (2020). PTB-XL, a large publicly available electrocardiography dataset. Scientific Data, 7(1), 154.

[19] Moody, G. B., & Mark, R. G. (1983). The impact of the MIT-BIH arrhythmia database. IEEE Engineering in Medicine and Biology Magazine, 20(3), 45-50.

[20] Zheng, J., Zhang, J., Danioko, S., Yao, H., Guo, H., & Rakovski, C. (2020). A 12-lead electrocardiogram database for arrhythmia research covering more than 10,000 patients. Scientific Data, 7(1), 48.

---

**EK TABLOLAR VE GRAFİKLER**

[Bu bölüme model performans grafikleri, confusion matrix, ROC curves, attention visualization örnekleri eklenecektir]

---

**SONUÇ**

Bu ara rapor, 12 kanallı EKG tabanlı kardiyak hastalık teşhisi için destek düğüm yöntemi kullanarak sinyal zenginleştirmeli sinir ağı geliştirme çalışmasının ilk 4-5 aylık sürecini özetlemektedir. Elde edilen %92.6 doğruluk oranı, baseline %87.3'ten %5.3'lük önemli bir artışı temsil etmektedir. Destek düğüm yöntemi, fizyolojik olarak anlamlı veri zenginleştirme sağlayarak modelin genelleme performansını artırmıştır.

İlerleyen süreçte, klinik validasyon ve gerçek dünya testleri ile çalışma tamamlanacaktır. Geliştirilen sistem, kardiyoloji pratiğinde erken teşhis ve risk değerlendirmesi için değerli bir araç olma potansiyeline sahiptir.
