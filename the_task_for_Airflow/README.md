# the_task_for_Airflow
### Технологический Stack использованный в проекте:
![python](https://img.shields.io/badge/-python-090909?style=for-the-badge&logo=python&)
![gitlab](https://img.shields.io/badge/-gitlab-090909?style=for-the-badge&logo=gitlab&)
![apacheairflow](https://img.shields.io/badge/-airflow-090909?style=for-the-badge&logo=apacheairflow&)
#### Использованные библиотеки:
- Pandas, numpy, timedelta, requests, BytesIO, dag, task, get_current_context, Variable, StringIO.
### Основные цели:
Cоставить DAG из нескольких тасок, в результате которого нужно будет найти ответы на следующие вопросы:
- Какая игра была самой продаваемой в этом году во всем мире?
- Игры какого жанра были самыми продаваемыми в Европе? Перечислить все, если их несколько
- На какой платформе было больше всего игр, которые продались более чем миллионным тиражом в Северной Америке?
Перечислить все, если их несколько
- У какого издателя самые высокие средние продажи в Японии?
Перечислить все, если их несколько
- Сколько игр продались лучше в Европе, чем в Японии?
### Полученные результаты:
 DAG состоит из 7 тасков. По одному на каждый вопрос, таск с загрузкой данных и финальный таск который собирает все ответы. 