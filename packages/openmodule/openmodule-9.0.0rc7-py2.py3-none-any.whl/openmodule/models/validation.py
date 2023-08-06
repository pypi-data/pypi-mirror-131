from datetime import datetime
from enum import Enum
from typing import List, Optional

from openmodule.models.base import OpenModuleModel, ZMQMessage, timezone_validator, base64_validator


class ValidationProviderRequestTicketType(str, Enum):
    qr = "qr"


class ValidationProviderResponseState(str, Enum):
    ok = "ok"
    not_applicable = "not_applicable"


class ValidationProviderResponseCommonError(str, Enum):
    # unique validation id was already used
    already_used = "already_used"
    # e.g. signature validation error
    invalid = "invalid"
    expired = "expired"
    outside_timewindow = "outside_timewindow"


class ValidationProviderRegisterRequestMessage(ZMQMessage):
    """
    sent by the controller as a request to all validation providers
    each validation provider who wants to register itself at the controller has to answer
    with a register message
    """
    type: str = "register_request"


class ValidationProviderRegisterMessage(ZMQMessage):
    """
    sent by a validation provider if it wants to register itself at the controller
    """
    type: str = "register"


class ValidationProviderUnregisterMessage(ZMQMessage):
    """
    sent by a validation provider if it shuts down and wants to unregister itself
    """
    type: str = "unregister"


class ValidateRequest(OpenModuleModel):
    name: str
    occupant_id: str
    type: ValidationProviderRequestTicketType
    # payload has to be base64 encoded
    payload: str

    # TODO: fix base64_validator
    # _b64_payload = base64_validator("payload")


class ValidateResponseError(OpenModuleModel):
    type: ValidationProviderResponseCommonError
    start: Optional[datetime]
    end: Optional[datetime]

    _tz_start = timezone_validator("start")
    _tz_end = timezone_validator("end")


class ValidateResponse(OpenModuleModel):
    occupant_id: str
    state: ValidationProviderResponseState
    error: Optional[ValidateResponseError]
    validation_id: Optional[str]
    cost_entries: Optional[List[dict]]
