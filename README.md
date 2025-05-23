# T-Bank Assistant 🤖

**T-Bank Assistant** — это Telegram-бот на базе RAG-системы (Retrieval-Augmented Generation), разработанный для клиентов T-Bank. Бот отвечает на вопросы о банковских продуктах и услугах, таких как лимиты счетов, оформление карт и переводы, с цитированием официальных документов (например, тарифов Tinkoff Black 2024). Он предоставляет удобные кнопки для быстрых действий, персонализированные ответы и интуитивный интерфейс.

📋 **Цель проекта**: Создать умного помощника для клиентов банка, который сочетает точность поиска по базе знаний с естественной генерацией ответов и интеграцией с действиями T-Bank.

---

## ✨ Основные возможности

- **Поиск и цитирование**: Отвечает на вопросы, опираясь на базу знаний (например, `train_our.jsonl`), с указанием источников.
- **Динамические кнопки**: 
  - "Открыть счёт" — ссылка на форму T-Bank.
  - "Связаться с поддержкой" — контактная страница.
  - "Проверить лимиты" — для вопросов о лимитах.
- **Персонализация**: Запоминает контекст диалога и предлагает релевантные действия (например, уточнение для повторных вопросов о счетах).
- **Интуитивный UX**: Приветственное меню, Markdown-оформление, команда `/help` с примерами.
- **Оптимизация**: Кэширование запросов через Redis для ускорения ответов.
- **Аналитика**: Логирование запросов и ответов в `bot.log` для анализа.
- **Генерация ответов**: Локально использует Retriever (Chroma), в Kaggle — квантизованную ruGPT-3.5 для естественных ответов.

---

## 🛠 Технологии

- **Язык**: Python
- **RAG-система**:
  - **Retriever**: Chroma (векторная база)
  - **Эмбеддинги**: Sentence Transformers (`paraphrase-multilingual-mpnet-base-v2`)
  - **Generator**: ruGPT-3.5 (`ai-forever/ruGPT-3.5`, с квантизацией в Kaggle)
- **Фреймворк**: LangChain
- **Telegram**: python-telegram-bot
- **Кэширование**: Redis
- **Логирование**: Python `logging`

---

## 📂 Структура проекта

```
TinkHelper/
├── bot.py               # Telegram-бот с интерфейсом и RAG
├── prepare_data.py      # Создание векторной базы Chroma
├── rag.py               # Логика RAG (Retriever + Generator)
├── train_our.jsonl      # Датасет с вопросами и ответами
├── requirements.txt     # Зависимости
├── bot.log              # Лог-файл запросов
└── chroma_db/           # Векторная база Chroma
```

---

## 🚀 Установка и запуск

### Требования
- Python 3.9+
- Redis (для кэширования)
- Telegram-бот токен (получить у @BotFather)
- Kaggle (для тестирования генерации с GPU)

### Локальная установка (MacOS/Linux/Windows)
1. **Клонируй репозиторий**:
   ```bash
   git clone https://github.com/your-username/TinkHelper.git
   cd TinkHelper
   ```

2. **Создай виртуальное окружение**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # MacOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Установи зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Установи Redis**:
   - MacOS: `brew install redis`, затем `redis-server`
   - Linux: `sudo apt-get install redis-server`
   - Windows: Используй WSL или Docker

5. **Подготовь данные**:
   - Помести файл `train_our.jsonl` в корень проекта.
   - Запусти создание векторной базы:
     ```bash
     python prepare_data.py
     ```

6. **Настрой Telegram-бота**:
   - В `bot.py` замени `YOUR_TELEGRAM_TOKEN_HERE` на токен от @BotFather.

7. **Запусти бота**:
   ```bash
   python bot.py
   ```

8. **Проверь в Telegram**:
   - Напиши боту `/start`, `/help` или вопрос, например, “Как посмотреть лимиты счета?”.

### Тестирование генерации в Kaggle
1. Загрузи `train_our.jsonl` как датасет в Kaggle.
2. Создай ноутбук, скопируй код из `kaggle_test.ipynb`.
3. Включи GPU (Notebook options → Accelerator → GPU P100).
4. Запусти и проверь генерацию с квантизованной ruGPT-3.5.

---

## 🖥 Пример работы

**Пользователь**: `/start`  
**Бот**:  
👋 *Привет!* Я TinkHelper. Задай вопрос или выбери действие ниже.  
Примеры: 'Как посмотреть лимиты счета?'  
[Оформить карту] [Узнать лимиты] [Связаться с поддержкой]

**Пользователь**: Как посмотреть лимиты счета?  
**Бот**:  
📋 *Ответ*: Вы можете посмотреть лимиты по счету на месяц...  
🔗 *Источник*: Руководство пользователя T-Bank (2024).  
Если у вас есть другие вопросы, напишите!  
[Открыть счёт] [Связаться с поддержкой] [Проверить лимиты]

**Пользователь**: Ещё раз про счёт  
**Бот**:  
Вы уже спрашивали про счёт. Хотите узнать про лимиты или открыть новый счёт?  
[Узнать лимиты] [Открыть счёт]

---

## 🔧 Возможные улучшения

- **Расширение базы знаний**: Добавить PDF-документы с тарифами или парсинг сайта T-Bank.
- **Голосовой ввод**: Интеграция с Tinkoff VoiceKit или `speech_recognition`.
- **Интеграция API**: Подключение к API T-Bank для проверки лимитов или оформления продуктов.
- **Многоязычность**: Поддержка английского или других языков.
