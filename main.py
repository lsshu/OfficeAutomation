from fastapi import FastAPI
from app.admin.main import router as admin_router
from app.member.main import router as member_route

app = FastAPI(
    title='Office Automation API Docs',
    description='Office Automation API接口文档',
    version='1.0.0'
)

app.include_router(admin_router, prefix='/api')
app.include_router(member_route, prefix='/api')
