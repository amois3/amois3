"""OpenAI cost tracking service."""
import logging
from datetime import datetime
from typing import Optional

from database.mongodb import db
from database.models import CostRecord
from utils.constants import OPENAI_COSTS
from config import settings

logger = logging.getLogger(__name__)


class CostTracker:
    """Track OpenAI API costs."""

    def __init__(self):
        self.daily_limit = settings.openai_cost_limit_daily
        self.warn_threshold = settings.openai_cost_warn_threshold

    async def track_cost(
        self,
        telegram_id: int,
        model: str,
        operation: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """
        Track API cost for a request.

        Args:
            telegram_id: User's Telegram ID
            model: Model used (e.g., "gpt-4o")
            operation: Operation type (e.g., "meal_analysis")
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Cost in USD
        """
        cost_usd = self._calculate_cost(model, input_tokens, output_tokens)

        # Save to database
        record = CostRecord(
            telegram_id=telegram_id,
            model=model,
            operation=operation,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd
        )

        await db.create_cost_record(record)

        logger.info(
            f"Cost tracked: user={telegram_id}, model={model}, "
            f"operation={operation}, cost=${cost_usd:.4f}"
        )

        return cost_usd

    async def track_voice_cost(
        self,
        telegram_id: int,
        duration_minutes: float
    ) -> float:
        """
        Track cost for voice transcription.

        Args:
            telegram_id: User's Telegram ID
            duration_minutes: Audio duration in minutes

        Returns:
            Cost in USD
        """
        cost_per_minute = OPENAI_COSTS.get("whisper-1", 0.006)
        cost_usd = duration_minutes * cost_per_minute

        # Save to database
        record = CostRecord(
            telegram_id=telegram_id,
            model="whisper-1",
            operation="voice_transcription",
            input_tokens=0,
            output_tokens=0,
            cost_usd=cost_usd
        )

        await db.create_cost_record(record)

        logger.info(
            f"Voice cost tracked: user={telegram_id}, "
            f"duration={duration_minutes:.2f}min, cost=${cost_usd:.4f}"
        )

        return cost_usd

    async def check_daily_limit(self, telegram_id: int) -> tuple[bool, float, float]:
        """
        Check if user is approaching or exceeded daily limit.

        Args:
            telegram_id: User's Telegram ID

        Returns:
            Tuple: (is_over_limit, current_cost, limit)
        """
        current_cost = await db.get_daily_cost(telegram_id)

        is_over_limit = current_cost >= self.daily_limit
        is_approaching_limit = current_cost >= (self.daily_limit * self.warn_threshold)

        if is_over_limit:
            logger.warning(
                f"User {telegram_id} exceeded daily limit: "
                f"${current_cost:.2f} / ${self.daily_limit:.2f}"
            )
        elif is_approaching_limit:
            logger.info(
                f"User {telegram_id} approaching daily limit: "
                f"${current_cost:.2f} / ${self.daily_limit:.2f}"
            )

        return is_over_limit, current_cost, self.daily_limit

    async def get_total_cost(self, telegram_id: int) -> float:
        """Get total cost for user."""
        return await db.get_total_cost(telegram_id)

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for token usage."""
        if model not in OPENAI_COSTS:
            logger.warning(f"Unknown model for cost calculation: {model}")
            return 0.0

        costs = OPENAI_COSTS[model]

        # Cost is per 1M tokens
        input_cost = (input_tokens / 1_000_000) * costs["input"]
        output_cost = (output_tokens / 1_000_000) * costs["output"]

        return round(input_cost + output_cost, 6)

    def format_cost_report(self, daily_cost: float, total_cost: float, limit: float) -> str:
        """Format cost report for user."""
        percent_of_limit = (daily_cost / limit) * 100 if limit > 0 else 0

        text = "💰 *Статистика расходов OpenAI*\n\n"
        text += f"📊 Сегодня: ${daily_cost:.4f}\n"
        text += f"📈 Лимит: ${limit:.2f}/день\n"
        text += f"📉 Использовано: {percent_of_limit:.1f}%\n"
        text += f"\n💵 Всего потрачено: ${total_cost:.4f}\n"

        if daily_cost >= limit:
            text += "\n⚠️ *Достигнут дневной лимит!*"
        elif daily_cost >= (limit * self.warn_threshold):
            text += f"\n⚡️ Приближается к лимиту ({self.warn_threshold * 100:.0f}%)"

        return text


# Global cost tracker instance
cost_tracker = CostTracker()
