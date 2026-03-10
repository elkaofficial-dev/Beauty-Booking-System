# 🚀 Развертывание на DockerHost

## 📋 Что необходимо

- DockerHost с поддержкой `docker-compose`
- Доступ к переменным окружения в интерфейсе DockerHost
- Telegram Bot Token от @BotFather

---

## ✅ Пошаговое развертывание

### 1️⃣ Загрузить репозиторий

Загрузитесь репо `portfolio-shop` на ваш DockerHost через веб-интерфейс или CLI.

### 2️⃣ Установить переменные окружения

В интерфейсе DockerHost'а установите переменные:

```env
BOT_TOKEN=ваш_реальный_токен_от_botfather
```

**Опционально** (если хотите разный хост БД):
```env
DATABASE_URL=postgresql://user:password@postgres_host:5432/beauty_shop
```

> ℹ️ Если `DATABASE_URL` не установлена, будет использоваться встроенная PostgreSQL из `docker-compose.yml`

### 3️⃣ Запустить контейнеры

Нажмите "Deploy" или выполните:

```bash
docker-compose up -d
```

### 4️⃣ Проверить статус

```bash
# Посмотреть все контейнеры
docker-compose ps

# Посмотреть логи бота
docker-compose logs -f bot

# Посмотреть логи БД
docker-compose logs -f postgres
```

---

## 🎯 Что должно произойти

Вы должны увидеть в логах бота:

```
INFO:__main__:🔧 Конфигурация:
INFO:__main__:   BOT_TOKEN: ✅ установлен
INFO:__main__:   DATABASE_URL: postgresql://beauty_user:...@postgres:5432/beauty_shop
INFO:__main__:🔄 Попытка подключения к БД (1/10)...
INFO:__main__:✅ Успешно подключилась к БД!
INFO:__main__:✅ Таблица records готова
INFO:__main__:🤖 Бот запущен и слушает обновления...
```

---

## 🔧 Команды управления

```bash
# Остановить все сервисы
docker-compose down

# Перезагрузить все контейнеры
docker-compose restart

# Перезагрузить только бота
docker-compose restart bot

# Очистить всё (включая БД)
docker-compose down -v

# Пересобрать образы
docker-compose build --no-cache

# Запустить сразу после пересборки
docker-compose up -d --build
```

---

## 🐛 Решение проблем

### Бот не подключается к БД

**Логи**: `OSError: Connect call failed`

**Решение**:
1. Проверьте, что PostgreSQL запущен: `docker-compose ps postgres`
2. Посмотрите логи БД: `docker-compose logs postgres`
3. Пересоберите без кеша: `docker-compose build --no-cache`
4. Перезагрузитесь: `docker-compose down && docker-compose up -d`

### BOT_TOKEN не установлен

**Логи**: `❌ BOT_TOKEN не установлен!`

**Решение**:
1. Убедитесь, что установлена переменная `BOT_TOKEN` в окружении
2. Перезигурьте контейнеры: `docker-compose restart bot`

### Контейнер постоянно перезагружается

**Причина**: Ошибка при запуске

**Решение**:
```bash
# Посмотрите полные логи
docker-compose logs bot --tail=50

# Остановите и посмотрите ошибку
docker-compose stop
docker-compose up bot  # (без -d, чтобы видеть вывод)
```

### БД не инициализируется

**Решение**:
```bash
# Удалите том БД и пересоздайте
docker-compose down -v
docker-compose up -d
```

---

## 📊 Мониторинг

### Проверка здоровья контейнеров

```bash
# Проверить статус всех контейнеров
docker-compose ps

# Вывод должен быть примерно:
# NAME                     STATUS
# beauty_shop_db          Up (health: healthy)
# beauty_shop_bot         Up
```

### Логирование

```bash
# Последние 50 строк логов бота
docker-compose logs bot --tail=50

# Следить за логами в реальном времени
docker-compose logs -f bot

# Логи сразу же после запуска
docker-compose up  # (без флага -d)
```

---

## 🎯 Успешное развертывание

Если вы видите в логах:

```
🤖 Бот запущен и слушает обновления...
```

**Поздравляем! 🎉 Бот работает!**

Теперь вы можете отправлять сообщения боту в Telegram и записываться на услуги.

---

## 📝 Полезные ссылки

- 📖 [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- 🤖 [aiogram Documentation](https://docs.aiogram.dev/)
- 🛢️ [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- 💬 [Telegram Bot API](https://core.telegram.org/bots/api)
