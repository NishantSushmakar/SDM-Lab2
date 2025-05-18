import pandas as pd
import numpy as np
import os
import random
from pathlib import Path

# Set random seed to ensure reproducible results
random.seed(42)
np.random.seed(42)

# Set paths
DATA_DIR = Path("../data")
OUTPUT_DIR = Path("../data_generated")
OUTPUT_DIR.mkdir(exist_ok=True)

# Load existing data
def load_csv(filename):
    try:
        return pd.read_csv(DATA_DIR / filename, dtype=str)
    except Exception as e:
        print(f"Unable to load {filename}: {e}")
        return pd.DataFrame()

# Save generated data
def save_csv(df, filename):
    df.to_csv(OUTPUT_DIR / filename, index=False)
    print(f"Saved {filename}, {len(df)} rows")

# Generate unique ID
def generate_id(prefix, index):
    return f"{prefix}_{index:05d}"

print("Starting data generation...")

# 1. Load existing data
authors_df = load_csv("author.csv")
journals_df = load_csv("journal.csv")
volumes_df = load_csv("volume.csv")
events_df = load_csv("event.csv")
editions_df = load_csv("edition.csv")
journal_volumes_df = load_csv("journal_hasVolume_volume.csv")
event_editions_df = load_csv("event_hasEdition_edition.csv")
reviews_df = load_csv("review.csv")
review_relations_df = load_csv("review_relations.csv")

# 2. Generate JournalEditor data
# Randomly select 20% of authors as journal editors
editor_count = int(len(authors_df) * 0.2)
editor_indices = random.sample(range(len(authors_df)), editor_count)

journal_editors = []
for i, idx in enumerate(editor_indices):
    author = authors_df.iloc[idx]
    editor_id = generate_id("editor", i+1)
    name = author.get('name', f"Editor {i+1}")
    # Generate virtual email address
    email = f"{name.lower().replace(' ', '.')}@{random.choice(['university.edu', 'research.org', 'institute.com'])}"
    
    journal_editors.append({
        "editorId": editor_id,
        "name": name,
        "email": email
    })

journal_editors_df = pd.DataFrame(journal_editors)
save_csv(journal_editors_df, "journal_editor.csv")

# 3. Generate ConferenceChair data
# Randomly select 15% of authors as conference chairs (excluding those already selected as editors)
remaining_indices = [i for i in range(len(authors_df)) if i not in editor_indices]
chair_count = int(len(authors_df) * 0.15)
chair_indices = random.sample(remaining_indices, min(chair_count, len(remaining_indices)))

conference_chairs = []
for i, idx in enumerate(chair_indices):
    author = authors_df.iloc[idx]
    chair_id = generate_id("chair", i+1)
    name = author.get('name', f"Chair {i+1}")
    # Generate virtual email address
    email = f"{name.lower().replace(' ', '.')}@{random.choice(['conference.org', 'university.edu', 'institute.com'])}"
    
    conference_chairs.append({
        "chairId": chair_id,
        "name": name,
        "email": email
    })

conference_chairs_df = pd.DataFrame(conference_chairs)
save_csv(conference_chairs_df, "conference_chair.csv")

# 4. Generate Volume and JournalEditor relationships
# Assign one editor to each volume
volume_editor_relations = []
for _, row in volumes_df.iterrows():
    volume_id = row.get('volumeId')
    if volume_id:
        editor_id = random.choice(journal_editors_df['editorId'])
        volume_editor_relations.append({
            "volumeId": volume_id,
            "editorId": editor_id
        })

volume_editor_df = pd.DataFrame(volume_editor_relations)
save_csv(volume_editor_df, "volume_hasJournalEditor_editor.csv")

# 5. Generate Edition and ConferenceChair relationships
# Assign one chair to each edition
edition_chair_relations = []
for _, row in editions_df.iterrows():
    edition_id = row.get('editionId')
    if edition_id:
        chair_id = random.choice(conference_chairs_df['chairId'])
        edition_chair_relations.append({
            "editionId": edition_id,
            "chairId": chair_id
        })

edition_chair_df = pd.DataFrame(edition_chair_relations)
save_csv(edition_chair_df, "edition_hasConferenceChair_chair.csv")

# 6. Generate JournalEditor and Journal relationships
# Each editor can edit 1-3 journals
editor_journal_relations = []
for _, editor in journal_editors_df.iterrows():
    num_journals = random.randint(1, 3)
    journals_sample = journals_df.sample(min(num_journals, len(journals_df)))
    
    for _, journal in journals_sample.iterrows():
        editor_journal_relations.append({
            "editorId": editor['editorId'],
            "journalId": journal['journalId']
        })

editor_journal_df = pd.DataFrame(editor_journal_relations)
save_csv(editor_journal_df, "journalEditor_editsJournal_journal.csv")

# 7. Generate ConferenceChair and Event relationships
# Each chair can be responsible for 1-2 events
chair_event_relations = []
for _, chair in conference_chairs_df.iterrows():
    num_events = random.randint(1, 2)
    events_sample = events_df.sample(min(num_events, len(events_df)))
    
    for _, event in events_sample.iterrows():
        chair_event_relations.append({
            "chairId": chair['chairId'],
            "eventId": event['eventId']
        })

chair_event_df = pd.DataFrame(chair_event_relations)
save_csv(chair_event_df, "conferenceChair_chairsEvent_event.csv")

# 8. Process Review data
# If review.csv exists, use it; otherwise generate review data from review_relations.csv
if 'reviewId' not in review_relations_df.columns:
    # Generate Review instances
    reviews = []
    author_reviewed_review = []
    review_reviews_paper = []
    
    # Transform records from author_reviewed_paper.csv into triples in the new model
    for i, row in review_relations_df.iterrows():
        review_id = generate_id("review", i+1)
        author_id = row.get('authorId')
        paper_id = row.get('paperId')
        comments = row.get('comments', "No comments provided")
        vote = row.get('vote', "0")
        
        # Review instance
        reviews.append({
            "reviewId": review_id,
            "comments": comments,
            "vote": vote
        })
        
        # Author-review relationship
        author_reviewed_review.append({
            "authorId": author_id,
            "reviewId": review_id
        })
        
        # Review-paper relationship
        review_reviews_paper.append({
            "reviewId": review_id,
            "paperId": paper_id
        })
    
    # Save processed data
    reviews_df = pd.DataFrame(reviews)
    save_csv(reviews_df, "review_generated.csv")
    
    author_reviewed_review_df = pd.DataFrame(author_reviewed_review)
    save_csv(author_reviewed_review_df, "author_reviewed_review.csv")
    
    review_reviews_paper_df = pd.DataFrame(review_reviews_paper)
    save_csv(review_reviews_paper_df, "review_reviews_paper.csv")
else:
    # If review.csv already exists in the correct format, process relationship data directly
    # TODO: Implement this logic
    pass

print("Data generation completed!") 