---
type_of_activity: strength
duration: long
age_group: 6-11
---

timing:
pre:
carbs_g_per_kg: [0.5, 0.8]
protein_g_per_kg: [0.1, 0.1]

during:
carbs_g_per_kg_per_hour: [0.3, 0.5]
protein_g_per_kg_per_hour: [0.0, 0.0]
electrolytes_mg_per_kg_per_hour: [11.0, 16.0]

post:
carbs_g_per_kg: [0.5, 0.8]
protein_g_per_kg: [0.2, 0.25]
fat_g_per_kg: [0.1, 0.1]

# NOTE: This should be computed dynamically based on pre + during + post timing and duration

overall_targets: !!computed
carbs_g_per_kg: sum of pre.carbs + (during.carbs * duration*hr) + post.carbs
protein_g_per_kg: sum of pre.protein + post.protein
fat_g_per_kg: sum of post.fat (optional)
electrolytes_mg_per_kg: during.electrolytes \* duration_hr

key_principles:

-   Post-workout carb + protein combo supports growth and recovery.
-   Use real food, and match intake to appetite.
-   Encourage hydration as part of the routine, not as a chore.

avoid:

-   Excessive protein (not needed in children)
-   Sports supplements
-   Meals too close to activity
