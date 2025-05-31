from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import RDF, RDFS, XSD

g = Graph()

RESEARCH = Namespace("http://example.org/research#")
g.bind("research", RESEARCH)


classes = [
    ("Person", "A person involved in research", "A human being who may be an author, journal editor, or conference chair of papers or events"),
    ("Paper", "A scientific or academic paper", "A document containing research findings or scholarly work"),
    ("Author", "A person who writes papers", "An individual who contributes to academic publications"),
    ("JournalEditor", "A person who edits journals", "An individual who edits academic journals and their volumes"),
    ("ConferenceChair", "A person who chairs conferences", "An individual who chairs or leads academic events such as conferences"),
    ("Journal", "A periodical publication", "A regular publication containing academic articles"),
    ("Edition", "A specific instance of a publication", "A particular version or issue of a publication"),
    ("Event", "An academic gathering", "A conference or workshop"),
    ("Conference", "A formal academic conference", "A large academic gathering for presenting research"),
    ("Workshop", "A focused academic workshop", "A smaller, specialized academic gathering"),
    ("Volume", "A collection of papers", "A bound collection of academic papers"),
    ("Keyword", "A topic identifier", "A term used to categorize research"),
    ("Affiliation", "An institution", "An organization or institution associated with authors"),
    ("Review", "A paper review", "An evaluation of a research paper")
]


object_properties = [
    ("wrote", "Author", "Paper", "Indicates authorship", "Links an author to papers they have written"),
    ("corresponded_by", "Paper", "Author", "Indicates correspondence", "Links a paper to its corresponding author"),
    ("cited_in", "Paper", "Paper", "Indicates citation", "Links a paper to papers it cites"),
    ("related_to", "Paper", "Keyword", "Indicates topic relation", "Links a paper to its keywords"),
    ("published_in", "Paper", "Edition", "Indicates publication venue", "Links a paper to its publication edition"),
    ("has_edition", "Event", "Edition", "Indicates event edition", "Links an event to its editions"),
    ("has_volume", "Journal", "Volume", "Indicates journal volume", "Links a journal to its volumes"),
    ("affiliated_with", "Author", "Affiliation", "Indicates institutional affiliation", "Links an author to their institution"),
    ("reviewed", "Author", "Review", "Indicates review authorship", "Links an author to reviews they have written"),
    ("reviews", "Review", "Paper", "Indicates paper review", "Links a review to the paper it reviews"),
    ("has_journal_editor", "Volume", "JournalEditor", "Has journal editor", "Links a volume to its journal editor"),
    ("has_conference_chair", "Edition", "ConferenceChair", "Has conference chair", "Links an event to its conference chair"),
    ("edits_journal", "JournalEditor", "Journal", "Edits journal", "Links a journal editor to the journals they edit"),
    ("chairs_event", "ConferenceChair", "Event", "Chairs event", "Links a conference chair to the events they chair")
]


data_properties = [
    ("paper_id", "Paper", XSD.string, "Paper identifier", "Unique identifier for a paper"),
    ("title", "Paper", XSD.string, "Paper title", "The title of the paper"),
    ("abstract", "Paper", XSD.string, "Paper abstract", "A summary of the paper's content"),
    ("url", "Paper", XSD.string, "Paper URL", "Web address of the paper"),
    ("start_page", "Paper", XSD.integer, "Starting page", "First page number of the paper"),
    ("end_page", "Paper", XSD.integer, "Ending page", "Last page number of the paper"),
    ("author_id", "Author", XSD.string, "Author identifier", "Unique identifier for an author"),
    ("name", "Author", XSD.string, "Author name", "Full name of the author"),
    ("journal_id", "Journal", XSD.string, "Journal identifier", "Unique identifier for a journal"),
    ("name", "Journal", XSD.string, "Journal name", "Name of the journal"),
    ("issn", "Journal", XSD.string, "ISSN", "International Standard Serial Number"),
    ("url", "Journal", XSD.string, "Journal URL", "Web address of the journal"),
    ("edition_id", "Edition", XSD.string, "Edition identifier", "Unique identifier for an edition"),
    ("edition", "Edition", XSD.integer, "Edition number", "Numerical identifier for the edition"),
    ("year", "Edition", XSD.gYear, "Publication year", "Year of publication"),
    ("location", "Edition", XSD.string, "Event location", "Location where the event took place"),
    ("event_id", "Event", XSD.string, "Event identifier", "Unique identifier for an event"),
    ("name", "Event", XSD.string, "Event name", "Name of the event"),
    ("issn", "Event", XSD.string, "Event ISSN", "International Standard Serial Number for the event"),
    ("url", "Event", XSD.string, "Event URL", "Web address of the event"),
    ("volume_id", "Volume", XSD.string, "Volume identifier", "Unique identifier for a volume"),
    ("number", "Volume", XSD.integer, "Volume number", "Numerical identifier for the volume"),
    ("year", "Volume", XSD.gYear, "Volume year", "Year of the volume"),
    ("keyword_id", "Keyword", XSD.string, "Keyword identifier", "Unique identifier for a keyword"),
    ("keyword", "Keyword", XSD.string, "Keyword text", "The actual keyword term"),
    ("affiliation_id", "Affiliation", XSD.string, "Affiliation identifier", "Unique identifier for an affiliation"),
    ("name", "Affiliation", XSD.string, "Affiliation name", "Name of the institution"),
    ("review_id", "Review", XSD.string, "Review identifier", "Unique identifier for a review"),
    ("comments", "Review", XSD.string, "Review comments", "Textual content of the review"),
    ("vote", "Review", XSD.integer, "Review vote", "Numerical rating in the review"),
    ("editor_id", "JournalEditor", XSD.string, "Editor identifier", "Unique identifier for a journal editor"),
    ("name", "JournalEditor", XSD.string, "Editor name", "Full name of the journal editor"),
    ("email", "JournalEditor", XSD.string, "Editor email", "Email address of the journal editor"),
    ("chair_id", "ConferenceChair", XSD.string, "Chair identifier", "Unique identifier for a conference chair"),
    ("name", "ConferenceChair", XSD.string, "Chair name", "Full name of the conference chair"),
    ("email", "ConferenceChair", XSD.string, "Chair email", "Email address of the conference chair")
]


for class_name, label, comment in classes:
    g.add((RESEARCH[class_name], RDF.type, RDFS.Class))
    g.add((RESEARCH[class_name], RDFS.label, Literal(label)))
    g.add((RESEARCH[class_name], RDFS.comment, Literal(comment)))


g.add((RESEARCH.Author, RDFS.subClassOf, RESEARCH.Person))
g.add((RESEARCH.JournalEditor, RDFS.subClassOf, RESEARCH.Person))
g.add((RESEARCH.ConferenceChair, RDFS.subClassOf, RESEARCH.Person))
g.add((RESEARCH.Conference, RDFS.subClassOf, RESEARCH.Event))
g.add((RESEARCH.Workshop, RDFS.subClassOf, RESEARCH.Event))


for prop_name, domain, range, label, comment in object_properties:
    prop = RESEARCH[prop_name]
    g.add((prop, RDF.type, RDF.Property))
    g.add((prop, RDFS.domain, RESEARCH[domain]))
    g.add((prop, RDFS.range, RESEARCH[range]))
    g.add((prop, RDFS.label, Literal(label)))
    g.add((prop, RDFS.comment, Literal(comment)))


for prop_name, domain, range_type, label, comment in data_properties:
    prop = RESEARCH[prop_name]
    g.add((prop, RDF.type, RDF.Property))
    g.add((prop, RDFS.domain, RESEARCH[domain]))
    g.add((prop, RDFS.range, range_type))
    g.add((prop, RDFS.label, Literal(label)))
    g.add((prop, RDFS.comment, Literal(comment)))



# Convert to RDFS format
g.serialize(destination="../resources/tbox.ttl", format="turtle")
print("Ontology has been converted to RDFS format and saved to tbox.rdfs")