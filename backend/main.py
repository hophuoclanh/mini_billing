from domains.sale.controllers import router as sale_controller
from domains.inventory.controllers import router as inventory_controller
from domains.authentication.controllers import router as authentication_controller
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import dotenv
dotenv.load_dotenv()

app = FastAPI(title='Mini Billing')


app.include_router(authentication_controller, prefix='/authentication')
app.include_router(inventory_controller, prefix='/inventory')
app.include_router(sale_controller, prefix='/sale')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', tags=['Main'])
async def root():
    return {'message': 'Hello World from backend API'}


def main():
    uvicorn.run('main:app', host='localhost', port=5000, reload=True)


if __name__ == '__main__':
    main()
