from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Подключение к БД при старте
    app.state.pool = await asyncpg.create_pool(
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'todo'),
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432')
    )
    
    # Создание таблицы при первом запуске
    async with app.state.pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN DEFAULT FALSE
            )
        ''')
    
    yield
    
    # Закрытие соединений при остановке
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

# Добавляем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/create/{title}")
async def create_task(title: str):
    async with app.state.pool.acquire() as conn:
        await conn.execute('INSERT INTO tasks (title) VALUES ($1)', title)
    return "created"

@app.get("/done/{task_id}")
async def mark_done(task_id: int):
    async with app.state.pool.acquire() as conn:
        result = await conn.execute('UPDATE tasks SET done = TRUE WHERE id = $1', task_id)
        if result == "UPDATE 0":
            return f"Задача с id {task_id} не найдена"
    return "updated"

@app.get("/pending")
async def list_pending():
    async with app.state.pool.acquire() as conn:
        rows = await conn.fetch('SELECT id, title FROM tasks WHERE done = FALSE ORDER BY id')
    
    if not rows:
        return "Нет невыполненных задач"
    
    return " ".join([f"{r['id']} {r['title']}" for r in rows])

@app.get("/stats")
async def get_stats():
    async with app.state.pool.acquire() as conn:
        total = await conn.fetchval('SELECT COUNT(*) FROM tasks')
        done = await conn.fetchval('SELECT COUNT(*) FROM tasks WHERE done = TRUE')
    
    pending = total - done
    return f"total: {total} done: {done} pending: {pending}"

@app.get("/")
async def root():
    return {
        "message": "Мини-трекер задач работает!",
        "endpoints": {
            "/create/<title>": "Создать задачу",
            "/done/<id>": "Отметить задачу выполненной",
            "/pending": "Список невыполненных задач",
            "/stats": "Статистика"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok"}