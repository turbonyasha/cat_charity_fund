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
            original_invested_amount = obj.invested_amount
            obj.invested_amount += invest_amount
            obj.fully_invested = (obj.invested_amount == obj.full_amount)
            if obj.fully_invested:
                obj.close_date = datetime.now()
            if obj.invested_amount != original_invested_amount:
                changed_sources.append(obj)
    return changed_sources
