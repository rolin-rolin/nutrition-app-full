---
type_of_activity: cardio
duration: long
age_group: 12-18
---

timing:
pre:
carbs_g_per_kg: [0.5, 1.0]
protein_g_per_kg: [0.1, 0.15]
fat_g_per_kg: [0.0, 0.1]

during:
carbs_g_per_kg_per_hour: [0.8, 1.0]
protein_g_per_kg_per_hour: [0.0, 0.1]
electrolytes_mg_per_kg_per_hour: [21, 31]

post:
carbs_g_per_kg: [1.0, 1.2]
protein_g_per_kg: [0.25, 0.3]
fat_g_per_kg: [0.1, 0.2]

# NOTE: This should be computed dynamically based on pre + during + post timing and duration

overall*targets: !!computed
carbs_g_per_kg: sum of pre.carbs + (during.carbs * duration*hr) + post.carbs
protein_g_per_kg: sum of pre.protein + (during.protein * duration_hr) + post.protein
fat_g_per_kg: sum of pre.fat + post.fat
electrolytes_mg_per_kg: during.electrolytes \* duration_hr

key_principles:

-   Energy Availability is crucial during adolescence; skipping post-exercise nutrition can impair growth, recovery, and performance.
-   Carbohydrates should be the primary fuel, especially for high-intensity or long-duration efforts.
-   Protein supports both recovery and developmental needs (muscle growth, hormones).
-   Hydration and electrolytes are essential to avoid cramping, fatigue, and heat stress.
-   Encourage real foods when possible — flavored milk, fruit, and whole grains are effective for teens.

avoid:

-   High-fiber foods (can cause GI discomfort)
-   High-fat foods (slow digestion during training)
-   Energy drinks with high caffeine
-   Large solid meals immediately before or during exercise
-   Skipping recovery nutrition, especially if training daily
