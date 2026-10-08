"""Generate the project overview infographic as SVG and PNG."""
from html import escape
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1920, 1320
BG = "#f3f7fc"
NAVY = "#123f73"
INK = "#18324b"
MUTED = "#516b84"
BLUE = "#dceeff"
BLUE_STROKE = "#9ac4ec"
GREEN = "#e4f5eb"
GREEN_STROKE = "#9dd6b1"
PURPLE = "#f0e8ff"
PURPLE_STROKE = "#c9b2f1"
AMBER = "#fff1d8"
AMBER_STROKE = "#efc77d"
TEAL = "#e0f7f4"
TEAL_STROKE = "#96d7cf"
PINK = "#fff0f3"
PINK_STROKE = "#f1b9c8"
WHITE = "#ffffff"

parts = []


def rect(x, y, w, h, fill, stroke="none", radius=18, sw=2):
    parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def line(x1, y1, x2, y2, color=MUTED, width=3, dash=None, start=None, end="arrow"):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    markers = f' marker-end="url(#{end})"' if end else ""
    if start:
        markers += f' marker-start="url(#{start})"'
    parts.append(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{width}"{dash_attr}{markers}/>'
    )


def text(x, y, lines, size=22, color=INK, weight=400, anchor="start", line_height=None):
    if isinstance(lines, str):
        lines = [lines]
    line_height = line_height or int(size * 1.35)
    spans = []
    for index, value in enumerate(lines):
        dy = 0 if index == 0 else line_height
        spans.append(f'<tspan x="{x}" dy="{dy}">{escape(value)}</tspan>')
    parts.append(
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Noto Sans CJK KR, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">{"".join(spans)}</text>'
    )


def label(x, y, w, title, fill=NAVY):
    rect(x, y, w, 42, fill, radius=12)
    text(x + w / 2, y + 28, title, 21, WHITE, 700, "middle")


def card(x, y, w, h, title, lines, fill=WHITE, stroke="#d4e0ec", accent=NAVY, num=None):
    rect(x, y, w, h, fill, stroke, radius=16, sw=2)
    rect(x, y, w, 42, accent, accent, radius=14, sw=0)
    # Mask the lower curved corners of the header strip.
    rect(x, y + 24, w, 18, accent, accent, radius=0, sw=0)
    title_x = x + 18
    if num is not None:
        parts.append(f'<circle cx="{x + 26}" cy="{y + 21}" r="15" fill="{WHITE}"/>')
        text(x + 26, y + 27, str(num), 17, accent, 800, "middle")
        title_x = x + 52
    text(title_x, y + 29, title, 20, WHITE, 700)
    text(x + 18, y + 70, lines, 17, INK, 450, line_height=24)


def pill(x, y, w, title, fill, stroke, color=INK, size=16):
    rect(x, y, w, 32, fill, stroke, radius=15, sw=1.5)
    text(x + w / 2, y + 22, title, size, color, 600, "middle")


def section_panel(x, y, w, h, name, fill=WHITE, stroke="#d8e4ef"):
    rect(x, y, w, h, fill, stroke, radius=20, sw=2)
    label(x + 16, y + 14, 136, name)


def build_svg():
    parts.clear()
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">')
    parts.append('''<defs>
      <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L10,5 L0,10 z" fill="#516b84"/>
      </marker>
      <marker id="blue-arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L10,5 L0,10 z" fill="#2878b9"/>
      </marker>
    </defs>''')
    rect(0, 0, WIDTH, HEIGHT, BG, radius=0)

    # Header: title, purpose, and design principles.
    rect(22, 20, 500, 125, NAVY, NAVY, radius=18)
    text(272, 70, "DeskMate", 38, WHITE, 750, "middle")
    text(272, 111, "사내 IT 지원 AI Agent 구조도", 27, WHITE, 700, "middle")

    rect(540, 20, 720, 125, "#f8fbff", "#c9dcf4", radius=18)
    label(558, 34, 120, "목표")
    text(700, 61, ["근거 기반으로 IT 문의를 안내하고,", "미해결 이슈는 직원 승인 후 티켓으로 연결"], 21, INK, 600, line_height=32)

    rect(1278, 20, 620, 125, "#f8fbff", "#c9dcf4", radius=18)
    label(1296, 34, 150, "핵심 설계")
    text(1470, 61, ["Spring: 권한·티켓 쓰기 통제", "Python: Agent·RAG·모델 연동", "현재 구현과 목표 구성을 구분"], 18, INK, 550, line_height=27)

    # User channels and cross-cutting governance.
    section_panel(22, 160, 1876, 140, "사용자 채널", "#eaf3ff", "#c8ddf5")
    card(180, 180, 440, 100, "직원", ["장애 문의 · 추가 질문 응답", "해결 가이드 · 티켓 초안 확인"], WHITE, "#c6d9ef", "#416b9e")
    card(640, 180, 440, 100, "IT 담당자", ["담당 티켓 확인 · 조치 기록", "상태 변경 · 해결 결과 입력"], WHITE, "#c6d9ef", "#416b9e")
    card(1100, 180, 440, 100, "IT 관리자", ["담당자 배정·재배정", "미할당·예외 상황 처리"], WHITE, "#c6d9ef", "#416b9e")
    pill(1560, 194, 290, "Web UI → Spring API", BLUE, BLUE_STROKE, "#255f95", 17)
    text(1705, 250, "브라우저는 Python AI를 직접 호출하지 않음", 14, MUTED, 500, "middle")

    # Main interaction layer.
    section_panel(22, 315, 1876, 340, "AI 상담 흐름", WHITE, "#d8e4ef")
    # Spring service block.
    rect(180, 375, 355, 245, BLUE, BLUE_STROKE, radius=18, sw=2)
    rect(180, 375, 355, 48, "#2878b9", "#2878b9", radius=16, sw=0)
    rect(180, 407, 355, 16, "#2878b9", "#2878b9", radius=0, sw=0)
    text(357, 407, "Spring Boot · 제품 백엔드", 21, WHITE, 700, "middle")
    card(198, 440, 319, 68, "공개 API", ["인증·인가 · 입력 검증"], WHITE, "#c6d9ef", "#2878b9")
    card(198, 520, 319, 68, "업무 서비스", ["대화 · 승인 · 티켓 · 배정"], WHITE, "#c6d9ef", "#2878b9")
    pill(235, 594, 245, "티켓 쓰기 권한은 Spring에만", "#e8f3fc", BLUE_STROKE, "#255f95", 14)

    # Python AI service block and sequential stages.
    rect(565, 375, 1315, 245, "#fffaf0", "#f0d8a8", radius=18, sw=2)
    rect(565, 375, 1315, 48, "#c58618", "#c58618", radius=16, sw=0)
    rect(565, 407, 1315, 16, "#c58618", "#c58618", radius=0, sw=0)
    text(1222, 407, "Python AI Service · 내부 서비스 · 목표 구성", 21, WHITE, 700, "middle")
    pill(888, 431, 664, "Spring ↔ Python: 내부 HTTP/JSON · 최소 상담 문맥 · request_id", WHITE, AMBER_STROKE, "#80550e", 15)

    card(585, 472, 290, 122, "증상 파악", ["분류 · 필요한 정보 확인", "부족하면 추가 질문"], WHITE, "#e8d4af", "#b47410", 1)
    card(903, 472, 290, 122, "지식 검색", ["승인된 가이드에서 검색", "출처·버전·근거 구절 반환"], WHITE, "#d9c9f1", "#7953b5", 2)
    card(1221, 472, 290, 122, "근거 기반 안내", ["검색 결과를 바탕으로 답변", "근거 부족 시 해결책 추측 금지"], WHITE, "#c4e8e3", "#21877d", 3)
    card(1539, 472, 320, 122, "티켓 초안 제안", ["미해결이면 사실 중심 초안", "초안은 확정 티켓이 아님"], WHITE, "#f2d4bc", "#c06b24", 4)
    line(875, 532, 898, 532, "#b47410", 3, end="arrow")
    line(1193, 532, 1216, 532, "#7953b5", 3, end="arrow")
    line(1511, 532, 1534, 532, "#21877d", 3, end="arrow")
    line(535, 489, 559, 489, "#2878b9", 3, end="arrow")
    line(565, 575, 535, 575, "#2878b9", 2.5, dash="7 5", end="arrow")
    text(1522, 458, "해결되지 않은 경우에만", 13, "#9a5a1c", 600, "middle")

    # Capabilities and external model services.
    section_panel(22, 670, 1876, 180, "서비스·도구", "#eaf3ff", "#c8ddf5")
    rect(180, 722, 600, 105, WHITE, "#c6d9ef", radius=16)
    text(200, 752, "Spring 업무 기능", 20, "#255f95", 700)
    pill(200, 775, 165, "인증·인가", BLUE, BLUE_STROKE)
    pill(377, 775, 165, "승인 경계", BLUE, BLUE_STROKE)
    pill(554, 775, 205, "티켓·담당자 배정", BLUE, BLUE_STROKE)

    rect(800, 722, 610, 105, WHITE, "#e8d4af", radius=16)
    text(820, 752, "Python AI 기능", 20, "#80550e", 700)
    pill(820, 775, 170, "Agents SDK 후보", AMBER, AMBER_STROKE, "#80550e")
    pill(1002, 775, 170, "RAG Retriever", PURPLE, PURPLE_STROKE, "#67449a")
    pill(1184, 775, 205, "평가·문서 ingestion", AMBER, AMBER_STROKE, "#80550e")

    rect(1430, 722, 450, 105, WHITE, "#d8c8ed", radius=16)
    text(1450, 752, "외부 모델 API · 후보 미확정", 19, "#67449a", 700)
    pill(1450, 775, 190, "LLM 생성 API", PURPLE, PURPLE_STROKE, "#67449a")
    pill(1650, 775, 210, "Embedding API", PURPLE, PURPLE_STROKE, "#67449a")

    # Data sources and storage ownership.
    section_panel(22, 865, 1876, 200, "데이터 계층", WHITE, "#d8e4ef")
    rect(180, 917, 890, 128, "#f7fbff", "#b9d1e8", radius=16)
    rect(180, 917, 890, 36, "#356c9e", "#356c9e", radius=14, sw=0)
    rect(180, 939, 890, 14, "#356c9e", "#356c9e", radius=0, sw=0)
    text(625, 942, "PostgreSQL + pgvector · 한 인스턴스 목표 · DB role 분리", 18, WHITE, 700, "middle")
    text(205, 980, "Spring 소유", 17, "#255f95", 700)
    text(205, 1007, ["상담 · 메시지 · 승인", "티켓 · 상태 이벤트 · 할당"], 16, INK, 500, line_height=22)
    line(610, 965, 610, 1030, "#cad8e5", 2, end=None)
    text(640, 980, "Python AI 소유", 17, "#80550e", 700)
    text(640, 1007, ["knowledge_documents", "knowledge_chunks · vector(1536)"], 16, INK, 500, line_height=22)

    card(1090, 917, 350, 128, "지식 자료", ["승인된 공식·내부 가이드", "synthetic 데모 문서"], WHITE, "#d8e4ef", "#21877d")
    card(1460, 917, 420, 128, "학습·평가 자료", ["공개 후보는 보조 자료", "고정 평가셋·검수 사례 필요"], WHITE, "#d8e4ef", "#7953b5")
    line(1090, 985, 1076, 985, "#c58618", 2.5, dash="6 4", end="arrow")

    # Shared security and governance.
    section_panel(22, 1080, 1876, 112, "보안·거버넌스", PINK, PINK_STROKE)
    pill(180, 1135, 380, "인증·역할 기반 접근 · 목표", WHITE, PINK_STROKE, "#9f3151", 16)
    pill(580, 1135, 380, "개인정보 최소 전송 · 목표", WHITE, PINK_STROKE, "#9f3151", 16)
    pill(980, 1135, 380, "직원 승인 전 티켓 생성 금지", WHITE, PINK_STROKE, "#9f3151", 16)
    pill(1380, 1135, 480, "요청 ID · 출처 · 모델/인덱스 버전 관측", WHITE, PINK_STROKE, "#9f3151", 16)

    # Explicitly separate the running baseline from the target architecture.
    rect(22, 1215, 1876, 85, "#e8eef5", "#cbd7e2", radius=16)
    pill(42, 1237, 180, "현재 구현", GREEN, GREEN_STROKE, "#236a45", 17)
    text(245, 1265, "정적 Web UI  →  Python 규칙 상담  →  PostgreSQL 티켓", 20, INK, 600)
    line(995, 1230, 995, 1286, "#b8c6d4", 2, end=None)
    pill(1020, 1237, 180, "목표 구성", BLUE, BLUE_STROKE, "#255f95", 17)
    text(1220, 1265, "Spring 업무 백엔드  +  Python AI/RAG  +  PostgreSQL/pgvector", 19, INK, 600)

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    svg_text = build_svg()
    svg_path = ROOT / "docs" / "project-architecture.svg"
    png_path = ROOT / "docs" / "project-architecture.png"
    svg_path.write_text(svg_text, encoding="utf-8")
    inkscape = shutil.which("inkscape")
    if not inkscape:
        raise SystemExit("Inkscape is required to render PNG; the SVG source was written.")
    with tempfile.TemporaryDirectory(prefix="deskmate-inkscape-") as profile_dir:
        env = os.environ.copy()
        env["XDG_CONFIG_HOME"] = str(Path(profile_dir) / "config")
        env["XDG_CACHE_HOME"] = str(Path(profile_dir) / "cache")
        Path(env["XDG_CONFIG_HOME"]).mkdir()
        Path(env["XDG_CACHE_HOME"]).mkdir()
        subprocess.run([inkscape, str(svg_path), "--export-filename", str(png_path)], check=True, env=env)
    print(f"Wrote {svg_path.relative_to(ROOT)} and {png_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
