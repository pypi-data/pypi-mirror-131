"""
Apache-2.0

Copyright 2021 RPS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the LICENSE file for the specific language governing permissions and
limitations under the License.
"""
from enum import Enum


class APIErrors(Enum):
    """Class Defines Error Enums: https://docs.plugify.cf/http/#apierror"""

    UNKNOWN = 0
    MISSING_TOKEN = 1
    INCORRECT_TOKEN = 2
    INVALID_DATA = 3
    INVALID_CAPTCHA_RESPONSE = 4
    INVALID_EMAIL = 5
    EMAIL_USED = 6
    USERNAME_CLAIMED = 7
    NO_SUCH_USER = 8
    NO_SUCH_GROUP = 9
    INCORRECT_PASSWORD = 10
    NOT_VERIFIED = 11
    INVALID_VERIFICATION_TOKEN = 12
    NO_SUCH_INVITE = 13
    NOT_ENOUGH_PERMS = 14
    NO_INVITE_CODE = 15
    INVALID_USERNAME = 16
    ALREADY_IN_GROUP = 17
    NO_SUCH_APP = 18
    INVALID_SECRET = 19
    NO_SUCH_CHANNEL = 20
    NO_SUCH_MEMBER = 21
    USER_NOT_BANNED = 22
