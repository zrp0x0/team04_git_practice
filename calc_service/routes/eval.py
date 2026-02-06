from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..models.model import EvalRequest, EvalResponse, Expression
from ..database.connection import get_session

router = APIRouter()

@router.post("/eval/", response_model=EvalResponse)
async def evaluate_expression(request: EvalRequest, session: Session = Depends(get_session)):
    expression_str = request.expr
    
    # eval 사용
    # - 수식을 계산할 수 있는 함수
    try:
        result_value = eval(expression_str) # eval을 사용 / 위험할 수 있기는 함
        result_str = str(result_value)
    except Exception:
        result_str = "Error"

    # DB 저장
    if result_str != "Error":
        new_expr = Expression(expr=expression_str)
        session.add(new_expr)
        session.commit()
        session.refresh(new_expr)

    return EvalResponse(result=result_str)
