# Telegram Fan-Bot (student project)

**Что в этом проекте**
- Бот на aiogram, который показывает ближайшие матчи, последние результаты, таблицу чемпионата, состав команды и локальные события.
- Использует API: https://www.football-data.org/ (нужна регистрация и API-ключ).
- Файлы: main.py, data_api.py, utils.py, config.example.py, requirements.txt

**Установка**
1. Скопируйте `config.example.py` -> `config.py` и заполните TELEGRAM_TOKEN и FOOTBALL_API_KEY.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите:
   ```bash
   python main.py
   ```

**Как получить API-ключ**
- Зарегистрируйтесь на https://www.football-data.org/ и получите API key (X-Auth-Token). Поместите значение в `FOOTBALL_API_KEY` в config.py.

**Примечания**
- Если у вас нет ключа, бот вернёт понятные ошибки и текст-заглушки.
- Team ID можно найти через API (endpoint /v4/teams) или в документации/примерных данных.

**Включённый файл задания**
- В архив также включён ваш загруженный ТЗ: `ТЗ тг бот (2).pdf`
