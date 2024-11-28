
from starlette.routing import Route

from . import views

routes = [

    Route(
        "/item/create/{id:int}",
        views.cmt_item_create,
        methods=["GET", "POST"]
    ),
    Route(
        "/products/create/{id:int}",
        views.cmt_products_create,
        methods=["GET", "POST"]
    ),
    Route(
        "/purchases/create/{id:int}",
        views.cmt_purchases_create,
        methods=["GET", "POST"]
    ),
    #..
    Route(
        "/item/update/{id:int}",
        views.cmt_item_update,
        methods=["GET", "POST"]
    ),
    Route(
        "/products/update/{id:int}",
        views.cmt_products_update,
        methods=["GET", "POST"]
    ),
    Route(
        "/purchases/update/{id:int}",
        views.cmt_purchases_update,
        methods=["GET", "POST"]
    ),
    #..
    Route(
        "/delete/{id:int}",
        views.cmt_delete,
        methods=["GET", "POST"]
    ),
]
