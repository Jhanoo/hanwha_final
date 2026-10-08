"""IT helpdesk demo: Python standard library, SQLite, local ticket adapter."""
import json
import os
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent
DB = ROOT / '.local' / 'tickets.db'
DB.parent.mkdir(exist_ok=True)

def connect():
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection

with connect() as db:
    db.execute('CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, category TEXT NOT NULL, priority TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL)')

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
        if self.path == '/api/tickets':
            with connect() as db:
                self.respond([dict(row) for row in db.execute('SELECT * FROM tickets ORDER BY id DESC')])
        elif self.path == '/api/health':
            self.respond({'status': 'ok', 'agent': 'rules-demo', 'tickets': 'sqlite'})
        else:
            super().do_GET()

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
                title = data.get('title', '')
                if not isinstance(title, str) or not title.strip() or len(title) > 2000:
                    raise ValueError('티켓 내용을 1~2000자로 입력해 주세요.')
                info = diagnose(title)
                priority = data.get('priority', '보통')
                if priority not in ['보통', '높음']:
                    raise ValueError('잘못된 우선순위입니다.')
                with connect() as db:
                    cur = db.execute('INSERT INTO tickets(title,category,priority,status,created_at) VALUES(?,?,?,?,?)', (title.strip(), info['category'], priority, '접수', datetime.now(timezone.utc).isoformat()))
                    row = dict(db.execute('SELECT * FROM tickets WHERE id=?', (cur.lastrowid,)).fetchone())
                self.respond(row, 201)
            elif self.path.startswith('/api/tickets/'):
                ticket_id = int(self.path.rsplit('/', 1)[1])
                status = data.get('status')
                if status not in ['접수', '처리 중', '해결']:
                    raise ValueError('잘못된 상태입니다.')
                with connect() as db:
                    cur = db.execute('UPDATE tickets SET status=? WHERE id=?', (status, ticket_id))
                    self.respond({'status': status} if cur.rowcount else {'error': '티켓을 찾을 수 없습니다.'}, 200 if cur.rowcount else 404)
            else:
                self.respond({'error': '없는 경로입니다.'}, 404)
        except (ValueError, TypeError):
            self.respond({'error': '입력 형식이나 값이 올바르지 않습니다.'}, 400)

if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', int(os.environ.get('PORT', '8000'))), Handler).serve_forever()
