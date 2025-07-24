---
type_of_activity: strength
duration: short
age_group: 6-11
---

timing:
pre:
carbs_g_per_kg: [0.3, 0.5]
protein_g_per_kg: [0.05, 0.1]

during:
carbs_g_per_kg_per_hour: [0.0, 0.0]
protein_g_per_kg_per_hour: [0.0, 0.0]
electrolytes_mg_per_kg_per_hour: [0.0, 0.0]

post:
carbs_g_per_kg: [0.5, 0.5]
protein_g_per_kg: [0.15, 0.2]
fat_g_per_kg: [0.1, 0.2]

# NOTE: This should be computed dynamically based on pre + during + post timing and duration

overall*targets: !!computed
carbs_g_per_kg: sum of pre.carbs + (during.carbs * duration*hr) + post.carbs
protein_g_per_kg: sum of pre.protein + post.protein
fat_g_per_kg: sum of post.fat (optional)
electrolytes_mg_per_kg: during.electrolytes * duration_hr

key_principles:

-   Strength training in children is light/moderate; focus is on movement patterns.
-   Recovery protein is more relevant than intra-workout nutrition.
-   Whole food snacks like milk + crackers work great post-exercise.

avoid:

-   Protein powders (not necessary)
-   High-sugar "energy" snacks
-   Forcing food if appetite is low post-workout
