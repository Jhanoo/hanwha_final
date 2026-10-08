"""Copy legacy SQLite tickets to PostgreSQL without modifying the source DB."""
from datetime import datetime
from hashlib import sha256
from pathlib import Path
import os
import sqlite3
import uuid

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')
DATABASE_URL = os.environ.get('DATABASE_URL')
SQLITE_PATH = Path(os.environ.get('SQLITE_PATH', ROOT / '.local' / 'tickets.db'))
if not DATABASE_URL:
    raise SystemExit('DATABASE_URL is missing; configure it in the local .env file.')
if not SQLITE_PATH.is_file():
    raise SystemExit(f'SQLite source does not exist: {SQLITE_PATH}')

status_map = {'접수': 'open', '처리 중': 'in_progress', '해결': 'resolved'}
namespace = uuid.UUID('1dfcd7c0-ae21-4d37-9658-d276e56f7e23')
with sqlite3.connect(f'file:{SQLITE_PATH}?mode=ro', uri=True) as source:
    source.row_factory = sqlite3.Row
    rows = source.execute('SELECT id,title,category,priority,status,created_at FROM tickets ORDER BY id').fetchall()

with psycopg.connect(DATABASE_URL) as target:
    with target.transaction():
        for row in rows:
            ticket_id = int(row['id'])
            conversation_id = uuid.uuid5(namespace, f'legacy-conversation-{ticket_id}')
            approval_id = uuid.uuid5(namespace, f'legacy-approval-{ticket_id}')
            title = row['title']
            created_at = datetime.fromisoformat(row['created_at'])
            status = status_map.get(row['status'], 'open')
            idempotency_key = f'legacy-sqlite-{ticket_id}'
            target.execute('''
                INSERT INTO conversations(id,created_at,status)
                VALUES (%s,%s,'escalated') ON CONFLICT (id) DO NOTHING
            ''', (conversation_id, created_at))
            target.execute('''
                INSERT INTO approvals(id,conversation_id,draft_sha256,status,created_at,approved_at)
                VALUES (%s,%s,%s,'approved',%s,%s) ON CONFLICT (id) DO NOTHING
            ''', (approval_id, conversation_id, sha256(title.encode()).hexdigest(), created_at, created_at))
            inserted = target.execute('''
                INSERT INTO tickets(id,conversation_id,approval_id,title,category,priority,status,summary,idempotency_key,created_at,updated_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (id) DO NOTHING RETURNING id
            ''', (ticket_id, conversation_id, approval_id, title, row['category'],
                  'normal' if row['priority'] in ('보통', 'normal') else 'high', status,
                  psycopg.types.json.Jsonb({'source': 'sqlite-import', 'legacy_priority': row['priority']}),
                  idempotency_key, created_at, created_at)).fetchone()
            if inserted:
                target.execute('''
                    INSERT INTO ticket_events(ticket_id,previous_status,new_status,actor,created_at)
                    VALUES (%s,NULL,%s,'system',%s)
                ''', (ticket_id, status, created_at))
        if rows:
            target.execute("SELECT setval(pg_get_serial_sequence('tickets','id'), GREATEST((SELECT max(id) FROM tickets),1), true)")

print(f'Copied or preserved {len(rows)} legacy tickets from {SQLITE_PATH}; source left unchanged.')
