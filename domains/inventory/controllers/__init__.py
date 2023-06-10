from fastapi import APIRouter, Depends, HTTPException
from domains.inventory.controllers.product_controller import router as product_controller
from domains.inventory.controllers.category_controller import router as category_controller

router = APIRouter(tags=['Inventory'])
router.include_router(product_controller, prefix='/product')
router.include_router(category_controller, prefix='/category')
