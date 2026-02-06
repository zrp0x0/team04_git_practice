from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from ..models.model import RecallRequest, RecallResponse, Expression
from ..database.connection import get_session

router = APIRouter()

@router.post("/mem/", response_model=RecallResponse)
async def recall_service(request: RecallRequest, session: Session = Depends(get_session)):
    cmd = request.recall
    
    # 전체 조회
    if cmd == "all":
        statement = select(Expression).order_by(Expression.id)
        results = session.exec(statement).all()
        # List[str] 형태로 반환
        expr_list = [expr.expr for expr in results]
        return RecallResponse(expr=expr_list)

    # 삭제 로직
    if cmd.startswith("-"):
        delete_target = cmd[1:]
        
        # -*
        if delete_target == "*":
            session.query(Expression).delete()

            statement = select(Expression)
            results = session.exec(statement).all()
            for item in results:
                session.delete(item)
            session.commit()
            return RecallResponse(expr=["ALL DELETED"])
        
        # --
        elif delete_target == "-":
            statement = select(Expression).order_by(Expression.id.desc()).limit(1)
            last_item = session.exec(statement).first()
            if last_item:
                session.delete(last_item)
                session.commit()
                return RecallResponse(expr=["LAST DELETED"])
            else:
                return RecallResponse(expr=["DB EMPTY"])
        
        # -ID
        else:
            try:
                target_id = int(delete_target)
                target_item = session.get(Expression, target_id)
                if target_item:
                    session.delete(target_item)
                    session.commit()
                    
                    # ID 재정렬 로직
                    next_items = session.exec(select(Expression).where(Expression.id > target_id)).all()
                    for item in next_items:
                        item.id = item.id - 1
                        session.add(item)
                    session.commit()
                    
                    return RecallResponse(expr=[f"ID {target_id} DELETED"])
                else:
                    return RecallResponse(expr=[f"No Such ID: {target_id}"])
            except ValueError:
                return RecallResponse(expr=["Invalid Command"])

    # 특정 ID 조회
    try:
        target_id = int(cmd)
        item = session.get(Expression, target_id)
        if item:
            return RecallResponse(expr=[item.expr])
        else:
            return RecallResponse(expr=[f"No Such Expression: {target_id}"])
    except ValueError:
        return RecallResponse(expr=["Invalid ID Format"])

