from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Model(BaseModel):
    message: Optional[str] = None