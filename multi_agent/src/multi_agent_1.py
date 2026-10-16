# agent 소스
import os

# 추적 끄기: 2과목 Day17에서 .env의 LANGSMITH_TRACING을 켰다면 오늘 호출이 전부 전송된다
os.environ["LANGSMITH_TRACING"] = "false"
os.environ["LANGCHAIN_TRACING_V2"] = "false"

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# from pydantic import BaseModel, Field, ValidationError

from multi_agent.src.roles import ROLES, role_to_system
from multi_agent.src.contracts import ResearchNotes, Draft, Review

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)  # 생성 역할: 조사원·작성자
llm_strict = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # 판정 역할: 검토자

print("준비 완료:", llm.model_name)

def researcher_agent(source):
    """조사원(계약 버전): 원문 → ResearchNotes"""
    # TODO: prompt를 채우세요 — 조사원 역할 + "핵심 사실 5개를 뽑으세요" + [원문] source (2-4와 같다)
    prompt = f"""
    {role_to_system(ROLES["researcher"])}

다음 원문에서 핵심 사실 5개를 뽑으세요.

[원문]
{source}
    """
    return llm.with_structured_output(ResearchNotes).invoke(prompt)


def writer_agent(facts):
    """작성자(계약 버전): 사실 리스트 → Draft"""
    facts_text = "\n".join(f"- {f}" for f in facts)
    # TODO: prompt를 채우세요 — 작성자 역할 + [조사원이 정리한 사실] facts_text + "위 사실로 서비스 소개 글을 작성하세요. 본문은 3~4문장."
    prompt = f"""role_to_system(ROLES["writer"])

[조사원이 정리한 사실]
{facts_text}

위 사실로 서비스 소개 글을 작성하세요. 본문은 3~4문장.
    """
    
    # TODO: llm에 Draft 계약을 걸어 prompt를 호출하고 결과를 반환하세요
    return llm.with_structured_output(Draft).invoke(prompt)


def reviewer_agent(facts, draft):
    """검토자(계약 버전): 사실+초안 → Review"""
    facts_text = "\n".join(f"- {f}" for f in facts)
    
    # TODO: prompt를 채우세요 — 검토자 역할 + [기준 사실] facts_text + [초안] 제목 draft.title·본문 draft.body
    #       + "각 사실이 초안에 반영됐는지, 사실에 없는 내용이 섞였는지 판정하세요"
    prompt = f"""
    {role_to_system(ROLES["reviewer"])}

[기준 사실]
{facts_text}

[초안]
제목: {draft.title}
본문: {draft.body}

각 사실이 초안에 반영됐는지, 사실에 없는 내용이 섞였는지 판정하세요.
    """
    
    # TODO: 판정용 모델(llm_strict)에 Review 계약을 걸어 prompt를 호출하고 결과를 반환하세요
    return llm_strict.with_structured_output(Review).invoke(prompt)


def run_research_team(source):
    """조사 → 작성 → 검토 파이프라인 (계약 적용)"""
    
    # TODO: 조사 → 작성 → 검토 순서로 연결하세요
    #       조사원은 source로 notes를, 작성자는 notes.facts로 draft를, 검토자는 notes.facts와 draft로 review를 만든다
    notes = researcher_agent(source)
    draft = writer_agent(notes.facts)
    review = reviewer_agent(notes.facts, draft)
    
    return notes, draft, review