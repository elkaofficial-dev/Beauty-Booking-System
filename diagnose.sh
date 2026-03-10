#!/bin/bash

# 🔍 Скрипт для диагностики Docker проблем

echo "╔═══════════════════════════════════╗"
echo "║   🔍 Docker Diagnostic Tool       ║"
echo "╚═══════════════════════════════════╝"
echo ""

# Определяем команду docker-compose
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

echo "📊 Статус контейнеров:"
$DOCKER_COMPOSE ps
echo ""

echo "📋 Логи PostgreSQL:"
$DOCKER_COMPOSE logs postgres | tail -20
echo ""

echo "📋 Логи Telegram Bot:"
$DOCKER_COMPOSE logs bot | tail -30
echo ""

echo "🌐 Проверка сетевого подключения:"
$DOCKER_COMPOSE exec -T bot ping -c 3 postgres 2>/dev/null || echo "❌ Нет подключения к postgres"
echo ""

echo "🗄️  Проверка БД через админ панель:"
$DOCKER_COMPOSE exec -T admin python -c "
import os, asyncpg, asyncio
async def check():
    try:
        pool = await asyncpg.create_pool(os.getenv('DATABASE_URL'))
        async with pool.acquire() as conn:
            result = await conn.fetch('SELECT * FROM records LIMIT 1')
            print('✅ БД доступна, таблица records существует')
        await pool.close()
    except Exception as e:
        print(f'❌ Ошибка БД: {e}')
asyncio.run(check())
" 2>/dev/null || echo "⚠️  Админ контейнер не запущен"
echo ""

echo "💡 Советы для решения проблем:"
echo "1️⃣  Проверьте, что БД готова: docker-compose logs postgres"
echo "2️⃣  Логи бота: docker-compose logs -f bot"
echo "3️⃣  Пересоберите образы: docker-compose build --no-cache"
echo "4️⃣  Очистите всё и начните заново: docker-compose down -v && docker-compose up -d"
