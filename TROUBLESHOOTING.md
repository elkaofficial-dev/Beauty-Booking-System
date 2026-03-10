# 🔧 Решение проблемы подключения к БД

## 🚨 Проблема

```
OSError: Multiple exceptions: [Errno 111] Connect call failed ('::1', 5432, 0, 0), [Errno 111] Connect call failed ('127.0.0.1', 5432)
```

**Причина**: Бот не может подключиться к PostgreSQL

---

## ✅ Что я исправил

### 1. **Добавлена retry-логика в `bot_main.py`**
   - Бот теперь ждёт до 30 секунд для подключения к БД
   - Пытается подключиться максимум 10 раз
   - Логирует каждую попытку

### 2. **Обновлён `docker-compose.yml`**
   - `restart: on-failure` — контейнер перезапускается при ошибке
   - `depends_on` с условием `service_healthy` — бот ждёт, пока БД будет готова
   - Правильный хост: `postgresql://...@postgres:5432/...` (postgres, а не localhost)

### 3. **Добавлен диагностический скрипт `diagnose.sh`**
   - Проверяет статус контейнеров
   - Выводит логи
   - Проверяет сетевое подключение

---

## 🚀 Как решить проблему

### Вариант 1: Пересобрать без кеша
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Вариант 2: Полная очистка и перезапуск
```bash
docker-compose down -v
docker-compose up -d
```

### Вариант 3: Проверка диагностикой
```bash
./diagnose.sh
```

---

## 📊 Проверка логов

### Логи PostgreSQL:
```bash
docker-compose logs postgres
```

### Логи Telegram бота:
```bash
docker-compose logs -f bot
```

### Логи администратора:
```bash
docker-compose logs -f admin
```

---

## ✨ После успешного подключения вы увидите:

```
[bot] 🔄 Попытка подключения к БД (1/10)...
[bot] ✅ Успешно подключилась к БД!
[bot] ✅ Таблица records готова
[bot] 🤖 Бот запущен и слушает обновления...
```

---

## 💡 Если всё ещё не работает

### 1. Проверьте **.env** файл:
```bash
cat .env
```

Должны быть строки:
```env
BOT_TOKEN=your_token_here
DATABASE_URL=postgresql://beauty_user:beauty_password@postgres:5432/beauty_shop
```

### 2. Проверьте, что Docker запущен:
```bash
docker --version
docker ps
```

### 3. Посмотрите все контейнеры (включая упавшие):
```bash
docker-compose ps -a
```

### 4. Удалите старые образы и начните с нуля:
```bash
docker system prune -a
docker-compose up -d --build
```

---

## 🎯 Порядок запуска на DockerHost

1. ✅ Загрузите репозиторий
2. ✅ Выставьте переменные окружения: `BOT_TOKEN`, `DATABASE_URL`
3. ✅ Запустите `docker-compose up -d`
4. ✅ Подождите 30-40 секунд для инициализации
5. ✅ Проверьте логи: `docker-compose logs bot`

**Всё должно работать! 🎉**
