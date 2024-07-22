from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class EmailDTO:
    """
    Data Transfer Object for email data.
    """
    message_id: str
    sensitive: bool
    date: str
    subject: str
    from_: str
    to: List[str]
    content_type: str
    body_plain: str
    body_html: str
    in_reply_to: Optional[str] = None
    references: List[str] = field(default_factory=list)
    mime_version: Optional[str] = None
    user_agent: Optional[str] = None
    content_language: Optional[str] = None
    responses: List['EmailDTO'] = field(default_factory=list)