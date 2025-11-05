"""Graph generation service."""
import logging
from datetime import datetime, timedelta
from typing import List, Optional
from io import BytesIO

import matplotlib
matplotlib.use('Agg')  # Non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np

from database.models import Meal, WeightRecord, Nutrition, User
from database.mongodb import db

logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (10, 6)


class GraphGenerator:
    """Generate nutrition and weight graphs."""

    def __init__(self):
        self.dpi = 100

    async def generate_nutrition_graph(
        self,
        telegram_id: int,
        days: int = 7,
        user: Optional[User] = None
    ) -> BytesIO:
        """
        Generate nutrition graph for last N days.

        Args:
            telegram_id: User's Telegram ID
            days: Number of days to include
            user: User object (for target lines)

        Returns:
            BytesIO with PNG image
        """
        # Get meals for period
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        meals = await db.get_meals_for_period(telegram_id, start_date, end_date)

        if not meals:
            return self._generate_no_data_graph("Нет данных о питании")

        # Group by day
        daily_data = {}
        for meal in meals:
            day = meal.meal_time.date()
            if day not in daily_data:
                daily_data[day] = Nutrition()

            daily_data[day].calories += meal.total_nutrition.calories
            daily_data[day].protein += meal.total_nutrition.protein
            daily_data[day].carbs += meal.total_nutrition.carbs
            daily_data[day].fats += meal.total_nutrition.fats

        # Sort by date
        sorted_days = sorted(daily_data.keys())
        calories = [daily_data[day].calories for day in sorted_days]
        protein = [daily_data[day].protein for day in sorted_days]
        carbs = [daily_data[day].carbs for day in sorted_days]
        fats = [daily_data[day].fats for day in sorted_days]

        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # Plot 1: Calories
        ax1.plot(sorted_days, calories, marker='o', linewidth=2, markersize=8, color='#FF6B6B', label='Калории')
        ax1.fill_between(sorted_days, calories, alpha=0.3, color='#FF6B6B')

        # Add target line if available
        if user and user.target_calories:
            ax1.axhline(y=user.target_calories, color='green', linestyle='--', linewidth=2, label=f'Цель ({user.target_calories:.0f})')

        ax1.set_ylabel('Калории (ккал)', fontsize=12)
        ax1.set_title('Калории по дням', fontsize=14, fontweight='bold')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)

        # Plot 2: Macros
        x = np.arange(len(sorted_days))
        width = 0.25

        ax2.bar(x - width, protein, width, label='Белки', color='#4ECDC4')
        ax2.bar(x, carbs, width, label='Углеводы', color='#FFE66D')
        ax2.bar(x + width, fats, width, label='Жиры', color='#FF6B6B')

        ax2.set_xlabel('Дата', fontsize=12)
        ax2.set_ylabel('Граммы', fontsize=12)
        ax2.set_title('Макронутриенты (БЖУ)', fontsize=14, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels([day.strftime('%d.%m') for day in sorted_days], rotation=45)
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        # Save to BytesIO
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        plt.close()

        return buf

    async def generate_weight_graph(
        self,
        telegram_id: int,
        days: int = 30
    ) -> BytesIO:
        """
        Generate weight tracking graph.

        Args:
            telegram_id: User's Telegram ID
            days: Number of days to include

        Returns:
            BytesIO with PNG image
        """
        # Get weight records
        records = await db.get_weight_history(telegram_id, limit=days)

        if not records or len(records) < 2:
            return self._generate_no_data_graph("Недостаточно данных о весе\n(минимум 2 записи)")

        # Sort by date (oldest first)
        records = sorted(records, key=lambda r: r.recorded_at)

        dates = [r.recorded_at.date() for r in records]
        weights = [r.weight for r in records]

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot weight
        ax.plot(dates, weights, marker='o', linewidth=2, markersize=10, color='#4ECDC4', label='Вес')
        ax.fill_between(dates, weights, alpha=0.2, color='#4ECDC4')

        # Add trend line if enough data
        if len(records) >= 3:
            z = np.polyfit(range(len(weights)), weights, 1)
            p = np.poly1d(z)
            trend = p(range(len(weights)))
            ax.plot(dates, trend, linestyle='--', linewidth=2, color='red', alpha=0.7, label='Тренд')

            # Calculate and display change
            weight_change = weights[-1] - weights[0]
            days_diff = (dates[-1] - dates[0]).days
            if days_diff > 0:
                change_per_week = (weight_change / days_diff) * 7
                change_text = f"Изменение: {weight_change:+.1f} кг ({change_per_week:+.2f} кг/неделя)"
                ax.text(0.02, 0.98, change_text, transform=ax.transAxes,
                       verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.set_xlabel('Дата', fontsize=12)
        ax.set_ylabel('Вес (кг)', fontsize=12)
        ax.set_title('Динамика веса', fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
        plt.xticks(rotation=45)

        plt.tight_layout()

        # Save to BytesIO
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        plt.close()

        return buf

    async def generate_weekly_summary_graph(
        self,
        telegram_id: int,
        user: Optional[User] = None
    ) -> BytesIO:
        """
        Generate weekly summary graph.

        Args:
            telegram_id: User's Telegram ID
            user: User object

        Returns:
            BytesIO with PNG image
        """
        # Get last 7 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)

        meals = await db.get_meals_for_period(telegram_id, start_date, end_date)

        if not meals:
            return self._generate_no_data_graph("Нет данных за последнюю неделю")

        # Group by day
        daily_totals = {}
        for meal in meals:
            day = meal.meal_time.date()
            if day not in daily_totals:
                daily_totals[day] = {"calories": 0, "meals": 0}

            daily_totals[day]["calories"] += meal.total_nutrition.calories
            daily_totals[day]["meals"] += 1

        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))

        days = sorted(daily_totals.keys())
        calories = [daily_totals[day]["calories"] for day in days]
        meal_counts = [daily_totals[day]["meals"] for day in days]

        # Create bars
        bars = ax.bar(range(len(days)), calories, color='#FF6B6B', alpha=0.7)

        # Color bars based on target
        if user and user.target_calories:
            for i, bar in enumerate(bars):
                if calories[i] < user.target_calories * 0.8:
                    bar.set_color('#FFE66D')  # Yellow for under target
                elif calories[i] > user.target_calories * 1.2:
                    bar.set_color('#FF6B6B')  # Red for over target
                else:
                    bar.set_color('#4ECDC4')  # Green for on target

            # Add target line
            ax.axhline(y=user.target_calories, color='green', linestyle='--',
                      linewidth=2, label=f'Цель ({user.target_calories:.0f})')

        # Add meal count labels
        for i, (bar, count) in enumerate(zip(bars, meal_counts)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                   f'{count} приемов',
                   ha='center', va='bottom', fontsize=9)

        weekdays_ru = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        ax.set_xticks(range(len(days)))
        ax.set_xticklabels([f"{weekdays_ru[day.weekday()]}\n{day.strftime('%d.%m')}" for day in days])

        ax.set_ylabel('Калории (ккал)', fontsize=12)
        ax.set_title('Недельная сводка', fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        # Save to BytesIO
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        plt.close()

        return buf

    def _generate_no_data_graph(self, message: str) -> BytesIO:
        """Generate a graph showing 'no data' message."""
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, message, horizontalalignment='center',
               verticalalignment='center', fontsize=16, transform=ax.transAxes)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
        buf.seek(0)
        plt.close()

        return buf


# Global graph generator instance
graph_generator = GraphGenerator()
