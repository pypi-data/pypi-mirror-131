""" Contains some shared types for properties """
import re
from typing import BinaryIO, Generic, List, MutableMapping, Optional, TextIO, Tuple, TypeVar, Union

import attr
from httpx import HTTPError, codes


class Unset:
    def __bool__(self) -> bool:
        return False


UNSET: Unset = Unset()
FileJsonType = Tuple[Optional[str], Union[BinaryIO, TextIO], Optional[str]]


@attr.s(auto_attribs=True)
class File:
    """Contains information for file uploads"""

    payload: Union[BinaryIO, TextIO]
    file_name: Optional[str] = None
    mime_type: Optional[str] = None

    def to_tuple(self) -> FileJsonType:
        """Return a tuple representation that httpx will accept for multipart/form-data"""
        return self.file_name, self.payload, self.mime_type


T = TypeVar("T")


@attr.s(auto_attribs=True)
class Response(Generic[T]):
    """A response from an endpoint"""

    status_code: int
    content: bytes
    headers: MutableMapping[str, str]
    parsed: Optional[T]

    @property
    def is_informational(self) -> bool:
        """
        A property which is `True` for 1xx status codes, `False` otherwise.
        """
        return codes.is_informational(self.status_code)

    @property
    def is_success(self) -> bool:
        """
        A property which is `True` for 2xx status codes, `False` otherwise.
        """
        return codes.is_success(self.status_code)

    @property
    def is_redirect(self) -> bool:
        """
        A property which is `True` for 3xx status codes, `False` otherwise.

        Note that not all responses with a 3xx status code indicate a URL redirect.

        Use `response.has_redirect_location` to determine responses with a properly
        formed URL redirection.
        """
        return codes.is_redirect(self.status_code)

    @property
    def is_client_error(self) -> bool:
        """
        A property which is `True` for 4xx status codes, `False` otherwise.
        """
        return codes.is_client_error(self.status_code)

    @property
    def is_server_error(self) -> bool:
        """
        A property which is `True` for 5xx status codes, `False` otherwise.
        """
        return codes.is_server_error(self.status_code)

    @property
    def is_error(self) -> bool:
        """
        A property which is `True` for 4xx and 5xx status codes, `False` otherwise.
        """
        return codes.is_error(self.status_code)

    @property
    def has_redirect_location(self) -> bool:
        """
        Returns True for 3xx responses with a properly formed URL redirection,
        `False` otherwise.
        """
        return (
            self.status_code
            in (
                # 301 (Cacheable redirect. Method may change to GET.)
                codes.MOVED_PERMANENTLY,
                # 302 (Uncacheable redirect. Method may change to GET.)
                codes.FOUND,
                # 303 (Client should make a GET or HEAD request.)
                codes.SEE_OTHER,
                # 307 (Equiv. 302, but retain method)
                codes.TEMPORARY_REDIRECT,
                # 308 (Equiv. 301, but retain method)
                codes.PERMANENT_REDIRECT,
            )
            and "Location" in self.headers
        )

    def raise_for_status(self):
        """Raises :class:`HTTPError`, if one occurred."""

        http_error_msg = ""
        if isinstance(self.content, bytes):
            # We attempt to decode utf-8 first because some servers
            # choose to localize their reason strings. If the string
            # isn't utf-8, we fall back to iso-8859-1 for all other
            # encodings. (See PR #3538)
            try:
                reason = self.content.decode("utf-8")
            except UnicodeDecodeError:
                reason = self.content.decode("iso-8859-1")
        else:
            reason = self.content

        if 400 <= self.status_code < 500:
            http_error_msg = "%s Client Error: %s" % (self.status_code, reason)

        elif 500 <= self.status_code < 600:
            http_error_msg = "%s Server Error: %s" % (self.status_code, reason)

        if http_error_msg:
            raise HTTPError(http_error_msg)


from bs4 import BeautifulSoup, Tag
from dateutil import parser


class TEI:
    """
    Methods to transform TEI (Text Encoding Initiative) XML into article objects.
    """

    @staticmethod
    def parse(stream, sentences=False, figures=False):
        """
        Parses a TEI XML datastream and returns a processed article.

        Args:
            stream: handle to input data stream
        Returns:
            Article
        """
        from .models import Article

        soup = BeautifulSoup(stream, "lxml")
        title = soup.title.text
        art = Article(identifier=None, title=title)
        art.publication = TEI.publication(soup)
        art.metadata = TEI.metadata(soup)
        if art.metadata.ids:
            art.identifier = art.metadata.ids["MD5"]

        # Parse text sections
        art.sections = TEI.text(soup, title, sentences, figures)
        return art

    @staticmethod
    def date(published):
        """
        Attempts to parse a publication date, if available. Otherwise, None is returned.

        Args:
            published: published object

        Returns:
            publication date if available/found, None otherwise
        """

        # Parse publication date
        # pylint: disable=W0702
        try:
            published = parser.parse(published["when"]) if published and "when" in published.attrs else None
        except:
            published = None

        return published

    @staticmethod
    def authors(source):
        """
        Parses authors and associated affiliations from the article.

        Args:
            elements: authors elements

        Returns:
            (semicolon separated list of authors, semicolon separated list of affiliations, primary affiliation)
        """
        from .models import Address, Affiliation, Author, PersName

        authors: List[Author] = []
        for author in source.find_all("author"):
            auth: Author = None
            affiliations: List[Affiliation] = []
            name = author.find("persname")
            if name:
                surname = name.find("surname")
                if surname:
                    pers = PersName(surname=surname.text)
                    auth = Author(pers_name=pers)
                    authors.append(auth)
                    for forename in name.find_all("forename"):
                        if "type" in forename.attrs and forename["type"] == "first":
                            pers.firstname = forename.text
                        elif "type" in forename.attrs and forename["type"] == "middle":
                            pers.middlename = forename.text
            if auth:
                email = author.find("email")
                if email:
                    auth.email = email.text
                for affiliation in author.find_all("affiliation"):
                    aff = Affiliation()
                    affiliations.append(aff)
                    for orgName in affiliation.find_all("orgname"):
                        if "type" in orgName.attrs and orgName["type"] == "institution":
                            aff.institution = orgName.text
                        if "type" in orgName.attrs and orgName["type"] == "department":
                            aff.department = orgName.text
                        if "type" in orgName.attrs and orgName["type"] == "laboratory":
                            aff.laboratory = orgName.text
                    auth.affiliations = affiliations
                    address = author.find("address")
                    if address:
                        aff.address = Address.from_dict(
                            {el.name: el.text for el in address.children if isinstance(el, Tag)}
                        )

        return authors

    @staticmethod
    def metadata(soup):
        """
        Extracts article metadata.

        Args:
            soup: bs4 handle

        Returns:
            (published, publication, authors, reference)
        """
        from .models import Metadata, MetadataIds

        # Build reference link
        source = soup.find("sourcedesc")
        meta = Metadata()
        if source:
            struct = source.find("biblstruct")
            meta.authors = TEI.authors(struct)
            ids_dict = {}
            for idno in struct.find_all("idno"):
                if "type" in idno.attrs:
                    ids_dict[idno["type"]] = idno.text
            meta.ids = MetadataIds.from_dict(ids_dict)
        return meta

    @staticmethod
    def publication(soup):
        """
        Extracts article publication.

        Args:
            soup: bs4 handle

        Returns:
            (published, publication, authors, reference)
        """
        from .models import Publication

        # Build reference link
        publicationStmt = soup.find("publicationstmt")
        pub = Publication()
        if publicationStmt:
            published = publicationStmt.find("date")
            publisher = publicationStmt.find("publisher")

            # Parse publication information
            pub.published = TEI.date(published)
            if publisher:
                pub.publisher = publisher.text
        return pub

    @staticmethod
    def abstract(soup, title, sentences=False):
        """
        Builds a list of title and abstract sections.

        Args:
            soup: bs4 handle
            title: article title

        Returns:
            list of sections
        """
        from .models import Section

        sections = [Section("TITLE", paragraphs=[[title]] if sentences else [title])]

        abstract = soup.find("abstract")
        secs = []
        if abstract:
            for div in abstract.find_all("div", recursive=False):
                sec = TEI.section("ABSTRACT", div.children, sentences)
                secs.append(sec)
            sections.extend(secs)

        return sections

    @staticmethod
    def section(name, children, sentences=False):
        from .models import Section

        sec = Section(name=name, paragraphs=[])
        for p in children:
            if p:
                if sentences:
                    if isinstance(p, Tag) and p.name == "p":
                        sents = []
                        for s in p.children:
                            if isinstance(s, Tag) and s.name == "s":
                                sents.append(s.text)
                            else:
                                sents.append(str(s))
                        sec.paragraphs.append(sents)
                    else:
                        sec.paragraphs.append([str(p)])
                else:
                    if isinstance(p, Tag) and p.name == "p":
                        sec.paragraphs.append(p.text)
                    else:
                        sec.paragraphs.append(str(p))
        return sec

    @staticmethod
    def text(soup, title, sentences=False, figures=False):
        """
        Builds a list of text sections.

        Args:
            soup: bs4 handle
            title: article title

        Returns:
            list of sections
        """

        # Initialize with title and abstract text
        sections = TEI.abstract(soup, title, sentences)

        secs = []
        div_or_fig = re.compile("div|figure") if figures else "div"
        for section in soup.find("text").find_all(div_or_fig, recursive=False):
            # Section name and text
            children = list(section.children)
            # Attempt to parse section header
            if children and not children[0].name:
                name = str(children[0])
                children = children[1:]
            else:
                name = None
            if section.name == "div":
                sec = TEI.section(name, children, sentences)
                secs.append(sec)
            elif section.name == "figure":
                label = None
                if children and children[0].name == "label":
                    label = children[0].text
                    children = children[1:]
                desc = None
                if children and children[0].name == "figdesc":
                    desc = children[0].find("div") or children[0]
                children = [name, label]
                if desc:
                    children.extend(desc.children)
                # Use XML Id as figure name to ensure figures are uniquely named
                name = section.get("xml:id")
                sec = TEI.section(name, children, sentences)
                secs.append(sec)
            # Transform and clean text
            # text = Text.transform(text)
            # Split text into sentences, transform text and add to sections
        sections.extend(secs)

        # Extract text from tables
        for figure in soup.find("text").find_all("figure"):
            name = figure.get("xml:id").upper()

            # Search for table
            figure.find("table")
            # if table:
            #     sections.extend([(name, x) for x in Table.extract(table)])

        return sections


__all__ = ["File", "Response", "FileJsonType", "TEI"]
