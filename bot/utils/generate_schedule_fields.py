from datetime import date, datetime
from zoneinfo import ZoneInfo

from django.conf import settings


def extract_unique_dates(dt_strings: list[datetime]) -> list[date]:
    dates = [d.astimezone(ZoneInfo(settings.TIME_ZONE)).date() for d in dt_strings]
    return sorted(list(set(dates)))


def generate_schedule_fields(schedule: list[dict]) -> dict[str, str]:
    unique_dates = extract_unique_dates([s["date"] for s in schedule])
    cb_fields_date: dict[date, list[str]] = {d: [] for d in unique_dates}

    for doc in schedule:
        dt: datetime = doc["date"].astimezone(ZoneInfo(settings.TIME_ZONE))
        dt_time = dt.strftime("%H:%M")
        if (descriptor := doc.get("album_type")) is not None:
            descriptor = descriptor.title()
        else:
            if (descriptor := doc.get("release")) is not None:
                if "japan" in descriptor.lower():
                    descriptor = "Japan"
                else:
                    descriptor = descriptor.title()
            else:
                descriptor = ""
        cb_fields_date[dt.date()].append(f"`[{dt_time}]` **{doc['artist']}** {descriptor} 『{doc['album_title']}』")

    cb_fields_str: dict[str, str] = {}
    for key in cb_fields_date.keys():
        is_today = " `<today>`" if key == datetime.now(ZoneInfo(settings.TIME_ZONE)).date() else ""
        str_key = f'{key.strftime("%b %d (%a)")}{is_today}'
        cb_fields_str[str_key] = "\n".join(cb_fields_date[key])

    return cb_fields_str
