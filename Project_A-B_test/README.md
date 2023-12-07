# Project_2_A-B_test
### Технологический Stack использованный в проекте:
![python](https://img.shields.io/badge/-python-090909?style=for-the-badge&logo=python&)
![MySQL](https://img.shields.io/badge/-SQL-090909?style=for-the-badge&logo=MySQL&)
![gitlab](https://img.shields.io/badge/-gitlab-090909?style=for-the-badge&logo=gitlab&)
### Основные цели:
1. Определение метрик;
2. Статистический анализ различий в показателях;
3. Решение о запуске новой механики.

### Полученные результаты:

1. Основные метрики: ARPU, ARPPU, CR;

2. В ходе анализа данных полученных при эксперименте, можно выделить следующие выводы: 
- Баг в системе сплитования - процентное соотношение пользователей в тестовой и контрольной группе значительно различается.
Рекомендация: наладить систему сплитования, провести дополнительно А-А тест и провести А_В тест заново.
- Проанализированны такие метрики как ARPU, ARPPU, CR. 
 В данном А-В тесте статистические различия есть только в метрике ARPPU, 
метрики ARPU  и  CR статистически не отличаются в тестовой и контрольной группе.
- Новая механика оплаты услуг на сайте существенно увеличивает метрику ARPPU на каждого платящего пользователя.
3. Вывод: провести А-В тест заново, с уже налаженной системой сплитования, и если в новом тесте результаты не изменяться, и метрика ARPPU так же существенно выше в тестовой группе (платящие пользователи с новой механникой покупают больше, чем контрольная группа) то стоит запускать новую механику оплаты на всех пользователей.