---
type_of_activity: cardio
duration: short
age_group: 12-18
---

timing:
pre:
carbs_g_per_kg: [0.3, 0.5]
protein_g_per_kg: [0.05, 0.1]
fat_g_per_kg: [0.0, 0.0]

during:
carbs_g_per_kg_per_hour: [0.0, 0.0]
protein_g_per_kg_per_hour: [0.0, 0.0]
electrolytes_mg_per_kg_per_hour: [16, 21]

post:
carbs_g_per_kg: [0.5, 0.7]
protein_g_per_kg: [0.15, 0.2]
fat_g_per_kg: [0.0, 0.0]

# NOTE: This should be computed dynamically based on pre + during + post timing and duration

overall_targets:
carbs_g_per_kg: sum of pre.carbs + post.carbs
protein_g_per_kg: sum of pre.protein (optional) + post.protein
fat_g_per_kg: sum of pre.fat + post.fat
electrolytes_mg_per_kg: during.electrolytes \* duration_hr

key_principles:

-   Nutritional support not strictly necessary for short cardio, but post-exercise fuel aids recovery especially for adolescents in growth phases.
-   Hydration and light carbs are sufficient for most short workouts.

avoid:

-   High-fiber or high-fat snacks right before exercise
-   Energy drinks or excess caffeine
-   Skipping post-exercise food, especially during periods of growth or heavy training
