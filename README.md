# FastAPI Online Store

Проект FastAPI, реализующий функционал интернет магазина.

Функционал:

+ Регистрация, аутентификация пользователей
+ Добавление товаров в ассортимент оператором
+ Добавление товаров в корзину
+ Размещение заказов
+ Отправка сообщения с информацией о заказе на электронную почту клиента
+ Разделение и ограничение доступа к ресурсам относительно роли пользователя

Используется:

+ Python3.11
+ Аутентификация по JWT
+ Пагинация (fastapi_pagination)
+ PostgreSQL 
+ SQLAlchemy
+ Alembic
+ Redis
+ Docker
+ pytest
+ pytest-cov
+ factory-boy


## Развертывание

1. В корне создать файл `.env` с переменными окружения

        
        POSTGRES_DATA_VOLUME=
        POSTGRES_DB=
        POSTGRES_USER=
        POSTGRES_PASSWORD=
        DB_HOST=
        
        JWT_SECRET_KEY=
        
        REDIS_HOST=
        REDIS_DATA_VOLUME=
        
        STATIC_FILES_VOLUME=
        LOGS_VOLUME=
        
        MAIL_USERNAME=
        MAIL_PASSWORD=
        MAIL_FROM=
        MAIL_PORT=
        MAIL_SERVER=


3. Собрать образ `Docker`

    
        docker image build . -t=fastapi_online_store
    

2. Запустить `docker-compose`


        docker compose up -d