from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DC, DCTERMS, RDF, RDFS, XSD
from lxml import etree
import urllib.parse

# Создаем граф RDF
g = Graph()

# Определяем пространства имен
SCHEMA = Namespace("http://schema.org/")
WD = Namespace("http://www.wikidata.org/entity/")
HL = Namespace("http://example.org/hedylamarr/")
TEI_NS = "http://www.tei-c.org/ns/1.0"

# Добавляем префиксы для красивого вывода
g.bind("dc", DC)
g.bind("dct", DCTERMS)
g.bind("schema", SCHEMA)
g.bind("wd", WD)
g.bind("hl", HL)

# Парсим TEI-файл
file_path = r"C:\Users\krasn\Desktop\C\tei1.xml"
tree = etree.parse(file_path)
root = tree.getroot()


# Функция для создания безопасных URI
def safe_uri(uri):
    return urllib.parse.quote(uri.replace(" ", "_").replace(":", ""))


# Определяем namespace mapping с явным указанием xml
nsmap = {
    "tei": TEI_NS,
    "xml": "http://www.w3.org/XML/1998/namespace",  # Добавляем стандартный xml namespace
}

# Извлекаем метаданные из TEI Header
tei_header = root.find(".//tei:teiHeader", namespaces=nsmap)
title = tei_header.find(".//tei:title", namespaces=nsmap).text
author = tei_header.find(".//tei:author/tei:persName", namespaces=nsmap).text
publisher = tei_header.find(".//tei:publisher", namespaces=nsmap).text
pub_date = tei_header.find(".//tei:pubDate", namespaces=nsmap).get("when")
pub_place = tei_header.find(".//tei:pubPlace", namespaces=nsmap).text
abstract = tei_header.find(".//tei:abstract/tei:p", namespaces=nsmap).text

# Создаем ресурс для книги
book_uri = HL[safe_uri(title)]
g.add((book_uri, RDF.type, SCHEMA.Book))
g.add((book_uri, DC.title, Literal(title)))
g.add((book_uri, DC.creator, Literal(author)))
g.add((book_uri, DC.publisher, Literal(publisher)))
g.add((book_uri, DC.date, Literal(pub_date, datatype=XSD.gYear)))
g.add((book_uri, SCHEMA.locationCreated, Literal(pub_place)))
g.add((book_uri, SCHEMA.abstract, Literal(abstract)))

# Добавляем ключевые слова
for term in tei_header.findall(".//tei:keywords/tei:term", namespaces=nsmap):
    g.add((book_uri, SCHEMA.keywords, Literal(term.text)))

# Создаем ресурс для Хеди Ламарр (исправленный XPath)
person_elem = tei_header.xpath('.//tei:person[@xml:id="HedyLamarr"]', namespaces=nsmap)[
    0
]
person_uri = HL["Hedy_Lamarr"]
g.add((person_uri, RDF.type, SCHEMA.Person))
g.add((person_uri, SCHEMA.name, Literal("Hedy Lamarr")))

birth = person_elem.find(".//tei:birth", namespaces=nsmap).get("when")
death = person_elem.find(".//tei:death", namespaces=nsmap).get("when")
g.add((person_uri, SCHEMA.birthDate, Literal(birth, datatype=XSD.gYear)))
g.add((person_uri, SCHEMA.deathDate, Literal(death, datatype=XSD.gYear)))

for occupation in person_elem.findall(".//tei:occupation", namespaces=nsmap):
    g.add((person_uri, SCHEMA.jobTitle, Literal(occupation.text)))

# Обрабатываем разделы (div)
for i, div in enumerate(root.findall(".//tei:body/tei:div", namespaces=nsmap)):
    div_type = div.get("type", f"section_{i}")
    chapter_uri = HL[safe_uri(div_type)]

    head = div.find(".//tei:head", namespaces=nsmap)
    title = head.text if head is not None else div_type

    g.add((chapter_uri, RDF.type, SCHEMA.Chapter))
    g.add((chapter_uri, DC.title, Literal(title)))
    g.add((chapter_uri, SCHEMA.position, Literal(i + 1)))
    g.add((book_uri, SCHEMA.hasPart, chapter_uri))

    # Обрабатываем цитаты в разделе
    for j, quote in enumerate(div.findall(".//tei:quote", namespaces=nsmap)):
        quote_uri = HL[f"quote_{safe_uri(div_type)}_{j+1}"]
        pb = quote.xpath("preceding::tei:pb[1]", namespaces=nsmap)
        page = pb[0].get("facs").replace("page", "") if pb else "?"

        # Получаем весь текст цитаты, включая вложенные элементы
        quote_text = " ".join(quote.itertext()).strip()

        g.add((quote_uri, RDF.type, SCHEMA.Quotation))
        g.add((quote_uri, SCHEMA.text, Literal(quote_text)))
        g.add((quote_uri, SCHEMA.pageStart, Literal(page)))
        g.add((quote_uri, SCHEMA.isPartOf, chapter_uri))
        g.add((chapter_uri, SCHEMA.hasPart, quote_uri))

        # Добавляем комментарии если есть
        note = quote.xpath("preceding::tei:note[@type='comment'][1]", namespaces=nsmap)
        if note and note[0].text:
            g.add((quote_uri, SCHEMA.comment, Literal(note[0].text)))

# Добавляем информацию о изобретении
invention_uri = HL["frequency_hopping"]
g.add((invention_uri, RDF.type, SCHEMA.CreativeWork))
g.add((invention_uri, DC.title, Literal("Secret Communication System")))
g.add((invention_uri, SCHEMA.creator, person_uri))
g.add((invention_uri, SCHEMA.dateCreated, Literal("1940s")))
g.add((invention_uri, SCHEMA.about, WD.Q9128))  # Radio communication
g.add(
    (
        invention_uri,
        SCHEMA.description,
        Literal("Frequency-hopping spread spectrum technology"),
    )
)
g.add((invention_uri, SCHEMA.relatedTo, WD.Q1786517))  # Bluetooth

# Сохраняем в TTL формате
output_path = r"C:\Users\krasn\Desktop\C\hedy_lamarr.ttl"
g.serialize(destination=output_path, format="turtle", encoding="utf-8")

print(f"RDF is ready: {output_path}")
