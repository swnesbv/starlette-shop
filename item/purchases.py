import json

from sqlalchemy.future import select

from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse
from starlette.responses import RedirectResponse, PlainTextResponse

from db_config.storage_config import engine, async_session

from account.models import User

from options_select.opt_slc import (
    for_id,
    purchases_comment,
    id_and_owner,
)

from .models import Products, Purchases
from .img import img


templates = Jinja2Templates(directory="templates")


async def purchases_create(request):
    # ..
    id = request.path_params["id"]
    template = "/purchases/create.html"

    async with async_session() as session:
        if request.method == "GET":
            i = await for_id(session, Products, id)
            amount_list = []
            price_list = []
            if i.amount:
                amount_list = json.loads(i.amount)
            if i.amount:
                price_list = json.loads(i.price)
            if i:
                return templates.TemplateResponse(
                    template,
                    {
                        "request": request,
                        "i": i,
                        "amount_list": amount_list,
                        "price_list": price_list,
                    },
                )
            return PlainTextResponse("none..! products..!")

        if request.method == "POST":
            # ..
            i = await for_id(session, Products, id)
            # ..
            form = await request.form()
            # ..
            amount = {
                "container": form.get("a_container"),
                "boxes": form.get("a_boxes"),
                "carton": form.get("a_carton"),
                "units": form.get("a_units"),
            }
            price = {
                "container": form.get("p_container"),
                "boxes": form.get("p_boxes"),
                "carton": form.get("p_carton"),
                "units": form.get("p_units"),
            }
            # ..
            payload = {
                "id": i.id,
                "title": i.title,
                "categories": i.categories,
                "cts": i.cts,
                "amount": amount,
                "price": price,
            }
            token = json.dumps(payload)
            response = RedirectResponse(
                f"/item/purchases/order/{id}", status_code=302
            )
            response.set_cookie(
                key="purchases", value=token, path="/", httponly=True
            )
            # ..
            # if "paid for the product":
            #     new = Purchases()
            #     new.title = i.title
            #     new.description = i.description
            #     new.categories = i.categories
            #     new.cts = i.cts
            #     new.amount = amount
            #     new.price = price
            #     new.created_at = datetime.now()
            #     return RedirectResponse("/", status_code=302)
            return response


async def get_token_purchases(request):
    if request.cookies.get("purchases"):
        token = request.cookies.get("purchases")
        if token:
            payload = json.loads(token)
            return payload
async def get_purchases(request):
    while True:
        payload = await get_token_purchases(request)
        if not payload:
            break
        return payload

async def purchases_order(request):
    # ..
    # payload = await get_purchases(request)
    # response = JSONResponse(payload)
    # return response
    # ..
    id = request.path_params["id"]
    payload = await get_purchases(request)
    if payload:
        response = JSONResponse(payload)
        return response
    return RedirectResponse(
        f"/item/purchases/{id}", status_code=302
    )






# ...
async def purchases_delete(request):
    # ..
    id = request.path_params["id"]
    template = "/purchases/delete.html"

    async with async_session() as session:
        if request.method == "GET":
            # ..
            i = await id_and_owner(session, Purchases, request.user.user_id, id)
            if i:
                return templates.TemplateResponse(
                    template,
                    {
                        "request": request,
                        "i": i,
                    },
                )
            return PlainTextResponse("You are banned - this is not your account..!")
        # ...
        if request.method == "POST":
            # ..
            i = await id_and_owner(session, Purchases, request.user.user_id, id)
            email = await for_id(session, User, i.owner)
            # ..
            await img.del_service(email.email, i.purchases_belongs, id)
            # ..
            await session.delete(i)
            await session.commit()
            # ..
            response = RedirectResponse(
                "/item/purchases/list",
                status_code=302,
            )
            return response
    await engine.dispose()


async def purchases_list(request):
    # ..
    template = "/purchases/list.html"

    async with async_session() as session:
        # ..
        result = await session.execute(select(Purchases).order_by(Purchases.id))
        obj_list = result.scalars().all()
        # ..
        context = {
            "request": request,
            "obj_list": obj_list,
        }
        return templates.TemplateResponse(template, context)
    await engine.dispose()


async def purchases_details(request):
    # ..
    id = request.path_params["id"]
    template = "/purchases/details.html"

    async with async_session() as session:
        # ..
        i = await for_id(session, Purchases, id)
        # ..
        cmt_list = await purchases_comment(session, id)
        # ..
        context = {
            "request": request,
            "i": i,
            "cmt_list": cmt_list,
        }
        return templates.TemplateResponse(template, context)
    await engine.dispose()
