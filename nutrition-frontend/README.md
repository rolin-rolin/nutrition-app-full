# Nutrition App Frontend

A web application for AI-powered nutrition recommendations built with Next.js, Tailwind CSS, and shadcn/ui.

## Features

-   **Personalized Recommendations**: Get nutrition advice tailored to your age, weight, and workout type
-   **AI-Powered**: Advanced AI analyzes your needs using scientific nutrition guidelines
-   **Instant Results**: Get detailed recommendations in seconds
-   **Mobile-Friendly**: Responsive design that works on all devices
-   **Modern UI**: Clean, intuitive interface built with shadcn/ui components

## Tech Stack

-   **Framework**: Next.js 14 with App Router
-   **Styling**: Tailwind CSS
-   **Components**: shadcn/ui
-   **Language**: TypeScript
-   **State Management**: React hooks
-   **API**: FastAPI backend integration

## Project Structure

```
src/
├── app/
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Main page
├── components/
│   ├── ui/                  # shadcn/ui components
│   ├── NutritionForm.tsx    # Form component
│   └── NutritionResults.tsx # Results display
├── lib/
│   ├── api.ts              # API service functions
│   └── utils.ts            # Utility functions
└── types/
    └── nutrition.ts        # TypeScript interfaces
```

## API Integration

The frontend communicates with the FastAPI backend through the following endpoints:

-   `POST /api/v1/macro-targets/` - Get nutrition recommendations

### Request Format

```typescript
interface MacroTargetRequest {
    user_query: string;
    age?: number;
    weight_kg?: number;
    sex?: "male" | "female";
    exercise_type?: string;
    exercise_duration_minutes?: number;
    exercise_intensity?: "low" | "moderate" | "high";
    timing?: "pre-workout" | "during-workout" | "post-workout" | "general";
}
```

### Response Format

```typescript
interface MacroTargetResponse {
  target_calories: number;
  target_protein: number;
  target_carbs: number;
  target_fat: number;
  target_electrolytes: number;
  pre_workout_macros?: {...};
  during_workout_macros?: {...};
  post_workout_macros?: {...};
  rag_context: string;
  reasoning: string;
  created_at: string;
}
```

This project is licensed under the MIT License.
