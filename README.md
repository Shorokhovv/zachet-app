Создать web-приложение “Мини-трекер задач (Todo API)”, развернуть его в GitHub Codespaces и запустить через Docker Compose.
Приложение должно работать с PostgreSQL и сохранять данные после перезапуска контейнеров.

Структура БД
Таблица:
tasks 
Поля:
id — SERIAL PRIMARY KEY title — TEXT done — BOOLEAN DEFAULT FALSE 

Endpoint’ы (обязательные)
1. /create/<title>
Создаёт задачу.
Пример:
/create/learn_docker 
Ответ:
created 
2. /done/<id>
Помечает задачу выполненной (done = true).
Пример:
/done/1 
Ответ:
updated 
3. /pending
Показывает только невыполненные задачи.
Пример ответа:
1 learn_docker 2 setup_postgres 
4. /stats
Возвращает статистику:
Пример:
total: 5 done: 2 pending: 3 

Бд в контейнере, volume, продемонстрировать, что данные сохраняются после перезапуска контейнера