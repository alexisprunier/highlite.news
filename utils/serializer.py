from datetime import datetime, date
from decimal import Decimal


class Serializer:

    @staticmethod
    def serialize(to_serialize, table_class):
        if isinstance(to_serialize, list):
            serialized_objects = []
            for o in to_serialize:
                serialized_objects.append(Serializer.serialize_object(o, table_class))
            return serialized_objects
        else:
            return Serializer.serialize_object(to_serialize, table_class)

    @staticmethod
    def serialize_join_result(to_serialize, table_class_left, table_class_right):
        result = []

        for t in to_serialize:
            value = [Serializer.serialize_object(t[0], table_class_left),
                     Serializer.serialize_object(t[1], table_class_right)]
            result.append(value)

        return result

    @staticmethod
    def serialize_object(o, table_class):
        obj = {}

        if o != None:
            for c in table_class.__table__.columns:
                if isinstance(getattr(o, c.name), datetime):
                    obj[c.name] = getattr(o, c.name).isoformat()
                elif isinstance(getattr(o, c.name), date):
                    obj[c.name] = getattr(o, c.name).isoformat()
                elif isinstance(getattr(o, c.name), Decimal):
                    obj[c.name] = float(getattr(o, c.name))
                else:
                    obj[c.name] = getattr(o, c.name)
        return obj
