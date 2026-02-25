from fastapi import FastAPI
import asyncpg
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'notes'),
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432')
    )
    
    async with app.state.pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    yield
    
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/add/{text}")
async def add_note(text: str):
    async with app.state.pool.acquire() as conn:
        await conn.execute('INSERT INTO notes (text) VALUES ($1)', text)
    return {"message": f"Заметка '{text}' добавлена"}

@app.get("/count")
async def count_notes():
    async with app.state.pool.acquire() as conn:
        count = await conn.fetchval('SELECT COUNT(*) FROM notes')
    return {"count": count}

@app.get("/list")
async def list_notes():
    async with app.state.pool.acquire() as conn:
        rows = await conn.fetch('SELECT id, text, created_at FROM notes ORDER BY id')
    
    if not rows:
        return "Нет заметок"
    
    result = "Список заметок:\n" + "\n".join([f"{r['id']}: {r['text']} (создано: {r['created_at']})" for r in rows])
    return result

@app.get("/")
async def root():
    return {"message": "Счётчик заметок работает! Используйте /add/<text>, /count, /list"}