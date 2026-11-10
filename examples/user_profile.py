"""Validate a user profile and show how invalid data is reported.

Run:

    python user_profile.py
"""

import re

from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator

PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
NAME_PATTERN = re.compile(r"^[A-Za-z]+(?: [A-Za-z]+)*$")


class UserProfile(BaseModel):
    name: str
    age: int = Field(ge=0, le=120)
    email: EmailStr
    pan: str

    @field_validator("name")
    @classmethod
    def name_is_letters(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned or not NAME_PATTERN.fullmatch(cleaned):
            raise ValueError("name must contain letters and single spaces only")
        return cleaned

    @field_validator("pan")
    @classmethod
    def pan_format(cls, value: str) -> str:
        cleaned = value.strip().upper()
        if not PAN_PATTERN.fullmatch(cleaned):
            raise ValueError("PAN must match ABCDE1234F")
        return cleaned


SAMPLES = [
    {
        "label": "invalid name",
        "data": {
            "name": "Ada 123",
            "age": 30,
            "email": "ada@example.com",
            "pan": "ABCDE1234F",
        },
    },
    {
        "label": "age out of range",
        "data": {
            "name": "Ada Lovelace",
            "age": 150,
            "email": "ada@example.com",
            "pan": "ABCDE1234F",
        },
    },
    {
        "label": "malformed email",
        "data": {
            "name": "Ada Lovelace",
            "age": 30,
            "email": "not-an-email",
            "pan": "ABCDE1234F",
        },
    },
    {
        "label": "malformed PAN",
        "data": {
            "name": "Ada Lovelace",
            "age": 30,
            "email": "ada@example.com",
            "pan": "ABCD1234",
        },
    },
    {
        "label": "valid profile",
        "data": {
            "name": "Ada Lovelace",
            "age": 36,
            "email": "ada@example.com",
            "pan": "abcde1234f",
        },
    },
]


def check(label: str, data: dict) -> None:
    print(f"\n{label}")
    try:
        profile = UserProfile.model_validate(data)
    except ValidationError as exc:
        for error in exc.errors():
            field = ".".join(str(part) for part in error["loc"])
            print(f"  {field}: {error['msg']} ({error['type']})")
        return
    print(f"  ok: {profile}")


def main() -> None:
    for sample in SAMPLES:
        check(sample["label"], sample["data"])


if __name__ == "__main__":
    main()
