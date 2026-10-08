"""Generate the project overview infographic as SVG and PNG."""
from html import escape
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1600, 1250
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
    parts.append('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1250" viewBox="0 0 1600 1250">')
    parts.append('<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#516b84"/></marker></defs>')
    rect(0, 0, 1600, 1250, BG, radius=0)
    rect(30, 25, 1540, 100, NAVY)
    text(65, 69, "DeskMate | 사내 시스템 장애 진단·담당자 연결 AI Agent", 31, WHITE, 700)
    text(65, 104, "목표 설계: Spring Boot 업무 백엔드 + Python AI Service + PostgreSQL/pgvector", 20, "#d8eaff", 500)

    card(60, 150, 470, 100, "직원", ["장애 문의 · 추가 질문 응답 · 초안 승인"], WHITE, BLUE_STROKE, "#416b9e")
    card(565, 150, 470, 100, "IT 담당자", ["티켓 확인 · 조치 기록 · 상태 변경"], WHITE, BLUE_STROKE, "#416b9e")
    card(1070, 150, 470, 100, "IT 관리자", ["담당자 배정·재배정 · 미할당 처리"], WHITE, BLUE_STROKE, "#416b9e")
    line(295, 250, 650, 285)
    line(800, 250, 800, 285)
    line(1305, 250, 950, 285)
    rect(500, 285, 600, 100, WHITE, BLUE_STROKE)
    text(800, 325, "Web UI · 직원 상담 / 담당자 보드", 25, NAVY, 700, "middle")
    text(800, 358, "문의 · 출처 확인 · 티켓 승인 · 처리 결과 조회", 19, MUTED, 500, "middle")
    parts.append('<path d="M650,385 L650,410 L390,410 L390,455" fill="none" stroke="#516b84" stroke-width="3" marker-end="url(#arrow)"/>')
    text(460, 434, "공개 HTTP API", 17, MUTED, 600)
    pill(995, 402, 545, "브라우저 요청은 Spring을 통해 처리", BLUE, BLUE_STROKE, NAVY, 18)

    rect(60, 455, 660, 310, BLUE, BLUE_STROKE)
    text(85, 498, "Spring Boot · 제품 백엔드", 27, "#255f95", 700)
    card(85, 525, 195, 155, "인증·상담", ["사용자 권한 검증", "대화 세션·이력", "AI 응답 검증"], WHITE, BLUE_STROKE, "#2878b9")
    card(292, 525, 195, 155, "승인·티켓", ["초안 확인·승인", "멱등 티켓 생성", "상태·이력 저장"], WHITE, BLUE_STROKE, "#2878b9")
    card(499, 525, 195, 155, "담당자 업무", ["진단 도구 Gateway", "소유 팀·배정 검증", "처리 결과 조회"], WHITE, BLUE_STROKE, "#2878b9")
    pill(85, 704, 610, "티켓 생성·수정과 최종 권한 판단은 Spring이 담당", WHITE, BLUE_STROKE, "#255f95", 17)

    rect(880, 455, 660, 310, "#fffaf0", AMBER_STROKE)
    text(905, 498, "Python AI Service · 내부 AI 런타임", 27, "#80550e", 700)
    card(905, 525, 195, 155, "증상 파악", ["의도·분류 판단", "필수 정보 확인", "추가 질문 생성"], WHITE, AMBER_STROKE, "#b47410", 1)
    card(1112, 525, 195, 155, "근거 조사", ["문서·DB·로그·코드", "사실·원인 후보 구분", "출처·버전 반환"], WHITE, PURPLE_STROKE, "#7953b5", 2)
    card(1319, 525, 195, 155, "초안 제안", ["해결 조치 또는 이관", "조사 근거 포함 초안", "현재 소유 팀 추천"], WHITE, TEAL_STROKE, "#21877d", 3)
    pill(905, 704, 610, "단일 Agent + 읽기 조사 도구 · 티켓 쓰기는 Spring에서 승인 후 실행", WHITE, AMBER_STROKE, "#80550e", 16)
    line(720, 566, 880, 566)
    text(800, 536, "내부 HTTP/JSON", 16, NAVY, 700, "middle")
    text(800, 598, ["최근 대화", "허용 검색 범위"], 15, MUTED, 500, "middle", 22)
    line(880, 658, 720, 658)
    text(800, 692, ["답변·출처", "티켓 초안"], 15, MUTED, 500, "middle", 22)

    line(390, 765, 390, 865)
    text(215, 818, "상담·승인·티켓 저장", 17, "#255f95", 600)
    parts.append('<path d="M1160,765 L1160,835 L700,835 L700,865" fill="none" stroke="#516b84" stroke-width="3" stroke-dasharray="7 5" marker-end="url(#arrow)"/>')
    text(765, 825, "지식 검색 / 별도 계정으로 적재", 16, "#80550e", 600)
    line(1040, 765, 1040, 865)
    text(1060, 798, "모델 호출", 16, "#67449a", 600)
    line(1380, 865, 1380, 765)
    text(1400, 823, "Spring 도구 경유", 14, "#21877d", 600)

    rect(60, 865, 700, 180, WHITE, BLUE_STROKE)
    text(85, 904, "PostgreSQL + pgvector · 공유 인스턴스", 24, NAVY, 700)
    line(403, 925, 403, 1022, "#d1deeb", 2, end=None)
    text(85, 940, "Spring 소유 · 업무 테이블", 18, "#255f95", 700)
    text(85, 971, ["상담 · 메시지 · 승인", "티켓 · 상태 이벤트 · 할당"], 17, INK, 500, line_height=28)
    text(425, 940, "Python 소유 · 지식 인덱스", 18, "#80550e", 700)
    text(425, 971, ["지식 문서 · chunk · embedding", "검색/적재 계정 권한 분리"], 17, INK, 500, line_height=28)
    card(880, 865, 320, 180, "LLM / Embedding", ["호스팅 API로 시작", "생성·벡터 계산", "모델·SDK는 후보 단계", "자체 추론은 향후 선택"], WHITE, PURPLE_STROKE, "#7953b5")
    card(1220, 865, 320, 180, "업무 시스템·근거", ["읽기 전용 업무 DB", "마스킹된 요청 로그" , "배포 코드·업무 정의", "현재 서비스 소유 팀"], WHITE, TEAL_STROKE, "#21877d")

    rect(60, 1070, 1480, 85, PINK, PINK_STROKE)
    text(85, 1104, "공통 보안·관측 · 목표", 21, "#9f3151", 700)
    text(85, 1134, "서비스 간 인증 · 개인정보 최소 전송 · 직원 승인 · 중복 생성 방지 · request_id / 출처 / 모델 버전 기록", 19, "#9f3151", 500)
    rect(60, 1180, 1480, 45, GREEN, GREEN_STROKE)
    text(85, 1210, "현재 구현: 정적 Web UI + Python 규칙 상담 + PostgreSQL 티켓 | Spring·AI·RAG는 구현 전", 19, "#236a45", 600)
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
