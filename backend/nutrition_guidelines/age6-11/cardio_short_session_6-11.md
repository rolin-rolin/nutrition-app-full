---
type_of_activity: cardio
duration: short
age_group: 6-11
---

timing:
pre:
carbs_g_per_kg: [0.3, 0.5]
protein_g_per_kg: [0.05, 0.1]
fat_g_per_kg: [0.0, 0.0]

during:
carbs_g_per_kg_per_hour: [0.0, 0.0]
protein_g_per_kg_per_hour: [0.0, 0.0]
electrolytes_mg_per_kg_per_hour: [0.0, 0.0]

post:
carbs_g_per_kg: [0.5, 0.5]
protein_g_per_kg: [0.1, 0.15]
fat_g_per_kg: [0.0, 0.0]

# NOTE: This should be computed dynamically based on pre + during + post timing and duration

overall*targets:
carbs_g_per_kg: sum of pre.carbs + (during.carbs * duration*hr) + post.carbs
protein_g_per_kg: sum of pre.protein + post.protein
fat_g_per_kg: assumed minimal or negligible
electrolytes_mg_per_kg: during.electrolytes * duration_hr (likely negligible)

key_principles:

-   Kids doing <30 min of cardio rarely need structured nutrition.
-   Focus on hydration, gentle carbs, and light recovery snack.
-   If intensity is high (sprinting, intervals), include a small carb dose post-workout.

avoid:

-   Sports drinks (unless high heat/intensity)
-   Large pre-workout meals
-   High-fiber or high-fat snacks before exercise
