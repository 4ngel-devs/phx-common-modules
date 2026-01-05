"""Date utilities with Mexico timezone support."""

from datetime import date, datetime
from zoneinfo import ZoneInfo

from loguru import logger

# Mexico timezone (America/Mexico_City)
MEXICO_TIMEZONE = ZoneInfo("America/Mexico_City")


class DateUtils:
    """Utility class for date and datetime operations using Mexico timezone."""

    @staticmethod
    def now() -> datetime:
        """
        Get the current datetime in Mexico timezone.

        Returns:
            datetime: Current datetime in Mexico timezone (America/Mexico_City)
        """
        mexico_now = datetime.now(MEXICO_TIMEZONE)
        logger.debug(f"Current Mexico time: {mexico_now}")
        return mexico_now

    @staticmethod
    def today() -> date:
        """
        Get the current date in Mexico timezone.

        Returns:
            date: Current date in Mexico timezone
        """
        mexico_today = datetime.now(MEXICO_TIMEZONE).date()
        logger.debug(f"Current Mexico date: {mexico_today}")
        return mexico_today

    @staticmethod
    def to_mexico_timezone(dt: datetime) -> datetime:
        """
        Convert a datetime to Mexico timezone.

        If the datetime is naive (no timezone), it's assumed to be in UTC.
        If it has a timezone, it will be converted to Mexico timezone.

        Args:
            dt: Datetime to convert

        Returns:
            datetime: Datetime in Mexico timezone
        """
        if dt.tzinfo is None:
            # Assume UTC if naive
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
            logger.debug(f"Naive datetime assumed as UTC: {dt}")

        mexico_dt = dt.astimezone(MEXICO_TIMEZONE)
        logger.debug(f"Converted {dt} to Mexico timezone: {mexico_dt}")
        return mexico_dt

    @staticmethod
    def from_mexico_timezone(dt: datetime, target_tz: ZoneInfo | str = ZoneInfo("UTC")) -> datetime:
        """
        Convert a datetime from Mexico timezone to another timezone.

        Args:
            dt: Datetime in Mexico timezone (if naive, assumed to be Mexico timezone)
            target_tz: Target timezone (default: UTC)

        Returns:
            datetime: Datetime in target timezone
        """
        if isinstance(target_tz, str):
            target_tz = ZoneInfo(target_tz)

        if dt.tzinfo is None:
            # Assume Mexico timezone if naive
            dt = dt.replace(tzinfo=MEXICO_TIMEZONE)
            logger.debug(f"Naive datetime assumed as Mexico timezone: {dt}")

        target_dt = dt.astimezone(target_tz)
        logger.debug(f"Converted {dt} from Mexico to {target_tz}: {target_dt}")
        return target_dt
