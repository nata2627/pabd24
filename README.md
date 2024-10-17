## Installation 

Клонируйте репозиторий, создайте виртуальное окружение, активируйте и установите зависимости:  

```sh
git clone https://github.com/nata2627/pabd24
cd pabd24
python3 -m venv venv
pip install -r requirements.txt
```

## Usage

### 1. Создание необходимых папок и файлов
```sh
mkdir -p data/raw
mkdir -p data/proc
touch log/preprocess_data.log
```

### 2. Сбор данных о ценах на недвижимость

```sh
 python3 src/parse_cian.py
```

### 3. Выгрузка данных в хранилище S3 
Для доступа к хранилищу скопируйте файл `.env` в корень проекта.  

```sh
 python3 src/upload_to_s3.py
```

### 4. Загрузка данных из S3 на локальную машину  

```sh
python3 src/download_from_s3.py
```

### 5. Предварительная обработка данных  

```sh
python3 src/preprocess_data.py
```

### 6. Обучение модели 

```sh
python3 src/train_model.py
```
 В качестве входных данных для парной линейной регрессии используется площадь квартиры `area`.
Модель возвращает цену недвижимости `price`.

### 7. Запуск приложения flask 

```sh
python3 src/predict_app.py 
```
#### Запуск приложения на prod (gunicorn)
```sh
gunicorn -b 0.0.0.0 src.predict_app:app 
```
Адрес задеплоенного приложения [http://176.123.164.139:8000](http://176.123.164.139:8000)

### 8. Использование сервиса через веб интерфейс 

Для использования сервиса используйте файл `web/index.html`.  

