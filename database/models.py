"""Data models."""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Gender(str, Enum):
    """User gender."""
    MALE = "male"
    FEMALE = "female"


class ActivityLevel(str, Enum):
    """Physical activity level."""
    SEDENTARY = "sedentary"  # Малоподвижный
    LIGHTLY_ACTIVE = "lightly_active"  # Легкая активность
    MODERATELY_ACTIVE = "moderately_active"  # Умеренная активность
    VERY_ACTIVE = "very_active"  # Высокая активность
    EXTRA_ACTIVE = "extra_active"  # Экстремальная активность


class Goal(str, Enum):
    """Nutrition goal."""
    LOSE_WEIGHT = "lose_weight"  # Похудеть
    MAINTAIN_WEIGHT = "maintain_weight"  # Поддерживать вес
    GAIN_WEIGHT = "gain_weight"  # Набрать вес
    GAIN_MUSCLE = "gain_muscle"  # Набрать мышечную массу


class MealType(str, Enum):
    """Type of meal."""
    BREAKFAST = "breakfast"  # Завтрак
    LUNCH = "lunch"  # Обед
    DINNER = "dinner"  # Ужин
    SNACK = "snack"  # Перекус


class Nutrition(BaseModel):
    """Nutritional information."""
    calories: float = 0.0
    protein: float = 0.0  # белки (г)
    carbs: float = 0.0  # углеводы (г)
    fats: float = 0.0  # жиры (г)
    fiber: float = 0.0  # клетчатка (г)
    sugar: float = 0.0  # сахар (г)


class FoodItem(BaseModel):
    """Single food item in a meal."""
    name: str
    description: Optional[str] = None
    nutrition: Nutrition
    weight: Optional[float] = None  # вес в граммах


class User(BaseModel):
    """User model."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    # Profile
    gender: Optional[Gender] = None
    age: Optional[int] = None
    height: Optional[float] = None  # см
    weight: Optional[float] = None  # кг
    activity_level: Optional[ActivityLevel] = None
    goal: Optional[Goal] = None
    lifestyle_context: Optional[str] = None

    # Calculated values
    bmr: Optional[float] = None  # Basal Metabolic Rate
    tdee: Optional[float] = None  # Total Daily Energy Expenditure

    # Target macros
    target_calories: Optional[float] = None
    target_protein: Optional[float] = None
    target_carbs: Optional[float] = None
    target_fats: Optional[float] = None

    # State
    in_chat_mode: bool = False

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_active_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Meal(BaseModel):
    """Meal record."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    telegram_id: int

    # Meal information
    meal_type: Optional[MealType] = None
    foods: List[FoodItem] = []
    total_nutrition: Nutrition

    # Input data
    photo_file_id: Optional[str] = None
    voice_file_id: Optional[str] = None
    description: Optional[str] = None

    # AI Analysis
    ai_analysis: Optional[str] = None
    health_score: Optional[float] = None  # 0-10

    # Timestamps
    meal_time: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ChatMessage(BaseModel):
    """Chat message in AI nutritionist mode."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    telegram_id: int
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class DailyNutrition(BaseModel):
    """Nutrition for one day."""
    date: datetime
    nutrition: Nutrition
    meals_count: int


class DailyReport(BaseModel):
    """Daily nutrition report."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    telegram_id: int
    date: datetime
    total_nutrition: Nutrition
    meals_count: int
    ai_recommendation: str
    previous_day_recommendation: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class WeeklyReport(BaseModel):
    """Weekly nutrition report."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    telegram_id: int
    start_date: datetime
    end_date: datetime
    avg_daily_nutrition: Nutrition
    total_meals_count: int
    daily_breakdown: List[DailyNutrition]
    ai_recommendation: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class WeightRecord(BaseModel):
    """Weight measurement record."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    telegram_id: int
    weight: float  # кг
    recorded_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CostRecord(BaseModel):
    """OpenAI API cost tracking."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    telegram_id: int
    model: str  # gpt-4o, gpt-4-turbo, etc.
    operation: str  # meal_analysis, chat, report, etc.
    input_tokens: int
    output_tokens: int
    cost_usd: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
