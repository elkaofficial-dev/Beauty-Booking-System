@echo off
REM 🚀 Скрипт для запуска Beauty Shop проекта (Windows)

cls
echo.
echo ╔═══════════════════════════════════════╗
echo ║   🚀 Beauty Shop Docker Setup 🚀     ║
echo ╚═══════════════════════════════════════╝
echo.

REM Проверяем наличие .env файла
if not exist ".env" (
    echo ⚠️  Файл .env не найден!
    echo 📋 Создаём .env из .env.example...
    
    if not exist ".env.example" (
        echo ❌ Файл .env.example не найден!
        pause
        exit /b 1
    )
    
    copy .env.example .env
    echo ✅ Файл .env создан
    echo.
    echo ⚠️  ВАЖНО: Отредактируйте .env и вставьте реальный BOT_TOKEN!
    echo.
    echo Пока отредактируйте .env и запустите скрипт снова.
    start .env
    pause
    exit /b 0
)

REM Проверяем наличие docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Desktop не установлен!
    echo 📖 Посетите https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Проверка окружения пройдена
echo.

REM Стартуем контейнеры
echo 🔨 Собираем и запускаем контейнеры...
docker-compose up -d

echo.
echo ⏳ Ожидание инициализации БД (30 сек)...
timeout /t 30 /nobreak

REM Проверяем статус
echo.
echo 📊 Статус сервисов:
docker-compose ps

echo.
echo ╔═══════════════════════════════════════╗
echo ║   ✅ Готово к запуску!                ║
echo ╚═══════════════════════════════════════╝
echo.
echo 📱 Telegram Bot: Запущен и слушает обновления
echo 🌐 Admin Panel: http://localhost:5000
echo 🗄️  Database: postgresql://localhost:5432/beauty_shop
echo.
echo 📖 Команды:
echo   • Остановить:     docker-compose down
echo   • Логи бота:      docker-compose logs -f bot
echo   • Перезагрузить:  docker-compose restart
echo   • Удалить все:    docker-compose down -v
echo.
pause
