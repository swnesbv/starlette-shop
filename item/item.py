import ast

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse, PlainTextResponse

from db_config.storage_config import engine, async_session

from account.models import User

from options_select.opt_slc import (
    for_id,
    item_comment,
    id_and_owner,
)

from auth_privileged.opt_slc import (
    get_privileged_user,
    privileged,
)

from .models import Item, Purchases, Products

from .img import im_item, img
from .create_update import parent_create, child_img_update


templates = Jinja2Templates(directory="templates")


@privileged()
# ...
async def item_create(request):
    obj = await parent_create(request, Item, "item", im_item)
    return obj

@privileged()
# ...
async def item_update(request):
    # ..
    id = request.path_params["id"]
    context = {}
    amount, price = ""
    # ..
    form = await request.form()
    obj = await child_img_update(request, form, context, Item, id, "item", im_item, amount, price)
    return obj

@privileged()
# ...
async def item_delete(request):
    # ..
    id = request.path_params["id"]
    template = "/item/delete.html"

    async with async_session() as session:
        if request.method == "GET":
            # ..
            prv = await get_privileged_user(request, session)
            # ..
            i = await id_and_owner(session, Item, prv.id, id)
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
            prv = await get_privileged_user(request, session)
            # ..
            i = await id_and_owner(
                session, Item, prv.id, id
            )
            email = await for_id(session, User, i.owner)
            # ..
            await img.del_tm(email.email, i.id)
            # ..
            await session.delete(i)
            await session.commit()
            # ..
            response = RedirectResponse(
                "/item/list",
                status_code=302,
            )
            return response
    await engine.dispose()


async def item_list(request):
    # ..
    template = "/item/list.html"

    async with async_session() as session:
        # ..
        stmt = await session.execute(
            select(Item)
            .options(
                selectinload(Item.item_products),
            )
            .order_by(Item.created_at.desc())
        )
        obj_list = stmt.scalars().all()
        # ..
        context = {
            "request": request,
            "obj_list": obj_list,
        }
        return templates.TemplateResponse(template, context)
    await engine.dispose()


async def item_details(request):
    # ..
    id = request.path_params["id"]
    template = "/item/details.html"

    async with async_session() as session:
        # ..
        i = await for_id(session, Item, id)
        cmt_list = await item_comment(session, id)
        prv = await get_privileged_user(request, session)
        # ..
        if i:
            stmt = await session.execute(
                select(Products).where(Products.products_belongs == id)
            )
            all_products = stmt.scalars().all()
            # ..
            stmt = await session.execute(
                select(Purchases).where(Purchases.purchases_belongs == id)
            )
            all_purchases = stmt.scalars().all()
            # ..
            context = {
                "request": request,
                "i": i,
                "prv": prv,
                "cmt_list": cmt_list,
                "all_products": all_products,
                "all_purchases": all_purchases,
            }
            # ..
            return templates.TemplateResponse(template, context)
        return RedirectResponse("/item/list", status_code=302)
    await engine.dispose()


async def search(request):
    # ..
    query = request.query_params.get("query")
    template = "/item/search.html"

    async with async_session() as session:
        if request.method == "GET":
            # ..
            stmt = await session.execute(
                select(Item).where(Item.title.like("%" + query + "%"))
            )
            search_title = stmt.scalars().all()
            # ...
            context = {
                "request": request,
                "search_title": search_title,
            }
            # ..
            return templates.TemplateResponse(template, context)
    await engine.dispose()


async def item_categories(request):
    # ..
    async with async_session() as session:
        if request.method == "GET":
            # ..
            template = "/item/categories.html"
            categories = request.path_params["cts"]

            a = categories.replace("%20", " ")
            output = ast.literal_eval(a)
            # ..
            stmt = await session.execute(
                select(Item)
                .options(
                    selectinload(Item.item_products),
                )
                .where(
                    Item.categories.contains(output)
                )
            )
            obj_list = stmt.scalars().unique()
            print( "i..", obj_list)
            # ..
            stmt = await session.execute(
                select(Item.categories)
            )
            result = stmt.scalars().all()

            obj = []
            for x in result:
                if x is not None:
                    obj.extend(x)

            _ = list(set(obj))

            obj_unique = []
            # for x in obj:
            #     if x not in obj_unique:
            #         obj_unique.append(x)
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
        cts = form.getlist("categories")

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
