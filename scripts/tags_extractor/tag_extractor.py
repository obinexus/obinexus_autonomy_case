#!/usr/bin/env python3
"""
Tag Extractor for OBINexus Legal Documents
Extracts and organizes tags from PDFs for trie-based searching and DAG proof validation
"""

import os
import re
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Set, Tuple
from pathlib import Path

class LegalTagExtractor:
    """Extract and organize tags from legal documents"""
    
    def __init__(self):
        # Define tag patterns and their categories
        self.tag_patterns = {
            # Housing-related patterns
            'housing_denial': [
                r'housing.*den(y|ied|ial)',
                r'not.*homeless',
                r'accommodation.*refus',
                r'shelter.*reject'
            ],
            'section_202': [
                r'section\s*202',
                r's\.?\s*202',
                r'housing\s*act\s*1996'
            ],
            'homelessness': [
                r'homeless(?:ness)?',
                r'no\s*fixed\s*abode',
                r'rough\s*sleep'
            ],
            
            # Mental health patterns
            'mental_health': [
                r'mental\s*health',
                r'psychiatric',
                r'psychological'
            ],
            'ellingham': [
                r'ellingham',
                r'hospital.*placement',
                r'institutional.*care'
            ],
            'child_protection': [
                r'child.*protection',
                r'under\s*18',
                r'minor.*care',
                r'age(?:d)?\s*1[5-7]'
            ],
            
            # Legal and administrative patterns
            'sar_denial': [
                r'sar.*den(y|ied|ial)',
                r'subject\s*access.*refus',
                r'data.*request.*reject'
            ],
            'discrimination': [
                r'discriminat',
                r'disability.*bias',
                r'unequal.*treatment'
            ],
            'compensation': [
                r'compensat',
                r'damages',
                r'£\d+.*million',
                r'financial.*remedy'
            ],
            
            # System failure patterns
            'entrapment': [
                r'entrap',
                r'circular.*refer',
                r'system.*loop'
            ],
            'negligence': [
                r'negligen',
                r'breach.*duty',
                r'fail.*care'
            ]
        }
        
        # Define date patterns
        self.date_patterns = [
            r'\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})\b',  # DD-MM-YYYY or DD/MM/YYYY
            r'\b(\d{2,4})[-/.](\d{1,2})[-/.](\d{1,2})\b',  # YYYY-MM-DD
            r'\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{2,4})\b',
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{2,4})\b'
        ]
        
        # Location mapping
        self.locations = {
            'thurrock': ['thurrock', 'council', 'borough'],
            'ellingham': ['ellingham', 'hospital'],
            'ak_housing': ['ak', 'housing', 'association']
        }
        
        # Critical evidence markers
        self.critical_markers = [
            'verdict', 'judgment', 'decision', 'ruling',
            'evidence', 'proof', 'exhibit', 'statement'
        ]

    def extract_from_filename(self, filename: str) -> Dict[str, any]:
        """Extract metadata from filename"""
        metadata = {
            'original_filename': filename,
            'normalized_name': self._normalize_filename(filename),
            'tags': set(),
            'extracted_date': None,
            'location': None
        }
        
        # Remove extension for analysis
        name_only = os.path.splitext(filename)[0]
        name_lower = name_only.lower()
        
        # Extract tags from filename
        for tag, patterns in self.tag_patterns.items():
            for pattern in patterns:
                if re.search(pattern, name_lower):
                    metadata['tags'].add(tag)
        
        # Extract date from filename
        for date_pattern in self.date_patterns:
            match = re.search(date_pattern, name_only)
            if match:
                metadata['extracted_date'] = self._parse_date(match)
                break
        
        # Extract location
        for location, keywords in self.locations.items():
            if any(keyword in name_lower for keyword in keywords):
                metadata['location'] = location
                break
        
        # Check for critical evidence
        if any(marker in name_lower for marker in self.critical_markers):
            metadata['tags'].add('critical_evidence')
        
        return metadata
    
    def _normalize_filename(self, filename: str) -> str:
        """Normalize filename for consistent processing"""
        # Remove extension
        name = os.path.splitext(filename)[0]
        # Replace separators with spaces
        name = re.sub(r'[_\-\.]', ' ', name)
        # Remove multiple spaces
        name = re.sub(r'\s+', ' ', name)
        # Trim
        return name.strip()
    
    def _parse_date(self, match) -> str:
        """Parse date from regex match"""
        try:
            groups = match.groups()
            # Handle different date formats
            if len(groups) == 3:
                if groups[1].isdigit():  # DD-MM-YYYY format
                    day, month, year = groups
                    if len(year) == 2:
                        year = '20' + year if int(year) < 50 else '19' + year
                    return f"{day.zfill(2)}-{month.zfill(2)}-{year}"
                else:  # Month name format
                    # Convert month name to number
                    months = {
                        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
                    }
                    day = groups[0]
                    month = months.get(groups[1][:3].lower(), '00')
                    year = groups[2]
                    if len(year) == 2:
                        year = '20' + year if int(year) < 50 else '19' + year
                    return f"{day.zfill(2)}-{month}-{year}"
        except:
            pass
        return None
    
    def analyze_directory(self, directory_path: str) -> Dict[str, any]:
        """Analyze all PDFs in a directory structure"""
        results = {
            'scan_date': datetime.now().isoformat(),
            'base_directory': directory_path,
            'documents': {},
            'tag_index': {},
            'location_index': {},
            'date_index': {},
            'statistics': {
                'total_documents': 0,
                'tagged_documents': 0,
                'dated_documents': 0,
                'critical_documents': 0
            }
        }
        
        # Scan directory recursively
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory_path)
                    
                    # Extract metadata
                    metadata = self.extract_from_filename(file)
                    metadata['relative_path'] = relative_path
                    metadata['category'] = os.path.basename(root)
                    metadata['file_hash'] = self._calculate_file_hash(file_path)
                    
                    # Store document info
                    doc_id = metadata['file_hash'][:12]  # Short hash for ID
                    results['documents'][doc_id] = metadata
                    
                    # Update indices
                    for tag in metadata['tags']:
                        if tag not in results['tag_index']:
                            results['tag_index'][tag] = []
                        results['tag_index'][tag].append(doc_id)
                    
                    if metadata['location']:
                        if metadata['location'] not in results['location_index']:
                            results['location_index'][metadata['location']] = []
                        results['location_index'][metadata['location']].append(doc_id)
                    
                    if metadata['extracted_date']:
                        date_key = metadata['extracted_date'][:7]  # YYYY-MM
                        if date_key not in results['date_index']:
                            results['date_index'][date_key] = []
                        results['date_index'][date_key].append(doc_id)
                    
                    # Update statistics
                    results['statistics']['total_documents'] += 1
                    if metadata['tags']:
                        results['statistics']['tagged_documents'] += 1
                    if metadata['extracted_date']:
                        results['statistics']['dated_documents'] += 1
                    if 'critical_evidence' in metadata['tags']:
                        results['statistics']['critical_documents'] += 1
        
        return results
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file"""
        try:
            hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return "hash_error"
    
    def generate_metadata_files(self, analysis_results: Dict, output_dir: str):
        """Generate metadata.json files for each category"""
        documents_by_category = {}
        
        # Group documents by category
        for doc_id, metadata in analysis_results['documents'].items():
            category = metadata['category']
            if category not in documents_by_category:
                documents_by_category[category] = {}
            
            filename = metadata['original_filename']
            documents_by_category[category][filename] = {
                'doc_id': doc_id,
                'tags': list(metadata['tags']),
                'date': metadata['extracted_date'],
                'location': metadata['location'],
                'hash': metadata['file_hash']
            }
        
        # Write metadata files
        for category, documents in documents_by_category.items():
            category_path = os.path.join(output_dir, category)
            if os.path.exists(category_path):
                metadata_path = os.path.join(category_path, 'metadata.json')
                with open(metadata_path, 'w') as f:
                    json.dump(documents, f, indent=2)
                print(f"Generated metadata for {category}: {len(documents)} documents")
    
    def create_searchable_index(self, analysis_results: Dict) -> Dict:
        """Create enhanced searchable index structure"""
        index = {
            'version': '1.0',
            'created': datetime.now().isoformat(),
            'total_documents': analysis_results['statistics']['total_documents'],
            'tags': {},
            'search_aliases': {},
            'proof_chains': [],
            'critical_documents': []
        }
        
        # Build tag hierarchy
        for tag, doc_ids in analysis_results['tag_index'].items():
            # Get all documents for this tag
            documents = []
            for doc_id in doc_ids:
                doc = analysis_results['documents'][doc_id]
                documents.append({
                    'id': doc_id,
                    'filename': doc['original_filename'],
                    'path': doc['relative_path'],
                    'date': doc['extracted_date'],
                    'location': doc['location']
                })
            
            # Categorize tag
            category = self._get_tag_category(tag)
            if category not in index['tags']:
                index['tags'][category] = {}
            
            index['tags'][category][tag] = {
                'document_count': len(documents),
                'documents': documents
            }
        
        # Create search aliases for common variations
        index['search_aliases'] = {
            'housing_denial': ['housing denial', 'denied housing', 'accommodation refused'],
            'section_202': ['section 202', 's202', 's.202', 'housing act 1996'],
            'ellingham': ['ellingham hospital', 'ellingham placement'],
            'sar': ['subject access request', 'data request', 'sar denial'],
            'compensation': ['damages', 'financial remedy', '181 million']
        }
        
        # Identify proof chains (simplified version)
        if 'housing_denial' in analysis_results['tag_index'] and 'compensation' in analysis_results['tag_index']:
            index['proof_chains'].append({
                'name': 'Housing Denial → Compensation',
                'start_tag': 'housing_denial',
                'end_tag': 'compensation',
                'intermediate_tags': ['discrimination', 'negligence']
            })
        
        # List critical documents
        for doc_id, metadata in analysis_results['documents'].items():
            if 'critical_evidence' in metadata['tags']:
                index['critical_documents'].append({
                    'id': doc_id,
                    'filename': metadata['original_filename'],
                    'tags': list(metadata['tags']),
                    'importance': 'high'
                })
        
        return index
    
    def _get_tag_category(self, tag: str) -> str:
        """Determine category for a tag"""
        category_mapping = {
            'housing': ['housing_denial', 'section_202', 'homelessness'],
            'mental_health': ['mental_health', 'ellingham', 'child_protection'],
            'legal': ['sar_denial', 'discrimination', 'compensation'],
            'system_failure': ['entrapment', 'negligence'],
            'evidence': ['critical_evidence']
        }
        
        for category, tags in category_mapping.items():
            if tag in tags:
                return category
        return 'other'
    
    def generate_report(self, analysis_results: Dict) -> str:
        """Generate human-readable analysis report"""
        report = f"""# Document Tag Analysis Report

**Generated**: {analysis_results['scan_date']}
**Base Directory**: {analysis_results['base_directory']}

## Summary Statistics
- Total Documents: {analysis_results['statistics']['total_documents']}
- Tagged Documents: {analysis_results['statistics']['tagged_documents']}
- Documents with Dates: {analysis_results['statistics']['dated_documents']}
- Critical Evidence Documents: {analysis_results['statistics']['critical_documents']}

## Tag Distribution
"""
        
        # Sort tags by document count
        tag_counts = [(tag, len(docs)) for tag, docs in analysis_results['tag_index'].items()]
        tag_counts.sort(key=lambda x: x[1], reverse=True)
        
        for tag, count in tag_counts:
            category = self._get_tag_category(tag)
            report += f"- **{tag}** ({category}): {count} documents\n"
        
        report += "\n## Location Distribution\n"
        for location, doc_ids in analysis_results['location_index'].items():
            report += f"- **{location}**: {len(doc_ids)} documents\n"
        
        report += "\n## Temporal Distribution\n"
        if analysis_results['date_index']:
            sorted_dates = sorted(analysis_results['date_index'].keys())
            report += f"- Earliest: {sorted_dates[0]}\n"
            report += f"- Latest: {sorted_dates[-1]}\n"
            report += f"- Date range spans: {len(sorted_dates)} months\n"
        
        report += "\n## Critical Evidence\n"
        critical_count = 0
        for doc_id, metadata in analysis_results['documents'].items():
            if 'critical_evidence' in metadata['tags']:
                report += f"- {metadata['original_filename']}\n"
                critical_count += 1
                if critical_count >= 10:  # Limit to first 10
                    report += f"  ... and {analysis_results['statistics']['critical_documents'] - 10} more\n"
                    break
        
        return report


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract tags from legal documents')
    parser.add_argument('directory', help='Directory to analyze')
    parser.add_argument('--output', '-o', default='tag_analysis.json',
                        help='Output file for analysis results')
    parser.add_argument('--generate-metadata', '-m', action='store_true',
                        help='Generate metadata.json files in each category')
    parser.add_argument('--report', '-r', action='store_true',
                        help='Generate human-readable report')
    
    args = parser.parse_args()
    
    # Initialize extractor
    extractor = LegalTagExtractor()
    
    print(f"Analyzing directory: {args.directory}")
    
    # Perform analysis
    results = extractor.analyze_directory(args.directory)
    
    # Save raw results
    with open(args.output, 'w') as f:
        # Convert sets to lists for JSON serialization
        json_results = json.loads(json.dumps(results, default=list))
        json.dump(json_results, f, indent=2)
    print(f"Analysis saved to: {args.output}")
    
    # Generate metadata files if requested
    if args.generate_metadata:
        extractor.generate_metadata_files(results, args.directory)
    
    # Create searchable index
    search_index = extractor.create_searchable_index(results)
    index_path = os.path.join(os.path.dirname(args.output), 'search_index.json')
    with open(index_path, 'w') as f:
        json.dump(search_index, f, indent=2)
    print(f"Search index saved to: {index_path}")
    
    # Generate report if requested
    if args.report:
        report = extractor.generate_report(results)
        report_path = os.path.join(os.path.dirname(args.output), 'tag_analysis_report.md')
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"Report saved to: {report_path}")
    
    # Print summary
    print(f"\nAnalysis Summary:")
    print(f"- Total documents: {results['statistics']['total_documents']}")
    print(f"- Unique tags found: {len(results['tag_index'])}")
    print(f"- Documents with dates: {results['statistics']['dated_documents']}")
    print(f"- Critical evidence: {results['statistics']['critical_documents']}")


if __name__ == "__main__":
    main()
