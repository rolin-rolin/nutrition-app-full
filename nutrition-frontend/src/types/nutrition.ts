export interface MacroTargetRequest {
    user_query: string;
    age?: number;
    weight_kg?: number;
    sex?: "male" | "female";
    exercise_type?: string;
    exercise_duration_minutes?: number;
    exercise_intensity?: "low" | "moderate" | "high";
    timing?: "pre-workout" | "during-workout" | "post-workout" | "general";
}

export interface MacroTargetResponse {
    target_calories: number;
    target_protein: number;
    target_carbs: number;
    target_fat: number;
    target_electrolytes: number;
    pre_workout_macros?: {
        carbs: number;
        protein: number;
        fat: number;
        calories: number;
    };
    during_workout_macros?: {
        carbs: number;
        protein: number;
        electrolytes: number;
    };
    post_workout_macros?: {
        carbs: number;
        protein: number;
        fat: number;
        calories: number;
    };
    rag_context: string;
    reasoning: string;
    created_at: string;
}

export interface NutritionFormData {
    user_query: string;
    age: string;
    weight_kg: string;
    sex: "male" | "female" | "";
    exercise_type: string;
    exercise_duration_minutes: string;
    exercise_intensity: "low" | "moderate" | "high" | "";
    timing: "pre-workout" | "during-workout" | "post-workout" | "general" | "";
}
