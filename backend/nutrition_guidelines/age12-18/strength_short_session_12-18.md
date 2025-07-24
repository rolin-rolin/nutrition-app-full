---
type_of_activity: strength
duration: short
age_group: 12-18
---

timing:
pre:
carbs_g_per_kg: [0.4, 0.5]
protein_g_per_kg: [0.05, 0.1] # optional

during:
carbs_g_per_kg_per_hour: [0.0, 0.0]
protein_g_per_kg_per_hour: [0.0, 0.0]
electrolytes_mg_per_kg_per_hour: [0, 0] # not needed

post:
carbs_g_per_kg: [0.5, 0.7]
protein_g_per_kg: [0.2, 0.25]
fat_g_per_kg: [0.0, 0.0] # not mentioned, assumed minimal

# NOTE: This should be computed dynamically based on pre + during + post timing and duration

overall_targets: !!computed
carbs_g_per_kg: [0.9, 1.2] # pre + post
protein_g_per_kg: [0.25, 0.35] # pre (optional) + post
fat_g_per_kg: [0.0, 0.0] # no explicit fat guidance
electrolytes_mg_per_kg_per_hour: {} # not relevant for short session

key_principles:

-   Post-strength protein is key to support muscle repair and growth during adolescence.
-   A simple carb + protein snack is typically enough after short lifting sessions.
-   Most adolescents meet their needs through food, but recovery snacks help consistency and progress.

avoid:

-   Protein powders unless advised by a pediatric sports dietitian
-   High-fat or high-fiber meals before training
-   Skipping protein-rich foods post-exercise during growth phases
