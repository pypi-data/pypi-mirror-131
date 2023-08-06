from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.metadata import Metadata
from ..models.publication import Publication
from ..models.section import Section
from ..types import UNSET, Unset

T = TypeVar("T", bound="Article")


@attr.s(auto_attribs=True)
class Article:
    """ """

    identifier: str
    title: str
    publication: Union[Unset, Publication] = UNSET
    metadata: Union[Unset, Metadata] = UNSET
    sections: Union[Unset, List[Section]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        identifier = self.identifier
        title = self.title
        publication: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.publication, Unset):
            publication = self.publication.to_dict()

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        sections: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sections, Unset):
            sections = []
            for sections_item_data in self.sections:
                sections_item = sections_item_data.to_dict()

                sections.append(sections_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "identifier": identifier,
                "title": title,
            }
        )
        if publication is not UNSET:
            field_dict["publication"] = publication
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if sections is not UNSET:
            field_dict["sections"] = sections

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        identifier = d.pop("identifier")

        title = d.pop("title")

        _publication = d.pop("publication", UNSET)
        publication: Union[Unset, Publication]
        if isinstance(_publication, Unset):
            publication = UNSET
        else:
            publication = Publication.from_dict(_publication)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        sections = []
        _sections = d.pop("sections", UNSET)
        for sections_item_data in _sections or []:
            sections_item = Section.from_dict(sections_item_data)

            sections.append(sections_item)

        article = cls(
            identifier=identifier,
            title=title,
            publication=publication,
            metadata=metadata,
            sections=sections,
        )

        return article
