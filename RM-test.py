import pandas as pd

from criteria import ContinuousCriterion, DiscreteCriterion, QualitativeCriterion

# Load the Excel file and focus on the "Topic 1" sheet
file_path = './RM project references.xlsx'
data_combined = pd.concat([
    pd.read_excel(file_path, sheet_name=sheet).assign(Topic=sheet)
    for sheet in ['Topic 1', 'Topic 2', 'Topic 3']
], ignore_index=True)

# Display the first few rows to understand the structure
# print(data_combined)

criteria_objects = []

# Is it fabricated
criterion_fabricated = QualitativeCriterion(
    name="Is it fabricated",
    description="Is the reference fabricated? 0 - Yes, 0.5 - Other, 1 - No.",
    value_score_mapping={'Yes': 0.0, 'Wrong Author Name': 0.5, 'Wrong Title': 0.5, 'No': 1.0}
)
criteria_objects.append(criterion_fabricated)

# Relevance
criterion_relevance = QualitativeCriterion(
    name="Relevance",
    description="Is the reference relevant? Yes = 1, No = 0.",
    value_score_mapping={'Yes': 1.0, 'No': 0.0}
)
criteria_objects.append(criterion_relevance)

# Has DOI
criterion_doi = QualitativeCriterion(
    name="Has DOI",
    description="Does the reference have a DOI? Yes = 1, No = 0.",
    value_score_mapping={'Yes': 1.0, 'No': 0.0}
)
criteria_objects.append(criterion_doi)

# Correct Referencing Format
criterion_referencing = QualitativeCriterion(
    name="Correct Referencing Format",
    description="Is the referencing format correct? Yes = 1, No = 0.",
    value_score_mapping={'Yes': 1.0, 'No': 0.0}
)
criteria_objects.append(criterion_referencing)

# H-index
criterion_h_index = ContinuousCriterion(
    name="H-index of first author",
    description="H-index of the first author.",
    points=[(5, 0.2), (15, 0.5), (30, 0.8), (100, 1.0)]
)
criteria_objects.append(criterion_h_index)
