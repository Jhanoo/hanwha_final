"""Render the DeskMate architecture overview as a PNG with Graphviz."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DOT = r'''
digraph DeskMate {
  graph [rankdir=TB, bgcolor="#f6f8fb", pad="0.35", nodesep="0.45", ranksep="0.85", splines=polyline,
         fontname="Noto Sans CJK KR", label="DeskMate | Spring 백엔드 + Python AI 서비스 목표 구성", labelloc=t, fontsize=22, fontcolor="#142633"];
  node [shape=box, style="rounded,filled", color="#cbd5df", penwidth=1.4, margin="0.18,0.14", fontname="Noto Sans CJK KR", fontsize=12, fontcolor="#182b3a"];
  edge [fontname="Noto Sans CJK KR", fontsize=10, color="#536b7e", fontcolor="#40586b", arrowsize=0.8, penwidth=1.6];

  employee [fillcolor="#ffffff", label="직원\n장애 문의 · 해결 확인"];
  operator [fillcolor="#ffffff", label="IT 담당자\n티켓 처리 · 상태 변경"];
  web [fillcolor="#e2f3e9", label="정적 Web UI\n현재 구현"];
  pycurrent [fillcolor="#e2f3e9", label="Python server.py\n현재 구현 · 규칙 상담"];
  pgcurrent [shape=cylinder, style=filled, fillcolor="#e2f3e9", label="PostgreSQL\n현재 티켓 CRUD"];
  spring [fillcolor="#dcecf8", color="#96b9d4", label="Spring Boot API\n계획 · 인증 · 대화 · 티켓 · 승인"];
  ai [fillcolor="#fff0d7", color="#e1c58f", label="Python AI Service\n계획 · Agents SDK · RAG\n상담 · 검색 · 초안 제안"];
  knowledge [shape=cylinder, style=filled, fillcolor="#fff0d7", color="#e1c58f", label="같은 PostgreSQL 인스턴스\npgvector 지식 schema 준비\n검색 미구현"];
  llm [fillcolor="#eee5f8", color="#c9bce0", label="호스팅 LLM API\n후보 · 미확정"];
  embeddings [fillcolor="#eee5f8", color="#c9bce0", label="Embedding API\n후보 · 미확정"];
  docs [shape=folder, fillcolor="#ffffff", label="승인된 / synthetic\nIT 가이드"];

  {rank=same; employee; operator}
  {rank=same; pycurrent; spring}
  {rank=same; pgcurrent; ai; docs}
  {rank=same; knowledge; llm; embeddings}

  employee -> web [label="문의"];
  operator -> web [label="티켓 처리"];
  web -> pycurrent [label="현재 HTTP", color="#258451", fontcolor="#258451"];
  pycurrent -> pgcurrent [label="현재 ticket CRUD", color="#258451", fontcolor="#258451"];
  web -> spring [label="향후 API", style=dashed, color="#357ca5", fontcolor="#357ca5"];
  spring -> ai [label="내부 HTTP JSON\n상담 요청 · 초안 응답", style=dashed, color="#357ca5", fontcolor="#357ca5"];
  spring -> pgcurrent [label="티켓 · 승인 · 대화 소유", style=dashed, color="#357ca5", fontcolor="#357ca5"];
  ai -> knowledge [label="검색 · ingestion role", style=dashed, color="#bd7a18", fontcolor="#8b5a16"];
  ai -> llm [label="생성 요청", style=dashed, color="#7752a6", fontcolor="#69518b"];
  ai -> embeddings [label="문서 벡터화", style=dashed, color="#7752a6", fontcolor="#69518b"];
  embeddings -> knowledge [label="vector 적재", style=dashed, color="#bd7a18", fontcolor="#8b5a16"];
  docs -> ai [label="검수 문서", style=dashed, color="#bd7a18", fontcolor="#8b5a16"];

  legend [shape=plain, label=<
    <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="10" CELLPADDING="5">
      <TR><TD BGCOLOR="#e2f3e9">현재 구현</TD><TD><FONT COLOR="#258451">초록 실선: 현재 흐름</FONT></TD>
          <TD BGCOLOR="#dcecf8">Spring / Python AI 계획</TD><TD><FONT COLOR="#357ca5">파란 점선: 서비스 간 호출</FONT></TD>
          <TD><FONT COLOR="#bd7a18">주황·보라 점선: RAG와 모델 연동</FONT></TD></TR>
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
