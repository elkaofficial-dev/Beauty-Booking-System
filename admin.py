import os, asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Template
from dotenv import load_dotenv

load_dotenv()

HTML = """
<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"><title>Админ</title>
<style>body{font-family:sans-serif;margin:2rem}table{border-collapse:collapse;width:100%;max-width:600px}
th,td{border:1px solid #ddd;padding:10px;text-align:left}th{background:#f4f4f4}
button{background:#ff4d4d;color:#fff;border:none;padding:5px 10px;cursor:pointer;border-radius:4px}</style></head>
<body><h2>📅 Панель управления</h2><table><tr><th>Дата</th><th>Услуга</th><th>Действие</th></tr>
{% for r in records %}<tr><td>{{ r['date'].strftime('%d.%m.%Y') }}</td><td>{{ r['srv'] }}</td><td>
<form action="/del" method="post" style="margin:0"><input type="hidden" name="date" value="{{ r['date'] }}"><button>Удалить</button></form>
</td></tr>{% endfor %}</table></body></html>
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))
    async with app.state.pool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS records (date DATE PRIMARY KEY, srv TEXT)")
    yield
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def index(req: Request):
    async with req.app.state.pool.acquire() as conn:
        records = await conn.fetch("SELECT * FROM records ORDER BY date")
    return Template(HTML).render(records=records)

@app.post("/del")
async def delete(req: Request, date: str = Form(...)):
    async with req.app.state.pool.acquire() as conn:
        await conn.execute("DELETE FROM records WHERE date = $1::date", date)
    return RedirectResponse(url="/", status_code=303)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=5000)