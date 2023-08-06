from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Section")


@attr.s(auto_attribs=True)
class Section:
    """ """

    name: Union[Unset, str] = UNSET
    paragraphs: Union[Unset, List[Union[List[str], str]]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        paragraphs: Union[Unset, List[Union[List[str], str]]] = UNSET
        if not isinstance(self.paragraphs, Unset):
            paragraphs = []
            for paragraphs_item_data in self.paragraphs:
                if isinstance(paragraphs_item_data, list):
                    paragraphs_item = paragraphs_item_data

                else:
                    paragraphs_item = paragraphs_item_data

                paragraphs.append(paragraphs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if paragraphs is not UNSET:
            field_dict["paragraphs"] = paragraphs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        paragraphs = []
        _paragraphs = d.pop("paragraphs", UNSET)
        for paragraphs_item_data in _paragraphs or []:

            def _parse_paragraphs_item(data: object) -> Union[List[str], str]:
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    paragraphs_item_type_0 = cast(List[str], data)

                    return paragraphs_item_type_0
                except:  # noqa: E722
                    pass
                return cast(Union[List[str], str], data)

            paragraphs_item = _parse_paragraphs_item(paragraphs_item_data)

            paragraphs.append(paragraphs_item)

        section = cls(
            name=name,
            paragraphs=paragraphs,
        )

        return section
