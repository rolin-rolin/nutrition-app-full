---
type_of_activity: strength
duration: long
age_group: 12-18
---

timing:
pre:
carbs_g_per_kg: [0.5, 0.8]
protein_g_per_kg: [0.1, 0.15]
fat_g_per_kg: [0.0, 0.1] # keep low

during:
carbs_g_per_kg_per_hour: [0.3, 0.5] # optional, if >60 min
protein_g_per_kg_per_hour: [0.05, 0.1] # optional
electrolytes_mg_per_kg_per_hour: [15, 25] # if in heat or high sweat

post:
carbs_g_per_kg: [0.8, 1.0]
protein_g_per_kg: [0.25, 0.3]
fat_g_per_kg: [0.1, 0.2]

# NOTE: This should be computed dynamically based on pre + during + post timing and duration

overall_targets: !!computed
carbs_g_per_kg: sum of pre.carbs + during.carbs/hour + post.carbs
protein_g_per_kg: sum of pre.protein + during.protein/hour + post.protein
fat_g_per_kg: sum of pre.fat + post.fat
electrolytes_mg_per_kg_per_hour:
sodium: [15, 25] # only relevant in heat or high sweat

key_principles:

-   Strength sessions longer than 45–60 min, especially with compound lifts or circuits, increase recovery needs.
-   Carbs + protein post-workout is critical for muscle repair, hormone support, and growth.
-   Adolescents have elevated protein synthesis windows, so post-training nutrition is especially impactful.
-   Emphasize whole foods with a mix of protein, carbs, and hydration — not just supplements.

avoid:

-   High-fat or high-fiber meals right before training (can slow digestion)
-   Skipping recovery food (affects growth, recovery, and future performance)
-   Over-reliance on powders or supplements — whole foods are ideal
-   Energy drinks or high-caffeine products (unnecessary and potentially risky)
