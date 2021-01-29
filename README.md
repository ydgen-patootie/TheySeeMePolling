## TheySeeMePolling

## Инструкция по разворачиванию приложения

1. Запустить командную строку
2. Перейти в основной каталог приложения (где находится файл requirements.txt) 
cd .....TheySeeMePolling
3. Выполнить pip install -r requirements.txt для установки необходимых пакетов (если они еще не установлены)
4. Перейти во вложенную папку TheySeeMePolling (где находится файл manage.py)
cd .....TheySeeMePolling\TheySeeMePolling
5. Выполнить python manage.py migrate
python manage.py createsuperuser <имя пользователя> <пароль> <почта>
python manage.py runserver 
Не закрывать командную строку
6. http://127.0.0.1:8000/admin/ для наполнения данных вручную

## Документация по API

# Получение токена пользователя
http://127.0.0.1:8000/api/login/
Запрос GET
Тело запроса:
username:<имя пользователя>
password:<пароль пользователя>

Пример с помощью requests:
data = {"username":"Vladimir", "password":"123456"}
headers = {'Content-type': 'application/json'}
r = client.get("http://127.0.0.1:8000/api/login/", data=json.dumps(data), headers=headers)

# Получение списка опросов (только актуальных на момент выполнения запроса)
http://127.0.0.1:8000/api/polls/
Запрос GET
заголовок запроса:
Authorization: Token <имя пользователя>

Пример с помощью requests:
headers = {'Authorization': 'Token ' + my_session_id}
r = requests.get('http://127.0.0.1:8000/api/polls/', headers=headers)
 
# Создание опроса
http://127.0.0.1:8000/api/polls/create_poll/'
Запрос POST
заголовок запроса:
Authorization: Token <имя пользователя>
Тело запроса:
name:<название опроса>
start_date:<дата старта, формат YYYY-MM-DDThh:mm:ss. После создания опроса изменить будет нельзя>
end_date:<дата окончания, формат YYYY-MM-DDThh:mm:ss>
description:<описание, необязательное>

Пример с помощью requests:
url = 'http://127.0.0.1:8000/api/polls/create_poll/'
headers = {
       "Content-Type": "application/json",
       'Authorization': 'Token ' + my_session_id,
   }
data = {
     "name":'Опросы Гордона',
     "start_date":'2019-09-04T00:00:00+0100',
     "end_date":'2042-09-04T00:00:00+0100',
 }
r = requests.post(url, headers=headers, data=json.dumps(data)) 

# Изменение опроса
http://127.0.0.1:8000/api/polls/update_poll/<id опроса>/
Запрос PUT
заголовок запроса:
Authorization: Token <имя пользователя>
Тело запроса:
name:<название опроса>
end_date:<дата окончания, формат YYYY-MM-DDThh:mm:ss>
description:<описание, необязательное>

Пример с помощью requests:
url = 'http://127.0.0.1:8000/api/polls/update_poll/2/'
headers = {
       "Content-Type": "application/json",
       'Authorization': 'Token ' + my_session_id,
   }
data = {
     "name":'Опросы Гордона!',
     "end_date":'2042-09-05T00:00:00+0100',
 }
r = requests.put(url, headers=headers, data=json.dumps(data)) 

# Удаление опроса
http://127.0.0.1:8000/api/polls/update_poll/<id опроса>/
Запрос DELETE
заголовок запроса:
Authorization: Token <имя пользователя>

Пример с помощью requests:
url = 'http://127.0.0.1:8000/api/polls/update_poll/2/'
headers = {
       "Content-Type": "application/json",
       'Authorization': 'Token ' + my_session_id,
   }
r = requests.delete(url, headers=headers) 

# Создание вопроса
http://127.0.0.1:8000/api/questions/create_question/
Запрос POST
заголовок запроса:
Authorization: Token <имя пользователя>
Тело запроса:
poll:<id опроса>
text:<текст вопроса>
qtype:<тип вопроса, TA - для вопроса с вводом ответа, PO - для вопроса с выбором варианта, PA - для вопроса с выбором нескольких вариантов>

Пример с помощью requests:
url = 'http://127.0.0.1:8000/api/questions/create_question/'
headers = {
       "Content-Type": "application/json",
       'Authorization': 'Token ' + my_session_id,
   }
data = {
     "poll":'2',
     "text":'Как вы можете описать условия?',
     "qtype":'PA',
 }
r = requests.post(url, headers=headers, data=json.dumps(data)) 

# Изменение вопроса
http://127.0.0.1:8000/api/questions/update_question/<id вопроса>/
Запрос PUT
заголовок запроса:
Authorization: Token <имя пользователя>
Тело запроса:
poll:<id опроса>
text:<текст вопроса>
qtype:<тип вопроса, TA - для вопроса с вводом ответа, PO - для вопроса с выбором варианта, PA - для вопроса с выбором нескольких вариантов>

Пример с помощью requests:
url = 'http://127.0.0.1:8000/api/questions/update_question/2/'
headers = {
       "Content-Type": "application/json",
       'Authorization': 'Token ' + my_session_id,
   }
data = {
     "poll":'2',
     "text":'Как вы можете описать условия?',
     "qtype":'PO',
 }
r = requests.put(url, headers=headers, data=json.dumps(data)) 

# Удаление вопроса
http://127.0.0.1:8000/api/questions/update_question/<id вопроса>/
Запрос DELETE
заголовок запроса:
Authorization: Token <имя пользователя>

Пример с помощью requests:
url = 'http://127.0.0.1:8000/api/questions/update_question/2/'
headers = {
       "Content-Type": "application/json",
       'Authorization': 'Token ' + my_session_id,
   }
r = requests.delete(url, headers=headers) 

# Создание выбора (варианта ответа)
http://127.0.0.1:8000/api/choices/create_choice/
Запрос POST
заголовок запроса:
Authorization: Token <имя пользователя>
Тело запроса:
question:<id вопроса>
choice:<текст варианта ответа>

Пример с помощью requests:
url = 'http://127.0.0.1:8000/api/choices/create_choice/'
headers = {
       "Content-Type": "application/json",
       'Authorization': 'Token ' + my_session_id,
   }
data = {
     "question":'3',
     "choice":'Как в бараке',
 }
r = requests.post(url, headers=headers, data=json.dumps(data)) 

# Изменение выбора (варианта ответа)
http://127.0.0.1:8000/api/choices/update_choice/<id вопроса>/
Запрос PUT
заголовок запроса:
Authorization: Token <имя пользователя>
Тело запроса:
question:<id вопроса>
choice:<текст варианта ответа>

Пример с помощью requests:
url = 'http://127.0.0.1:8000/api/questions/update_question/2/'
headers = {
       "Content-Type": "application/json",
       'Authorization': 'Token ' + my_session_id,
   }
data = {
     "question":'3',
     "choice":'Как в бараке',
 }
r = requests.put(url, headers=headers, data=json.dumps(data)) 

# Удаление выбора (варианта ответа)
http://127.0.0.1:8000/api/choices/update_choice/<id вопроса>/
Запрос DELETE
заголовок запроса:
Authorization: Token <имя пользователя>

Пример с помощью requests:
url = 'http://127.0.0.1:8000/api/choices/update_choice/5/'
headers = {
       "Content-Type": "application/json",
       'Authorization': 'Token ' + my_session_id,
   }
r = requests.delete(url, headers=headers) 

# Получение списка ответов (по идентификатору пользователя)
http://127.0.0.1:8000/api/answers/<id пользователя>/
Запрос GET
заголовок запроса:
Authorization: Token <имя пользователя>

Пример с помощью requests:
headers = {'Authorization': 'Token ' + my_session_id}
r = requests.get('http://127.0.0.1:8000/api/answers/1/', headers=headers)

# Создание ответа
http://127.0.0.1:8000/api/answers/create_answer/
Запрос POST
заголовок запроса:
Authorization: Token <имя пользователя>
Тело запроса:
user_id:<id пользователя, 0 для анонимного ответа>
poll:<id опроса>
question:<id вопроса>
choice:<id выбора, может быть null если предполагается вопрос с вводом ответа (TA)>
answer:<тестовый ответ, может быть пустым, если предполагается вопрос с выбором варианта (PO, PA)>
Если используется вопрос с выбором нескольких вариантов, то каждый выбранный вариант ответа нужно посылать отдельным запросом, см. пример ниже.

Пример с помощью requests:
url = 'http://127.0.0.1:8000/api/answers/create_answer/'
headers = {
       "Content-Type": "application/json",
       'Authorization': 'Token ' + my_session_id,
   }
data = {
     "user_id":'209',
     "poll":'1',
     "question":'1',
     "choice":'1',
     "answer":'',
 }
 data1 = {
     "user_id":'209',
     "poll":'1',
     "question":'1',
     "choice":'2',
     "answer":'',
 }
r = requests.post(url, headers=headers, data=json.dumps(data)) 
r = requests.post(url, headers=headers, data=json.dumps(data1)) 

