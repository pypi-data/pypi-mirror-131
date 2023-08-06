from typing import Optional, Any, Union, Dict

import jwt
from packaging.version import Version, parse


def encode_jwt_token(
    payload: Union[Dict[str, Any]],
    key: str,
    algorithm: str = 'HS256',
    headers: Optional[dict] = None,
    json_encoder: Optional[Any] = None
) -> str:
    """Compatability function for creating a JWT token.

    Handles difference in jwt v1 which returns ``bytes`` type and jwt v2 which returns
    ``str`` type by always choosing to return a ``str`` type (manually decoding into
    ascii characters if required).

    Function arguments are the same for both JWT versions.
    """
    jwt_version = parse(jwt.__version__)
    if Version("1.0") <= jwt_version < Version('2.0'):
        res = jwt.encode(payload=payload, key=key, algorithm=algorithm, headers=headers, json_encoder=json_encoder)
        return res.decode('ascii')
    elif Version("2.0") <= jwt_version < Version("3.0"):
        return jwt.encode(payload=payload, key=key, algorithm=algorithm, headers=headers, json_encoder=json_encoder)
    else:
        raise RuntimeError(f"PyJWT version: {jwt_version} is not supported. please use v1.0 <= jwt_version <= v3.0")
