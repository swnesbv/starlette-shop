
from pathlib import Path

import shutil

from sqlalchemy import func, and_
from sqlalchemy.future import select

from comment.models import Comment

from config.settings import BASE_DIR


async def all_total(session, model):
    stmt = await session.execute(select(func.count(model.id)))
    result = stmt.scalars().all()
    return result


async def for_in(session, model):
    stmt = await session.execute(
        select(model)
    )
    result = stmt.scalars().all()
    return result


async def for_id(session, model, id):
    stmt = await session.execute(
        select(model)
        .where(model.id == id)
    )
    result = stmt.scalars().first()
    return result


async def left_right_first(session, model, left, right):
    stmt = await session.execute(
        select(model)
        .where(left == right)
    )
    result = stmt.scalars().first()
    return result

async def left_right_all(session, model, left, right):
    stmt = await session.execute(
        select(model)
        .where(left == right)
    )
    result = stmt.scalars().all()
    return result


async def id_and_owner(session, model, owner, id):
    stmt = await session.execute(
        select(model).where(
            and_(
                model.id == id,
                model.owner == owner,
            )
        )
    )
    result = stmt.scalars().first()
    return result


async def owner_request(session, model, owner):
    stmt = await session.execute(
        select(model).where(model.owner == owner)
    )
    result = stmt.scalars().all()
    return result


# ..
async def item_comment(session, id):
    stmt = await session.execute(
        select(Comment)
        .where(Comment.cmt_item_id == id)
        .order_by(Comment.created_at.desc())
    )
    result = stmt.scalars()
    return result


async def products_comment(session, id):
    stmt = await session.execute(
        select(Comment)
        .where(Comment.cmt_products_id == id)
        .order_by(Comment.created_at.desc())
    )
    result = stmt.scalars()
    return result


async def purchases_comment(session, id):
    stmt = await session.execute(
        select(Comment)
        .where(Comment.cmt_purchases_id == id)
        .order_by(Comment.created_at.desc())
    )
    result = stmt.scalars()
    return result


async def id_fle_delete(request, mdl, id_fle):
    # ..
    directory = (
        BASE_DIR
        / f"static/upload/{mdl}/{request.user.email}/{id_fle}"
    )
    if Path(directory).exists():
        result = shutil.rmtree(directory)
        return result
