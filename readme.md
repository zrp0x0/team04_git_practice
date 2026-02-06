# 코드 실행 가이드
``` 
# python version 3.10.x
python3 -m venv .venv
source ./.venv/bin/activate (Linux) # 가상환경 사용
pip install -r requirements.txt

uvicorn calc_service.main:app --reload

// frontend
webcalc.html click
```