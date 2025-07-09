# OBINexus Legal Case Archive

## Case: Nnamdi Michael Okpala v. Thurrock Council

### Primary Claim
- **Amount**: £181 million compensatory damages
- **Grounds**: Housing denial, SAR denial, autism-related discrimination, care violations
- **Critical Evidence**: Ellingham Hospital placement (ages 15-16) under UK child protection law

### Repository Structure
This repository uses a Directed Acyclic Graph (DAG) proof system with trie-based search indexing.

#### Phase Structure
- **Phase 1**: Verified foundational documents (Complete)
- **Phase 2**: Print-ready court bundle with chronological indexing (Active)
- **Phase 3**: Reform bill proposals based on case outcomes (Planning)

### Key Dates
- **Phase 2 Completion**: July 12, 2025
- **Court Bundle Submission**: July 12, 2025

### Navigation Guide
1. Use `search_index/master.trie` for keyword-based document lookup
2. Check `dag_graphs/master_proof_dag.graphml` for proof relationships
3. Review `phase_2_print_index/exhibit_manifest.md` for court bundle organization

### Document Tags
All documents are tagged with:
- Event Date (DD-MM-YYYY)
- Location (e.g., Thurrock, Ellingham, AK Housing)
- Legal relevance tags in format `[Tag: Category_Subcategory]`

### Search System
The repository implements:
- Trie-based keyword indexing for O(m) lookup time
- DAG validation to prevent circular proof dependencies
- Boolean search operators (AND, OR)
- Regex pattern matching for complex queries

### Compliance
All documents must be:
- Print-ready PDF format
- Tagged with appropriate metadata
- Linked in the DAG proof structure
- Indexed in the search trie
