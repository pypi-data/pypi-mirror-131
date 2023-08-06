import os
from collections import defaultdict
from functools import lru_cache
from typing import List, cast, Type

from grobid_client import Client
from grobid_client.api.pdf import process_fulltext_document
from grobid_client.models import ProcessForm, Article
from grobid_client.types import File, TEI
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, Sentence, Boundary
from starlette.datastructures import UploadFile

# _home = os.path.expanduser('~')
# xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or os.path.join(_home, '.cache')
APP_GROBID_URI = os.environ.get('APP_GROBID_URI', "https://sherpa-grobid.kairntech.com")


class GrobidParameters(ConverterParameters):
    sourceText: bool = Field(False, description='Set source text in conversion output')
    sentences: bool = Field(False, description='Force sentence segmentation')
    figures: bool = Field(False, description='Do extract figures and tables descriptions')


class GrobidConverter(ConverterBase):
    """Grodbid PDF converter .
    """

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: GrobidParameters = \
            cast(GrobidParameters, parameters)

        client = get_client()
        doc = None
        form = ProcessForm(
            segment_sentences="1" if params.sentences else "0",
            input_=File(file_name=source.filename, payload=source.file, mime_type=source.content_type),
        )
        r = process_fulltext_document.sync_detailed(client=client, multipart_data=form)
        if r.is_success:
            doc = article_to_doc(r, params)
        else:
            r.raise_for_status()
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return GrobidParameters


def article_to_doc(response, params):
    article: Article = TEI.parse(response.content, sentences=params.sentences, figures=params.figures)
    doc = Document(identifier=article.identifier, title=article.title)
    if params.sourceText:
        doc.sourceText = response.content.decode("utf-8")
    doc.metadata = {}
    if article.publication:
        if article.publication.published:
            doc.metadata['published'] = str(article.publication.published)
        if article.publication.publisher:
            doc.metadata['publisher'] = article.publication.publisher
    if article.metadata:
        if article.metadata.ids:
            for k, v in article.metadata.ids.additional_properties.items():
                doc.metadata[k] = v
        if article.metadata.authors:
            authors = set()
            affiliations = set()
            for author in article.metadata.authors:
                auth = []
                if author.pers_name.firstname:
                    auth.append(author.pers_name.firstname)
                if author.pers_name.middlename:
                    auth.append(author.pers_name.middlename)
                if author.pers_name.surname:
                    auth.append(author.pers_name.surname)
                authors.add(" ".join(auth))
                if author.affiliations:
                    for affiliation in author.affiliations:
                        aff = []
                        if affiliation.institution:
                            aff.append(affiliation.institution)
                        if affiliation.department:
                            aff.append(affiliation.department)
                        if affiliation.laboratory:
                            aff.append(affiliation.laboratory)
                        affiliations.add(", ".join(aff))
                doc.metadata['authors'] = list(authors)
                doc.metadata['affiliations'] = list(affiliations)
    sections_to_text(doc, article.sections, params)
    return doc


def sections_to_text(doc, sections, params):
    if sections:
        text = ""
        sentences = []
        boundaries = defaultdict(list)
        for section in sections:
            start = len(text)
            bstart = start
            text += section.name + "\n"
            end = len(text)
            sentences.append(Sentence(start=start, end=end))
            if section.paragraphs:
                for paragraph in section.paragraphs:
                    if params.sentences:
                        for sentence in paragraph:
                            start = len(text)
                            text += sentence + " "
                            end = len(text)
                            sentences.append(Sentence(start=start, end=end))
                        text += "\n"
                    else:
                        start = len(text)
                        text += paragraph + "\n"
                        end = len(text)
                        sentences.append(Sentence(start=start, end=end))
            text += "\n"
            boundaries[section.name].append(Boundary(start=bstart, end=len(text)))
        doc.text = text
        doc.sentences = sentences
        doc.boundaries = boundaries


@lru_cache(maxsize=None)
def get_client():
    return Client(base_url=APP_GROBID_URI + "/api", timeout=600)
