from datetime import datetime

from app.models.base import BaseInvestModel


def invest(
    target: BaseInvestModel,
    sources: list[BaseInvestModel]
) -> list[BaseInvestModel]:
    changed_sources = []
    for source in sources:
        invest_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in [target, source]:
            obj.invested_amount += invest_amount
            obj.fully_invested = (obj.invested_amount == obj.full_amount)
            if obj.fully_invested:
                obj.close_date = datetime.now()
        for obj in [target, source]:
            if obj.invested_amount != obj.full_amount:
                changed_sources.append(obj)
        if target.fully_invested:
            break
    return changed_sources
