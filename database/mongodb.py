"""MongoDB database connection and operations."""
import logging
from datetime import datetime, timedelta
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId

from .models import (
    User, Meal, ChatMessage, DailyReport, WeeklyReport,
    WeightRecord, CostRecord, Nutrition
)
from config import settings

logger = logging.getLogger(__name__)


class Database:
    """Database operations."""

    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None

    async def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_uri)
            self.db = self.client[settings.mongodb_database]

            # Test connection
            await self.client.admin.command('ping')
            logger.info("Connected to MongoDB successfully")

            # Create indexes
            await self._create_indexes()
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def disconnect(self):
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")

    async def _create_indexes(self):
        """Create database indexes."""
        # Users
        await self.db.users.create_index([("telegram_id", ASCENDING)], unique=True)

        # Meals
        await self.db.meals.create_index([("telegram_id", ASCENDING), ("meal_time", DESCENDING)])

        # Chat messages
        await self.db.chat_messages.create_index([("telegram_id", ASCENDING), ("created_at", DESCENDING)])

        # Reports
        await self.db.daily_reports.create_index([("telegram_id", ASCENDING), ("date", DESCENDING)])
        await self.db.weekly_reports.create_index([("telegram_id", ASCENDING), ("start_date", DESCENDING)])

        # Cost tracking
        await self.db.cost_records.create_index([("telegram_id", ASCENDING), ("created_at", DESCENDING)])

    # User operations
    async def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram ID."""
        doc = await self.db.users.find_one({"telegram_id": telegram_id})
        return User(**doc) if doc else None

    async def create_user(self, user: User) -> User:
        """Create a new user."""
        result = await self.db.users.insert_one(user.dict(by_alias=True, exclude={"id"}))
        user.id = result.inserted_id
        return user

    async def update_user(self, user: User) -> User:
        """Update user."""
        user.updated_at = datetime.utcnow()
        await self.db.users.update_one(
            {"telegram_id": user.telegram_id},
            {"$set": user.dict(by_alias=True, exclude={"id"})}
        )
        return user

    async def get_or_create_user(self, telegram_id: int, username: str = None,
                                  first_name: str = None, last_name: str = None) -> User:
        """Get existing user or create new one."""
        user = await self.get_user(telegram_id)
        if user:
            # Update last active
            user.last_active_at = datetime.utcnow()
            await self.update_user(user)
            return user

        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        return await self.create_user(user)

    # Meal operations
    async def create_meal(self, meal: Meal) -> Meal:
        """Create a new meal record."""
        result = await self.db.meals.insert_one(meal.dict(by_alias=True, exclude={"id"}))
        meal.id = result.inserted_id
        return meal

    async def get_meals_for_period(self, telegram_id: int,
                                   start_date: datetime, end_date: datetime) -> List[Meal]:
        """Get meals for a specific time period."""
        cursor = self.db.meals.find({
            "telegram_id": telegram_id,
            "meal_time": {"$gte": start_date, "$lte": end_date}
        }).sort("meal_time", ASCENDING)

        meals = []
        async for doc in cursor:
            meals.append(Meal(**doc))
        return meals

    async def get_recent_meals(self, telegram_id: int, limit: int = 30) -> List[Meal]:
        """Get recent meals."""
        cursor = self.db.meals.find({
            "telegram_id": telegram_id
        }).sort("meal_time", DESCENDING).limit(limit)

        meals = []
        async for doc in cursor:
            meals.append(Meal(**doc))
        return meals

    async def update_meal(self, meal: Meal) -> Meal:
        """Update meal."""
        await self.db.meals.update_one(
            {"_id": meal.id},
            {"$set": meal.dict(by_alias=True, exclude={"id"})}
        )
        return meal

    async def delete_meal(self, meal_id: ObjectId) -> bool:
        """Delete meal."""
        result = await self.db.meals.delete_one({"_id": meal_id})
        return result.deleted_count > 0

    async def search_meals(self, telegram_id: int, query: str, limit: int = 20) -> List[Meal]:
        """Search meals by text."""
        cursor = self.db.meals.find({
            "telegram_id": telegram_id,
            "$or": [
                {"description": {"$regex": query, "$options": "i"}},
                {"foods.name": {"$regex": query, "$options": "i"}},
                {"ai_analysis": {"$regex": query, "$options": "i"}}
            ]
        }).sort("meal_time", DESCENDING).limit(limit)

        meals = []
        async for doc in cursor:
            meals.append(Meal(**doc))
        return meals

    # Chat operations
    async def create_chat_message(self, message: ChatMessage) -> ChatMessage:
        """Create chat message."""
        result = await self.db.chat_messages.insert_one(message.dict(by_alias=True, exclude={"id"}))
        message.id = result.inserted_id
        return message

    async def get_recent_chat_messages(self, telegram_id: int, limit: int = 20) -> List[ChatMessage]:
        """Get recent chat messages."""
        cursor = self.db.chat_messages.find({
            "telegram_id": telegram_id
        }).sort("created_at", ASCENDING).limit(limit)

        messages = []
        async for doc in cursor:
            messages.append(ChatMessage(**doc))
        return messages

    async def clear_chat_history(self, telegram_id: int) -> int:
        """Clear chat history."""
        result = await self.db.chat_messages.delete_many({"telegram_id": telegram_id})
        return result.deleted_count

    # Report operations
    async def create_daily_report(self, report: DailyReport) -> DailyReport:
        """Create daily report."""
        result = await self.db.daily_reports.insert_one(report.dict(by_alias=True, exclude={"id"}))
        report.id = result.inserted_id
        return report

    async def get_daily_report(self, telegram_id: int, date: datetime) -> Optional[DailyReport]:
        """Get daily report for specific date."""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        doc = await self.db.daily_reports.find_one({
            "telegram_id": telegram_id,
            "date": {"$gte": start_of_day, "$lt": end_of_day}
        })
        return DailyReport(**doc) if doc else None

    async def create_weekly_report(self, report: WeeklyReport) -> WeeklyReport:
        """Create weekly report."""
        result = await self.db.weekly_reports.insert_one(report.dict(by_alias=True, exclude={"id"}))
        report.id = result.inserted_id
        return report

    async def get_recent_weekly_reports(self, telegram_id: int, limit: int = 4) -> List[WeeklyReport]:
        """Get recent weekly reports."""
        cursor = self.db.weekly_reports.find({
            "telegram_id": telegram_id
        }).sort("start_date", DESCENDING).limit(limit)

        reports = []
        async for doc in cursor:
            reports.append(WeeklyReport(**doc))
        return reports

    # Weight tracking
    async def create_weight_record(self, record: WeightRecord) -> WeightRecord:
        """Create weight record."""
        result = await self.db.weight_records.insert_one(record.dict(by_alias=True, exclude={"id"}))
        record.id = result.inserted_id
        return record

    async def get_weight_history(self, telegram_id: int, limit: int = 30) -> List[WeightRecord]:
        """Get weight history."""
        cursor = self.db.weight_records.find({
            "telegram_id": telegram_id
        }).sort("recorded_at", DESCENDING).limit(limit)

        records = []
        async for doc in cursor:
            records.append(WeightRecord(**doc))
        return records

    # Cost tracking
    async def create_cost_record(self, record: CostRecord) -> CostRecord:
        """Create cost record."""
        result = await self.db.cost_records.insert_one(record.dict(by_alias=True, exclude={"id"}))
        record.id = result.inserted_id
        return record

    async def get_daily_cost(self, telegram_id: int, date: datetime = None) -> float:
        """Get total cost for a day."""
        if date is None:
            date = datetime.utcnow()

        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        pipeline = [
            {
                "$match": {
                    "telegram_id": telegram_id,
                    "created_at": {"$gte": start_of_day, "$lt": end_of_day}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_cost": {"$sum": "$cost_usd"}
                }
            }
        ]

        result = await self.db.cost_records.aggregate(pipeline).to_list(length=1)
        return result[0]["total_cost"] if result else 0.0

    async def get_total_cost(self, telegram_id: int) -> float:
        """Get total cost for all time."""
        pipeline = [
            {
                "$match": {"telegram_id": telegram_id}
            },
            {
                "$group": {
                    "_id": None,
                    "total_cost": {"$sum": "$cost_usd"}
                }
            }
        ]

        result = await self.db.cost_records.aggregate(pipeline).to_list(length=1)
        return result[0]["total_cost"] if result else 0.0


# Global database instance
db = Database()
