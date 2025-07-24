---
type_of_activity: strength
duration: long
age_group: 19-59
---

timing:
pre:
carbs_g_per_kg: [0.5, 0.8]
protein_g_per_kg: [0.1, 0.15]
fat_g_per_kg: [0.0, 0.1]

during:
carbs_g_per_kg_per_hour: [0.3, 0.5]
protein_g_per_kg_per_hour: [0.05, 0.1]
electrolytes_mg_per_kg_per_hour: [21, 32]

post:
carbs_g_per_kg: [0.8, 1.0]
protein_g_per_kg: [0.3, 0.4]
fat_g_per_kg: [0.1, 0.2]

# NOTE: This should be computed dynamically based on pre + during + post timing and duration

overall_targets: !!computed
carbs_g_per_kg: [1.6, 2.3] # pre (0.5–0.8) + post (0.8–1.0) + during per hour
protein_g_per_kg: [0.45, 0.65] # pre (0.1–0.15) + post (0.3–0.4) + during per hour
fat_g_per_kg: [0.1, 0.3] # pre (≤0.1) + post (0.1–0.2)
electrolytes_mg_per_kg_per_hour:
sodium: [20, 30]

key_principles:

-   Post-workout carb + protein combination supports muscle repair, glycogen replenishment, and recovery.
-   Hydration and electrolyte replacement important in long or sweaty sessions.

avoid:

-   Skipping recovery nutrition
-   Large fatty meals close to training
-   Excess caffeine or energy drinks
