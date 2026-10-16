from multi_agent.src.contracts import ResearchNotes, Draft, Review
from multi_agent.src.multi_agent_1 import run_research_team

# 에이전트 테스트 프로그램

SOURCE = """[내부 소개 자료] 달빛 도서관
달빛 도서관은 밤 10시부터 새벽 2시까지 여는 무인 야간 도서관이다.
서울 마포구에 1호점이 있으며, 좌석은 총 48석이다.
입장은 월 구독제이며, 구독료는 월 19,900원이다.
사서 대신 안내 로봇 '루나'가 책 추천과 반납을 돕는다.
조용한 환경을 위해 통화와 취식은 금지된다.
회원의 62%가 20~30대 직장인이다.
2026년 12월에 부산 2호점이 문을 열 예정이다."""

# print(SOURCE)

SOURCE2 = """[내부 소개 자료] 새벽 수영 클럽
새벽 수영 클럽은 평일 오전 5시 30분부터 7시까지 운영하는 직장인 수영 모임이다.
장소는 성수동의 실내 수영장이며, 레인 3개를 통째로 빌려 쓴다.
월 회비는 89,000원이고, 강습료가 포함되어 있다.
초급반·중급반·자유수영반 세 반으로 나뉜다.
수료 기준을 통과하면 한강 야외 수영 행사에 참가할 수 있다.
현재 회원은 74명이며 대기자가 30명이 넘는다."""

results = []

def check(name, ok):
    """검사 하나의 결과를 출력하고 기록한다."""
    print(f"  {'O' if ok else 'X'} {name}")
    results.append((name, ok))


def print_result(notes, draft, review):
    """노트북 3-3과 같은 모양으로 결과를 출력한다."""
    print("[조사원의 사실]")
    for f in notes.facts:
        print("-", f)
    print("[작성자의 초안]")
    print("제목:", draft.title)
    print("본문:", draft.body)
    print("[검토자의 판정]")
    print(
        "통과:",
        review.passed,
        "| 빠진 사실:",
        review.missing_facts,
        "| 총평:",
        review.comments,
    )

def check_team(label, notes, draft, review, keyword):
    """두 자료에 공통으로 쓰는 검사 — 계약·개수·자료 반영"""
    print(f"\n[{label} 검사]")
    check(
        f"{label}: 세 역할의 출력이 계약 객체다",
        isinstance(notes, ResearchNotes)
        and isinstance(draft, Draft)
        and isinstance(review, Review),
    )
    check(f"{label}: 사실이 5개다", len(notes.facts) == 5)
    check(
        f"{label}: 제목과 본문이 비어 있지 않다",
        bool(draft.title.strip()) and bool(draft.body.strip()),
    )
    check(f"{label}: 판정이 True/False다", isinstance(review.passed, bool))
    check(
        f"{label}: 사실에 자료의 고유 단어 '{keyword}'가 들어 있다",
        any(keyword in f for f in notes.facts),
    )
    check(f"{label}: 본문에 '{keyword}'가 들어 있다", keyword in draft.body)

# 3-3 파이프라인 실행
print("===3-3. 달빛 도서관 ===")
notes, draft, review = run_research_team(SOURCE)
print_result(notes, draft, review)
check_team("3-3", notes, draft, review, "달빛 도서관")

# 3-4 새 자료로 재사용
print("===3-4. 새벽 수영 클럽 ===")
notes2, draft2, review2 = run_research_team(SOURCE2)
print_result(notes2, draft2, review2)
check_team("3-4", notes2, draft2, review2, "새벽 수영 클럽")
check(
    "3-4: 새 자료의 사실에 앞 자료(달빛 도서관)가 섞이지 않았다.",
    not any("달빛" in f for f in notes2.facts)
)

# 요약
failures = [name for name, ok in results if not ok]
print("failures:", failures)
