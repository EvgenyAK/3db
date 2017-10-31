# 3db - three DB

Небольшая БД для хранения и работы с данными используемыми при проведении [DDT](https://en.wikipedia.org/wiki/Data-driven_testing).

## Возможности хранения

### Плоский список файлов

```
числовой индекс

data_1.txt
etalon_1.txt
data_2.txt
etalon_2.txt

или в начале

0001_data.txt
0001_etalon.txt
0002_data.txt
0002_etalon.txt

или буквенный

data_A.txt
etalon_A.txt
data_B.txt
etalon_B.txt
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
IntegrationServiceAServiceB/
    10001_ServiceAUp_ServiceBDown/
        data_1.txt
        etalon_1.txt
    10002_ServiceADown_ServiceBUp/
        data_1.txt
        etalon_1.txt
    10003_ServiceAUp_ServiceBUp/
        data_A_1.txt
        etalon_A_1.txt
        data_B_1.txt
        data_B_1.txt
    ....
Some/
    BugFix44/
        ServiceA/
            data_1.txt
            etalon_2.txt
        ServiceB/
            data_2.txt
            etalon_2.txt
    ServiceD
        001_A/
            data_1.txt
            etalon_1.txt
```

## Тегирование данных

Часто удобно тегировать данные и производить выборки по произвольным тагам.
Теги прописываюися в фале *metadata.yaml*.
```
$ cat metadata.yaml

# навесить на все тесты таг serviceA
tags:
    - serviceA
0001:
   # теги навесить только на serviceA, serviceB
   tags:
       - serviceA
       - serviceB
0002:
   # Исключить таг serviceC
   tags:
       - serviceC:false
```

### Древовидная структура metadata.yaml
Поддержка нескольких вложенных файлов metadata.yaml для удобства разнесения тегов данных.

```
Some/
    metadata.yaml # tags: notci
    BugFix44/
        metadata.yaml # tags: bugfix
        ServiceA/
            data_1.txt
            etalon_2.txt
        ServiceB/
            data_2.txt
            etalon_2.txt
    ServiceD
        001_A/
            data_1.txt
            etalon_1.txt
```
