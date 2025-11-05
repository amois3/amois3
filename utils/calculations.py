"""Nutritional calculations."""
from database.models import Gender, ActivityLevel, Goal


def calculate_bmr(gender: Gender, age: int, height: float, weight: float) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation.

    BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + s
    where s is +5 for males and -161 for females
    """
    bmr = (10 * weight) + (6.25 * height) - (5 * age)

    if gender == Gender.MALE:
        bmr += 5
    else:
        bmr -= 161

    return round(bmr, 2)


def calculate_tdee(bmr: float, activity_level: ActivityLevel) -> float:
    """
    Calculate Total Daily Energy Expenditure.

    TDEE = BMR × Activity Factor
    """
    activity_factors = {
        ActivityLevel.SEDENTARY: 1.2,  # сидячий образ жизни
        ActivityLevel.LIGHTLY_ACTIVE: 1.375,  # легкая активность (1-3 дня в неделю)
        ActivityLevel.MODERATELY_ACTIVE: 1.55,  # умеренная активность (3-5 дней в неделю)
        ActivityLevel.VERY_ACTIVE: 1.725,  # высокая активность (6-7 дней в неделю)
        ActivityLevel.EXTRA_ACTIVE: 1.9,  # экстремальная активность
    }

    factor = activity_factors.get(activity_level, 1.2)
    return round(bmr * factor, 2)


def calculate_target_calories(tdee: float, goal: Goal) -> float:
    """Calculate target calories based on goal."""
    if goal == Goal.LOSE_WEIGHT:
        return round(tdee - 500, 2)  # дефицит 500 ккал (~0.5 кг в неделю)
    elif goal in (Goal.GAIN_WEIGHT, Goal.GAIN_MUSCLE):
        return round(tdee + 300, 2)  # профицит 300 ккал
    else:  # MAINTAIN_WEIGHT
        return round(tdee, 2)


def calculate_macros(target_calories: float, goal: Goal) -> tuple[float, float, float]:
    """
    Calculate recommended protein, carbs, and fats based on target calories and goal.

    Returns:
        tuple: (protein_grams, carbs_grams, fats_grams)
    """
    if goal == Goal.LOSE_WEIGHT:
        # Высокий белок: 35% белка, 35% углеводов, 30% жиров
        protein = (target_calories * 0.35) / 4  # 4 ккал на грамм белка
        carbs = (target_calories * 0.35) / 4  # 4 ккал на грамм углеводов
        fats = (target_calories * 0.30) / 9  # 9 ккал на грамм жиров

    elif goal == Goal.GAIN_MUSCLE:
        # Высокий белок для роста мышц: 30% белка, 45% углеводов, 25% жиров
        protein = (target_calories * 0.30) / 4
        carbs = (target_calories * 0.45) / 4
        fats = (target_calories * 0.25) / 9

    elif goal == Goal.GAIN_WEIGHT:
        # Сбалансированный: 25% белка, 45% углеводов, 30% жиров
        protein = (target_calories * 0.25) / 4
        carbs = (target_calories * 0.45) / 4
        fats = (target_calories * 0.30) / 9

    else:  # MAINTAIN_WEIGHT
        # Сбалансированный: 30% белка, 40% углеводов, 30% жиров
        protein = (target_calories * 0.30) / 4
        carbs = (target_calories * 0.40) / 4
        fats = (target_calories * 0.30) / 9

    return round(protein, 1), round(carbs, 1), round(fats, 1)
