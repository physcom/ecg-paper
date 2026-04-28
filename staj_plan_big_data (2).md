# LİSANSÜSTÜ EĞİTİM ENSTİTÜSÜ FORMLARI
## STAJ UYGULAMA VE DEĞERLENDİRME FORMU

**Doküman No:** KTMU-FR-LEE-39  
**İlk Yayın Tarihi:** 15/12/2024  
**Sayfa No:** 1

---

## RAPOR/Отчет

**Anabilim Dalı / Билим багыты:** Компьютердик инженерия

**Öğrencinin Adı ve Soyadı / Магистранттын аты жөнү:** [Студенттин аты]  
**Numarası / Номери:** [Номер]

**Danışman Öğretim Üyesi / Илимий жетекчиси:** [Жетекчинин аты]

**Staj Türü / Практиканын түрү:**
- ( ) Bilimsel Araştırma / Илимий изилдөө
- ( ) Pedagojik / Педагогикалык
- ( ✓ ) Mesleki / Кесиптик
- ( ) Endüstriyel / Өндүрүштүк
- ( ) Teknolojik / Технологиялык

**Staj Yeri / Практика өткөн мекеменин аталышы:** [Компаниянын аталышы]

**Adres, Telefon, E-posta / Адреси, телефону жана электрондук дареги:** [Байланыш маалыматтары]

**Yetkili Amirin Adı ve Soyadı / Жетекчинин аты-жөнү:** _______________  
**İmza/Колу:** _______________

**Dönem ve Süre / Семестр жана убакыт:** 2025 Жазгы семестр

**Staj Günü / Иш күндөрү:** 96 күн (эс алуу күндөрүсүз)

**Staj Saatleri / Сааттар:** 9:00 - 18:00

---

## Çalışma Planı/Takvimi
## Практикасынын программасы

### 1. Hafta/Апта

**Аткарылган иштер:**

Docker платформасы менен таанышып, иштөө чөйрөсүн даярдадым. Docker Desktop орноттум жана негизги командалар менен иштедим (docker run, pull, ps, images). Dockerfile түзүп, custom образдарды билдирүү практикасын өздөштүрдүм. Docker Compose менен бир нече сервистерди башкарууну үйрөндүм. Big Data системаларын Docker'де иштетүүнүн артыкчылыктарын түшүндүм - тез deployment, версиялык контроль, ресурстарды изоляциялоо.

**Данışман Değerlendirilmesi/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başarısız / Ийгиликсиз

---

### 2. Hafta/Апта

**Аткарылган иштер:**

Hadoop экосистемасы менен терең таанышып, distributed computing концепциясын түшүндүм. HDFS архитектурасын үйрөндүм - NameNode, DataNode, блоктордун репликациясы. Docker контейнерлеринде multi-node Hadoop кластерин орноттум (1 NameNode + 2-3 DataNode). HDFS командалары менен практикалык иш жүргүздүм - hdfs dfs -ls, -put, -get, -cat. Чоң файлдарды жүктөп, алардын автоматтык түрдө бөлүктөргө бөлүнүп, репликацияланышын байкадым.

**Данışман Değерlendirilmesi/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başarısız / Ийгиликсиз

---

### 3. Hafta/Апта

**Аткарылган иштер:**

Apache Spark менен таанышып, анын Hadoop экосистемасындагы ролун түшүндүм. Spark архитектурасын үйрөндүм - Driver, Executors, Cluster Manager жана RDD концепциясы. Docker'де Spark кластерин Standalone режимде орнотуп, веб-интерфейстерге кирдим. PySpark орнотуп, Jupyter Notebook менен интеграциялап иштедим. Биринчи Spark приложенияларын жаздым жана Spark'тын MapReduce'тан артыкчылыгын практикада көрдүм - in-memory процесстөө.

**Данışман Değerlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарısız / Ийгиликсиз

---

### 4. Hafta/Апта

**Аткарылган иштер:**

Spark DataFrames API менен терең иштедим - CSV, JSON, Parquet булактарынан маалыматтарды окудум. DataFrame трансформацияларын колдондум - select, filter, groupBy, join операциялары. Aggregation функцияларын жана Window функцияларын үйрөндүм - ROW_NUMBER, RANK, LEAD, LAG. UDF (User Defined Functions) түзүп, Python функцияларын Spark'ка интеграциялоодум. Чоң маалыматтарды процесстөп, натыйжаларды оптималдуу түрдө файлга жаздым.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарısız / Ийгиликсиз

---

### 5. Hafta/Апта

**Аткарылган иштер:**

Apache Hive менен таанышып, HDFS үстүнөн SQL интерфейси берүүчү data warehouse системасын үйрөндүм. Hive архитектурасын өздөштүрдүм - Metastore, HiveServer2, Beeline. Docker'де Hive орнотуп, PostgreSQL метастор конфигурациялоодум. Биринчи таблицаларды түздүм - EXTERNAL жана MANAGED таблицалар. CSV жана JSON файлдарын Hive таблицаларына жүктөп, партициялоо концепциясын практикада колдондум.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başarісız / Ийгиликсиз

---

### 6. Hafta/Апта

**Аткарылган иштер:**

Hive менен татаал аналитикалык суроолорду жаздым - JOIN, подзапросы, UNION операциялары. Аналитикалык функцияларды колдондум - ROW_NUMBER(), RANK(), LEAD(), LAG(). Hive оптимизациясы техникаларын үйрөндүм - партициялоо стратегиялары, ORC жана Parquet форматтары. Vectorization жана CBO (Cost-Based Optimizer) жөндөдүм. Масштабдуу маалыматтар менен оптималдаштырылган суроолорду аткардым.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 7. Hafta/Апта

**Аткарылган иштер:**

Spark жана Hive интеграциясын ишке ашырдым. SparkSession конфигурациялап, Hive Metastore менен туташтырдым. Hive таблицаларын Spark DataFrames катары окуп, Spark'тын in-memory процесстөөсүн колдондум. Натыйжаларды Hive'ге кайра жаздым - saveAsTable(), insertInto() методдору менен. Hybrid pipeline архитектурасын түздүм - Hive ETL + Spark аналитика.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 8. Hafta/Апта

**Аткарылган иштер:**

Электронный счет-фактура (ЭСФ) маалыматтары менен иштөө практикасын баштадым. Hadoop архитектурасынын миллиондогон ЭСФ маалыматтарын distributed түрдө сактоо жана процесстөө артыкчылыктарын практикада көрдүм. HDFS'тин fault-tolerance механизмин түшүндүм - маалыматтар автоматтык репликацияланат. ЭСФ маалыматтарын HDFS'ке жүктөп, Hive'де structured таблицаларга өткөрдүм. Партициялоо стратегиясын ишке ашырдым - дата жана контрагент боюнча бөлүштүрүү.

**Данışман Değerlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başarісız / Ийгиликсиз

---

### 9. Hafta/Апта

**Аткарылган иштер:**

ЭСФ маалыматтарын тазалоодум жана трансформациялоодум - ETL процессин ишке ашырдым. PySpark'тын distributed процесстөө мүмкүнчүлүктөрүн колдондум - бардык кластерде параллель аткаруу. Spark'тын lazy evaluation концепциясын практикада көрдүм. Маалыматтарды стандарттоодум, data quality текшердим жана дубликаттарды таптым. Комплекстүү ETL pipeline түздүм - бир нече source'тардан окуу, трансформация, validation, Hive'ге жазуу.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 10. Hafta/Апта

**Аткарылган иштер:**

ЭСФ маалыматтарынан бизнес инсайттарды чыгардым. Spark SQL менен аналитикалык суроолорду жаздым - контрагенттер боюнча транзакциялар, убакыт боюнча трендлер. Татаал аналитикалык суроолорду иштеп чыктым - time-series тенденциялар, moving averages. Window функцияларын колдонуп, географиялык аналитиканы жүргүздүм. HiveQL жана Spark SQL'ди салыштырдым - код окшош, бирок execution engine башка.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 11. Hafta/Апта

**Аткарылган иштер:**

Алдамчылыкты (fraud) аныктоо үчүн feature engineering жүргүздүм. Электронный счет-фактураларда fraud patterns'тарды изилдедим - адаттан тыш суммалар, бейтааныш контрагенттер, географиялык аномалиялар. Anomaly detection техникаларын колдондум - statistical жана time-series методдор. Spark DataFrame API менен features түздүм - transaction frequency, average amount, time patterns. Бул features машиналык үйрөнүү моделдери үчүн даярдадым.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 12. Hafta/Апта

**Аткарылган иштер:**

Spark MLlib аркылуу машиналык үйрөнүү моделдерин fraud detection үчүн колдондум. Classification моделдерди үйрөттүм - Logistic Regression, Random Forest, Gradient Boosted Trees. Pipeline API колдонуп, ETL жана ML'ди бир workflow'до бириктирдим. Cross-validation жана hyperparameter tuning жүргүздүм. Model evaluation жасап, үйрөтүлгөн моделди HDFS'ке сактадым.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 13. Hafta/Апта

**Аткарылган иштер:**

Аналитикалык натыйжаларды визуализациялоодум жана отчеттор түздүм. Spark натыйжаларын pandas DataFrame'ге өткөрдүм (toPandas()) - кичине маалыматтар үчүн, чоң болсо coalesce() аркылуу partition санын азайтып алуу. Matplotlib, Seaborn, Plotly аркылуу графиктерди түздүм - time-series, bar charts, heatmaps, geographical maps.

Интерактивдүү дашбордлорду түздүм - Apache Superset же Metabase менен Hive'ге туташуу. BI инструменттери HiveQL колдонуп таблицалардан маалыматты алат. Scheduled отчеттор конфигурациялоодум - PySpark скрипттери cron job же Airflow аркылуу убакыт боюнча автоматтык иштесин. Email жана Slack билдирүүлөрүн жөндөдүм - критикалык метрикалар же аномалиялар табылганда. Stakeholder'лор үчүн презентация даярдадым - техникалык эмес аудитория үчүн түшүнүктүү визуализациялар.

**Данışман Değerlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 14. Hafta/Апта

**Аткарылган иштер:**

Performance оптимизациясы жана масштабдоо боюнча иштер жүргүздүм. Spark UI (порт 4040) аркылуу job'лордун аткаруу планын талдадым - DAG (Directed Acyclic Graph) визуализациясы, stages, tasks. Bottleneck таптым - эң узак аткарылган stage же task. Memory жана CPU колдонууну мониторинг кылдым - Driver жана Executor logs.

Оптимизация техникаларын колдондум - Partitioning: маалыматтарды туура бөлүштүрдүм (repartition vs coalesce, optimal partition саны - 2-3x ядролордун саны). Caching жана persistence колдондум - frequently колдонулган DataFrame'лерди memory'де сактоо (cache(), persist()). Broadcast variables колдондум - кичинекей маалыматтарды бардык executor'лорго жөнөтүү, join операцияларын оптималдаштыруу. Data skewness менен күрөштүм - бир partition башкалардан чоң болсо (salting техникасы). Hive таблицаларын compaction жана ANALYZE TABLE статистика жыйнадым. Cluster ресурстарын эффективдүү бөлүштүрдүм - executor саны, memory, cores.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başarісız / Ийгиликсиз

---

### 15. Hafta/Апта

**Аткарылган иштер:**

Apache Airflow менен таанышып, workflow orchestration платформасын үйрөндүм. Airflow'дун Big Data системаларында pipeline'дарды автоматташтыруу ролун түшүндүм. Docker'де Airflow орнотуп, биринчи DAG түздүм - daily ЭСФ ETL pipeline. BashOperator, PythonOperator, SparkSubmitOperator колдондум. Task dependencies, retry logic жана alerting конфигурациялоодум.

**Данışман Değerlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 16. Hafta/Апта

**Аткарылган иштер:**

Airflow менен production-level fraud detection workflow автоматташтырдым - ЭСФ жүктөө, тазалоо, feature engineering, ML prediction, билдирүү жөнөтүү. Airflow'дун кошумча мүмкүнчүлүктөрүн үйрөндүм - SubDAGs, TaskGroups, XComs. Production deployment боюнча иштер жасадым - Git integration, CI/CD pipeline. Долбоорду жыйынтыктап, толук документация жана презентация даярдадым. Код база GitHub'га жүктөп, финалдык архитектуралык диаграмма түздүм.

**Данışман Değerlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başarісız / Ийгиликсиз

---

## Danışman Öğretim Üyesi'nin Görüşleri / Илимий жетекчисинин ой-пикири

[Жетекчинин комментарийлери]

---

## SONUÇ/ЖЫЙЫНТЫК:

**Başarılı/Ийгиликтүү:** ☐  
**Başarısız/Ийгиликсиз:** ☐

**Tarih/Дата:** ___/___/20___

**Danışman/Илимий жетекчи:** _______________

---

## ÖĞRENCİ TARAFINDAN HAZIRLANAN RAPOR/МАГИСТРАНТТЫН ОТЧЕТУ

Бул 16 жумалык практикада заманбап Big Data технологияларынын толук стегин терең үйрөндүм - Docker, Hadoop, Spark, Hive жана Apache Airflow. Биринчи жумалардан баштап контейнерлештирүү принциптери менен таанышып, андан кийин distributed системаларды орнотуп, конфигурациялоону үйрөндүм.

**Hadoop жана Spark архитектурасы боюнча түшүнүк:**

Hadoop экосистемасы менен иштөө мага distributed storage жана процесстөөнүн негиздерин үйрөттү. HDFS'тин fault-tolerance механизмдери - маалыматтар автоматтык түрдө репликацияланат, эгер бир нодд түшсө, башкалары жумушу улантат. Бул traditional системалардан (PostgreSQL, MySQL) негизги айырма - алар vertical scaling менен чектелген, ал эми Hadoop horizontal scaling берет, жаңы нодлорду кошуу менен системанын мүмкүнчүлүгүн арттырабыз.

Spark'тын архитектурасы өзгөчө кызыктуу болду - in-memory процесстөө MapReduce'тан он эселе тезирээк. Lazy evaluation концепциясы - Spark трансформацияларды дароо аткарбайт, бардык операцияларды жыйнап, оптималдаштырылган plan түзөт. Driver жана Executor модели - Driver координациялайт, Executor'лор параллель иштейт. Бул архитектура миллиондогон саптарды тез процесстөөгө мүмкүндүк берет.

**Электронный счет-фактура (ЭСФ) маалыматтарын талдоо:**

ЭСФ системалары күн сайын миллиондогон транзакцияларды генерациялайт. Traditional базалар мындай көлөмдү туура башкара албайт. Hadoop/Spark stack бул маселени чечет:

1. **Storage layer** - HDFS миллиардтаган саптарды distributed түрдө сактайт
2. **Processing layer** - Spark параллель түрдө процесстөөнү жүзөгө ашырат
3. **Query layer** - Hive SQL интерфейси берет, business analyst'лор колдонот
4. **Orchestration layer** - Airflow workflow'ларды автоматташтырат

Бул архитектура Data Engineer катары иштөө үчүн фундаменталдуу. Мен ETL pipeline'дарды түзүп, ЭСФ маалыматтарын тазалап, трансформациялап, аналитика үчүн даярладым. Partitioning стратегиясы - дата боюнча бөлүштүрүү суроолорду 10-20 эсе тездетти.

**Fraud Detection жана Machine Learning:**

Fraud detection практикасы өзгөчө баалуу болду. Feature engineering этапта түшүндүм - моделдин сапаты features'ке көз каранды. Spark window функциялары аркылуу time-series features түзүү - акыркы 7 күндүн орточо транзакциясы, максималдуу сумма, transaction frequency.

Spark MLlib менен моделдерди үйрөтүү distributed түрдө - бул чоң маалыматтар үчүн абсолют зарыл. Traditional scikit-learn бир машинанын RAM'ине чектелген (10-50 GB), ал эми Spark MLlib бүтүндөй кластердин ресурстарын колдонот (терабайттар). Random Forest жана Gradient Boosted Trees моделдери fraud patterns жакшы кармайт.

**Apache Airflow жана Production Workflows:**

Airflow менен таанышуу практиканын эң практикалык бөлүгү болду. Production'до бардык процесстер автоматташтырылган болууга тийиш - күн сайын жаңы ЭСФ маалыматтарын жүктөө, тазалоо, моделге киргизип, fraud detect кылуу, аналитиктерге билдирүү жөнөтүү. Cron jobs жетишсиз - алар dependency management, retry logic, monitoring бербейт.

Airflow DAG'лери бул маселелерди чечет. Мен толук fraud detection pipeline түздүм - 6-7 task'лар бир-бирине көз каранды, Airflow автоматтык туура тартипте аткарат. Эгер бир task fail болсо, Airflow retry кылат, эгер баары эле fail болсо, alert жөнөтөт. Web UI аркылуу бардык process'терди визуалдык көрүү - каалаган task'тын log'ун окуп, эмне болгонун түшүнөбүз.

**Data Engineer катары даярдык:**

Практика аяктаганда өзүмдү data engineer катары ишенимдүү сезем:

- **Infrastructure**: Docker менен системаларды контейнерлештирүү
- **Storage**: Hadoop HDFS'те петабайттык маалыматтарды башкаруу
- **Processing**: Spark менен масштабдуу ETL pipeline'дар түзүү
- **Analytics**: Hive менен SQL интерфейси аркылуу бизнес метрикалар эсептөө
- **ML**: Spark MLlib менен fraud detection моделдерин үйрөтүү
- **Orchestration**: Airflow менен production workflow'ларды автоматташтыруу

**Келечектеги пландар:**

Бул базаны real-time системалар менен толуктагым келет:

1. **Kafka + Spark Streaming** - ЭСФ маалыматтарын real-time процесстөө
2. **Cloud migration** - AWS EMR же GCP Dataproc'ко өткөрүү
3. **Advanced ML** - Deep Learning моделдери (TensorFlow + Spark)
4. **Data Governance** - Apache Atlas менен metadata башкаруу
5. **Monitoring** - Prometheus + Grafana интеграциясы

Бул практика мага data engineering карьерасы үчүн бекем негиз берди. Теория менен практиканын комбинациясы - архитектуралык принциптер жана real-world implementation - өзгөчө пайдалуу болду.

---

**İmza/Колу:** _______________

**Öğrencinin Adı Soyadı/Студенттин аты жөнү:** _______________

**Tarih/Дата:** ___/___/20___

---

*Kırgızistan-Türkiye Manas Üniversitesi Rektörlük © 2024*
