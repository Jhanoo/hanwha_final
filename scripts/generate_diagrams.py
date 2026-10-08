"""Render the DeskMate architecture overview as a PNG with Graphviz."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DOT = r'''
digraph DeskMate {
  graph [rankdir=TB, bgcolor="#f6f8fb", pad="0.35", nodesep="0.45", ranksep="0.75", splines=polyline,
         fontname="Noto Sans CJK KR", label="DeskMate | 사내 IT 장애 대응 AI Agent 아키텍처", labelloc=t, fontsize=24, fontcolor="#142633"];
  node [shape=box, style="rounded,filled", color="#cbd5df", penwidth=1.4, margin="0.18,0.14", fontname="Noto Sans CJK KR", fontsize=12, fontcolor="#182b3a"];
  edge [fontname="Noto Sans CJK KR", fontsize=10, color="#536b7e", fontcolor="#40586b", arrowsize=0.8, penwidth=1.6];

  employee [fillcolor="#ffffff", label="직원\n장애 문의 · 해결 확인"];
  operator [fillcolor="#ffffff", label="IT 담당자\n티켓 확인 · 상태 변경"];
  web [fillcolor="#e2f3e9", label="Web UI · 현재 구현\nHTML / CSS / JS\n대화 · 티켓 보드"];
  api [fillcolor="#e2f3e9", label="Python HTTP API · 현재 구현\nserver.py\n입력 검증 · 규칙 진단 · 티켓 API"];
  rules [fillcolor="#e2f3e9", label="키워드 상담\n현재 구현"];
  agent [fillcolor="#fff0d7", color="#e1c58f", label="IT Support Agent\n계획 · OpenAI Agents SDK\n추가 질문 · 응답 구조화 · 도구 선택"];
  approval [fillcolor="#fff0d7", color="#e1c58f", label="TicketAdapter + 승인 경계\n계획\n승인 · 멱등 키 · 쓰기 권한 분리"];
  retriever [fillcolor="#fff0d7", color="#e1c58f", label="Knowledge Retriever\n계획 · RAG\ntop-k 근거 · 출처 ID"];
  tickets [shape=cylinder, style=filled, fillcolor="#e2f3e9", label="PostgreSQL 티켓\n현재 구현\ntickets · ticket_events"];
  knowledge [shape=cylinder, style=filled, fillcolor="#fff0d7", color="#e1c58f", label="PostgreSQL + pgvector\nschema 준비 · 검색 미구현\nknowledge_chunks · vector(1536)"];
  llm [fillcolor="#eee5f8", color="#c9bce0", label="호스팅 LLM API\n후보: gpt-4.1-mini\n가용성 · 가격 확인 전"];
  source [shape=folder, fillcolor="#ffffff", label="승인된 / synthetic\nIT 가이드"];
  ingestion [fillcolor="#fff0d7", color="#e1c58f", label="문서 ingestion\n계획 · 분할 · metadata"];
  embeddings [fillcolor="#eee5f8", color="#c9bce0", label="Embedding API\n후보: text-embedding-3-small\n1536 dimensions"];

  {rank=same; employee; operator}
  {rank=same; rules; agent; source}
  {rank=same; approval; retriever; ingestion}
  {rank=same; tickets; llm; knowledge; embeddings}

  employee -> web [label="문의"];
  operator -> web [label="티켓 처리"];
  web -> api [label="HTTP / JSON"];
  api -> rules [label="현재 /api/chat", color="#258451", fontcolor="#258451"];
  api -> tickets [label="현재 ticket CRUD", color="#258451", fontcolor="#258451"];
  api -> agent [label="대화 전달", style=dashed, color="#bd7a18", fontcolor="#8b5a16"];
  agent -> llm [label="추론 · tool calling", style=dashed, color="#7752a6", fontcolor="#69518b"];
  agent -> retriever [label="검색 tool", style=dashed, color="#bd7a18", fontcolor="#8b5a16"];
  api -> approval [label="승인된 접수", style=dashed, color="#bd7a18", fontcolor="#8b5a16"];
  approval -> tickets [label="쓰기 tool", style=dashed, color="#bd7a18", fontcolor="#8b5a16"];
  retriever -> knowledge [label="근거 검색", style=dashed, color="#bd7a18", fontcolor="#8b5a16"];
  source -> ingestion [label="문서", style=dashed, color="#bd7a18", fontcolor="#8b5a16"];
  ingestion -> embeddings [label="문서 벡터화", style=dashed, color="#7752a6", fontcolor="#69518b"];
  embeddings -> knowledge [label="임베딩 적재", style=dashed, color="#7752a6", fontcolor="#69518b"];

  // Keep the two main paths visually legible while allowing planned AI components below the current path.
  employee -> operator [style=invis, weight=8];
  rules -> agent [style=invis, weight=5];
  approval -> retriever [style=invis, weight=5];
  tickets -> llm [style=invis, weight=2];

  legend [shape=plain, label=<
    <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="10" CELLPADDING="5">
      <TR><TD BGCOLOR="#e2f3e9">현재 구현</TD><TD><FONT COLOR="#258451">실선: 현재 흐름</FONT></TD>
          <TD BGCOLOR="#fff0d7">계획 기능</TD><TD><FONT COLOR="#bd7a18">점선: 향후 연결</FONT></TD></TR>
    </TABLE>>];
  {rank=sink; legend}
}
'''


def main():
    dot = shutil.which('dot')
    if not dot:
        raise SystemExit('Graphviz dot is required. Install Graphviz and rerun this script.')
    output = ROOT / 'docs' / 'architecture.png'
    with tempfile.NamedTemporaryFile('w', suffix='.dot', encoding='utf-8') as source:
        source.write(DOT)
        source.flush()
        subprocess.run([dot, '-Tpng', '-Gdpi=150', source.name, '-o', str(output)], check=True)
    print(f'Wrote {output.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
