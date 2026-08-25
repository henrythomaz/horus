from app.models.enums import RiskLevel



def calculate_risk(
    predictions_count: int,
):


    if predictions_count == 0:

        return RiskLevel.VERY_LOW


    if predictions_count < 5:

        return RiskLevel.LOW


    if predictions_count < 15:

        return RiskLevel.MODERATE


    if predictions_count < 30:

        return RiskLevel.HIGH


    return RiskLevel.VERY_HIGH
