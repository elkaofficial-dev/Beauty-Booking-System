#!/bin/bash

# 🚀 Скрипт для запуска Beauty Shop проекта

set -e

echo "╔═══════════════════════════════════════╗"
echo "║   🚀 Beauty Shop Docker Setup 🚀     ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден!"
    echo "📋 Создаём .env из .env.example..."
    
    if [ ! -f .env.example ]; then
        echo "❌ Файл .env.example не найден!"
        exit 1
    fi
    
    cp .env.example .env
    echo "✅ Файл .env создан"
    echo ""
    echo "⚠️  ВАЖНО: Отредактируйте .env и вставьте реальный BOT_TOKEN!"
    echo "Открыто: $(pwd)/.env"
    echo ""
    echo "Пока отредактируйте .env и запустите скрипт снова."
    exit 0
fi

# Проверяем наличие docker-compose
if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "📖 Посетите https://docs.docker.com/get-docker/"
    exit 1
fi

# Определяем команду docker-compose
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

echo "✅ Проверка окружения пройдена"
echo ""

# Стартуем контейнеры
echo "🔨 Собираем и запускаем контейнеры..."
$DOCKER_COMPOSE up -d

echo ""
echo "⏳ Ожидание инициализации БД (30 сек)..."
sleep 30

# Проверяем статус
echo ""
echo "📊 Статус сервисов:"
$DOCKER_COMPOSE ps

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║   ✅ Готово к запуску!                ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "📱 Telegram Bot: Запущен и слушает обновления"
echo ""
echo "📖 Команды:"
echo "  • Остановить:     docker-compose down"
echo "  • Логи бота:      docker-compose logs -f bot"
echo "  • Перезагрузить:  docker-compose restart"
echo "  • Удалить все:    docker-compose down -v"
echo ""

