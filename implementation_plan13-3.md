# Πλάνο Αυτοματοποίησης Μνήμης & Ανάλυσης Bugs

Αυτό το πλάνο περιγράφει πώς θα διατηρούμε τη μνήμη του Orion AI ενημερωμένη αυτόματα και τις διορθώσεις που προτείνω για το project Ippokampos.

## Proposed Changes

### [Memory Module]

#### [MODIFY] [ingest_project.py](file:///C:/code/orion_memory/ingest_project.py)
Βελτίωση του script ώστε να αγνοεί φακέλους βιβλιοθηκών (όπως `.venv`, `node_modules`, `build`) και να εστιάζει στον πηγαίο κώδικα.

#### [NEW] [automation_setup.md](file:///C:/code/orion_memory/automation_setup.md)
Οδηγίες για την εγκατάσταση ενός **Git Hook** που θα εκτελεί το ingestion αυτόματα μετά από κάθε commit.

#### [MODIFY] [requirements.txt](file:///C:/code/orion_memory/requirements.txt)
Προσθήκη της βιβλιοθήκης `streamlit` για τη δημιουργία του Dashboard.

#### [NEW] [dashboard.py](file:///C:/code/orion_memory/dashboard.py)
Δημιουργία ενός διαδραστικού UI με Streamlit που περιλαμβάνει:
- **Search Bar**: Αναζήτηση στη ChromaDB.
- **Memory Browser**: Προβολή όλων των εγγραφών.
- **Status Panel**: Κατάσταση της βάσης και σύνολο chunks.
- **Add Memory**: Χειροκίνητη προσθήκη πληροφοριών.

### [Ippokampos Project]

#### [BUG REPORT] Session & Payment Indexes
Εντοπίστηκε ανάγκη για σύνθετα indexes στη Firestore στα παρακάτω σημεία:
- **Sessions**: Φίλτρο `trainerId` + Ταξινόμηση `startTime` (DESC).
- **Payments**: Φίλτρο `recordedBy` + Ταξινόμηση [date](file:///C:/code/orion_memory/memory_manager.py#71-82) (DESC).

## Verification Plan

### Automated Tests
- Εκτέλεση του [test_memory.py](file:///C:/code/orion_memory/test_memory.py) για επιβεβαίωση ότι η μνήμη "θυμάται" τα νέα αρχεία του Ippokampos.

### Manual Verification
- Έλεγχος του [memory_log.json](file:///C:/code/orion_memory/memory_log.json) μετά από μια δοκιμαστική αλλαγή στον κώδικα για να δούμε αν το Git hook λειτούργησε.
