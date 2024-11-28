from starlette.routing import Route

from . import (
    item,
    products,
    purchases,
)


routes = [
    # ..
    Route("/search", item.search, methods=["GET", "POST"]),
    # ..
    Route("/list", item.item_list),
    Route("/item/details/{id:int}", item.item_details),
    Route("/item/categories/{cts:str}", item.item_categories, methods=["GET", "POST"]),
    Route("/products/cts/{cts:str}", products.products_cts, methods=["GET", "POST"]),
    Route("/create", item.item_create, methods=["GET", "POST"]),
    Route("/update/{id:int}", item.item_update, methods=["GET", "POST"]),
    Route("/delete/{id:int}", item.item_delete, methods=["GET", "POST"]),
    # ..
    Route("/products/list", products.products_list),
    Route("/products/list-prv", products.products_list_prv),
    Route("/products/details/{id:int}", products.products_details),
    Route("/products/create", products.products_create, methods=["GET", "POST"]),
    Route(
        "/products/update/{id:int}", products.products_update, methods=["GET", "POST"]
    ),
    Route(
        "/products/delete/{id:int}", products.products_delete, methods=["GET", "POST"]
    ),
    # ..
    Route("/purchases/list", purchases.purchases_list),
    Route("/purchases/details/{id:int}", purchases.purchases_details),
    # ..
    Route("/purchases/{id:int}", purchases.purchases_create, methods=["GET", "POST"]),
    Route(
        "/purchases/order/{id:int}", purchases.purchases_order, methods=["GET", "POST"]
    ),
    Route(
        "/purchases/delete/{id:int}",
        purchases.purchases_delete,
        methods=["GET", "POST"],
    ),
]
