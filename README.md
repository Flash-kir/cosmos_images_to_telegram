## cosmos_images_to_telegram.py

Программа принимает на вход аргументы:

    -d DATE, --date DATE  начальная дата
    -t TIME_SLEEP, --time_sleep TIME_SLEEP пауза между публикациями в секундах
    -p PATH_INFINITE, --path_infinite PATH_INFINITE путь к файлам для бесконечного цикла публикаций
    -i IMAGE_PATH, --image_path IMAGE_PATH опубликовать фото по указанному пути

Затем скачиваются файлы с использованием api nasa и spacex.
Бот публикует фото в телеграм канале.

## Установка и запуск

Клонируйте реппозиторий:

    git clone git@github.com:Flash-kir/cosmos_images_to_telegram.git

Выполните команду:

    pip install -r requirenments.txt

У кажите токены nasa и бота telegram в файле .env, предварительно выполнив команду:

    cp example.env .env

Запустите программу командой:

    python cosmos_images_to_telegram.py -d [YYYY-MM-DD]

