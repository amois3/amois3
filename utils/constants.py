"""Constants and translations."""
from database.models import MealType, Gender, ActivityLevel, Goal

# Russian translations
MEAL_TYPE_TRANSLATIONS = {
    MealType.BREAKFAST: "Завтрак",
    MealType.LUNCH: "Обед",
    MealType.DINNER: "Ужин",
    MealType.SNACK: "Перекус",
}

GENDER_TRANSLATIONS = {
    Gender.MALE: "Мужской",
    Gender.FEMALE: "Женский",
}

ACTIVITY_LEVEL_TRANSLATIONS = {
    ActivityLevel.SEDENTARY: "Малоподвижный",
    ActivityLevel.LIGHTLY_ACTIVE: "Легкая активность (1-3 дня в неделю)",
    ActivityLevel.MODERATELY_ACTIVE: "Умеренная активность (3-5 дней в неделю)",
    ActivityLevel.VERY_ACTIVE: "Высокая активность (6-7 дней в неделю)",
    ActivityLevel.EXTRA_ACTIVE: "Экстремальная активность (дважды в день)",
}

GOAL_TRANSLATIONS = {
    Goal.LOSE_WEIGHT: "Похудеть",
    Goal.MAINTAIN_WEIGHT: "Поддерживать вес",
    Goal.GAIN_WEIGHT: "Набрать вес",
    Goal.GAIN_MUSCLE: "Набрать мышечную массу",
}

WEEKDAY_TRANSLATIONS = {
    0: "Пн",
    1: "Вт",
    2: "Ср",
    3: "Чт",
    4: "Пт",
    5: "Сб",
    6: "Вс",
}

# Reactions for meal messages
MEAL_REACTIONS = ["👍", "👌", "😋", "🔥", "💪", "✨", "⭐️", "🎯", "💯"]

# OpenAI Cost per 1M tokens (USD) - update as needed
OPENAI_COSTS = {
    "gpt-4o": {
        "input": 2.50,  # per 1M input tokens
        "output": 10.00,  # per 1M output tokens
    },
    "gpt-4-turbo-preview": {
        "input": 10.00,
        "output": 30.00,
    },
    "gpt-4-turbo": {
        "input": 10.00,
        "output": 30.00,
    },
    "whisper-1": 0.006,  # per minute
}
