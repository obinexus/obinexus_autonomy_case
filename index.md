# OBINexus Legal Case Repository Structure

## Repository Root: `obinexus-legal-case/`

### Directory Structure
```
obinexus-legal-case/
├── .gitignore
├── README.md
├── phase_1_verified/
│   ├── index.md
│   ├── Housing_Denial/
│   │   ├── Nnamdi_Okpala_Not_Homeless.pdf
│   │   └── metadata.json
│   ├── Legal_Verdicts/
│   │   ├── Verdict.pdf
│   │   └── metadata.json
│   ├── Compensation_Claims/
│   │   ├── 2_Million_Pounds_Compensation.pdf
│   │   └── metadata.json
│   └── dag_proof_chain.graphml
├── phase_2_print_index/
│   ├── index.md
│   ├── Housing_Claims/
│   │   └── [Tagged PDFs]
│   ├── NHS_Evidence/
│   │   └── [Tagged PDFs]
│   ├── Care_Records_Ellingham/
│   │   ├── Meeting_Date_12092017.pdf
│   │   ├── Child_Adult_Transition.pdf
│   │   └── metadata.json
│   ├── Police_Interaction/
│   │   └── [Tagged PDFs]
│   ├── System_Entrapment_Proof/
│   │   └── [Tagged PDFs]
│   ├── Chronological_SAR_Proof/
│   │   └── [Tagged PDFs]
│   ├── exhibit_manifest.md
│   └── print_bundle.md
├── phase_3_reform_bills/
│   ├── index.md
│   ├── Civic_Policy_Proposals_Nnamdi_Okpala.pdf
│   ├── draft_bills/
│   │   ├── autonomy_rights_bill.md
│   │   ├── digital_sar_recovery_law.md
│   │   └── neurodivergent_exit_protocol.md
│   └── clause_mapping.json
├── dag_graphs/
│   ├── master_proof_dag.graphml
│   ├── contradiction_nodes.json
│   ├── claim_resolution_paths.json
│   └── visualization/
│       └── proof_flow.svg
├── search_index/
│   ├── master.trie
│   ├── tag_index.json
│   ├── keyword_mappings.json
│   └── search_api.md
└── utilities/
    ├── build_trie.py
    ├── validate_dag.py
    ├── generate_manifest.py
    └── tag_extractor.py
```

## File Descriptions

### `.gitignore`
```
# OS files
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak

# Personal information
personal_notes/
drafts/

# Large binary files (keep PDFs)
*.zip
*.rar

# Editor files
.vscode/
.idea/
```

### `README.md` (Root)
```markdown
# OBINexus Legal Case Archive

## Purpose
Structured legal evidence repository for Nnamdi Michael Okpala v. Thurrock Council
- Primary Claim: £181 million compensatory damages
- Grounds: Housing denial, SAR denial, autism-related discrimination, care violations
- Critical Evidence: Ellingham Hospital placement (ages 15-16) under UK child protection law

## Repository Structure
- **Phase 1**: Verified foundational documents
- **Phase 2**: Print-ready court bundle with chronological indexing
- **Phase 3**: Reform bill proposals based on case outcomes

## Search System
Uses trie-based indexing with DAG proof construction. No circular dependencies.

## Legal Deadlines
- Phase 2 Completion: July 12, 2025
- Court Bundle Submission: July 12, 2025

## Navigation
Use `search_index/master.trie` for keyword lookup
Check `dag_graphs/master_proof_dag.graphml` for proof relationships
```

### `phase_1_verified/index.md`
```markdown
# Phase 1: Verified Documents

## Document Categories
1. **Housing Denial** - Core evidence of systematic housing rejection
2. **Legal Verdicts** - Court decisions supporting claims
3. **Compensation Claims** - Calculated damages documentation

## Key Evidence Chain
- Start: Housing application denial
- Link: Disability discrimination evidence
- Link: SAR request denials
- Result: Verdict establishing liability

## Tags
- `[Tag: Housing_Denial]`
- `[Tag: Legal_Verdict]`
- `[Tag: Compensation_Basis]`
- `[Tag: Section_202_Housing_Act_1996]`
```

### `phase_2_print_index/exhibit_manifest.md`
```markdown
# Court Bundle Exhibit Manifest

## Exhibit Organization
All exhibits tagged with:
- Event Date (DD-MM-YYYY)
- Location (Thurrock/Ellingham/AK Housing)
- Legal Relevance
- Page Numbers

## Exhibit List
### A. Housing Claims
- A1: Not Homeless Declaration [Tag: Housing_Denial]
- A2: Section 202 Application [Tag: Legal_Basis]

### B. NHS Evidence  
- B1: Ellingham Hospital Records [Tag: Child_Mental_Health]
- B2: Transition Meeting 12.09.2017 [Tag: Developmental_Transition]

### C. System Entrapment
- C1: Circular Referrals [Tag: Entrapment_By_Assertion]
- C2: Denial Patterns [Tag: Systematic_Discrimination]
```

### `dag_graphs/master_proof_dag.graphml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <graph id="legal_proof" edgedefault="directed">
    <!-- Root Claims -->
    <node id="claim_housing_denial"/>
    <node id="claim_disability_discrimination"/>
    <node id="claim_child_protection_breach"/>
    
    <!-- Evidence Nodes -->
    <node id="doc_not_homeless"/>
    <node id="doc_ellingham_records"/>
    <node id="doc_verdict"/>
    
    <!-- Proof Edges -->
    <edge source="doc_not_homeless" target="claim_housing_denial"/>
    <edge source="doc_ellingham_records" target="claim_child_protection_breach"/>
    <edge source="claim_child_protection_breach" target="claim_disability_discrimination"/>
    <edge source="claim_disability_discrimination" target="doc_verdict"/>
    
    <!-- No cycles - DAG validated -->
  </graph>
</graphml>
```

### `search_index/tag_index.json`
```json
{
  "housing": {
    "denial": ["Nnamdi_Okpala_Not_Homeless.pdf", "Section_202_Application.pdf"],
    "autonomy": ["Supported_Housing_Exit_Request.pdf"],
    "section_202": ["Housing_Act_1996_Claim.pdf"]
  },
  "mental_health": {
    "ellingham": ["Meeting_Date_12092017.pdf", "Child_Adult_Transition.pdf"],
    "child_rights": ["Under_18_Protection_Breach.pdf"],
    "institution": ["Developmental_Years_15_16.pdf"]
  },
  "sar": {
    "denial": ["SAR_Request_Refused.pdf", "ICO_Complaint.pdf"],
    "data_breach": ["Missing_Records.pdf"]
  },
  "verdict": {
    "liability": ["Verdict.pdf"],
    "compensation": ["2_Million_Pounds_Compensation.pdf"]
  }
}
```

### `search_index/master.trie` (Conceptual Structure)
```
ROOT
├── housing
│   ├── denial → [doc_ids: 1, 2]
│   ├── autonomy → [doc_ids: 3]
│   └── section_202 → [doc_ids: 4]
├── mental
│   └── health
│       ├── ellingham → [doc_ids: 5, 6]
│       └── institution → [doc_ids: 7]
├── sar
│   └── denial → [doc_ids: 8, 9]
└── verdict → [doc_ids: 10, 11]
```

## Implementation Notes

### DAG Validation Rules
1. **No Circular Dependencies**: Each proof must flow forward only
2. **Contradiction Detection**: If document X disproves claim Y, mark as terminal node
3. **Soundness Test**: Every claim must trace to at least one evidence document

### Search Implementation
The trie structure allows O(m) lookup where m is query length. Boolean queries supported:
- `housing AND denial` → Intersection of document sets
- `mental_health OR ellingham` → Union of document sets
- `/section.*202/` → Regex pattern matching

### GitHub Setup Commands
```bash
# Initialize repository
git init obinexus-legal-case
cd obinexus-legal-case

# Create directory structure
mkdir -p phase_{1_verified,2_print_index,3_reform_bills}/{Housing_Claims,NHS_Evidence,Care_Records_Ellingham}
mkdir -p {dag_graphs/visualization,search_index,utilities}

# Add files
git add .
git commit -m "Initial case structure with DAG proof system"

# Set up remote
git remote add origin https://github.com/[username]/obinexus-legal-case.git
git push -u origin main
```
