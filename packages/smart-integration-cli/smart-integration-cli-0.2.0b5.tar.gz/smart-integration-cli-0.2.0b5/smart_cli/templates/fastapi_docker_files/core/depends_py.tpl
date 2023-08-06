import os
from typing import Optional, Tuple, Any, no_type_check
from importlib import import_module
from fastapi import Request, HTTPException, Security
from fastapi.param_functions import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security.api_key import (
    APIKeyBase,
    APIKey,
    APIKeyIn,
)
from fastapi.security.oauth2 import get_authorization_scheme_param
from integration_tools.api import BaseCredentialMixin
from integration_tools.exceptions import PermissionDenied

settings = import_module(os.environ.get('FASTAPI_SETTINGS', 'app.config.settings'))
credential_module_path, credential_model_name = settings.CREDENTIAL_MODEL.rsplit('.', 1) # type: ignore
module = import_module(credential_module_path)
CREDENTIAL_MODEL = getattr(module, credential_model_name)

__all__ = ('get_smart_auth', 'get_credential')


class SmartHTTPToken(APIKeyBase):
    def __init__(
        self, *, name: str, scheme_name: Optional[str] = None, auto_error: bool = True
    ):
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name=name)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization: str = request.headers.get(self.model.name)
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=403, detail="Permission Denied",
                )
            else:
                return None
        if scheme.lower() not in ("token",):
            if self.auto_error:
                raise HTTPException(
                    status_code=403, detail="Permission Denied",
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


sec = SmartHTTPToken(name='Authorization')


@no_type_check
async def check_auth_params(
    platform_id: str, auth: HTTPAuthorizationCredentials = Security(sec),
) -> Tuple:
    if platform_id not in ('dev', 'prod'):
        raise HTTPException(
            status_code=403, detail="Permission Denied, invalid platform_id",
        )
    return auth.credentials, platform_id


class Auth(BaseCredentialMixin):
    pass


@no_type_check
async def get_smart_auth(auth_params: tuple = Depends(check_auth_params)):
    auth = Auth()
    try:
        user_info = await auth.get_user_info_async(*auth_params)
        return {
            'smart_user_name': user_info['username'],
            'smart_user_id': user_info['id'],
            'platform_id': auth_params[-1],
        }

    except PermissionDenied as e:
        raise HTTPException(status_code=e.status, detail=e.error_detail)

@no_type_check
async def get_credential(credential_id: str, _=Depends(get_smart_auth)) -> Any:
    credential = None
    raise NotImplementedError('implement get credential')
    # if not credential:
    #     HTTPException(
    #         status_code=403, detail="Invalid credential",
    #     )
    # return credential
