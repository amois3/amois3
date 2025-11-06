"""Google Gemini AI service - compact version."""
import json
import logging
import asyncio
import base64
from typing import Optional, List, Tuple
import google.generativeai as genai

from database.models import User, Meal, ChatMessage, FoodItem, Nutrition, MealType
from config import settings

logger = logging.getLogger(__name__)
genai.configure(api_key=settings.gemini_api_key)


class GeminiService:
    """Google Gemini AI service."""

    def __init__(self):
        self.model_vision = genai.GenerativeModel(settings.gemini_model_vision)
        self.model_text = genai.GenerativeModel(settings.gemini_model_text)
    
    async def analyze_meal_from_photo(self, photo_base64: str, description: Optional[str], user: Optional[User]) -> Tuple:
        """Analyze meal from photo."""
        prompt = f"Проанализируй еду и верни JSON: {{foods: [{{name, description, nutrition: {{calories, protein, carbs, fats, fiber, sugar}}, weight}}], total_nutrition: {{calories, protein, carbs, fats, fiber, sugar}}, analysis: string, health_score: 0-10, meal_type: breakfast/lunch/dinner/snack}}"
        if description:
            prompt += f" Описание: {description}"
        
        photo_bytes = base64.b64decode(photo_base64)
        response = await asyncio.to_thread(
            lambda: self.model_vision.generate_content([prompt, {"mime_type": "image/jpeg", "data": photo_bytes}])
        )
        return self._parse(response.text)
    
    async def analyze_meal_from_text(self, text: str, user: Optional[User]) -> Tuple:
        """Analyze meal from text."""
        prompt = f"Проанализируй: {text}. Верни JSON как в примере: {{foods: [{{name, nutrition: {{calories, protein, carbs, fats}}}}], total_nutrition, analysis, health_score, meal_type}}"
        response = await asyncio.to_thread(lambda: self.model_text.generate_content(prompt))
        return self._parse(response.text)
    
    async def generate_daily_report(self, meals, total_nutrition, user, previous_recommendation):
        """Generate daily report."""
        prompt = f"AI-нутрициолог. Проанализируй день. Приемов: {len(meals)}. Итого: {total_nutrition.calories:.0f} ккал. Напиши отчет (4-5 предложений) с эмодзи."
        response = await asyncio.to_thread(lambda: self.model_text.generate_content(prompt))
        return response.text
    
    async def generate_weekly_report(self, daily_breakdown, avg_nutrition, user):
        """Generate weekly report."""
        prompt = f"AI-нутрициолог. Недельный отчет. Среднее: {avg_nutrition.calories:.0f} ккал/день. Напиши анализ (5-7 предложений) с эмодзи."
        response = await asyncio.to_thread(lambda: self.model_text.generate_content(prompt))
        return response.text
    
    async def chat_with_context(self, user_message, chat_history, recent_meals, user):
        """Chat with context."""
        prompt = f"AI-нутрициолог. Вопрос: {user_message}. Ответь персонально."
        response = await asyncio.to_thread(lambda: self.model_text.generate_content(prompt))
        return response.text
    
    def _parse(self, content):
        """Parse JSON response."""
        try:
            json_str = content.strip()
            if "```" in json_str:
                json_str = json_str.split("```")[1].replace("json", "").strip()
            data = json.loads(json_str)
            
            foods = []
            for f in data.get("foods", []):
                foods.append(FoodItem(
                    name=f["name"],
                    description=f.get("description"),
                    nutrition=Nutrition(**f.get("nutrition", {})),
                    weight=f.get("weight")
                ))
            
            total = Nutrition(**data.get("total_nutrition", {}))
            analysis = data.get("analysis", "")
            health_score = data.get("health_score", 5.0)
            meal_type = MealType(data.get("meal_type", "snack"))
            
            return foods, total, analysis, health_score, meal_type
        except Exception as e:
            logger.error(f"Parse error: {e}")
            # Fallback
            return [], Nutrition(calories=300, protein=15, carbs=40, fats=10), "Анализ недоступен", 5.0, MealType.SNACK
