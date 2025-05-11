from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import RDF, RDFS, XSD
# Create a new RDF graph
g = Graph()
# Define namespaces
RESEARCH = Namespace("http://example.org/research#")
g.bind("research", RESEARCH)

# Define classes with their labels and comments
classes = [
    ("Paper", "A scientific or academic paper", "A document containing research findings or scholarly work"),
    ("Author", "A person who writes papers", "An individual who contributes to academic publications"),
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

# Define object properties with their labels and comments
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
    ("reviews", "Review", "Paper", "Indicates paper review", "Links a review to the paper it reviews")
]

# Define data properties with their labels and comments
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
    ("vote", "Review", XSD.integer, "Review vote", "Numerical rating in the review")
]

# Add classes with labels and comments
for class_name, label, comment in classes:
    g.add((RESEARCH[class_name], RDF.type, RDFS.Class))
    g.add((RESEARCH[class_name], RDFS.label, Literal(label)))
    g.add((RESEARCH[class_name], RDFS.comment, Literal(comment)))

# Add subclass relationships
g.add((RESEARCH.Conference, RDFS.subClassOf, RESEARCH.Event))
g.add((RESEARCH.Workshop, RDFS.subClassOf, RESEARCH.Event))

# Add object properties with labels and comments
for prop_name, domain, range, label, comment in object_properties:
    prop = RESEARCH[prop_name]
    g.add((prop, RDF.type, RDF.Property))
    g.add((prop, RDFS.domain, RESEARCH[domain]))
    g.add((prop, RDFS.range, RESEARCH[range]))
    g.add((prop, RDFS.label, Literal(label)))
    g.add((prop, RDFS.comment, Literal(comment)))

# Add data properties with labels and comments
for prop_name, domain, range_type, label, comment in data_properties:
    prop = RESEARCH[prop_name]
    g.add((prop, RDF.type, RDF.Property))
    g.add((prop, RDFS.domain, RESEARCH[domain]))
    g.add((prop, RDFS.range, range_type))
    g.add((prop, RDFS.label, Literal(label)))
    g.add((prop, RDFS.comment, Literal(comment)))

# Add some additional constraints and documentation
g.add((RESEARCH.Review, RDFS.comment, Literal("A review of a paper with comments and vote")))
g.add((RESEARCH.comments, RDFS.comment, Literal("The textual content of a review")))
g.add((RESEARCH.vote, RDFS.comment, Literal("Numerical rating given in a review")))

g.serialize(destination="../resources/tbox.ttl", format="turtle")
print("Enhanced ontology has been created and saved to tbox.ttl")