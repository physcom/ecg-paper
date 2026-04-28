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

Docker платформасы менен таанышып, иштөө чөйрөсүн даярдадым. Docker Desktop орноттум, негизги командалар менен иштедим (docker run, pull, ps, images, logs, exec). Контейнерлердин принциптерин үйрөндүм - изоляция, портативдүүлүк, микросервистер архитектурасы.

Dockerfile түзүп, custom образдарды билдирүү практикасын өздөштүрдүм. Docker Compose менен таанышып, бир нече сервистерди ыңгайлуу башкарууну үйрөндүм. Портторду маплоо, volume'дарды колдонуу жана docker network түшүнүгүн практикада колдондум. Big Data системаларын Docker'де иштетүүнүн артыкчылыктарын түшүндүм - тез deployment, версиялык контроль, ресурстарды изоляциялоо.

**Данışман Değerlendirilmesi/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başarısız / Ийгиликсиз

---

### 2. Hafta/Апта

**Аткарылган иштер:**

Hadoop экосистемасы менен терең таанышып чыктым. Distributed computing концепциясын жана анын заманбап маалыматтарды процесстөөдөгү милдетин түшүндүм. HDFS (Hadoop Distributed File System) архитектурасын үйрөндүм - NameNode (метамаалыматтарды башкаруу), DataNode (маалыматтарды сактоо), блоктордун репликациясы (default 3 копия).

Docker контейнерлеринде Hadoop кластерин орноттум. Multi-node конфигурация түздүм (1 NameNode + 2-3 DataNode) Docker Compose файлы аркылуу. HDFS командалары менен практикалык иш жүргүздүм - hdfs dfs -ls, -mkdir, -put, -get, -cat, -rm. Чоң файлдарды жүктөп, алардын автоматтык түрдө бөлүктөргө бөлүнүп, репликацияланышын байкадым.

**Данışман Değерlendirilmesi/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başarısız / Ийгиликсиз

---

### 3. Hafta/Апта

**Аткарылган иштер:**

Apache Spark менен таанышып, анын Hadoop экосистемасындагы ролун түшүндүм. Spark архитектурасынын компоненттерин үйрөндүм - Driver (мастер процесс, кодду координациялайт), Executors (иштөөчү процесстер), Cluster Manager (ресурстарды бөлүштүрүү). RDD (Resilient Distributed Datasets) концепциясын өздөштүрдүм - immutability, lazy evaluation, fault tolerance.

Docker контейнерлеринде Spark кластерин Standalone режимде орноттум. Spark Master жана Worker ноддорун конфигурациялап, веб-интерфейстерге кирдим (Master UI: 8080, Worker UI: 8081). PySpark орнотуп, Jupyter Notebook менен интеграциялап иштедим. Биринчи Spark приложенияларын жаздым - классикалык Word Count мисалын RDD API аркылуу аткардым. Spark'тын MapReduce'тан негизги артыкчылыгын практикада көрдүм - in-memory процесстөө, ал эми MapReduce ар бир операциядан кийин дискке жазат.

**Данışман Değerlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарısız / Ийгиликсиз

---

### 4. Hafta/Апта

**Аткарылган иштер:**

Spark DataFrames API менен терең иштедим - бул SQL-сымал абстракция RDD үстүнөн. DataFrame түзүүнү ар түрдүү булактардан үйрөндүм - CSV, JSON, Parquet, JDBC. Schema аныктоону өздөштүрдүм (явный жана автоматтык inferSchema). Маалымат типтери менен иштедим - StructType, StructField.

PySpark DataFrames трансформацияларын практикада колдондум - select, filter, where, groupBy, agg, join, union, distinct. Aggregation функцияларын колдондум - count, sum, avg, max, min, collect_list, collect_set. Window функцияларын иштетип көрдүм - ROW_NUMBER, RANK, DENSE_RANK, LEAD, LAG, партицияларды аныктоо. UDF (User Defined Functions) түздүм - Python функцияларын Spark'ка интеграциялоо. Чоң маалыматтарды процесстөп, натыйжаларды файлга жаздым - coalesce аркылуу partition санын контроллдодум.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарısız / Ийгиликсиз

---

### 5. Hafta/Апта

**Аткарылган иштер:**

Apache Hive менен таанышып чыктым - HDFS үстүнөн SQL интерфейси берүүчү data warehouse система. Hive архитектурасын үйрөндүм - Metastore (таблица метамаалыматтары Derby же PostgreSQL'де сакталат), HiveServer2 (клиенттер менен өз ара аракеттенүү), Beeline (CLI клиенти). HiveQL синтаксисин өздөштүрдүм - SQL'ге окшош, бирок MapReduce же Tez же Spark үстүндө аткарылат.

Docker'де Hive орнотуп, конфигурациялоодум. PostgreSQL же Derby метастор түздүм. Биринчи таблицаларды түздүм - EXTERNAL таблицалар (маалыматтар HDFS'те калат) жана MANAGED таблицалар (Hive башкарат). CSV же JSON файлдарын Hive таблицаларына жүктөдүм - LOAD DATA, INSERT INTO. Partitioning концепциясын практикада колдондум - таблицаларды логикалык бөлүктөргө бөлүү (мисалы, дата боюнча), бул суроолорду тездетет. Bucketing - partitioning'дин кошумча деңгээлин үйрөндүм.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başarісız / Ийгиликсиз

---

### 6. Hafta/Апта

**Аткарылган иштер:**

Hive менен татаал аналитикалык суроолорду жаздым. JOIN операцияларын колдондум - INNER, LEFT, RIGHT, FULL OUTER, CROSS. Подзапросы (subqueries) иштетип чыктым - WHERE, FROM, SELECT ичинде. UNION жана UNION ALL операцияларын практикада колдондум. Аналитикалык функцияларды үйрөндүм - ROW_NUMBER(), RANK(), DENSE_RANK(), LEAD(), LAG(), FIRST_VALUE(), LAST_VALUE().

Hive оптимизациясы техникаларын колдондум. Партициялоо стратегияларын иштеп чыктым - көп колдонулган суроолор боюнча эң эффективдүү partition scheme тандадым. ORC (Optimized Row Columnar) жана Parquet форматтарынын артыкчылыктарын практикада көрдүм - компрессия, columnar storage, predicate pushdown. Vectorization иштеттим - бир эле убакта бир нече саптарды процесстөө. CBO (Cost-Based Optimizer) жөндөдүм - статистика жыйнап, план оптималдаштырууну үйрөндүм.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 7. Hafta/Апта

**Аткарылган иштер:**

Spark жана Hive интеграциясын ишке ашырдым - эки системанын күчтүү жактарын бириктирдим. SparkSession конфигурациялап, Hive Metastore менен иштөөнү жөндөдүм - enableHiveSupport() методун колдондум. Hive таблицаларын Spark DataFrames катары окуп иштедим - spark.sql() жана spark.table() аркылуу. Spark'та процесстөөнүн артыкчылыктарын практикада көрдүм - in-memory, MLlib кашаанасы.

Spark'тан натыйжаларды Hive'ге кайра жаздым - saveAsTable(), insertInto() методдорун колдондум. Hybrid pipeline архитектурасын түздүм - Hive ETL (батч процесстөө, сактоо) + Spark аналитика (тез процесстөө, ML). Кайсы учурда кайсы инструментти колдонуу керектигин практикада үйрөндүм - Hive ad-hoc суроолор жана долгосрочное сактоо үчүн, Spark татаал трансформациялар жана машиналык үйрөнүү үчүн.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 8. Hafta/Апта

**Аткарылган иштер:**

Электронный счет-фактура (ЭСФ) маалыматтары менен иштөө практикасын баштадым - Big Data технологияларынын реалдуу колдонуусу. Hadoop архитектурасынын миллиондогон ЭСФ маалыматтарын эффективдүү сактоо жана процесстөө артыкчылыктарын практикада көрдүм. HDFS'тин distributed storage принцибин түшүндүм - маалыматтар автоматтык түрдө бир нече ноддордо репликацияланат (default 3 копия), бул fault-tolerance жана жогорку жеткиликтүүлүктү камсыз кылат.

Data Engineering перспективасын өздөштүрдүм - ЭСФ системалары күн сайын миллиондогон транзакцияларды генерациялайт. Traditional системалар (PostgreSQL, MySQL) мындай көлөмдү туура башкара албай турганын түшүндүм - вертикалдык масштабдоо чектүү. Hadoop horizontal scaling берерин практикада көрдүм - жаңы нодлорду кошуу менен системанын мүмкүнчүлүгүн арттырдым. ЭСФ маалыматтарын HDFS'ке жүктөп, Hive'де structured таблицаларга өткөрдүм. Партициялоо стратегиясын ишке ашырдым - дата жана контрагент боюнча, бул келечекте тез суроолорду жүзөгө ашырууга мүмкүндүк берди.

**Данışман Değerlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başarісız / Ийгиликсиз

---

### 9. Hafta/Апта

**Аткарылган иштер:**

ЭСФ маалыматтарын тазалоодум жана трансформациялоодум - ETL (Extract, Transform, Load) процессин ишке ашырдым. PySpark'тын distributed процесстөө мүмкүнчүлүктөрүн колдондум - бир task бир ноддо эмес, бардык кластерде параллель аткарылат. Spark'тын lazy evaluation концепциясын өздөштүрдүм - трансформациялар дароо аткарылбайт, action чакырылганга чейин план түзүлөт, андан кийин оптималдаштырылган plan аткарылат.

Маалыматтарды стандарттоодум - дата форматтары, суммалар, валюталар. Data quality текшердим - логикалык consistency, null баалуулуктарды каалоо. Дубликаттарды таптым - dropDuplicates() же window функциялары аркылуу. Spark DataFrames менен комплекстүү ETL pipeline түздүм - бир нече source'тардан окуу, join, трансформация, validation, Hive'ге жазуу. Бул pipeline келечекте fraud detection үчүн тазаланган маалыматтарды камсыз кылат.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 10. Hafta/Апта

**Аткарылган иштер:**

ЭСФ маалыматтарынан бизнес инсайттарды чыгардым. Spark SQL менен аналитикалык суроолорду жаздым - контрагенттер боюнча транзакциялар, убакыт боюнча трендлер, региондор боюнча көрсөткүчтөр. Aggregation логикасы distributed түрдө аткарылат - ар бир executor өз partition'унда локалдык аггрегацияны жасайт, андан кийин driver жыйынтыктайт.

Татаал аналитикалык суроолорду иштеп чыктым - time-series тенденциялар (күн, жума, ай, квартал боюнча динамика), moving averages, growth rate. Window функцияларын колдондум - PARTITION BY date ORDER BY amount. Географиялык аналитиканы жүргүздүм - регион же шаар боюнча сатуулар. HiveQL жана Spark SQL'ди салыштырдым - код окшош, бирок execution engine башка (Hive - MapReduce/Tez, Spark - in-memory).

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 11. Hafta/Апта

**Аткарылган иштер:**

Алдамчылыкты (fraud) аныктоо үчүн feature engineering жүргүздүм. Электронный счет-фактураларда fraud patterns'тарды изилдедим - адаттан тыш чоң суммалар, бейтааныш контрагенттер, түндө транзакциялар, географиялык аномалиялар, такталбаган КДВ эсептөөлөр. Big Data архитектурасынын бул маселелерди кантип чечээрин түшүндүм - тарыхый миллиондогон транзакцияларды анализдеп, patterns табуу.

Anomaly detection техникаларын колдондум - statistical методдор (Z-score, IQR), time-series методдор (сезондуулукту эске алуу). Spark DataFrame API менен features түздүм - transaction frequency, average amount, time patterns, counterparty relationships. Window функцияларын колдонуп - акыркы N транзакциялардын статистикасы. Бул features келечекте машиналык үйрөнүү моделдерине киреди.

**Данışман Değерlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 12. Hafta/Апта

**Аткарылган иштер:**

Spark MLlib аркылуу машиналык үйрөнүү моделдерин fraud detection үчүн колдондум. MLlib менен иштедим - Spark'тын distributed машиналык үйрөнүү кашаанасы, ал масштабдуу маалыматтар менен иштей алат (traditional scikit-learn бир машинада ишке ашат). Classification моделдер - Logistic Regression, Random Forest, Gradient Boosted Trees.

Data Engineering перспективасынан иш жүргүздүм - чоң маалыматтарды үйрөтүү (training) үчүн Spark'тын distributed алгоритмдерин колдонуу. Pipeline API колдондум - ETL жана ML'ди бир workflow'до бириктирүү (VectorAssembler, StandardScaler, StringIndexer). Model training distributed түрдө жүргүздүм - ар бир executor training dataset'тин бир partition'унда иштейт. Cross-validation жана hyperparameter tuning жүргүздүм - ParamGridBuilder жана TrainValidationSplit. Model evaluation жасадым - accuracy, precision, recall, F1-score, ROC-AUC. Үйрөтүлгөн моделди HDFS'ке сактадым - келечекте production'до колдонуу үчүн.

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

Apache Airflow менен таанышып чыктым - workflow orchestration платформасы. Airflow'дун Big Data системаларындагы ролун түшүндүм - татаал data pipeline'дарды автоматташтыруу, schedule кылуу, мониторинг кылуу. Эмне үчүн Airflow керектигин түшүндүм - cron jobs жетишсиз (no dependency management, no retry logic, no monitoring). Airflow концепцияларын үйрөндүм - DAG (Directed Acyclic Graph), Tasks, Operators, Dependencies.

Docker'де Airflow орноттум. Биринчи DAG түздүм - daily ЭСФ ETL pipeline (HDFS'тен окуу → Spark'та тазалоо → Hive'ге жазуу → отчет генерациялоо → email жөнөтүү). BashOperator, PythonOperator, SparkSubmitOperator колдондум. Task dependencies аныктадым - set_upstream(), set_downstream(), >> оператору. Airflow UI аркылуу DAG'лерди мониторинг кылдым - task status, logs, execution time. Retry logic жана alerting конфигурациялоодум.

**Данışман Değerlendirilмеси/Баалоо:**
- ☐ Başarılı / Ийгиликтүү
- ☐ Başарісız / Ийгиликсиз

---

### 16. Hafta/Апта

**Аткарылган иштер:**

Airflow менен татаал production-level pipeline'дарды долборлоодум. Fraud detection workflow автоматташтырдым - (1) Жаңы ЭСФ маалыматтарын HDFS'ке жүктөө, (2) Spark ETL аркылуу тазалоо, (3) Feature engineering, (4) MLlib моделине киргизип prediction алуу, (5) Подозрительные транзакцияларды флагдоо, (6) Аналитиктерге билдирүү жөнөтүү. Бул бүтүндөй workflow бир DAG ичине киргиздим - ар бир task башкаларга көз каранды, Airflow автоматтык түрдө туура тартипте аткарат.

Airflow'дун кошумча мүмкүнчүлүктөрүн үйрөндүм - SubDAGs (чоң DAG'лерди модулдарга бөлүү), TaskGroups (визуализацияны жакшыртуу), XComs (task'лар арасында маалымат өткөрүү), Dynamic DAGs (параметрлер боюнча DAG генерациялоо). Monitoring жана troubleshooting жүргүздүм - task logs карап, ката себептерин табуу, retry конфигурациялоо. Production deployment боюнча иштер жасадым - Git integration, CI/CD pipeline (automated testing, deployment), environment variables (dev, staging, prod).

Долбоорду жыйынтыктап, документтештирдим. Толук архитектуралык диаграмма түздүм - Docker контейнерлери, Hadoop кластери, Spark кластери, Hive metastore, Airflow scheduler, data flow. Код база GitHub'га жүктөдүм - README, requirements.txt, docker-compose.yml. Финалдык презентация даярдадым - проблема (чоң ЭСФ маалыматтарын процесстөө, fraud detection), чечим (Hadoop/Spark/Hive/Airflow stack), натыйжалар, үйрөнгөн практикалар, келечектеги өркүндөтүүлөр (Kafka + Spark Streaming, cloud migration, ML моделдердин жакшыртылышы).

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
