from app.models import DonationCharityBase


def investment(
        target: DonationCharityBase,
        sources: list[DonationCharityBase]
) -> list[DonationCharityBase]:
    if target.invested_amount is None:
        target.invested_amount = 0
    results = []
    for item in sources:
        transfer = min(item.remaining_amount, target.remaining_amount)
        for object in item, target:
            object.invested_amount += transfer
            if object.invested_amount == object.full_amount:
                object.set_fully_invested()
        results.append(item)
        if transfer == 0:
            break
    return results
