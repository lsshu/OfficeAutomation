from fastapi import FastAPI
from app.admin.main import router as admin_router
from app.member.main import router as member_route
from app.region.main import router as region_route

app = FastAPI(
    title='Office Automation API Docs',
    description='Office Automation API接口文档',
    version='1.0.0'
)

app.include_router(admin_router, prefix='/api')
app.include_router(region_route, prefix='/api')
app.include_router(member_route, prefix='/api')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
