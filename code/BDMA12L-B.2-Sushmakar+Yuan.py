import pandas as pd
import uuid
from rdflib import Graph, Namespace, Literal, URIRef, XSD
from rdflib.namespace import RDF, RDFS
import os
from pathlib import Path


DATA_DIR = Path("../data")
GEN_DATA_DIR = Path("../data_generated")  # Added generated data directory
OUTPUT_DIR = Path("../resources")
OUTPUT_DIR.mkdir(exist_ok=True)


g = Graph()

# Import TBOX definition
g.parse("../resources/tbox.ttl", format="turtle")

# Define namespaces
RESEARCH = Namespace("http://example.org/research#")
RESOURCE = Namespace("http://example.org/resource/")
g.bind("research", RESEARCH)
g.bind("resource", RESOURCE)


def create_uri(resource_type, identifier):
    return RESOURCE[f"{resource_type}/{str(identifier)}"]


def load_csv(filename, generated=False):
    try:
        if generated:
            return pd.read_csv(GEN_DATA_DIR / filename, dtype=str)
        else:
            return pd.read_csv(DATA_DIR / filename, dtype=str)
    except Exception as e:
        print(f"Warning: Could not load {filename}: {e}")
        return pd.DataFrame()

# Add Paper instances
def add_papers():
    print("Adding Paper instances...")
    papers_df = load_csv("paper.csv")
    
    # Process page numbers from paper_publishedIn_volume.csv
    vol_pages_df = load_csv("paper_publishedIn_volume.csv")
    vol_pages_dict = dict(zip(vol_pages_df['paperId'], vol_pages_df['pages']))
    
    # Process page numbers from paper_publishedIn_edition.csv
    ed_pages_df = load_csv("paper_publishedIn_edition.csv")
    ed_pages_dict = dict(zip(ed_pages_df['paperId'], ed_pages_df['pages']))
    
    count = 0
    for _, row in papers_df.iterrows():
        paper_uri = create_uri("paper", row['paperId'])
        g.add((paper_uri, RDF.type, RESEARCH.Paper))
        g.add((paper_uri, RESEARCH.paper_id, Literal(row['paperId'])))
        
        if pd.notna(row['title']):
            g.add((paper_uri, RESEARCH.title, Literal(row['title'])))
        
        if pd.notna(row['url']):
            g.add((paper_uri, RESEARCH.url, Literal(row['url'])))
        
        if pd.notna(row['abstract']):
            g.add((paper_uri, RESEARCH.abstract, Literal(row['abstract'])))
        
        # Add page information (moved from relationship to Paper attributes)
        if row['paperId'] in vol_pages_dict and pd.notna(vol_pages_dict[row['paperId']]):
            pages = vol_pages_dict[row['paperId']]
            try:
                if '-' in pages:
                    start_page, end_page = pages.split('-')
                    g.add((paper_uri, RESEARCH.start_page, Literal(int(start_page))))
                    g.add((paper_uri, RESEARCH.end_page, Literal(int(end_page))))
            except:
                # Handle invalid page format
                pass
        
        # If page information not found in volume, try from edition
        elif row['paperId'] in ed_pages_dict and pd.notna(ed_pages_dict[row['paperId']]):
            pages = ed_pages_dict[row['paperId']]
            try:
                if '-' in pages:
                    start_page, end_page = pages.split('-')
                    g.add((paper_uri, RESEARCH.start_page, Literal(int(start_page))))
                    g.add((paper_uri, RESEARCH.end_page, Literal(int(end_page))))
            except:
                # Handle invalid page format
                pass
                
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} papers")
    
    print(f"Added a total of {count} papers")

# Add Person class and Author instances
def add_authors():
    print("Adding Author instances...")
    authors_df = load_csv("author.csv")
    count = 0
    for _, row in authors_df.iterrows():
        author_uri = create_uri("author", row['authorId'])
        # Add both Person and Author types
        g.add((author_uri, RDF.type, RESEARCH.Person))
        g.add((author_uri, RDF.type, RESEARCH.Author))
        g.add((author_uri, RESEARCH.author_id, Literal(row['authorId'])))
        
        if pd.notna(row['name']):
            g.add((author_uri, RESEARCH.name, Literal(row['name'])))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} authors")
    
    print(f"Added a total of {count} authors")

# Add JournalEditor instances
def add_journal_editors():
    print("Adding JournalEditor instances...")
    editors_df = load_csv("journal_editor.csv", generated=True)
    count = 0
    
    if len(editors_df) == 0:
        print("Could not find journal_editor.csv, skipping JournalEditor instances")
        return
    
    for _, row in editors_df.iterrows():
        editor_uri = create_uri("editor", row['editorId'])
        # Add both Person and JournalEditor types
        g.add((editor_uri, RDF.type, RESEARCH.Person))
        g.add((editor_uri, RDF.type, RESEARCH.JournalEditor))
        g.add((editor_uri, RESEARCH.editor_id, Literal(row['editorId'])))
        
        if pd.notna(row['name']):
            g.add((editor_uri, RESEARCH.name, Literal(row['name'])))
        
        if pd.notna(row['email']):
            g.add((editor_uri, RESEARCH.email, Literal(row['email'])))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} journal editors")
    
    print(f"Added a total of {count} journal editors")

# Add ConferenceChair instances
def add_conference_chairs():
    print("Adding ConferenceChair instances...")
    chairs_df = load_csv("conference_chair.csv", generated=True)
    count = 0
    
    if len(chairs_df) == 0:
        print("Could not find conference_chair.csv, skipping ConferenceChair instances")
        return
    
    for _, row in chairs_df.iterrows():
        chair_uri = create_uri("chair", row['chairId'])
        # Add both Person and ConferenceChair types
        g.add((chair_uri, RDF.type, RESEARCH.Person))
        g.add((chair_uri, RDF.type, RESEARCH.ConferenceChair))
        g.add((chair_uri, RESEARCH.chair_id, Literal(row['chairId'])))
        
        if pd.notna(row['name']):
            g.add((chair_uri, RESEARCH.name, Literal(row['name'])))
        
        if pd.notna(row['email']):
            g.add((chair_uri, RESEARCH.email, Literal(row['email'])))
        
        count += 1
        if count % 100 == 0:
            print(f"Processed {count} conference chairs")
    
    print(f"Added a total of {count} conference chairs")

# Add Journal instances
def add_journals():
    print("Adding Journal instances...")
    journals_df = load_csv("journal.csv")
    count = 0
    for _, row in journals_df.iterrows():
        journal_uri = create_uri("journal", row['journalId'])
        g.add((journal_uri, RDF.type, RESEARCH.Journal))
        g.add((journal_uri, RESEARCH.journal_id, Literal(row['journalId'])))
        
        if pd.notna(row['name']):
            g.add((journal_uri, RESEARCH.name, Literal(row['name'])))
        
        if pd.notna(row['ISSN']):
            g.add((journal_uri, RESEARCH.issn, Literal(row['ISSN'])))
        
        if pd.notna(row['url']):
            g.add((journal_uri, RESEARCH.url, Literal(row['url'])))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} journals")
    
    print(f"Added a total of {count} journals")

# Add Event instances
def add_events():
    print("Adding Event instances...")
    events_df = load_csv("event.csv")
    count = 0
    for _, row in events_df.iterrows():
        event_uri = create_uri("event", row['eventId'])
        
        # Determine if it's a Conference or Workshop based on type
        if row['type'] == 'Conference':
            g.add((event_uri, RDF.type, RESEARCH.Conference))
        elif row['type'] == 'Workshop':
            g.add((event_uri, RDF.type, RESEARCH.Workshop))
        else:
            g.add((event_uri, RDF.type, RESEARCH.Event))
        
        g.add((event_uri, RESEARCH.event_id, Literal(row['eventId'])))
        
        if pd.notna(row['name']):
            g.add((event_uri, RESEARCH.name, Literal(row['name'])))
        
        if pd.notna(row['ISSN']):
            g.add((event_uri, RESEARCH.issn, Literal(row['ISSN'])))
        
        if pd.notna(row['url']):
            g.add((event_uri, RESEARCH.url, Literal(row['url'])))
        
        count += 1
        if count % 500 == 0:
            print(f"Processed {count} events")
    
    print(f"Added a total of {count} events")

# Add Edition instances
def add_editions():
    print("Adding Edition instances...")
    editions_df = load_csv("edition.csv")
    count = 0
    for _, row in editions_df.iterrows():
        edition_uri = create_uri("edition", row['editionId'])
        g.add((edition_uri, RDF.type, RESEARCH.Edition))
        g.add((edition_uri, RESEARCH.edition_id, Literal(row['editionId'])))
        
        if pd.notna(row['edition']):
            g.add((edition_uri, RESEARCH.edition, Literal(int(float(row['edition'])))))
        
        if pd.notna(row['location']):
            g.add((edition_uri, RESEARCH.location, Literal(row['location'])))
        
        if pd.notna(row['year']):
            g.add((edition_uri, RESEARCH.year, Literal(int(float(row['year'])), datatype=XSD.gYear)))
        
        count += 1
        if count % 500 == 0:
            print(f"Processed {count} editions")
    
    print(f"Added a total of {count} editions")

# Add Volume instances
def add_volumes():
    print("Adding Volume instances...")
    volumes_df = load_csv("volume.csv")
    count = 0
    for _, row in volumes_df.iterrows():
        volume_uri = create_uri("volume", row['volumeId'])
        g.add((volume_uri, RDF.type, RESEARCH.Volume))
        g.add((volume_uri, RESEARCH.volume_id, Literal(row['volumeId'])))
        
        if pd.notna(row['number']):
            g.add((volume_uri, RESEARCH.number, Literal(int(float(row['number'])) if row['number'].replace('.', '', 1).isdigit() else row['number'])))
        
        if pd.notna(row['year']):
            g.add((volume_uri, RESEARCH.year, Literal(int(row['year']), datatype=XSD.gYear)))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} volumes")
    
    print(f"Added a total of {count} volumes")

# Add Keyword instances
def add_keywords():
    print("Adding Keyword instances...")
    keywords_df = load_csv("keyword.csv")
    count = 0
    for _, row in keywords_df.iterrows():
        keyword_uri = create_uri("keyword", row['keywordId'])
        g.add((keyword_uri, RDF.type, RESEARCH.Keyword))
        g.add((keyword_uri, RESEARCH.keyword_id, Literal(row['keywordId'])))
        
        if pd.notna(row['keyword']):
            g.add((keyword_uri, RESEARCH.keyword, Literal(row['keyword'])))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} keywords")
    
    print(f"Added a total of {count} keywords")

# Add Affiliation instances
def add_affiliations():
    print("Adding Affiliation instances...")
    affiliations_df = load_csv("affiliation.csv")
    count = 0
    for _, row in affiliations_df.iterrows():
        affiliation_uri = create_uri("affiliation", row['affId'])
        g.add((affiliation_uri, RDF.type, RESEARCH.Affiliation))
        g.add((affiliation_uri, RESEARCH.affiliation_id, Literal(row['affId'])))
        
        if pd.notna(row['name']):
            g.add((affiliation_uri, RESEARCH.name, Literal(row['name'])))
        
        count += 1
        if count % 500 == 0:
            print(f"Processed {count} affiliations")
    
    print(f"Added a total of {count} affiliations")


def add_reviews():
    print("Adding Review instances...")
    
    reviews_df = load_csv("review_relations.csv")
    count = 0
    for _, row in reviews_df.iterrows():
        
        review_id = f"rev_{row['authorId']}_{row['paperId']}"
        review_uri = create_uri("review", review_id)
        
        g.add((review_uri, RDF.type, RESEARCH.Review))
        g.add((review_uri, RESEARCH.review_id, Literal(review_id)))
        
        if pd.notna(row['comments']):
            g.add((review_uri, RESEARCH.comments, Literal(row['comments'])))
        
        if pd.notna(row['vote']):
            try:
                vote_value = int(row['vote'])
                g.add((review_uri, RESEARCH.vote, Literal(vote_value)))
            except:
                # If vote is not a number, handle as string
                g.add((review_uri, RESEARCH.vote, Literal(row['vote'])))
        
        # Add review relationships
        author_uri = create_uri("author", row['authorId'])
        paper_uri = create_uri("paper", row['paperId'])
        
        g.add((author_uri, RESEARCH.reviewed, review_uri))  # Author reviewed the review
        g.add((review_uri, RESEARCH.reviews, paper_uri))    # Review reviews the paper
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} reviews")
    
    print(f"Added a total of {count} reviews")


def add_volume_has_journal_editor():
    print("Adding Volume-Editor relationships...")
    relations_df = load_csv("volume_hasJournalEditor_editor.csv", generated=True)
    count = 0
    
    if len(relations_df) == 0:
        print("Could not find volume_hasJournalEditor_editor.csv, skipping Volume-Editor relationships")
        return
    
    for _, row in relations_df.iterrows():
        volume_uri = create_uri("volume", row['volumeId'])
        editor_uri = create_uri("editor", row['editorId'])
        
        g.add((volume_uri, RESEARCH.has_journal_editor, editor_uri))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} volume-editor relationships")
    
    print(f"Added a total of {count} volume-editor relationships")


def add_edition_has_conference_chair():
    print("Adding Edition-Chair relationships...")
    relations_df = load_csv("edition_hasConferenceChair_chair.csv", generated=True)
    count = 0
    
    if len(relations_df) == 0:
        print("Could not find edition_hasConferenceChair_chair.csv, skipping Edition-Chair relationships")
        return
    
    for _, row in relations_df.iterrows():
        edition_uri = create_uri("edition", row['editionId'])
        chair_uri = create_uri("chair", row['chairId'])
        
        g.add((edition_uri, RESEARCH.has_conference_chair, chair_uri))
        
        count += 1
        if count % 500 == 0:
            print(f"Processed {count} edition-chair relationships")
    
    print(f"Added a total of {count} edition-chair relationships")


def add_editor_edits_journal():
    print("Adding Editor-Journal relationships...")
    relations_df = load_csv("journalEditor_editsJournal_journal.csv", generated=True)
    count = 0
    
    if len(relations_df) == 0:
        print("Could not find journalEditor_editsJournal_journal.csv, skipping Editor-Journal relationships")
        return
    
    for _, row in relations_df.iterrows():
        editor_uri = create_uri("editor", row['editorId'])
        journal_uri = create_uri("journal", row['journalId'])
        
        g.add((editor_uri, RESEARCH.edits_journal, journal_uri))
        
        count += 1
        if count % 500 == 0:
            print(f"Processed {count} editor-journal relationships")
    
    print(f"Added a total of {count} editor-journal relationships")


def add_chair_chairs_event():
    print("Adding Chair-Event relationships...")
    relations_df = load_csv("conferenceChair_chairsEvent_event.csv", generated=True)
    count = 0
    
    if len(relations_df) == 0:
        print("Could not find conferenceChair_chairsEvent_event.csv, skipping Chair-Event relationships")
        return
    
    for _, row in relations_df.iterrows():
        chair_uri = create_uri("chair", row['chairId'])
        event_uri = create_uri("event", row['eventId'])
        
        g.add((chair_uri, RESEARCH.chairs_event, event_uri))
        
        count += 1
        if count % 500 == 0:
            print(f"Processed {count} chair-event relationships")
    
    print(f"Added a total of {count} chair-event relationships")


def add_author_wrote_paper():
    print("Adding Author-Paper relationships...")
    relations_df = load_csv("author_wrote_paper.csv")
    count = 0
    for _, row in relations_df.iterrows():
        author_uri = create_uri("author", row['authorId'])
        paper_uri = create_uri("paper", row['paperId'])
        
        g.add((author_uri, RESEARCH.wrote, paper_uri))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} author-paper relationships")
    
    print(f"Added a total of {count} author-paper relationships")


def add_paper_corresponded_by_author():
    print("Adding Paper-Corresponding Author relationships...")
    relations_df = load_csv("paper_correspondedBy_author.csv")
    count = 0
    for _, row in relations_df.iterrows():
        paper_uri = create_uri("paper", row['paperId'])
        author_uri = create_uri("author", row['authorId'])
        
        g.add((paper_uri, RESEARCH.corresponded_by, author_uri))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} paper-corresponding author relationships")
    
    print(f"Added a total of {count} paper-corresponding author relationships")


def add_author_affiliated_with_affiliation():
    print("Adding Author-Affiliation relationships...")
    relations_df = load_csv("author_affiliatedWith_affiliation.csv")
    count = 0
    for _, row in relations_df.iterrows():
        author_uri = create_uri("author", row['authorId'])
        affiliation_uri = create_uri("affiliation", row['affId'])
        
        g.add((author_uri, RESEARCH.affiliated_with, affiliation_uri))
        
        count += 1
        if count % 500 == 0:
            print(f"Processed {count} author-affiliation relationships")
    
    print(f"Added a total of {count} author-affiliation relationships")


def add_paper_cited_in_paper():
    print("Adding Paper Citation relationships...")
    relations_df = load_csv("paper_citedIn_paper.csv")
    count = 0
    for _, row in relations_df.iterrows():
        paper_uri = create_uri("paper", row['paperId'])
        citing_paper_uri = create_uri("paper", row['citingPaperId'])
        
        g.add((paper_uri, RESEARCH.cited_in, citing_paper_uri))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} paper citation relationships")
    
    print(f"Added a total of {count} paper citation relationships")


def add_paper_related_to_keyword():
    print("Adding Paper-Keyword relationships...")
    relations_df = load_csv("paper_isRelatedTo_keyword.csv")
    count = 0
    for _, row in relations_df.iterrows():
        paper_uri = create_uri("paper", row['paperId'])
        keyword_uri = create_uri("keyword", row['keywordId'])
        
        g.add((paper_uri, RESEARCH.related_to, keyword_uri))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} paper-keyword relationships")
    
    print(f"Added a total of {count} paper-keyword relationships")


def add_paper_published_in_edition():
    print("Adding Paper-Edition relationships...")
    relations_df = load_csv("paper_publishedIn_edition.csv")
    count = 0
    for _, row in relations_df.iterrows():
        paper_uri = create_uri("paper", row['paperId'])
        edition_uri = create_uri("edition", row['editionId'])
        
        g.add((paper_uri, RESEARCH.published_in, edition_uri))
        
        count += 1
        if count % 500 == 0:
            print(f"Processed {count} paper-edition relationships")
    
    print(f"Added a total of {count} paper-edition relationships")


def add_paper_published_in_volume():
    print("Adding Paper-Volume relationships...")
    relations_df = load_csv("paper_publishedIn_volume.csv")
    count = 0
    for _, row in relations_df.iterrows():
        paper_uri = create_uri("paper", row['paperId'])
        volume_uri = create_uri("volume", row['volumeId'])
        
        g.add((paper_uri, RESEARCH.published_in, volume_uri))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} paper-volume relationships")
    
    print(f"Added a total of {count} paper-volume relationships")


def add_event_has_edition():
    print("Adding Event-Edition relationships...")
    relations_df = load_csv("event_hasEdition_edition.csv")
    count = 0
    for _, row in relations_df.iterrows():
        event_uri = create_uri("event", row['eventId'])
        edition_uri = create_uri("edition", row['editionId'])
        
        g.add((event_uri, RESEARCH.has_edition, edition_uri))
        
        count += 1
        if count % 500 == 0:
            print(f"Processed {count} event-edition relationships")
    
    print(f"Added a total of {count} event-edition relationships")


def add_journal_has_volume():
    print("Adding Journal-Volume relationships...")
    relations_df = load_csv("journal_hasVolume_volume.csv")
    count = 0
    for _, row in relations_df.iterrows():
        journal_uri = create_uri("journal", row['journalId'])
        volume_uri = create_uri("volume", row['volumeId'])
        
        g.add((journal_uri, RESEARCH.has_volume, volume_uri))
        
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count} journal-volume relationships")
    
    print(f"Added a total of {count} journal-volume relationships")


def main():
    print("Starting ABOX creation...")
    
    # Add entities
    add_papers()
    add_authors()
    add_journal_editors()  
    add_conference_chairs()  
    add_journals()
    add_events()
    add_editions()
    add_volumes()
    add_keywords()
    add_affiliations()
    add_reviews()
    
    # Add relationships
    add_author_wrote_paper()
    add_paper_corresponded_by_author()
    add_author_affiliated_with_affiliation()
    add_paper_cited_in_paper()
    add_paper_related_to_keyword()
    add_paper_published_in_edition()
    add_paper_published_in_volume()
    add_event_has_edition()
    add_journal_has_volume()
    
    
    add_volume_has_journal_editor()  
    add_edition_has_conference_chair()  
    add_editor_edits_journal()  
    add_chair_chairs_event() 
    

    # Save ABOX in RDFS format
    output_file = OUTPUT_DIR / "abox.ttl"
    print(f"Saving ABOX to {output_file}...")
    g.serialize(destination=str(output_file), format="turtle")
    
    # Print statistics
    print("\n==== ABOX Statistics ====")
    class_counts = {}
    for cls in [RESEARCH.Paper, RESEARCH.Person, RESEARCH.Author, RESEARCH.JournalEditor, RESEARCH.ConferenceChair,
                RESEARCH.Journal, RESEARCH.Conference, RESEARCH.Workshop, RESEARCH.Edition, 
                RESEARCH.Volume, RESEARCH.Keyword, RESEARCH.Affiliation, RESEARCH.Review]:
        count = len(list(g.subjects(RDF.type, cls)))
        class_name = cls.split('#')[-1]
        class_counts[class_name] = count
        print(f"Class {class_name}: {count} instances")
    
    property_counts = {}
    for prop in [RESEARCH.wrote, RESEARCH.corresponded_by, RESEARCH.cited_in,
                 RESEARCH.related_to, RESEARCH.published_in, RESEARCH.has_edition,
                 RESEARCH.has_volume, RESEARCH.affiliated_with, RESEARCH.reviewed,
                 RESEARCH.reviews, RESEARCH.has_journal_editor, RESEARCH.has_conference_chair,
                 RESEARCH.edits_journal, RESEARCH.chairs_event]:
        count = len(list(g.triples((None, prop, None))))
        prop_name = prop.split('#')[-1]
        property_counts[prop_name] = count
        print(f"Relationship {prop_name}: {count} triples")
    
    total_triples = len(g)
    print(f"\nTotal number of triples: {total_triples}")
    
    # Save statistics to JSON file
    import json
    stats = {
        "classes": class_counts,
        "properties": property_counts,
        "total_triples": total_triples
    }
    with open(OUTPUT_DIR / "abox_stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    
    print("ABOX creation completed!")

if __name__ == "__main__":
    main() 