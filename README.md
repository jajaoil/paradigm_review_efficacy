# paradigm_review_efficacy
Reproducible materials for the study Code Review Effectiveness Across Paradigms. Includes raw data analysis scripts and platform screenshots for verification.

# Code Review Effectiveness Across Paradigms

This repository contains all materials required to reproduce the analyses and figures reported in the study titled
"Code Review Effectiveness Across Paradigms". The study used a controlled experiment with fifty participants
twenty five professional developers and twenty five advanced graduate students and provides raw data,
analysis code, platform screenshots and instructions to verify the results.

## Contents

- data timing raw csv templates and example rows
- analysis scripts for NASA TLX scoring Krippendorff alpha and mixed effects models
- reproducible notebook to run all analyses
- screenshots originals and a checksum manifest for verification
- ethics documents consent and IRB approval

## Quick reproduction instructions

1. Clone this repository
2. Create a Python environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

bash
Copy code
3. Put your platform exports in the data folder replacing the template files:
- data/timing_raw_template.csv rename to data/timing_raw.csv
- data/nasa_tlx_raw_template.csv rename to data/nasa_tlx_raw.csv
- data/comments_raw_template.csv rename to data/comments_raw.csv
- data/coding_sheet_template.csv rename to data/coding_sheet.csv
- data/eye_aggregates_template.csv rename to data/eye_aggregates.csv
- data/defects_per_participant_template.csv rename to data/defects_per_participant.csv
4. Place original screenshots in screenshots/originals
5. Generate checksums
chmod +x analysis/checksums_generate.sh
analysis/checksums_generate.sh

pgsql
Copy code
This will update checksums.sha256 with exact SHA256 hashes for files under data and screenshots originals.
6. Run the reproducible notebook
- Start Jupyter
  ```
  jupyter notebook analysis/reproduce_main_results.ipynb
  ```
- Run all cells to reproduce tables and figures used in the paper
