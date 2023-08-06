import json

from azure.iot.device import Message

from eolian.database.models.cetasa import Magana10Mindata, Met10Mindata, Oncala10Mindata
from eolian.database.models.plc import PLCData


# Function to convert an object to an IotHub message
def obj_to_message(obj, model):
    msg = Message(
        data=json.dumps(obj), content_encoding="utf-8", content_type="application/json"
    )
    msg.custom_properties["model"] = model.__name__

    return msg


# Function to convert an IotHub message to its corresponding Eolian object
def message_to_obj(event):
    if not event.properties:
        return None

    model_name = event.properties[b"model"].decode("utf-8")

    models_by_name = {
        Oncala10Mindata.__name__: Oncala10Mindata,
        Magana10Mindata.__name__: Magana10Mindata,
        Met10Mindata.__name__: Met10Mindata,
        PLCData.__name__: PLCData,
    }

    return models_by_name[model_name](**event.body_as_json())
