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

WORKFLOW_DOT = r'''
digraph DeskMateWorkflow {
  graph [rankdir=TB, bgcolor="#f6f8fb", pad="0.35", nodesep="0.32", ranksep="0.5", splines=polyline,
         fontname="Noto Sans CJK KR", label="DeskMate | 직원 상담부터 티켓 처리까지", labelloc=t, fontsize=22, fontcolor="#142633"];
  node [shape=box, style="rounded,filled", color="#cbd5df", penwidth=1.3, margin="0.16,0.12", fontname="Noto Sans CJK KR", fontsize=11, fontcolor="#182b3a"];
  edge [fontname="Noto Sans CJK KR", fontsize=9, color="#536b7e", fontcolor="#40586b", arrowsize=0.75, penwidth=1.4];

  employee [fillcolor="#ffffff", label="직원\n장애·지원 문의"];
  ui [fillcolor="#e2f3e9", label="Web UI\n현재 구현"];
  spring [fillcolor="#dcecf8", color="#96b9d4", label="Spring API\n대화·권한·흐름 관리\n목표 구성"];
  python [fillcolor="#fff0d7", color="#e1c58f", label="Python AI Service\n증상 분류·필요 정보 파악\n목표 구성"];
  enough [shape=diamond, style=filled, fillcolor="#fff7dc", label="필수 정보가\n충분한가?"];
  question [fillcolor="#dcecf8", color="#96b9d4", label="Spring이 추가 질문 표시\n직원 답변을 받아 재전달"];
  rag [fillcolor="#fff0d7", color="#e1c58f", label="승인된 IT 문서 검색\n출처·버전 포함"];
  evidence [shape=diamond, style=filled, fillcolor="#fff7dc", label="적용 가능한\n근거가 있는가?"];
  guide [fillcolor="#dcecf8", color="#96b9d4", label="Spring 검증 후 안내\n근거와 확인 절차 표시"];
  solved [shape=diamond, style=filled, fillcolor="#fff7dc", label="직원이 해결을\n확인했는가?"];
  draft [fillcolor="#fff0d7", color="#e1c58f", label="Python이 사실 기반\n티켓 초안을 제안"];
  validate [fillcolor="#dcecf8", color="#96b9d4", label="Spring이 schema·정책 검증\n초안은 아직 티켓 아님"];
  review [fillcolor="#ffffff", label="직원이 초안 검토\n수정 또는 승인"];
  approved [shape=diamond, style=filled, fillcolor="#fff7dc", label="승인했는가?"];
  revise [fillcolor="#ffffff", label="초안 수정"];
  create [fillcolor="#dcecf8", color="#96b9d4", label="Spring이 승인·권한·hash·\nidempotency 검증 후 생성"];
  db [shape=cylinder, style=filled, fillcolor="#e2f3e9", label="PostgreSQL\n티켓·상태 이력"];
  known [shape=diamond, style=filled, fillcolor="#fff7dc", label="생성 결과가\n확정됐는가?"];
  recover [fillcolor="#fde7e7", color="#d69b9b", label="idempotency key로 결과 조회\n미확정이면 중복 생성 금지"];
  assign [fillcolor="#dcecf8", color="#96b9d4", label="Spring 배정 정책 또는\n관리자 배정"];
  assigned [shape=diamond, style=filled, fillcolor="#fff7dc", label="담당자가\n할당됐는가?"];
  unassigned [fillcolor="#fde7e7", color="#d69b9b", label="미할당 티켓으로 안내\n관리자 확인·재배정"];
  handler [fillcolor="#ffffff", label="IT 담당자\n확인·조치·상태 변경"];
  status [fillcolor="#dcecf8", color="#96b9d4", label="Spring이 상태·이력 저장\n직원에게 진행 결과 표시"];
  done [shape=oval, style=filled, fillcolor="#e2f3e9", label="해결 확인·상담 종료"];
  fail [fillcolor="#fde7e7", color="#d69b9b", label="미해결이면 담당자 재확인\n또는 재배정"];

  employee -> ui;
  ui -> spring [label="문의"];
  spring -> python [label="최소 문맥 · request_id", color="#357ca5", fontcolor="#357ca5"];
  python -> enough;
  enough -> question [label="아니오"];
  question -> python [label="답변 포함 재질의"];
  enough -> rag [label="예"];
  rag -> evidence;
  evidence -> guide [label="예"];
  guide -> ui [label="응답 + citations", color="#357ca5", fontcolor="#357ca5"];
  ui -> solved [label="해결 여부 확인"];
  solved -> done [label="예"];
  solved -> draft [label="아니오"];
  evidence -> draft [label="없음·검색 실패"];
  draft -> validate [label="draft 제안", color="#357ca5", fontcolor="#357ca5"];
  validate -> review;
  review -> approved;
  approved -> revise [label="수정"];
  revise -> review;
  approved -> done [label="거부·종료"];
  approved -> create [label="승인"];
  create -> db [label="쓰기"];
  db -> known [label="결과"];
  known -> recover [label="불명확"];
  recover -> spring [label="상태 결과 회신", style=dashed, color="#bd6b64", fontcolor="#a14f48"];
  known -> assign [label="성공"];
  assign -> assigned;
  assigned -> unassigned [label="아니오"];
  unassigned -> assign [label="재배정"];
  assigned -> handler [label="예"];
  handler -> status;
  status -> db [label="상태 이력"];
  status -> done [label="해결"];
  status -> fail [label="미해결"];
  fail -> assign [label="재배정"];

  legend [shape=plain, label=<
    <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="8" CELLPADDING="4">
      <TR><TD BGCOLOR="#ffffff">직원 흐름</TD><TD BGCOLOR="#dcecf8">Spring 업무 경계</TD>
          <TD BGCOLOR="#fff0d7">Python AI 단계</TD><TD BGCOLOR="#fde7e7">오류·미확정 대응</TD></TR>
    </TABLE>>];
  {rank=sink; legend}
}
'''


def main():
    dot = shutil.which('dot')
    if not dot:
        raise SystemExit('Graphviz dot is required. Install Graphviz and rerun this script.')
    outputs = {
        ROOT / 'docs' / 'architecture.png': DOT,
        ROOT / 'docs' / 'workflow.png': WORKFLOW_DOT,
    }
    with tempfile.NamedTemporaryFile('w', suffix='.dot', encoding='utf-8') as source:
        for output, graph in outputs.items():
            source.seek(0)
            source.truncate()
            source.write(graph)
            source.flush()
            subprocess.run([dot, '-Tpng', '-Gdpi=150', source.name, '-o', str(output)], check=True)
            print(f'Wrote {output.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
