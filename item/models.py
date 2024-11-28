from __future__ import annotations

from sqlalchemy import String, Text, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_config.storage_config import (
    Base,
    intpk,
    chapter,
    affair,
    pictures,
    points,
    user_fk,
    tm_fk,
    allcts,
    alljson
)


class Item(Base):
    __tablename__ = "item_tm"

    id: Mapped[intpk]
    title: Mapped[chapter]
    description: Mapped[affair]
    categories: Mapped[allcts]
    file: Mapped[pictures]
    created_at: Mapped[points]
    modified_at: Mapped[points]
    # ...
    owner: Mapped[user_fk]
    # ...
    item_user: Mapped[list["User"]] = relationship(
        back_populates="user_item",
    )
    item_cmt: Mapped[list["Comment"]] = relationship(
        back_populates="cmt_item", cascade="all, delete-orphan"
    )
    item_products: Mapped[list["Products"]] = relationship(
        back_populates="products_item", cascade="all, delete-orphan"
    )
    item_purchases: Mapped[list["Purchases"]] = relationship(
        back_populates="purchases_item", cascade="all, delete-orphan"
    )

    def __str__(self):
        return str(self.id)


class Products(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    title: Mapped[chapter]
    description: Mapped[affair]
    file: Mapped[pictures]
    categories: Mapped[allcts]
    cts: Mapped[allcts]
    amount: Mapped[alljson]
    price: Mapped[alljson]
    created_at: Mapped[points]
    modified_at: Mapped[points]
    # ...
    owner: Mapped[user_fk]
    products_belongs: Mapped[tm_fk]
    # ...
    products_user: Mapped[list["User"]] = relationship(
        back_populates="user_products",
    )
    products_item: Mapped[list["Item"]] = relationship(
        back_populates="item_products",
    )
    products_cmt: Mapped[list["Comment"]] = relationship(
        back_populates="cmt_products", cascade="all, delete-orphan"
    )

    def __str__(self):
        return str(self.id)


class Purchases(Base):
    __tablename__ = "purchases"

    id: Mapped[intpk]
    title: Mapped[chapter]
    description: Mapped[affair]
    file: Mapped[pictures]
    categories: Mapped[allcts]
    cts: Mapped[allcts]
    amount: Mapped[alljson]
    price: Mapped[alljson]
    created_at: Mapped[points]
    modified_at: Mapped[points]
    # ...
    owner: Mapped[user_fk]
    purchases_belongs: Mapped[tm_fk]
    order_belongs: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    # ...
    purchases_user: Mapped[list["User"]] = relationship(
        back_populates="user_purchases",
    )
    purchases_item: Mapped[list["Item"]] = relationship(
        back_populates="item_purchases",
    )
    purchases_cmt: Mapped[list["Comment"]] = relationship(
        back_populates="cmt_purchases", cascade="all, delete-orphan"
    )

    def __str__(self):
        return str(self.id)


class Slider(Base):
    __tablename__ = "slider"
    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    # ...
    id_sl: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    file: Mapped[pictures]
    # ...
    created_at: Mapped[points]
    modified_at: Mapped[points]
