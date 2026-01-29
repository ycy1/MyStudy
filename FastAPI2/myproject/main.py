from fastapi import FastAPI,APIRouter, Depends, Header, Query, HTTPException
import uvicorn


'''
# 依赖注入执行顺序
# 函数参数级 < 路径级 < 路由级 < 全局级
'''
class ParamToken:
    def __init__(self, token_class: str = Header(...)):
        if token_class != "456":
            raise HTTPException(status_code=401, detail="Invalid token222")

def get_ParamToken(token_class:str=Header(...)):
    return ParamToken(token_class) # 作为路径级依赖注入
def param_token(token: str = Header(...)):
    if token != "123":
        raise HTTPException(status_code=401, detail="Invalid token")

app = FastAPI(dependencies=[Depends(param_token)])

route = APIRouter(prefix="/api", tags=["api"],dependencies=[Depends(param_token)])

@route.get("/root")
async def root():
    return {"message": "Hello World"}


@route.get("/root2", dependencies=[Depends(get_ParamToken)])
async def root2():
    return {"message": "Hello World2"}

def param(q: str = None):
    return q.upper()
def param2(q: int = Query("10" ,ge = 20), q2: str = None):
    return {"q": q, "q2": q2}

@app.get("/info")
async def info(q: str = Depends(param)):
    return q

@app.get("/info2")
async def info2(q: dict = Depends(param2)):
    return q
@app.get("/token", dependencies=[Depends(param_token)])
async def token():
    return "OK"


app.include_router(route)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
