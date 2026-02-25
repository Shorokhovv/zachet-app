Инструкция по проверке работы
Ссылка на приложение:
https://silver-spoon-4xg466xvv5jhjqvr-8000.app.github.dev

Как пользоваться:

Перейдите по ссылке, нажмите "Continue" (предупреждение стандартное для Codespaces).

Откроется главная страница API.

Для проверки эндпоинтов дописывайте в адресную строку:
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

Проверка сохранения данных:
Перезапустите контейнеры (docker-compose down && docker-compose up -d) и снова откройте /pending и /stats — данные сохранятся благодаря Docker volume.