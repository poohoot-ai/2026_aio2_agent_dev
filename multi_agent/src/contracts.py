from pydantic import BaseModel, Field

class ResearchNotes(BaseModel):
    """조사원의 출력 계약"""

    # TODO: facts 필드를 만드세요 — 문자열 리스트, description은 "원문에서 뽑은 핵심 사실 5개. 각 사실은 한 문장."
    facts: list[str] = Field(description="원문에서 뽑은 핵심 사실 5개, 각 사실은 한 문장.")

class Draft(BaseModel):
    """작성자의 출력 계약"""

    # TODO: 두 Field에 description을 채우세요 — title: "소개 글 제목", body: "사실에 근거한 소개 단락 (3~4문장)"
    title: str = Field(description="소개 글 제목")
    body: str = Field(description="사실에 근거한 소개 단락 (3~4문장)")

class Review(BaseModel):
    """검토자의 출력 계약"""

    # TODO: passed 필드를 만드세요 — True/False 타입, description은 "모든 사실이 정확히 반영되고 지어낸 내용이 없으면 True"
    passed: bool = Field(description="모든 사실이 정확히 반영되고 지어낸 내용이 없으면 True")
    missing_facts: list[str] = Field(description="초안에 빠졌거나 왜곡된 사실 목록")
    comments: str = Field(description="한 줄 총평")