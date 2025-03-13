from datetime import datetime
from typing import Union

from app.models import Donation, CharityProject


def invest(target: Union[Donation, CharityProject], sources: list) -> list:
    changed_sources = []
    for source in sources:
        if target.invested_amount is None:
            target.invested_amount = 0
        if target.full_amount is None:
            target.full_amount = 0
        if target.invested_amount < target.full_amount:
            invest_amount = min(
                target.full_amount - target.invested_amount,
                source.full_amount - source.invested_amount
            )
            source.invested_amount += invest_amount
            target.invested_amount += invest_amount
            source.fully_invested = (
                source.invested_amount == source.full_amount)
            if source.fully_invested:
                source.close_date = datetime.now()
            changed_sources.append(source)
            if target.invested_amount >= target.full_amount:
                target.fully_invested = True
                target.close_date = datetime.now()
                break
    return changed_sources
