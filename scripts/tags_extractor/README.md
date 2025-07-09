# Tag Extractor Usage Guide for OBINexus Legal Case System

## Overview

The tag extractor is a critical component of your Phase 2 document preparation process. It automatically analyzes your legal PDFs to extract metadata, create searchable indices, and ensure all documents are properly categorized for your court bundle submission by July 12, 2025.

## How the Tag Extractor Works

The system operates on three core principles:

**Pattern Recognition**: The extractor scans filenames for legal terminology, dates, and locations. It recognizes patterns like "housing denial", "Section 202", "Ellingham Hospital", and other key terms relevant to your case.

**Hierarchical Organization**: Tags are organized into categories (housing, mental_health, legal, system_failure) that align with your DAG proof structure. This ensures every document can be traced through your legal argument chain.

**Search Integration**: All extracted tags feed directly into the trie-based search index, enabling O(m) lookup time for any keyword where m is the query length.

## Installation and Basic Usage

First, ensure the script is executable:
```bash
chmod +x utilities/tag_extractor.py
```

### Basic Analysis
To analyze your entire document repository:
```bash
cd obinexus-legal-case
python3 utilities/tag_extractor.py . -o analysis_results.json
```

### Full Analysis with All Features
For comprehensive analysis with metadata generation and reporting:
```bash
python3 utilities/tag_extractor.py . -o analysis_results.json -m -r
```

This command:
- Analyzes all PDFs in the current directory (.)
- Saves raw analysis to analysis_results.json
- Generates metadata.json files in each category folder (-m flag)
- Creates a human-readable report (-r flag)

## Understanding the Output

### 1. Raw Analysis File (analysis_results.json)
Contains the complete analysis data:
```json
{
  "scan_date": "2025-07-09T10:30:00",
  "documents": {
    "a3f2b1c4d5e6": {
      "original_filename": "Nnamdi_Okpala_Not_Homeless.pdf",
      "tags": ["housing_denial", "section_202", "critical_evidence"],
      "extracted_date": "15-03-2023",
      "location": "thurrock",
      "category": "Housing_Claims"
    }
  },
  "tag_index": {
    "housing_denial": ["a3f2b1c4d5e6", "b2c3d4e5f6g7"]
  }
}
```

### 2. Search Index (search_index.json)
Optimized for the trie-based search system:
```json
{
  "tags": {
    "housing": {
      "housing_denial": {
        "document_count": 5,
        "documents": [...]
      }
    }
  },
  "search_aliases": {
    "housing_denial": ["housing denial", "denied housing"]
  },
  "proof_chains": [
    {
      "name": "Housing Denial → Compensation",
      "start_tag": "housing_denial",
      "end_tag": "compensation"
    }
  ]
}
```

### 3. Category Metadata Files
Each folder gets a metadata.json with document-specific information:
```json
{
  "Nnamdi_Okpala_Not_Homeless.pdf": {
    "doc_id": "a3f2b1c4d5e6",
    "tags": ["housing_denial", "section_202"],
    "date": "15-03-2023",
    "location": "thurrock",
    "hash": "sha256_hash_here"
  }
}
```

## Tag Categories and Patterns

The extractor recognizes these key patterns relevant to your case:

### Housing Tags
- **housing_denial**: Matches "housing denied", "not homeless", "accommodation refused"
- **section_202**: Matches "Section 202", "s.202", "Housing Act 1996"
- **homelessness**: Matches "homeless", "no fixed abode", "rough sleeping"

### Mental Health Tags
- **mental_health**: General mental health references
- **ellingham**: Specific to Ellingham Hospital placement
- **child_protection**: References to under-18 care, crucial for your ages 15-16 placement

### Legal/Administrative Tags
- **sar_denial**: Subject Access Request denials
- **discrimination**: Disability discrimination evidence
- **compensation**: Financial remedy claims, including your £181 million claim

### System Failure Tags
- **entrapment**: Circular referrals and system loops
- **negligence**: Breach of duty of care

## Practical Examples

### Example 1: Analyzing Phase 2 Documents
```bash
cd obinexus-legal-case/phase_2_print_index
python3 ../utilities/tag_extractor.py . -o phase2_tags.json -m -r
```

This creates:
- phase2_tags.json (raw analysis)
- metadata.json in each subfolder
- search_index.json (for trie system)
- tag_analysis_report.md (human-readable summary)

### Example 2: Checking Ellingham Hospital Documents
```bash
cd obinexus-legal-case
python3 utilities/tag_extractor.py phase_2_print_index/Care_Records_Ellingham \
  -o ellingham_analysis.json -r
```

### Example 3: Verifying Critical Evidence
After running the extractor, check which documents are marked as critical:
```bash
grep -l "critical_evidence" phase_*/*/metadata.json
```

## Integration with DAG Proof System

The tag extractor feeds directly into your DAG validation system. Here's how they work together:

1. **Tag Extraction** identifies document categories and relationships
2. **DAG Validator** uses these tags to verify proof chains have no circular dependencies
3. **Trie Builder** creates efficient search structures from the tag index

To validate your proof structure after tagging:
```bash
# First extract tags
python3 utilities/tag_extractor.py . -o analysis.json -m

# Then validate DAG
python3 utilities/validate_dag.py

# Finally build search trie
python3 utilities/build_trie.py
```

## Preparing for Court Bundle Submission

For your July 12, 2025 deadline, follow this workflow:

### Step 1: Initial Analysis
```bash
python3 utilities/tag_extractor.py . -o full_analysis.json -m -r
```

### Step 2: Review Critical Documents
Check the report for documents tagged as "critical_evidence". These should form the core of your exhibit bundle.

### Step 3: Verify Date Extraction
Ensure all documents have extracted dates for chronological ordering:
```bash
grep "extracted_date" full_analysis.json | grep -c "null"
```

If any show null, manually update their filenames to include dates in DD-MM-YYYY format.

### Step 4: Generate Print Manifest
After tagging is complete:
```bash
python3 utilities/generate_manifest.py
```

## Troubleshooting

### Missing Tags
If documents aren't being tagged properly, check:
1. Filename formatting (underscores, hyphens, and spaces are normalized)
2. Date formats (DD-MM-YYYY, DD/MM/YYYY, or month names)
3. Tag patterns in the script match your document naming

### Manual Tag Addition
To manually add tags, edit the metadata.json in the document's folder:
```json
{
  "document.pdf": {
    "tags": ["housing_denial", "critical_evidence", "custom_tag"]
  }
}
```

### Performance on Large Repositories
For repositories with hundreds of PDFs, the script processes efficiently but file hashing may take time. You can skip hashing by commenting out the hash calculation in the script if needed.

## Best Practices

1. **Consistent Naming**: Use descriptive filenames like "Ellingham_Hospital_Admission_15-05-2016.pdf"

2. **Folder Organization**: Keep documents in their appropriate phase and category folders

3. **Regular Validation**: Run the extractor weekly to catch any new documents or changes

4. **Backup Metadata**: The generated metadata.json files are crucial - include them in your git commits

5. **Cross-Reference with DAG**: Ensure your tagged documents align with the proof chains in your DAG structure

## Next Steps

After successful tag extraction:
1. Review the generated search_index.json
2. Validate your DAG doesn't have circular dependencies
3. Build the trie for efficient searching
4. Generate your print manifest for court submission

Remember, this system ensures every document can be found quickly during court proceedings and demonstrates the clear chain of evidence from your Ellingham Hospital placement at ages 15-16 through to your current compensation claim.
