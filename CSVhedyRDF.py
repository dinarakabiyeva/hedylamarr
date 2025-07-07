from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import DC, XSD
import pandas as pd
import urllib.parse

SCHEMA = Namespace("http://schema.org/")
WD = Namespace("http://www.wikidata.org/entity/")
BASE = Namespace("http://example.org/hedy-lamarr/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


g = Graph()
g.bind("dc", DC)
g.bind("xsd", XSD)
g.bind("schema", SCHEMA)
g.bind("wd", WD)
g.bind("foaf", FOAF)


# убираем странные символы
def sanitize_uri(value):

    return urllib.parse.quote(value.replace(" ", "_"))


def wd_or_literal(value):
    if pd.isna(value):
        return None
    value = str(value).strip()
    if value.startswith("Q"):
        return WD[value]
    return Literal(value, datatype=XSD.string)


def ensure_list(value):
    if pd.isna(value):
        return []
    if isinstance(value, list):
        return value
    return [v.strip() for v in str(value).split(";") if v.strip()]


def add_item(row):
    # основной uri
    uri = URIRef(BASE + sanitize_uri(row["URI_Name"]))

    g.add((uri, RDF.type, SCHEMA[sanitize_uri(row["Type"])]))
    g.add((uri, DC.title, Literal(row["Title"], datatype=XSD.string)))

    if not pd.isna(row["Date"]):
        date_str = str(row["Date"])
        if "-" in date_str:
            g.add((uri, DC.date, Literal(date_str, datatype=XSD.string)))
        else:
            g.add((uri, DC.date, Literal(int(date_str), datatype=XSD.gYear)))

    if not pd.isna(row["Description"]):
        g.add((uri, DC.description, Literal(row["Description"], datatype=XSD.string)))

    if not pd.isna(row["Provider"]):
        g.add((uri, DC.publisher, Literal(row["Provider"], datatype=XSD.string)))

    if not pd.isna(row["URL"]):
        g.add((uri, SCHEMA.url, URIRef(row["URL"])))

    if not pd.isna(row["Creator"]):
        for creator in ensure_list(row["Creator"]):
            creator_uri = URIRef(BASE + sanitize_uri(creator))

            g.add((creator_uri, RDF.type, FOAF.Person))
            g.add((creator_uri, FOAF.name, Literal(creator)))

            g.add((uri, DC.creator, creator_uri))

    if not pd.isna(row["Relation"]):
        for relation in ensure_list(row["Relation"]):
            relation_uri = URIRef(BASE + sanitize_uri(relation))

            g.add((relation_uri, RDF.type, SCHEMA.Thing))

            if "Lamarr" in relation or "Antheil" in relation:
                g.add((relation_uri, RDF.type, FOAF.Person))
                g.add((relation_uri, FOAF.name, Literal(relation.replace("_", " "))))

            g.add((uri, SCHEMA.relatedTo, relation_uri))


try:
    df = pd.read_csv(r"C:\Users\krasn\Desktop\C\KnowRepr.csv")
    for _, row in df.iterrows():
        add_item(row)

    g.serialize(destination="hedy_lamarr_knowledge.ttl", format="turtle")
    print("RDF is saved as 'hedy_lamarr_knowledge.ttl'")
except Exception as e:
    print(f"error: {str(e)}")
