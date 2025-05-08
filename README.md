# Password Manager

Локальное десктопное приложение на Python и PyQt5 для безопасного хранения паролей.  
Данные хранятся в зашифрованном виде в базе данных SQLite.

## Основные возможности

- Хранение логинов, паролей и комментариев
- Шифрование паролей с помощью AES
- Копирование расшифрованного пароля в буфер обмена
- Отображение таблицы со всеми сохранёнными записями
- Минималистичный интерфейс на PyQt5



## Установка

```bash
git clone https://github.com/morz1ck/Password-Manager.git
cd Password-Manager

# опционально
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
python main.py
