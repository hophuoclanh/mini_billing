import dotenv
dotenv.load_dotenv()
import uvicorn
from fastapi import FastAPI, Request
from domains.authentication.controllers import router as authentication_controller

app = FastAPI(title='Mini Billing')

app.include_router(authentication_controller, prefix='/authentication')

@app.get('/', tags=['Main'])
async def root():
    return {'message': 'Hello World'}

def main():
    uvicorn.run('main:app', host='localhost', port=1000, reload=True)

if __name__ == '__main__':
    main()
