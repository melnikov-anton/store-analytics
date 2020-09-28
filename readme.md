# Store Analytics
## Описание
Скрипт **generate_input_data.py** создает в директории **input_data** файлы входных данных
**drone_cells.csv** и **video_barcodes.csv**.  
(Директория **input_with_unresolved** содержит входные данные с неразрешимым случаем)  
Скрипт **process_input_data.py** загружает входные данные, обрабатывает их и
создает в директории **output_data** файл результата **cells_barcodes.csv**.  
Скрипт **server.py** запускает веб-приложение (сервер), визуализирующее результат.


## Для запуска локального сервера
Из директории приложения создать виртуальную среду  
```
python3 -m venv virtenv
```
Активировать виртуальную среду
```
source virtenv/bin/activate
```
Установить модули согласно **requirements.txt**
```
pip3 install -r requirements.txt
```
Запустить локальный веб-сервер
```
gunicorn server:app
```
После запуска сервер доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)
