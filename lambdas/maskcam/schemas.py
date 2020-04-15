"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

from typing import (
    Type,
    List,
    Any,
    Union,
)

from marshmallow import (
    Schema,
    ValidationError,
    fields,
)

ValidationError = ValidationError


class QuerySchema(Schema):
    bounds = fields.Tuple((
        fields.Float(),
        fields.Float(),
        fields.Float(),
        fields.Float(),
    ), required=True)

    limit = fields.Integer(required=False)


class UploadSchema(Schema):
    device_serial = fields.String(required=True)
    timestamp = fields.DateTime(required=True)
    photo_data = fields.String(required=True)
    person_threshold = fields.Float(required=True)
    mask_threshold = fields.Float(required=True)
    override = fields.String(required=True)


class RatingSchema(Schema):
    activity_id = fields.UUID(required=True)
    rating = fields.Integer(required=True)


class PingSchema(Schema):
    device_serial = fields.String(required=True)
    device_name = fields.String(required=True)


def apply_schema(schema: Type[Schema], data: Union[str, dict]):
    if isinstance(data, str):
        return schema().loads(data)
    else:
        return schema().load(data)


def dump_schema_list(schema: Type[Schema], data: Any) -> List[dict]:
    # noinspection PyTypeChecker
    return schema().dump(data, many=True)
