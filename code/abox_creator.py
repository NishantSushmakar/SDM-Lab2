import pandas as pd
import numpy as np
import os
import random
from pathlib import Path
import rdflib
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD, OWL, FOAF
import re

# Set data directories
DATA_DIR = Path("../data")
GEN_DATA_DIR = Path("../data_generated")
OUTPUT_DIR = Path("../resources")
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize the RDF graph
g = Graph()

# Parse existing TBOX
g.parse("../resources/tbox.ttl", format="turtle")

# Define namespaces
BASE = Namespace("http://example.org/academicworld#")
g.bind("base", BASE)
g.bind("foaf", FOAF)

# Processing functions
def clean_string(s):
    """Clean a string for use in URIs"""
    if not isinstance(s, str):
        return str(s)
    # Replace spaces and special characters
    s = re.sub(r'[^\w\s]', '', s)
    s = re.sub(r'\s+', '_', s)
    return s

def create_uri(entity_type, identifier):
    """Create a URI for an entity"""
    if isinstance(identifier, str):
        clean_id = clean_string(identifier)
    else:
        clean_id = str(identifier)
    return URIRef(BASE + entity_type + "/" + clean_id)

def load_csv(filepath):
    """Load a CSV file as DataFrame"""
    try:
        return pd.read_csv(filepath, dtype=str)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return pd.DataFrame()

# Process Author data
def process_authors():
    print("Processing Authors...")
    count = 0
    df = load_csv(DATA_DIR / "author.csv")
    
    for _, row in df.iterrows():
        author_uri = create_uri("Author", row['authorId'])
        g.add((author_uri, RDF.type, BASE.Author))
        
        if 'name' in row and row['name']:
            g.add((author_uri, FOAF.name, Literal(row['name'], datatype=XSD.string)))
        
        if 'email' in row and row['email']:
            g.add((author_uri, FOAF.mbox, Literal(row['email'], datatype=XSD.string)))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} authors")
    
    print(f"Completed processing {count} authors")

# Process Journal data
def process_journals():
    print("Processing Journals...")
    count = 0
    df = load_csv(DATA_DIR / "journal.csv")
    
    for _, row in df.iterrows():
        journal_uri = create_uri("Journal", row['journalId'])
        g.add((journal_uri, RDF.type, BASE.Journal))
        
        if 'name' in row and row['name']:
            g.add((journal_uri, RDFS.label, Literal(row['name'], datatype=XSD.string)))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} journals")
    
    print(f"Completed processing {count} journals")

# Process Volume data
def process_volumes():
    print("Processing Volumes...")
    count = 0
    df = load_csv(DATA_DIR / "volume.csv")
    
    for _, row in df.iterrows():
        volume_uri = create_uri("Volume", row['volumeId'])
        g.add((volume_uri, RDF.type, BASE.Volume))
        
        if 'number' in row and row['number']:
            g.add((volume_uri, BASE.number, Literal(row['number'], datatype=XSD.integer)))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} volumes")
    
    print(f"Completed processing {count} volumes")

# Process Conference data
def process_events():
    print("Processing Events...")
    count = 0
    df = load_csv(DATA_DIR / "event.csv")
    
    for _, row in df.iterrows():
        event_uri = create_uri("Event", row['eventId'])
        g.add((event_uri, RDF.type, BASE.Event))
        
        if 'name' in row and row['name']:
            g.add((event_uri, RDFS.label, Literal(row['name'], datatype=XSD.string)))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} events")
    
    print(f"Completed processing {count} events")

# Process Edition data
def process_editions():
    print("Processing Editions...")
    count = 0
    df = load_csv(DATA_DIR / "edition.csv")
    
    for _, row in df.iterrows():
        edition_uri = create_uri("Edition", row['editionId'])
        g.add((edition_uri, RDF.type, BASE.Edition))
        
        if 'number' in row and row['number']:
            g.add((edition_uri, BASE.number, Literal(row['number'], datatype=XSD.integer)))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} editions")
    
    print(f"Completed processing {count} editions")

# Process Paper data
def process_papers():
    print("Processing Papers...")
    count = 0
    df = load_csv(DATA_DIR / "paper.csv")
    
    for _, row in df.iterrows():
        paper_uri = create_uri("Paper", row['paperId'])
        g.add((paper_uri, RDF.type, BASE.Paper))
        
        if 'title' in row and row['title']:
            g.add((paper_uri, RDFS.label, Literal(row['title'], datatype=XSD.string)))
        
        if 'year' in row and row['year'] and row['year'] != 'nan':
            g.add((paper_uri, BASE.year, Literal(row['year'], datatype=XSD.integer)))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} papers")
    
    print(f"Completed processing {count} papers")

# Process relationships
def process_paper_authors():
    print("Processing Paper-Author relationships...")
    count = 0
    df = load_csv(DATA_DIR / "paper_hasAuthor_author.csv")
    
    for _, row in df.iterrows():
        paper_uri = create_uri("Paper", row['paperId'])
        author_uri = create_uri("Author", row['authorId'])
        
        g.add((paper_uri, BASE.hasAuthor, author_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} paper-author relationships")
    
    print(f"Completed processing {count} paper-author relationships")

def process_volume_papers():
    print("Processing Volume-Paper relationships...")
    count = 0
    df = load_csv(DATA_DIR / "volume_hasPaper_paper.csv")
    
    for _, row in df.iterrows():
        volume_uri = create_uri("Volume", row['volumeId'])
        paper_uri = create_uri("Paper", row['paperId'])
        
        g.add((volume_uri, BASE.hasPaper, paper_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} volume-paper relationships")
    
    print(f"Completed processing {count} volume-paper relationships")

def process_journal_volumes():
    print("Processing Journal-Volume relationships...")
    count = 0
    df = load_csv(DATA_DIR / "journal_hasVolume_volume.csv")
    
    for _, row in df.iterrows():
        journal_uri = create_uri("Journal", row['journalId'])
        volume_uri = create_uri("Volume", row['volumeId'])
        
        g.add((journal_uri, BASE.hasVolume, volume_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} journal-volume relationships")
    
    print(f"Completed processing {count} journal-volume relationships")

def process_edition_papers():
    print("Processing Edition-Paper relationships...")
    count = 0
    df = load_csv(DATA_DIR / "edition_hasPaper_paper.csv")
    
    for _, row in df.iterrows():
        edition_uri = create_uri("Edition", row['editionId'])
        paper_uri = create_uri("Paper", row['paperId'])
        
        g.add((edition_uri, BASE.hasPaper, paper_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} edition-paper relationships")
    
    print(f"Completed processing {count} edition-paper relationships")

def process_event_editions():
    print("Processing Event-Edition relationships...")
    count = 0
    df = load_csv(DATA_DIR / "event_hasEdition_edition.csv")
    
    for _, row in df.iterrows():
        event_uri = create_uri("Event", row['eventId'])
        edition_uri = create_uri("Edition", row['editionId'])
        
        g.add((event_uri, BASE.hasEdition, edition_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} event-edition relationships")
    
    print(f"Completed processing {count} event-edition relationships")

# Process generated data
def process_journal_editors():
    print("Processing JournalEditor data...")
    count = 0
    df = load_csv(GEN_DATA_DIR / "journal_editor.csv")
    
    for _, row in df.iterrows():
        editor_uri = create_uri("JournalEditor", row['editorId'])
        g.add((editor_uri, RDF.type, BASE.JournalEditor))
        
        if 'name' in row and row['name']:
            g.add((editor_uri, FOAF.name, Literal(row['name'], datatype=XSD.string)))
        
        if 'email' in row and row['email']:
            g.add((editor_uri, FOAF.mbox, Literal(row['email'], datatype=XSD.string)))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} journal editors")
    
    print(f"Completed processing {count} journal editors")

def process_conference_chairs():
    print("Processing ConferenceChair data...")
    count = 0
    df = load_csv(GEN_DATA_DIR / "conference_chair.csv")
    
    for _, row in df.iterrows():
        chair_uri = create_uri("ConferenceChair", row['chairId'])
        g.add((chair_uri, RDF.type, BASE.ConferenceChair))
        
        if 'name' in row and row['name']:
            g.add((chair_uri, FOAF.name, Literal(row['name'], datatype=XSD.string)))
        
        if 'email' in row and row['email']:
            g.add((chair_uri, FOAF.mbox, Literal(row['email'], datatype=XSD.string)))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} conference chairs")
    
    print(f"Completed processing {count} conference chairs")

def process_volume_editors():
    print("Processing Volume-JournalEditor relationships...")
    count = 0
    df = load_csv(GEN_DATA_DIR / "volume_hasJournalEditor_editor.csv")
    
    for _, row in df.iterrows():
        volume_uri = create_uri("Volume", row['volumeId'])
        editor_uri = create_uri("JournalEditor", row['editorId'])
        
        g.add((volume_uri, BASE.hasJournalEditor, editor_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} volume-editor relationships")
    
    print(f"Completed processing {count} volume-editor relationships")

def process_edition_chairs():
    print("Processing Edition-ConferenceChair relationships...")
    count = 0
    df = load_csv(GEN_DATA_DIR / "edition_hasConferenceChair_chair.csv")
    
    for _, row in df.iterrows():
        edition_uri = create_uri("Edition", row['editionId'])
        chair_uri = create_uri("ConferenceChair", row['chairId'])
        
        g.add((edition_uri, BASE.hasConferenceChair, chair_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} edition-chair relationships")
    
    print(f"Completed processing {count} edition-chair relationships")

def process_editor_journals():
    print("Processing JournalEditor-Journal relationships...")
    count = 0
    df = load_csv(GEN_DATA_DIR / "journalEditor_editsJournal_journal.csv")
    
    for _, row in df.iterrows():
        editor_uri = create_uri("JournalEditor", row['editorId'])
        journal_uri = create_uri("Journal", row['journalId'])
        
        g.add((editor_uri, BASE.editsJournal, journal_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} editor-journal relationships")
    
    print(f"Completed processing {count} editor-journal relationships")

def process_chair_events():
    print("Processing ConferenceChair-Event relationships...")
    count = 0
    df = load_csv(GEN_DATA_DIR / "conferenceChair_chairsEvent_event.csv")
    
    for _, row in df.iterrows():
        chair_uri = create_uri("ConferenceChair", row['chairId'])
        event_uri = create_uri("Event", row['eventId'])
        
        g.add((chair_uri, BASE.chairsEvent, event_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} chair-event relationships")
    
    print(f"Completed processing {count} chair-event relationships")

def process_reviews():
    print("Processing Reviews...")
    count = 0
    
    # Try the standard reviews file first
    reviews_df = load_csv(DATA_DIR / "review.csv")
    
    # If standard file doesn't exist or is empty, try the generated one
    if len(reviews_df) == 0:
        reviews_df = load_csv(GEN_DATA_DIR / "review_generated.csv")
    
    for _, row in reviews_df.iterrows():
        review_uri = create_uri("Review", row['reviewId'])
        g.add((review_uri, RDF.type, BASE.Review))
        
        if 'comments' in row and row['comments']:
            g.add((review_uri, BASE.comments, Literal(row['comments'], datatype=XSD.string)))
        
        if 'vote' in row and row['vote']:
            g.add((review_uri, BASE.vote, Literal(row['vote'], datatype=XSD.integer)))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} reviews")
    
    print(f"Completed processing {count} reviews")

def process_author_reviews():
    print("Processing Author-Review relationships...")
    count = 0
    df = load_csv(GEN_DATA_DIR / "author_reviewed_review.csv")
    
    for _, row in df.iterrows():
        author_uri = create_uri("Author", row['authorId'])
        review_uri = create_uri("Review", row['reviewId'])
        
        g.add((author_uri, BASE.reviewed, review_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} author-review relationships")
    
    print(f"Completed processing {count} author-review relationships")

def process_review_papers():
    print("Processing Review-Paper relationships...")
    count = 0
    df = load_csv(GEN_DATA_DIR / "review_reviews_paper.csv")
    
    for _, row in df.iterrows():
        review_uri = create_uri("Review", row['reviewId'])
        paper_uri = create_uri("Paper", row['paperId'])
        
        g.add((review_uri, BASE.reviews, paper_uri))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} review-paper relationships")
    
    print(f"Completed processing {count} review-paper relationships")

# Main process
def create_abox():
    print("Starting ABOX creation process...")
    
    # Process entities
    process_authors()
    process_journals()
    process_volumes()
    process_events()
    process_editions()
    process_papers()
    
    # Process base relationships
    process_paper_authors()
    process_volume_papers()
    process_journal_volumes()
    process_edition_papers()
    process_event_editions()
    
    # Process generated data
    process_journal_editors()
    process_conference_chairs()
    process_volume_editors()
    process_edition_chairs()
    process_editor_journals()
    process_chair_events()
    
    # Process reviews
    process_reviews()
    process_author_reviews()
    process_review_papers()
    
    # Save the results
    output_file = OUTPUT_DIR / "abox.ttl"
    g.serialize(destination=output_file, format="turtle")
    print(f"ABOX has been saved to {output_file}")
    print(f"Total triples: {len(g)}")

if __name__ == "__main__":
    create_abox() 