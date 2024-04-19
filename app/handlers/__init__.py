from aiogram import Router

from .orders import orders_router
from .command import command_router
from .catalog import catalog_router
from .faqs import faqs_router

__routers = [
    command_router,
    catalog_router,
    orders_router,
    faqs_router
]

routers = Router()
for _router in __routers:
    routers.include_router(_router)