"""Text formatters for bot messages."""
from datetime import datetime
from typing import Optional
from database.models import User, Meal, Nutrition, DailyReport, WeeklyReport
from .constants import (
    MEAL_TYPE_TRANSLATIONS,
    GENDER_TRANSLATIONS,
    ACTIVITY_LEVEL_TRANSLATIONS,
    GOAL_TRANSLATIONS,
    WEEKDAY_TRANSLATIONS
)


def format_nutrition(nutrition: Nutrition) -> str:
    """Format nutrition data as a string."""
    return (
        f"🔥 {nutrition.calories:.0f} ккал | "
        f"🥩 {nutrition.protein:.1f}г Б | "
        f"🍞 {nutrition.carbs:.1f}г У | "
        f"🥑 {nutrition.fats:.1f}г Ж"
    )


def format_meal(meal: Meal, user: Optional[User] = None) -> str:
    """Format a meal as a string."""
    text = "✅ *Прием пищи записан!*\n\n"

    # Time and type
    meal_time = meal.meal_time.strftime("%H:%M")
    text += f"⏰ {meal_time}"

    if meal.meal_type:
        meal_type_ru = MEAL_TYPE_TRANSLATIONS.get(meal.meal_type, meal.meal_type)
        text += f" • {meal_type_ru}"

    text += "\n\n"

    # Foods
    if meal.foods:
        text += "*Блюда:*\n"
        for i, food in enumerate(meal.foods, 1):
            text += f"{i}. {food.name}\n"
            if food.description:
                text += f"   _{food.description}_\n"
        text += "\n"

    # Nutrition
    text += f"📊 *КБЖУ:*\n"
    text += f"🔥 {meal.total_nutrition.calories:.0f} ккал\n"
    text += f"🥩 {meal.total_nutrition.protein:.1f}г белков\n"
    text += f"🍞 {meal.total_nutrition.carbs:.1f}г углеводов\n"
    text += f"🥑 {meal.total_nutrition.fats:.1f}г жиров\n"

    # Compare with targets if available
    if user and user.target_calories:
        calories_percent = (meal.total_nutrition.calories / user.target_calories) * 100
        text += f"\n📈 Это {calories_percent:.0f}% от дневной нормы ({user.target_calories:.0f} ккал)\n"

    # Health score
    if meal.health_score:
        text += f"\n⭐️ *Оценка здоровья:* {meal.health_score:.1f}/10\n"

    # AI Analysis
    if meal.ai_analysis:
        text += f"\n💡 *Анализ:*\n{meal.ai_analysis}\n"

    return text


def format_user_profile(user: User) -> str:
    """Format user profile information."""
    text = "👤 *Ваш профиль*\n\n"

    if user.gender:
        text += f"Пол: {GENDER_TRANSLATIONS.get(user.gender, user.gender)}\n"
    if user.age:
        text += f"Возраст: {user.age} лет\n"
    if user.height:
        text += f"Рост: {user.height:.0f} см\n"
    if user.weight:
        text += f"Вес: {user.weight:.1f} кг\n"
    if user.activity_level:
        text += f"Активность: {ACTIVITY_LEVEL_TRANSLATIONS.get(user.activity_level, user.activity_level)}\n"
    if user.goal:
        text += f"Цель: {GOAL_TRANSLATIONS.get(user.goal, user.goal)}\n"

    if user.bmr:
        text += f"\n📊 BMR: {user.bmr:.0f} ккал\n"
    if user.tdee:
        text += f"📊 TDEE: {user.tdee:.0f} ккал\n"

    if user.target_calories:
        text += f"\n🎯 *Целевые показатели:*\n"
        text += f"Калории: {user.target_calories:.0f} ккал/день\n"
        if user.target_protein:
            text += f"Белки: {user.target_protein:.0f}г | "
            text += f"Углеводы: {user.target_carbs:.0f}г | "
            text += f"Жиры: {user.target_fats:.0f}г\n"

    if user.lifestyle_context:
        text += f"\n📝 *Контекст:* {user.lifestyle_context}\n"

    if not any([user.gender, user.age, user.height, user.weight]):
        text += "\n_Профиль не заполнен. Используйте кнопки ниже для настройки._"

    return text


def format_daily_report(report: DailyReport, user: Optional[User] = None) -> str:
    """Format daily report."""
    date_str = report.date.strftime("%d.%m.%Y")
    text = f"📊 *Отчет за {date_str}*\n\n"

    text += f"📝 Приемов пищи: {report.meals_count}\n\n"

    text += "*Итого за день:*\n"
    text += f"🔥 {report.total_nutrition.calories:.0f} ккал\n"
    text += f"🥩 {report.total_nutrition.protein:.1f}г белков\n"
    text += f"🍞 {report.total_nutrition.carbs:.1f}г углеводов\n"
    text += f"🥑 {report.total_nutrition.fats:.1f}г жиров\n"

    # Compare with targets
    if user and user.target_calories:
        calories_diff = report.total_nutrition.calories - user.target_calories
        percent = (report.total_nutrition.calories / user.target_calories) * 100

        text += "\n*Сравнение с целью:*\n"
        if calories_diff > 0:
            text += f"📈 +{calories_diff:.0f} ккал ({percent:.0f}% от нормы)\n"
        else:
            text += f"📉 {calories_diff:.0f} ккал ({percent:.0f}% от нормы)\n"

    # AI Recommendation
    if report.ai_recommendation:
        text += f"\n🤖 *AI-рекомендация:*\n{report.ai_recommendation}\n"

    return text


def format_weekly_report(report: WeeklyReport, user: Optional[User] = None) -> str:
    """Format weekly report."""
    start_str = report.start_date.strftime("%d.%m")
    end_str = (report.end_date).strftime("%d.%m")

    text = f"📊 *Отчет за неделю*\n{start_str} - {end_str}\n\n"

    text += f"📝 Всего приемов пищи: {report.total_meals_count}\n\n"

    # Daily breakdown
    text += "*По дням:*\n"
    for day in report.daily_breakdown:
        weekday = WEEKDAY_TRANSLATIONS.get(day.date.weekday(), "")
        if day.meals_count > 0:
            text += f"{weekday}: {day.nutrition.calories:.0f} ккал ({day.meals_count} приемов)\n"
        else:
            text += f"{weekday}: нет данных\n"

    # Average
    text += "\n*Среднее за день:*\n"
    text += f"🔥 {report.avg_daily_nutrition.calories:.0f} ккал\n"
    text += f"🥩 {report.avg_daily_nutrition.protein:.1f}г белков\n"
    text += f"🍞 {report.avg_daily_nutrition.carbs:.1f}г углеводов\n"
    text += f"🥑 {report.avg_daily_nutrition.fats:.1f}г жиров\n"

    # Compare with targets
    if user and user.target_calories:
        avg_diff = report.avg_daily_nutrition.calories - user.target_calories

        text += "\n*Сравнение с целью:*\n"
        if avg_diff > 0:
            text += f"📈 +{avg_diff:.0f} ккал в среднем\n"
        else:
            text += f"📉 {avg_diff:.0f} ккал в среднем\n"

    # AI Recommendation
    if report.ai_recommendation:
        text += f"\n🤖 *AI-рекомендация на следующую неделю:*\n{report.ai_recommendation}\n"

    return text
