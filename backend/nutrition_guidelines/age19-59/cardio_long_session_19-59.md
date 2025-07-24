---
type_of_activity: cardio
duration: long
age_group: 19-59
---

timing:
pre:
carbs_g_per_kg: [0.5, 1.0]
protein_g_per_kg: [0.1, 0.2]
fat_g_per_kg: [0.1, 0.1]

during:
carbs_g_per_kg_per_hour: [0.8, 1.2]
protein_g_per_kg_per_hour: [0.1, 0.2]
electrolytes_mg_per_kg_per_hour: [31, 52]

post:
carbs_g_per_kg: [1.0, 1.2]
protein_g_per_kg: [0.25, 0.4]
fat_g_per_kg: [0.1, 0.2]

# NOTE: This should be computed dynamically based on pre + during + post timing and duration

overall_targets: !!computed
carbs_g_per_kg: [1.5, 2.2] # pre + post (during is per hour)
protein_g_per_kg: [0.35, 0.6] # pre + post
fat_g_per_kg: [0.2, 0.3] # pre + post
electrolytes_mg_per_kg_per_hour:
sodium: [31, 52]

key_principles:

-   Carbohydrates: Use fast-digesting forms during and after (e.g., glucose, maltodextrin).
-   Protein: Essential post-exercise for recovery; optional during prolonged sessions.
-   Hydration: Match sweat loss with fluid intake; monitor urine color.
-   Electrolytes: Prioritize sodium, especially in hot/humid conditions or heavy sweaters.
-   Recovery: Aim to eat within 30 minutes, followed by a full meal within 2 hours.

avoid:

-   High-fiber foods (can cause bloating or GI distress)
-   High-fat meals (slow gastric emptying)
-   Large solid meals close to or during exercise
-   Excess caffeine (especially if dehydrated or heat-stressed)
