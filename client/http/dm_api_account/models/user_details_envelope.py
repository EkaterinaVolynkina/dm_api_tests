from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (
    List,
    Optional,
    Union,
)

from pydantic import BaseModel, Field


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class Info(BaseModel):
    value: str
    parse_mode: str = Field(..., alias='parseMode')

class UserRole(str, Enum):
    #Guest, Player, Administrator, NannyModerator, RegularModerator, SeniorModerator
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINICTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'
class Paging(BaseModel):
    posts_per_page: int = Field(None, alias='postsPerPage')
    comments_per_page: int = Field(None, alias='commentsPerPage')
    topics_per_page: int = Field(None, alias='topicsPerPage')
    messages_per_page: int = Field(None, alias='messagesPerPage')
    entities_per_page: int = Field(None, alias='entitiesPerPage')


class Settings(BaseModel):
    color_schema: str = Field(None, alias='colorSchema')
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: Paging


class UserDetails(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None, alias='status')
    rating: Rating
    online: datetime = Field(None, alias='online')
    name: str = Field(None, alias='name')
    location: str = Field(None, alias='location')
    registration: datetime = Field(None, alias='registration')
    icq: Optional[str] = Field(None, alias='icq')
    skype: Optional[str] = Field(None, alias='skype')
    original_picture_url: Optional[str] = Field(None, alias='originalPictureUrl')
    info: Union[Info, str, None] = None
    settings: Settings


class UserDetailsEnvelope(BaseModel):
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
