"""Apply ordered SQL migrations once per PostgreSQL database."""
from pathlib import Path
import os

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise SystemExit('DATABASE_URL is missing; configure it in the local .env file.')

with psycopg.connect(DATABASE_URL) as connection:
    connection.execute('''
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version text PRIMARY KEY,
            applied_at timestamptz NOT NULL DEFAULT now()
        )
    ''')
    for path in sorted((ROOT / 'db' / 'migrations').glob('*.sql')):
        with connection.transaction():
            if connection.execute('SELECT 1 FROM schema_migrations WHERE version = %s', (path.name,)).fetchone():
                print(f'SKIP {path.name}: already applied')
                continue
            connection.execute(path.read_text())
            connection.execute('INSERT INTO schema_migrations(version) VALUES (%s)', (path.name,))
            print(f'APPLIED {path.name}')
