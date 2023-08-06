from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.author import Author
from ..models.metadata_ids import MetadataIds
from ..types import UNSET, Unset

T = TypeVar("T", bound="Metadata")


@attr.s(auto_attribs=True)
class Metadata:
    """ """

    authors: Union[Unset, List[Author]] = UNSET
    ids: Union[Unset, MetadataIds] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        authors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.authors, Unset):
            authors = []
            for authors_item_data in self.authors:
                authors_item = authors_item_data.to_dict()

                authors.append(authors_item)

        ids: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ids, Unset):
            ids = self.ids.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if authors is not UNSET:
            field_dict["authors"] = authors
        if ids is not UNSET:
            field_dict["ids"] = ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        authors = []
        _authors = d.pop("authors", UNSET)
        for authors_item_data in _authors or []:
            authors_item = Author.from_dict(authors_item_data)

            authors.append(authors_item)

        _ids = d.pop("ids", UNSET)
        ids: Union[Unset, MetadataIds]
        if isinstance(_ids, Unset):
            ids = UNSET
        else:
            ids = MetadataIds.from_dict(_ids)

        metadata = cls(
            authors=authors,
            ids=ids,
        )

        return metadata
