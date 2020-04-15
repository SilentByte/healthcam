"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

import pytz
import psycopg2
from uuid import UUID, uuid4
from datetime import datetime


def _utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=pytz.utc)


DatabaseError = psycopg2.Error


class Repo:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
        )

    def insert_record(self, id: UUID, device_serial: str, recorded_on: datetime, min_confidence: float,
                      people_in_frame: int, activity: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO detections (
                    id,
                    device_serial,
                    created_on,
                    recorded_on,
                    min_confidence,
                    people_in_frame,
                    activity
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    str(id),
                    device_serial,
                    _utc_now(),
                    recorded_on,
                    min_confidence,
                    people_in_frame,
                    activity,
                )
            )
            self.connection.commit()

    def get_all_activities(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT d.id,
                       c.device_name,
                       d.created_on,
                       d.recorded_on,
                       d.min_confidence,
                       d.people_in_frame,
                       d.activity
                FROM detections AS d
                JOIN cameras AS c ON c.device_serial = d.device_serial
                WHERE rating = 0
                ORDER BY recorded_on;
                """
            )

            return [
                {
                    'id': a[0],
                    'device_name': a[1],
                    'created_on': a[2],
                    'recorded_on': a[3],
                    'min_confidence': a[4],
                    'people_in_frame': a[5],
                    'activity': a[6],
                }
                for a in cursor.fetchall()
            ]

    def rate_activity(self, activity_id: UUID, rating: int) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE detections
                SET rating = %s
                WHERE id = %s
                """,
                (
                    rating,
                    str(activity_id),
                )
            )
            self.connection.commit()

    def get_all_cameras(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, device_name, pinged_on,
                (SELECT count(*) FROM detections WHERE device_serial = c.device_serial AND activity = 'compliant'),
                (SELECT count(*) FROM detections WHERE device_serial = c.device_serial AND activity = 'violation'),
                (SELECT count(*) FROM detections WHERE device_serial = c.device_serial AND activity = 'override')
                FROM cameras AS c
                ORDER BY device_name;
                """
            )

            return [
                {
                    'id': a[0],
                    'device_name': a[1],
                    'pinged_on': a[2],
                    'compliant_count': a[3],
                    'violation_count': a[4],
                    'override_count': a[5],
                }
                for a in cursor.fetchall()
            ]

    def get_stats(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    ARRAY(
                        SELECT count(*)
                        FROM detections
                        WHERE activity = 'compliant'
                        GROUP BY date_trunc('day', recorded_on)
                        ORDER BY date_trunc('day', recorded_on)
                        LIMIT 7
                    ) AS compliant_count,
                    ARRAY(
                        SELECT count(*)
                        FROM detections
                        WHERE activity = 'violation'
                        GROUP BY date_trunc('day', recorded_on)
                        ORDER BY date_trunc('day', recorded_on)
                        LIMIT 7
                    ) AS violation_count,
                    ARRAY(
                        SELECT count(*)
                        FROM detections
                        WHERE activity = 'override'
                        GROUP BY date_trunc('day', recorded_on)
                        ORDER BY date_trunc('day', recorded_on)
                        LIMIT 7
                    ) AS override_count
                """
            )

            stats = cursor.fetchone()
            return {
                'compliant_count': ([0] * 7 + stats[0])[-7:],
                'violation_count': ([0] * 7 + stats[1])[-7:],
                'override_count': ([0] * 7 + stats[2])[-7:],
            }

    def insert_ping(self, device_serial: str, device_name: str):
        with self.connection.cursor() as cursor:
            pinged_on = _utc_now()
            cursor.execute(
                """
                INSERT INTO cameras (id, device_serial, device_name, pinged_on)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (device_serial)
                DO UPDATE SET device_serial = %s, device_name = %s, pinged_on = %s
                """,
                (
                    str(uuid4()),
                    device_serial,
                    device_name,
                    pinged_on,
                    device_serial,
                    device_name,
                    pinged_on,
                )
            )
            self.connection.commit()
