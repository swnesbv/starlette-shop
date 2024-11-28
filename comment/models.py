from __future__ import annotations

from sqlalchemy import Text, ForeignKey, JSON

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_config.storage_config import Base, intpk, points, user_fk


class Comment(Base):
    __tablename__ = "comment_cmt"

    id: Mapped[intpk]
    opinion: Mapped[str] = mapped_column(Text, nullable=False)
    user_on: Mapped[dict|list] = mapped_column(JSON, nullable=True)
    created_at: Mapped[points]
    modified_at: Mapped[points]
    # ...
    owner: Mapped[user_fk]
    # ...
    cmt_item_id: Mapped[int] = mapped_column(
        ForeignKey(
            "item_tm.id",
            ondelete="CASCADE",
        ), nullable=True
    )
    cmt_products_id: Mapped[int] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ), nullable=True
    )
    cmt_purchases_id: Mapped[int] = mapped_column(
        ForeignKey(
            "purchases.id",
            ondelete="CASCADE",
        ), nullable=True
    )

    # ...
    cmt_user: Mapped[list["User"]] = relationship(
        back_populates="user_cmt"
    )
    cmt_item: Mapped[list["Item"]] = relationship(
        back_populates="item_cmt"
    )
    cmt_products: Mapped[list["Products"]] = relationship(
        back_populates="products_cmt"
    )
    cmt_purchases: Mapped[list["Purchases"]] = relationship(
        back_populates="purchases_cmt"
    )

    def __str__(self):
        return str(self.id)
