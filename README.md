# 3db - three DB

Небольшая БД для хранения и работы с данными используемыми при проведении [DDT](https://en.wikipedia.org/wiki/Data-driven_testing).

### Возможности хранения

### Плоский список фалов

```
data_1.txt
etalon_1.txt
data_2.txt
etalon_2.txt

или

0001_data.txt
0001_etalon.txt
0002_data.txt
0002_etalon.txt
```

### Плоская структура папок

```
0001_Single_Data/
    data_1.txt
    etalon_1.txt

0002_Few_Data/
    data_1.txt
    etalon_1.txt
    data_2.txt
    etalon_2.txt
```

### Дерево папок

```
ServiceA/
    0001_Single_Data/
        data_1.txt
        etalon_1.txt
    ....
ServiceB/
    0001_Single_Data/
        data_1.txt
        etalon_1.txt
    ....
IntegrationServiceAServiceB
    10001_ServiceAUp_ServiceBDown/
        data_1.txt
        etalon_1.txt
    10002_ServiceADown_ServiceBUp/
        data_1.txt
        etalon_1.txt
    ....
```
