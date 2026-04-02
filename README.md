# Habit-tracker -

Веб-приложение для отслеживания и формирования полезных привычек.

### Модель Привычки

* Пользователь: создатель привычки.
* Место: место выполнения привычки.
* Время: время выполнения привычки.
* Действие: действие привычки.
* Признак приятной привычки: флаг, указывающий, является ли привычка приятной.
* Связанная привычка: ссылка на приятную привычку, которая служит вознаграждением (доступно только для полезных
  привычек).
* Периодичность: частота выполнения привычки (в днях, по умолчанию ежедневно).
* Вознаграждение: чем пользователь может себя вознаградить после выполнения (доступно только для полезных привычек).
* Время на выполнение: максимальное время, которое должно быть потрачено на выполнение привычки (не более 120 секунд).
* Признак публичности: флаг, определяющий доступность привычки другим пользователям.

#### Типы привычек:

- Полезная привычка: основное действие, которое может сопровождаться вознаграждением или связанной приятной привычкой.
- Приятная привычка: способ вознаграждения, который не может иметь собственного вознаграждения или связанной привычки.

#### Валидация:

- Нельзя одновременно указывать вознаграждение и связанную привычку для одной привычки.
- Время на выполнение должно быть ≤ 120 секунд.
- Связанные привычки могут быть только типа "приятная".
- Приятные привычки не могут иметь вознаграждение или связанную привычку.
- Периодичность должна быть ≥ 1 раза в 7 дней (то есть, минимум раз в неделю).

#### Пагинация:

- Вывод списка привычек осуществляется по 5 элементов на страницу.

#### Права доступа:

- CRUD операции (Создание, Чтение, Обновление, Удаление) доступны только для собственных привычек пользователя.
- Просмотр публичных привычек доступен всем пользователям без возможности редактирования.

#### Интеграции:

- Telegram-бот: Для отправки напоминаний о выполнении привычек.
- Celery: Для обработки отложенных задач (например, отправка напоминаний, обработка периодических проверок).
- CORS: Для обеспечения возможности взаимодействия фронтенда с API.
- Автодокументация API: Генерация документации (например, с использованием Swagger/OpenAPI).

#### Подключены сторонние пакеты:

- Django REST Framework — для реализации API
- django-filter — для расширенной фильтрации данных настроена обработка
  медиафайлов для загрузки изображений и аватаров

#### Технологический Стек:

- Backend: Python (Django REST Framework)
- База данных: PostgreSQL (предпочтительно)
- Кэширование: Redis
- Очередь задач: Celery с Redis
- Управление зависимостями: Poetry
- API документирование: drf-yasg (Swagger/OpenAPI)

#### Тестирование: coverage

Покрытие тестами составляет более 80%. Тестирование всех CRUD операций, валидация данных, бизнес-логика и интеграции.

### Установка и Запуск:

Данный проект использует Poetry для управления зависимостями.

- Клонируйте репозиторий: git clone https://github.com/PavelOleynikov/Habit-tracker cd Habit-tracker
- Создайте и активируйте виртуальное окружение: python -m venv venv source venv/bin/activate - для Linux/macOS;
  venv\Scripts\activate - для Windows
- Установите зависимости с помощью Poetry:
  poetry install
- Настройте переменные окружения. Рекомендуется использовать файл .env и установить переменную DJANGO_SETTINGS_MODULE в
  соответствии
  с вашим файловым путем.
- Примените миграции базы данных: poetry run python manage.py migrate
- Запустите сервер разработки
  Django: poetry run python manage.py runserver
- Для работы напоминаний и отложенных задач, запустите Celery worker и Celery beat:
  Убедитесь, что Redis запущен
  poetry run celery -A config worker -l info
  poetry run celery -A config beat -l info
- Для запуска всех тестов: poetry run python manage.py test

  Перед запуском скопируйте `.env.example` в `.env` и укажите свои значения

### Запуск проекта с использованием Docker Compose

Файл docker-compose.yaml определяет конфигурацию для запуска всех необходимых сервисов вашего проекта: веб-приложения
Django, базы данных PostgreSQL, Nginx, Redis и Celery (worker и beat).

Предварительные требования:

- Docker установлен и работает.
- Docker Compose установлен (обычно входит в состав Docker Desktop).
- Файл .env с необходимыми переменными окружения (например, NAME, DB_USER, PASSWORD).

Процесс запуска

- сборка и запуск всех сервисов -
  перейдите в корневую директорию вашего проекта (где находится файл docker-compose.yaml и Dockerfile).

- Затем выполните следующую команду:
  docker compose up -d --build или docker compose -f docker-compose.yaml up

* API будет доступно по адресу: http://localhost:8000/
* Для авторизации используйте полученный при регистрации email и пароль
* Для доступа к админке используйте адрес: http://localhost:8000/admin/

Проверка сервисов

- docker compose ps — все контейнеры должны быть в статусе Up
- docker compose logs -f web — логи Django
- docker compose logs -f celery — логи Celery

Команды

- Остановка: docker compose down и удаление контейнеров
- Перезапуск: docker compose restart
- Миграции: docker compose exec web python manage.py migrate
- Суперпользователь: docker compose exec web python manage.py createsuperuser

### Настройка удаленного сервера

  Требования

- Ubuntu 22.04/24.04 LTS
- Docker и Docker Compose
- Открыты порты: 22 (SSH), 8080 (HTTP)

Установка Docker и Docker Compose

Обновление системы
* sudo apt update && sudo apt upgrade -y

Установка Docker
* curl -fsSL https://get.docker.com -o get-docker.sh
* sudo sh get-docker.sh
* sudo usermod -aG docker $USER

Установка Docker Compose
* sudo apt install docker-compose-plugin -y

Проверка установки

* docker --version
* docker compose version

### Клонирование проекта на сервер

Клонирование репозитория
* git clone https://github.com/PavelOleynikov/Habit-tracker.git
* cd Habit-tracker

Настройка .env
* cp .env.example .env
  - Отредактируйте .env с вашими значениями

Запуск проекта
* docker compose up -d --build
* docker compose exec web python manage.py migrate
* docker compose exec web python manage.py collectstatic --noinput
* docker compose exec web python manage.py createsuperuser

### Раздел "CI/CD Pipeline (GitHub Actions)"

```markdown

Файл `.github/workflows/ci.yml`:

| Job | Описание |
|-----|----------|
| **lint** | Проверка кода flake8 |
| **test** | Запуск тестов Django |
| **build** | Сборка и публикация Docker образа |
| **deploy** | Деплой на сервер через SSH |

### Secrets GitHub
- `SECRET_KEY` — ключ Django
- `DOCKER_HUB_USERNAME` — логин Docker Hub
- `DOCKER_HUB_ACCESS_TOKEN` — токен Docker Hub
- `SSH_KEY` — приватный ключ
- `SSH_USER` — пользователь сервера
- `SERVER_IP` — IP сервера

### Процесс деплоя
1. Push → запуск workflow
2. Линтинг → тесты → сборка образа → публикация в Docker Hub → деплой на сервер

### Мониторинг деплоя

# На сервере
cd ~/Habit-tracker
docker compose ps
docker compose logs -f web
docker compose logs -f nginx

* API будет доступно по адресу: http://213.165.220.82:8080/
* Для авторизации используйте полученный при регистрации email и пароль
* Для доступа к админке используйте адрес: http://213.165.220.82:8080/admin/
* API документация: http://213.165.220.82:8080/swagger/

👤 Автор
Pavel Oleynikov