import ast
import json

from sqlalchemy.future import select

from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse, PlainTextResponse

from db_config.storage_config import engine, async_session

from account.models import User

from auth_privileged.opt_slc import (
    privileged,
    id_and_owner_prv,
    token_privileged
)

from options_select.opt_slc import for_id, products_comment

from .create_update import child_img_create, child_img_update

from .img import im_products, img
from .models import Item, Products

templates = Jinja2Templates(directory="templates")


def nonesafe_loads(obj):
    if obj is not None:
        return json.loads(obj)

@privileged()
# ...
async def products_create(request):
    # ..
    form = await request.form()
    obj_amount = {
        "container": form.get("a_container"),
        "boxes": form.get("a_boxes"),
        "carton": form.get("a_carton"),
        "units": form.get("a_units"),
    }
    obj_price = {
        "container": form.get("p_container"),
        "boxes": form.get("p_boxes"),
        "carton": form.get("p_carton"),
        "units": form.get("p_units"),
    }
    amount = json.dumps(obj_amount)
    price = json.dumps(obj_price)

    belongs = form.get("belongs")
    new = Products()

    if belongs is not None:
        new.products_belongs = int(belongs)
        new.amount = amount
        new.price = price
    # ..
    obj = await child_img_create(
        request, form, belongs, Item, new, "products", "item", im_products
    )
    return obj


@privileged()
# ...
async def products_update(request):
    # ..
    id = request.path_params["id"]
    context = {}
    # ..
    async with async_session() as session:
        # ..
        i = await id_and_owner_prv(request, session, Products, id)
        # ..
        amount_list = nonesafe_loads(i.amount)
        price_list = nonesafe_loads(i.price)
        context["amount_list"] = amount_list
        context["price_list"] = price_list
        # ..
        form = await request.form()
        # ..
        obj_amount = {
            "container": form.get("a_container"),
            "boxes": form.get("a_boxes"),
            "carton": form.get("a_carton"),
            "units": form.get("a_units"),
        }
        obj_price = {
            "container": form.get("p_container"),
            "boxes": form.get("p_boxes"),
            "carton": form.get("p_carton"),
            "units": form.get("p_units"),
        }
        amount = json.dumps(obj_amount)
        price = json.dumps(obj_price)
        # ..
        obj = await child_img_update(
            request, form, context, Products, id, "products", im_products, amount, price
        )

        return obj


@privileged()
# ...
async def products_delete(request):
    # ..
    id = request.path_params["id"]
    template = "/products/delete.html"

    async with async_session() as session:
        if request.method == "GET":
            # ..
            i = await id_and_owner_prv(request, session, Products, id)
            # ..
            if i:
                return templates.TemplateResponse(
                    template,
                    {"request": request},
                )
            return PlainTextResponse("You are banned - this is not your account..!")
        # ...
        if request.method == "POST":
            # ..
            i = await id_and_owner_prv(request, session, Products, id)
            email = await for_id(session, User, i.owner)
            # ..
            await img.del_rent(email.email, i.rent_belongs, id)
            # ..
            await session.delete(i)
            await session.commit()
            # ..
            response = RedirectResponse(
                "/item/products/list",
                status_code=302,
            )
            return response
    await engine.dispose()


async def products_list(request):
    # ..
    template = "/products/list.html"

    async with async_session() as session:
        # ..
        stmt = await session.execute(
            select(Products).order_by(Products.id.desc())
        )
        result = stmt.scalars().all()
        obj_list = [
            {
                "id": i.id,
                "title": i.title,
                "description": i.description,
                "file": i.file,
                "categories": i.categories,
                "cts": i.cts,
                "amount": nonesafe_loads(i.amount),
                "price": nonesafe_loads(i.price),
                "created_at": i.created_at,
                "modified_at": i.modified_at,
                "owner": i.owner,
            }
            for i in result
        ]
        # ..
        context = {
            "request": request,
            "obj_list": obj_list,
        }
        return templates.TemplateResponse(template, context)
    await engine.dispose()


async def products_list_prv(request):
    # ..
    template = "/products/list_prv.html"

    async with async_session() as session:
        # ..
        i = await token_privileged(request, session, Products)
        if i:
            context = {
                "request": request,
                "obj_list": i,
            }
            return templates.TemplateResponse(template, context)
        return RedirectResponse("/privileged/login")
    await engine.dispose()


async def products_details(request):
    # ..
    id = request.path_params["id"]
    template = "/products/details.html"

    async with async_session() as session:
        # ..
        i = await for_id(session, Products, id)
        # ..
        amount_list = nonesafe_loads(i.amount)
        price_list = nonesafe_loads(i.price)
        # ..
        cmt_list = await products_comment(session, id)
        # ..
        context = {
            "request": request,
            "i": i,
            "amount_list": amount_list,
            "price_list": price_list,
            "cmt_list": cmt_list,
        }
        return templates.TemplateResponse(template, context)
    await engine.dispose()


async def products_cts(request):
    # ..
    async with async_session() as session:
        if request.method == "GET":
            # ..
            template = "/products/cts.html"
            categories = request.path_params["cts"]

            a = categories.replace("%20", "")
            output = ast.literal_eval(a)
            # ..
            stmt = await session.execute(
                select(Products)
                .where(
                    Products.cts.contains(output)
                )
            )
            obj_list = stmt.scalars().all()
            # ..
            stmt = await session.execute(
                select(Products.cts)
            )
            result = stmt.scalars().all()

            obj = []
            for x in result:
                if x is not None:
                    obj.extend(x)

            _ = list(set(obj))

            obj_unique = []
            _ = [obj_unique.append(x) for x in obj if x not in obj_unique]

            # ..
            context = {
                "request": request,
                "obj_list": obj_list,
                "obj_unique": obj_unique,
            }
            # ..
            return templates.TemplateResponse(template, context)

    if request.method == "POST":
        form = await request.form()
        on_off = form.getlist("on_off")
        cts = form.getlist("cts")

        params = []
        for (c, d) in zip(on_off, cts):
            if c == "1" :
                params.append(d)
        print(" params..", params)
        print("..")
        return RedirectResponse(
            f"/item/item/categories/{params}",
            status_code=302,
        )
