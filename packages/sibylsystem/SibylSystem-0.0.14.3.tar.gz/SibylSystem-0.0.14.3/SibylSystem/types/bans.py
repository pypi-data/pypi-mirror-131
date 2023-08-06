# SibylSystem-py

# Copyright (C) 2021 Sayan Biswas, AnonyIndian

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel
from .error import Error


class Ban(BaseModel):
    date: datetime.datetime = None
    user_id: int = None
    reason: Optional[str] = None
    message: Optional[str] = None
    banned: Optional[bool] = None
    is_bot: Optional[bool] = False
    hue_color: Optional[str] = None
    banned_by: Optional[int] = None
    source_group: Optional[str] = None
    ban_source_url: Optional[str] = None
    ban_flags: Optional[List[str]] = None
    crime_coefficient: Optional[int] = None


@dataclass
class MultiBanInfo:
    user_id: Optional[int] = None
    is_bot: Optional[bool] = False
    reason: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = None
    source_group: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "is_bot": self.is_bot,
            "reason": self.reason,
            "message": self.message,
            "source": self.source,
            "source_group": self.source_group
        }


class BanRes(BaseModel):
    previous_ban: Optional[Ban] = None
    current_ban: Optional[Ban] = None


class BanResult(BaseModel):
    success: Optional[bool] = False
    result: Optional[BanRes] = None
    error: Optional[Error] = None
