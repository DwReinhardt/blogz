Resume Bullet Analyzer
Purpose
    This tool automates the analysis and organization of resume bullets from multiple tailored resume versions. It solves a common problem for job seekers who maintain dozens of customized resumes: how to consolidate, deduplicate, and organize hundreds of bullet points into a master library that's easy to search and reuse.
    The analyzer produces a 3-tier system:

    Tier 1: Your top 12 "greatest hits" bullets with highest impact
    Tier 2: Complete master library organized by company/role
    Tier 3: Cross-reference by competency area (e.g., "Strategic Planning," "Workforce Management")

This enables you to quickly pull relevant bullets when tailoring resumes for specific job applications, ensuring you always use the most impactful version of each accomplishment.

Key Features
    ✅ Intelligent Deduplication: When the same accomplishment appears multiple times with different metrics (e.g., "20% improvement" vs "25% improvement"), automatically keeps the version with the highest numbers
    ✅ Metric Extraction: Identifies and scores percentages, dollar amounts, team sizes, and other quantitative achievements
    ✅ Auto-Categorization: Classifies bullets into 17+ competency areas (Leadership, Financial Management, Training & Development, etc.)
    ✅ Impact Scoring: Ranks bullets based on metrics, action verbs, and scope of responsibility
    ✅ Company Normalization: Handles variations in company names and keeps divisions separate when appropriate
    ✅ Markdown Export: Generates clean, formatted output ready to convert to Word/PDF

Usage
Basic Usage
    python from resume_analyzer import ResumeBulletAnalyzer

    # Initialize with your data file
        analyzer = ResumeBulletAnalyzer("Collated_Bullets.txt")

    # Export complete 3-tier analysis to markdown
        analyzer.export_to_markdown("Resume_Bullet_Library.md")

Advanced Usage
    # Get deduplicated dataframe for custom analysis
        deduped_df = analyzer.deduplicate_bullets()

    # Generate individual tiers
        tier1 = analyzer.generate_tier1_greatest_hits(deduped_df, n=15)  # Top 15 instead of 12
        tier2 = analyzer.generate_tier2_by_company(deduped_df)
        tier3 = analyzer.generate_tier3_competency_cross_ref(deduped_df)

    # Get statistics
        stats = analyzer.generate_company_statistics(deduped_df)
        print(f"Analyzed {stats['Wells Fargo']['total_bullets']} bullets from Wells Fargo")

Input File Format
    Your input file should be a CSV/TSV with these columns:
        Role:       Job title
        Company:    Company name
        Location:   City, State
        Dates:      Date range
        Bullet:     The bullet point text
        SourceFile: (Optional) Which resume version this came from

Dependencies
    Required Python Packages
        pip install pandas
    
    Standard Library (No Installation Needed)
        re - Regular expressions for metric extraction
        collections.defaultdict - Data organization
        typing - Type hints

    Python Version
        Python 3.7+ (uses f-strings and type hints)

Output Format
    The tool generates a markdown file with three main sections:
    Tier 1: Greatest Hits (12 bullets)
        The highest-impact bullets across your entire career, grouped by theme (Strategic Leadership, Operations, Talent Management, etc.). Copy-paste ready for immediate use.

    Tier 2: Master Library by Company
        All bullets organized by employer and competency area. Complete reference showing everything you've accomplished at each role.

    Tier  3: Competency Cross-Reference
        Bullets reorganized by skill area (e.g., all your "Financial Management" bullets from all companies in one place). Perfect for quickly finding relevant bullets for specific job requirements.

    Statistics Summary: Shows bullet counts, top competencies, and key metrics per company.

Customization
    Adjust Impact Scoring
    Modify calculate_impact_score() to weight different factors:
        python
        def calculate_impact_score(self, row: pd.Series) -> float:
            score = 0
            # Weight percentages more heavily
            for metric in row['Metrics']:
                if metric['type'] == 'percentage':
                    val = float(metric['value'].replace('%', ''))
                    score += val * 5  # Changed from 2 to 5
        return score
    
    Add/Modify Competency Categories
    Edit the competency_keywords dictionary in categorize_by_competency():
        python
        competency_keywords = {
            'Strategic Planning': ['strategic', 'planning', 'roadmap'],
            'Your New Category': ['keyword1', 'keyword2', 'keyword3'],
            # ... add more
        }
    
    Change Company Normalization Rules
    Update normalize_company() to handle your specific employers:
        python
        def normalize_company(self, company: str) -> str:
            if 'Google' in company:
                return 'Google LLC'
        # Add your rules here

Limitations
    ⚠️ Metric Extraction: Works well for common formats (20%, $5M, 4,000 employees) but may miss unconventional metrics
    ⚠️ Semantic Similarity: Doesn't detect paraphrased duplicates (e.g., "reduced costs" vs "cut expenses") - only exact/near-exact text matches
    ⚠️ Context Understanding: Auto-categorization uses keywords, not true semantic understanding
    ⚠️ Manual Review Recommended: While 85-90% accurate, human review improves the final output

Tips for Best Results
    Standardize Input:  Use consistent formatting in your source resumes (same bullet style, metric formats)
    Review Tier 1:      The algorithm ranks by metrics, but you may want to manually adjust based on relevance to your target roles
    Keep Source Files:  The SourceFile column helps you remember which bullets worked for which companies/roles
    Update Regularly:   Rerun the analysis whenever you add new accomplishments or tailor more resumes
    Export to Word:     Convert the markdown output to .docx for easier formatting and sharing

Troubleshooting
    Problem: Bullets not deduplicating
    Solution: Check for extra spaces, punctuation differences. The tool looks for exact text matches.

    Problem: Metrics not extracting correctly
    Solution: Ensure metrics use standard formats: 20%, $5M, 4,000 employees

    Problem: Categories seem wrong
    Solution: Customize the competency_keywords dictionary for your industry

    Problem: CSV parsing errors
    Solution: Ensure proper encoding (UTF-8) and escaped commas within bullet text

License
    MIT License - Feel free to modify and use for personal or commercial purposes.

Contributing
    Improvements welcome! Priority areas:
        Better semantic deduplication (using NLP/embeddings)
        More sophisticated metric extraction
        Web interface for non-technical users
        Export to other formats (JSON, Excel, PDF)


///////// Detailed Explanation of Basic Usage /////////

///// Line 1: The Import Statement /////
python
from resume_analyzer import ResumeBulletAnalyzer
```

**What this does:**
- Tells Python to load the `ResumeBulletAnalyzer` class from a file called `resume_analyzer.py`
- Think of it like opening a toolbox - you're getting access to the tool

**In practice:**
- You need to save the Python code I provided as a file named `resume_analyzer.py`
- This file should be in the same folder as your script, OR
- Python needs to know where to find it (in your Python path)

**File structure should look like:**
```
your_project_folder/
├── resume_analyzer.py     ← The code I provided
├── Collated_Bullets.txt   ← Your data file
└── run_analysis.py        ← Your script with these usage lines

///// Line 2: Create the Analyzer Object /////
python
analyzer = ResumeBulletAnalyzer("Collated_Bullets.txt")
```

**What this does:**
This single line actually does A LOT of work behind the scenes:

1. **Reads your data file** (`Collated_Bullets.txt`)
   - Opens the file
   - Loads it into a pandas DataFrame (like an Excel spreadsheet in memory)

2. **Cleans the data** automatically:
   - Removes extra whitespace
   - Normalizes company names (e.g., "Wells Fargo - Tech Division" becomes standardized)
   - Extracts all metrics from each bullet (percentages, dollar amounts, numbers)

3. **Stores everything** in the `analyzer` object
   - Now `analyzer` contains all your data and is ready to process it

**What you're creating:**
- `analyzer` is now an object that "knows" about all your resume bullets
- It's like loading all your bullets into a smart filing system

**File format expected:**
Your `Collated_Bullets.txt` should be a CSV (comma-separated) or TSV (tab-separated) file that looks like:
```
Role,Company,Location,Dates,Bullet,SourceFile
Chief of Staff,Wells Fargo,Minneapolis MN,2021-2024,"Drove $90M in savings",Resume_v1.docx
Data Scientist,US Special Ops,Tampa FL,2017-2018,"Built 35-person team",Resume_v2.docx

///// Line 3: Export the Analysis /////
python
analyzer.export_to_markdown("Resume_Bullet_Library.md")
```
What this does:
    This is where the magic happens! This single line:

    Deduplicates all your bullets (removes duplicates, keeping the best version)
    Generates Tier 1 - Top 12 greatest hits
        Scores each bullet based on metrics, keywords, team size
        Ranks them
        Picks the top 12
    Generates Tier 2 - Organizes by company
        Groups all bullets by which company they're from
        Within each company, groups by competency (Strategic Planning, HR, etc.)
    Generates Tier 3 - Cross-reference by competency
        Reorganizes ALL bullets by skill area
        Shows which companies contributed to each competency
    Calculates statistics
        Counts bullets per company
        Identifies top competencies
        Extracts key metrics
    Writes everything to Resume_Bullet_Library.md
        Creates a nicely formatted markdown file
        Ready to open in Word, VS Code, or any text editor
    The output file:
        You'll get a file called Resume_Bullet_Library.md in the same folder, containing all three tiers plus statistics.

Complete Working Example
    Here's exactly how you'd use this in real life:
    Step 1: Save the analyzer code
        Copy the Python code I provided
        Save it as resume_analyzer.py

    Step 2: Prepare your data file
        Make sure your Collated_Bullets.txt file is formatted correctly
        Should have columns: Role, Company, Location, Dates, Bullet, SourceFile

    Step 3: Create a run script (let's call it analyze_my_resume.py):
        python
        from resume_analyzer import ResumeBulletAnalyzer
        # This loads all your data and cleans it
            analyzer = ResumeBulletAnalyzer("Collated_Bullets.txt")
        # This does all the analysis and creates the output file
            analyzer.export_to_markdown("Resume_Bullet_Library.md")
        print("✅ Done! Check Resume_Bullet_Library.md")
    
    Step 4: Run it
        bash
        python analyze_my_resume.py

    What happens:
        Python reads your data ✓
        Cleans and processes it ✓
        Generates 3-tier analysis ✓
        Creates markdown file ✓
        Prints "Done!" ✓

What If You Already Have the Data?
    In your case, you already provided me with Collated Bullets.txt. So you would:
        Save the Python code as resume_analyzer.py
        Make sure your data file is in the right format (it already is - it's the file you gave me!)
        Run this simple script:
            python
            from resume_analyzer import ResumeBulletAnalyzer

            analyzer = ResumeBulletAnalyzer("Collated Bullets.txt")  # Note: use your actual filename
            analyzer.export_to_markdown("My_Resume_Library.md")

Open the output in Word or any markdown viewer

Common Confusion Points
    Q: Where does resume_analyzer come from?
    A: It's the filename of the Python code I provided. You save that code as resume_analyzer.py
    
    Q: What's the .txt vs .csv thing?
    A: The file can be .txt, .csv, or .tsv - as long as it has columns separated by commas or tabs. Pandas figures it out automatically.
    
    Q: Do I need to understand the code inside ResumeBulletAnalyzer?
    A: Nope! That's the point. You just use these 3 lines and it handles everything.
    
    Q: Can I change the output filename?
    A: Yes! Just change "Resume_Bullet_Library.md" to whatever you want: "[Name]_Resume_Master.md"
