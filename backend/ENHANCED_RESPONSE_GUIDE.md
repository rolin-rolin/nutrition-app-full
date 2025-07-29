# Enhanced Recommendation Response Guide

## Overview

The enhanced recommendation response provides all the information needed for frontend display, including user profile information, macro targets, bundle statistics, preferences, and key principles from nutrition knowledge documents.

## Response Structure

```json
{
  "recommended_products": [...],
  "macro_targets": {...},
  "reasoning": "...",
  "user_profile": {...},
  "bundle_stats": {...},
  "preferences": {...},
  "key_principles": [...]
}
```

## Frontend Display Format

### 1. Macro Targets Display

**Format:** "Based on your profile: `<age_display>`, `<weight_display>`, `<exercise_display>`, these are your macro targets: `<target_protein>`g protein, `<target_carbs>`g carbs, `<target_fat>`g fat, `<target_electrolytes>`mg electrolytes"

**Example:**

```
Based on your profile: 25 years old, 70kg, cardio for 60 minutes, these are your macro targets: 25g protein, 75g carbs, 15g fat, 1000mg electrolytes
```

**Default Values:**

-   Age: "using default age 21"
-   Weight: "using default 70kg weight"
-   Exercise: "using default 60-minute duration" or "using default exercise type"

### 2. Bundle Statistics Display

**Format:** "What this bundle provides: `<total_protein>`g protein, `<total_carbs>`g carbs, `<total_fat>`g fat, `<total_electrolytes>`mg electrolytes, `<total_calories>` calories"

**Example:**

```
What this bundle provides: 28.5g protein, 78.2g carbs, 16.8g fat, 120mg electrolytes, 485 calories
```

### 3. Layer 2 Optimization Stats

**Format:** "Selected `<num_snacks>` snacks with `<target_match_percentage>`% target match."

**Example:**

```
Selected 6 snacks with 85.2% target match.
```

### 4. Preferences Display

**Format:** "These snacks are tagged: `<soft_preferences>`, `<hard_filters>`"

**Example:**

```
These snacks are tagged: sweet flavor, fruity flavor, crunchy texture, vegan, no nuts
```

### 5. Key Principles Display

**Format:**

```
Some key principles:
- <principle_1>
- <principle_2>
```

**Example:**

```
Some key principles:
- Focus on easily digestible carbohydrates before cardio
- Include moderate protein for muscle preservation
```

### 6. Product Recommendations

**Format:** Display each product with:

-   Product name
-   Macro breakdown (protein, carbs, fat, calories)
-   Product image
-   Buy link

**Example:**

```
1. Product Name
   Protein: 10g | Carbs: 25g | Fat: 5g | Calories: 165
   [Product Image] [Buy Now]
```

## Response Fields Reference

### `user_profile` (UserProfileInfo)

```typescript
{
  age?: number;
  weight_kg?: number;
  exercise_type?: string;
  exercise_duration_minutes?: number;
  age_display: string;        // "25 years old" or "using default age 21"
  weight_display: string;     // "70kg" or "using default 70kg weight"
  exercise_display: string;   // "cardio for 60 minutes" or "using default cardio"
}
```

### `macro_targets` (MacroTargetResponse)

```typescript
{
  target_calories?: number;
  target_protein?: number;
  target_carbs?: number;
  target_fat?: number;
  target_electrolytes?: number;
  reasoning: string;
  // ... other fields
}
```

### `bundle_stats` (BundleStats)

```typescript
{
    total_protein: number;
    total_carbs: number;
    total_fat: number;
    total_electrolytes: number;
    total_calories: number;
    num_snacks: number;
    target_match_percentage: number;
}
```

### `preferences` (PreferenceInfo)

```typescript
{
  soft_preferences: string[];  // ["sweet flavor", "high-protein"]
  hard_filters: string[];      // ["vegan", "no nuts"]
}
```

### `key_principles` (KeyPrinciple[])

```typescript
[{ principle: string }, { principle: string }];
```

### `recommended_products` (Product[])

```typescript
[
  {
    id: number;
    name: string;
    protein: number;
    carbs: number;
    fat: number;
    calories: number;
    electrolytes_mg: number;
    image_url?: string;
    buy_link?: string;
    // ... other fields
  }
]
```

## Conditional Display Logic

### When Activity Info is Available

-   Display user profile section
-   Display macro targets
-   Display bundle statistics
-   Display key principles (if available)

### When No Activity Info is Available

-   Hide user profile section
-   Hide macro targets section
-   Hide bundle statistics section
-   Hide key principles section
-   Only show product recommendations and preferences

### When Strength Activity is Detected

-   Automatically include "high-protein" in soft preferences
-   Display higher protein targets
-   Extract strength-specific key principles

## API Endpoint

**POST** `/api/v1/recommend/`

**Request Body:**

```json
{
    "user_query": "I need snacks for my workout",
    "age": 25,
    "weight_kg": 70.0,
    "exercise_type": "cardio",
    "exercise_duration_minutes": 60,
    "preferences": {
        "flavor_preferences": ["sweet"],
        "dietary_requirements": ["vegan"]
    }
}
```

**Response:** EnhancedRecommendationResponse with all display information

## Error Handling

-   If `user_profile` is `null`, don't display profile section
-   If `macro_targets` is `null`, don't display macro targets section
-   If `bundle_stats` is `null`, don't display bundle statistics
-   If `key_principles` is empty array, don't display principles section
-   If `preferences.soft_preferences` is empty, don't display soft preferences
-   If `preferences.hard_filters` is empty, don't display hard filters

## Example Frontend Implementation

```typescript
interface EnhancedRecommendationResponse {
    recommended_products: Product[];
    macro_targets?: MacroTargetResponse;
    reasoning: string;
    user_profile?: UserProfileInfo;
    bundle_stats?: BundleStats;
    preferences?: PreferenceInfo;
    key_principles: KeyPrinciple[];
}

function displayRecommendations(response: EnhancedRecommendationResponse) {
    // 1. Display user profile and macro targets
    if (response.user_profile && response.macro_targets) {
        console.log(
            `Based on your profile: ${response.user_profile.age_display}, ${response.user_profile.weight_display}, ${response.user_profile.exercise_display}, these are your macro targets: ${response.macro_targets.target_protein}g protein, ${response.macro_targets.target_carbs}g carbs, ${response.macro_targets.target_fat}g fat, ${response.macro_targets.target_electrolytes}mg electrolytes`
        );
    }

    // 2. Display bundle statistics
    if (response.bundle_stats) {
        console.log(
            `What this bundle provides: ${response.bundle_stats.total_protein}g protein, ${response.bundle_stats.total_carbs}g carbs, ${response.bundle_stats.total_fat}g fat, ${response.bundle_stats.total_electrolytes}mg electrolytes, ${response.bundle_stats.total_calories} calories`
        );
        console.log(
            `Selected ${response.bundle_stats.num_snacks} snacks with ${response.bundle_stats.target_match_percentage}% target match.`
        );
    }

    // 3. Display preferences
    if (response.preferences) {
        const allTags = [...response.preferences.soft_preferences, ...response.preferences.hard_filters];
        if (allTags.length > 0) {
            console.log(`These snacks are tagged: ${allTags.join(", ")}`);
        }
    }

    // 4. Display key principles
    if (response.key_principles.length > 0) {
        console.log("Some key principles:");
        response.key_principles.forEach((principle) => {
            console.log(`- ${principle.principle}`);
        });
    }

    // 5. Display products
    response.recommended_products.forEach((product, index) => {
        console.log(`${index + 1}. ${product.name}`);
        console.log(
            `   Protein: ${product.protein}g | Carbs: ${product.carbs}g | Fat: ${product.fat}g | Calories: ${product.calories}`
        );
        console.log(`   [Product Image] [Buy Now]`);
    });
}
```
