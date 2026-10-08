"""IT helpdesk demo: Python HTTP server with PostgreSQL and pgvector storage."""
import hashlib
import json
import os
import uuid
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / '.env')
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL is missing; copy .env.example to .env and configure PostgreSQL.')


def connect():
    return psycopg.connect(DATABASE_URL, row_factory=psycopg.rows.dict_row)


STATUS_TO_DB = {'접수': 'open', '처리 중': 'in_progress', '해결': 'resolved'}
STATUS_FROM_DB = {value: key for key, value in STATUS_TO_DB.items()}
PRIORITY_TO_DB = {'보통': 'normal', '높음': 'high'}
PRIORITY_FROM_DB = {value: key for key, value in PRIORITY_TO_DB.items()}


def ticket_json(row):
    result = dict(row)
    result['status'] = STATUS_FROM_DB.get(result['status'], result['status'])
    result['priority'] = PRIORITY_FROM_DB.get(result['priority'], result['priority'])
    for key, value in result.items():
        if isinstance(value, uuid.UUID):
            result[key] = str(value)
    result['created_at'] = result['created_at'].isoformat()
    result['updated_at'] = result['updated_at'].isoformat()
    return result


GUIDES = [
    ('VPN', ['vpn', '접속', '재택'], 'VPN 연결 장애', '네트워크', ['인터넷 연결이 정상인지 확인해 주세요.', 'VPN 클라이언트를 종료한 뒤 다시 실행해 주세요.', '다시 로그인하고 MFA 인증을 완료해 주세요.']),
    ('계정', ['로그인', '비밀번호', '계정', '잠김'], '계정 로그인 장애', '계정·권한', ['Caps Lock과 사내 계정 ID를 확인해 주세요.', '사내 비밀번호 재설정 페이지에서 재설정을 진행해 주세요.', '계정 잠김이 계속되면 담당자 확인이 필요합니다. 비밀번호는 채팅에 입력하지 마세요.']),
    ('메일', ['메일', 'outlook', '아웃룩'], '메일 송수신 장애', '업무 도구', ['웹메일에서도 동일한 문제가 발생하는지 확인해 주세요.', 'Outlook의 오프라인 작업 모드를 확인해 주세요.', '오류 코드와 발생 시각을 기록해 주세요.']),
    ('프린터', ['프린터', '인쇄'], '프린터 인쇄 장애', '장비', ['프린터 전원과 연결 상태를 확인해 주세요.', '올바른 프린터를 선택했는지 확인해 주세요.', '대기 중인 인쇄 작업을 취소하고 다시 시도해 주세요.']),
]


def diagnose(message):
    for _, keywords, title, category, steps in GUIDES:
        if any(keyword in message.lower() for keyword in keywords):
            return {'title': title, 'category': category, 'steps': steps, 'answer': '먼저 아래 순서대로 확인해 주세요. 해결되지 않으면 담당자에게 티켓으로 전달하겠습니다.', 'mode': 'rules-demo'}
    return {'title': 'IT 문의', 'category': '기타', 'steps': ['문제가 발생한 서비스와 오류 메시지를 확인해 주세요.', '발생 시각과 다른 직원에게도 발생하는지 알려 주세요.'], 'answer': '증상을 더 확인해야 합니다. 아래 내용을 확인하거나 바로 티켓을 접수할 수 있습니다.', 'mode': 'rules-demo'}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'web'), **kwargs)

    def respond(self, data, status=200):
        payload = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        try:
            if self.path == '/api/tickets':
                with connect() as db:
                    rows = db.execute('SELECT * FROM tickets ORDER BY id DESC').fetchall()
                self.respond([ticket_json(row) for row in rows])
            elif self.path == '/api/health':
                with connect() as db:
                    db.execute('SELECT 1').fetchone()
                self.respond({'status': 'ok', 'agent': 'rules-demo', 'tickets': 'postgresql'})
            else:
                super().do_GET()
        except psycopg.Error:
            self.log_error('PostgreSQL request failed')
            self.respond({'error': '저장소 요청을 처리하지 못했습니다. 잠시 후 다시 시도해 주세요.'}, 503)

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            if not 0 < length <= 16384:
                raise ValueError('요청 크기가 올바르지 않습니다.')
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError('잘못된 요청입니다.')
            if self.path == '/api/chat':
                message = data.get('message', '')
                if not isinstance(message, str) or not message.strip() or len(message) > 2000:
                    raise ValueError('증상을 1~2000자로 입력해 주세요.')
                self.respond(diagnose(message))
            elif self.path == '/api/tickets':
                self.create_ticket(data)
            elif self.path.startswith('/api/tickets/'):
                self.change_ticket_status(data)
            else:
                self.respond({'error': '없는 경로입니다.'}, 404)
        except (ValueError, TypeError) as exc:
            self.log_error('Invalid request (%s)', type(exc).__name__)
            self.respond({'error': '입력 형식이나 값이 올바르지 않습니다.'}, 400)
        except psycopg.Error:
            self.log_error('PostgreSQL request failed')
            self.respond({'error': '저장소 요청을 처리하지 못했습니다. 잠시 후 다시 시도해 주세요.'}, 503)

    def create_ticket(self, data):
        title = data.get('title', '')
        if not isinstance(title, str) or not title.strip() or len(title) > 2000:
            raise ValueError('티켓 내용을 1~2000자로 입력해 주세요.')
        priority = data.get('priority', '보통')
        if priority not in PRIORITY_TO_DB:
            raise ValueError('잘못된 우선순위입니다.')
        idempotency_key = data.get('idempotency_key')
        if not isinstance(idempotency_key, str) or not 1 <= len(idempotency_key) <= 128:
            raise ValueError('접수 요청 식별자가 필요합니다.')

        info = diagnose(title.strip())
        with connect() as db:
            row = db.execute('SELECT * FROM tickets WHERE idempotency_key=%s', (idempotency_key,)).fetchone()
            if row is None:
                conversation_id = uuid.uuid4()
                approval_id = uuid.uuid4()
                draft_hash = hashlib.sha256(title.strip().encode()).hexdigest()
                db.execute("INSERT INTO conversations(id,status) VALUES (%s,'escalated')", (conversation_id,))
                db.execute("INSERT INTO approvals(id,conversation_id,draft_sha256,status,approved_at) VALUES (%s,%s,%s,'approved',now())", (approval_id, conversation_id, draft_hash))
                row = db.execute('''
                    INSERT INTO tickets(conversation_id,approval_id,title,category,priority,status,summary,idempotency_key)
                    VALUES (%s,%s,%s,%s,%s,'open',%s,%s) RETURNING *
                ''', (conversation_id, approval_id, title.strip(), info['category'], PRIORITY_TO_DB[priority],
                      psycopg.types.json.Jsonb({'symptom': title.strip(), 'source': 'chat'}), idempotency_key)).fetchone()
                db.execute("INSERT INTO ticket_events(ticket_id,previous_status,new_status,actor) VALUES (%s,NULL,%s,'employee')", (row['id'], row['status']))
        self.respond(ticket_json(row), 201)

    def change_ticket_status(self, data):
        ticket_id = int(self.path.rsplit('/', 1)[1])
        status = data.get('status')
        if status not in STATUS_TO_DB:
            raise ValueError('잘못된 상태입니다.')
        with connect() as db:
            old = db.execute('SELECT status FROM tickets WHERE id=%s FOR UPDATE', (ticket_id,)).fetchone()
            if old is None:
                row = None
            else:
                new_status = STATUS_TO_DB[status]
                db.execute('UPDATE tickets SET status=%s,updated_at=now() WHERE id=%s', (new_status, ticket_id))
                if old['status'] != new_status:
                    db.execute("INSERT INTO ticket_events(ticket_id,previous_status,new_status,actor) VALUES (%s,%s,%s,'it_operator')", (ticket_id, old['status'], new_status))
                row = {'status': status}
        if row is None:
            self.respond({'error': '티켓을 찾을 수 없습니다.'}, 404)
        else:
            self.respond(row)


if __name__ == '__main__':
    with connect() as db:
        db.execute('SELECT 1')
    ThreadingHTTPServer(('127.0.0.1', int(os.environ.get('PORT', '8000'))), Handler).serve_forever()
