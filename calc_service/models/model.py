from typing import Optional, List
from sqlmodel import SQLModel, Field

# DB 테이블
class Expression(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    expr: str

# Request
class EvalRequest(SQLModel):
    expr: str

class RecallRequest(SQLModel):
    recall: str

# Response
class EvalResponse(SQLModel):
    result: str

class RecallResponse(SQLModel):
    expr: List[str]
# PR 테스트 - parsksehun

