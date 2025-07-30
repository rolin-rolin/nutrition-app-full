---
type_of_activity: cardio
duration: long
age_group: 6-11
---

timing:
pre:
carbs_g_per_kg: [0.5, 0.8]
protein_g_per_kg: [0.05, 0.1]
fat_g_per_kg: [0.0, 0.0]

during:
carbs_g_per_kg_per_hour: [0.5, 1.0]
protein_g_per_kg_per_hour: [0.0, 0.0]
electrolytes_mg_per_kg_per_hour: [11, 21]

post:
carbs_g_per_kg: [1.0, 1.0]
protein_g_per_kg: [0.2, 0.25]
fat_g_per_kg: [0.0, 0.0]

# NOTE: This should be computed dynamically based on pre + during + post timing and duration

overall*targets:
carbs_g_per_kg: sum of pre.carbs + (during.carbs * duration*hr) + post.carbs
protein_g_per_kg: sum of pre.protein + post.protein
fat_g_per_kg: sum of pre.fat + post.fat
electrolytes_mg_per_kg: during.electrolytes * duration_hr

key_principles:

-   Carbs First: Kids rely more on carbs than adults for energy during exercise.
-   Frequent Fueling: Small, regular snacks or drinks are better tolerated than large meals.
-   Hydration: Children may not feel thirsty until they’re dehydrated. Encourage regular sips.
-   Parental Supervision: Ensure availability of age-appropriate, appealing options — avoid complex sports nutrition products unless supervised by a pediatric dietitian.
-   Food Familiarity: Stick with familiar foods to reduce risk of GI distress or refusal.
-   Children tend to regulate intake based on hunger/thirst more instinctively. Offering frequent, small, easily digestible options is preferred over strict numeric targets.

avoid:

-   High-fiber snacks (e.g., raw vegetables, bran cereals)
-   Fatty, fried foods (can slow digestion)
-   New or unfamiliar snacks
-   Caffeinated or carbonated drinks
-   Rigid schedules — be flexible and responsive to the child’s preferences and tolerance
