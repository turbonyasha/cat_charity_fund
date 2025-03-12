from datetime import datetime


def invest(target, sources: list):
    total_invested = 0
    changed_sources = []
    for source in sources:
        if total_invested < target.full_amount:
            remaining_amount = target.full_amount - total_invested
            invest_amount = min(
                remaining_amount,
                source.full_amount - source.invested_amount)
            source.invested_amount += invest_amount
            total_invested += invest_amount
            source.fully_invested = (
                source.invested_amount == source.full_amount)
            if source.fully_invested:
                source.close_date = datetime.now()
            changed_sources.append(source)
            if total_invested >= target.full_amount:
                target.fully_invested = True
                target.close_date = datetime.now()
                break
    if total_invested > 0:
        target.invested_amount = total_invested
        if target.invested_amount >= target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.now()
    return target, changed_sources
