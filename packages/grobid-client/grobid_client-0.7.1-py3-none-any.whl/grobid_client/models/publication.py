import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Publication")


@attr.s(auto_attribs=True)
class Publication:
    """ """

    publisher: Union[Unset, str] = UNSET
    published: Union[Unset, datetime.date] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        publisher = self.publisher
        published: Union[Unset, str] = UNSET
        if not isinstance(self.published, Unset):
            published = self.published.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if publisher is not UNSET:
            field_dict["publisher"] = publisher
        if published is not UNSET:
            field_dict["published"] = published

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        publisher = d.pop("publisher", UNSET)

        _published = d.pop("published", UNSET)
        published: Union[Unset, datetime.date]
        if isinstance(_published, Unset):
            published = UNSET
        else:
            published = isoparse(_published).date()

        publication = cls(
            publisher=publisher,
            published=published,
        )

        return publication
