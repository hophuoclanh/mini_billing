import dotenv
dotenv.load_dotenv()
import uvicorn
from fastapi import FastAPI, Request
from domains.authentication.controllers import router as authentication_controller
from domains.inventory.controllers import router as inventory_controller
from domains.sale.controllers import router as sale_controller

app = FastAPI(title='Mini Billing')

app.include_router(authentication_controller, prefix='/authentication')
app.include_router(inventory_controller, prefix='/inventory')
app.include_router(sale_controller, prefix='/sale')

@app.get('/', tags=['Main'])
async def root():
    return {'message': 'Hello World'}

def main():
    uvicorn.run('main:app', host='localhost', port=2000, reload=True)

if __name__ == '__main__':
    main()
