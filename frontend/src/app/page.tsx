"use client";

import { useState } from "react";
import { NutritionForm } from "@/components/NutritionForm";
import { NutritionResults } from "@/components/NutritionResults";
import { getMacroTargets, ApiError } from "@/lib/api";
import { MacroTargetRequest, MacroTargetResponse, NutritionFormData } from "@/types/nutrition";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { SparklesText } from "@/components/ui/sparkles-text";

export default function Home() {
    const [results, setResults] = useState<MacroTargetResponse | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (formData: NutritionFormData) => {
        setIsLoading(true);
        setError(null);
        setResults(null);

        try {
            // Convert form data to API request format
            const request: MacroTargetRequest = {
                user_query: formData.user_query,
                age: formData.age ? parseInt(formData.age) : undefined,
                weight_kg: formData.weight_kg ? parseFloat(formData.weight_kg) : undefined,
                sex: formData.sex || undefined,
                exercise_type: formData.exercise_type || undefined,
                exercise_duration_minutes: formData.exercise_duration_minutes
                    ? parseInt(formData.exercise_duration_minutes)
                    : undefined,
                exercise_intensity: formData.exercise_intensity || undefined,
                timing: formData.timing || undefined,
            };

            const response = await getMacroTargets(request);
            setResults(response);
        } catch (err) {
            if (err instanceof ApiError) {
                setError(`API Error (${err.status}): ${err.message}`);
            } else {
                setError("An unexpected error occurred. Please try again.");
            }
        } finally {
            setIsLoading(false);
        }
    };

    const handleReset = () => {
        setResults(null);
        setError(null);
    };

    return (
        <main className="scroll-smooth">
            {/* Hero Section */}
            <section className="flex flex-col items-center justify-center min-h-screen w-full text-center bg-gradient-to-br from-blue-50 via-white to-purple-100 px-4">
                <SparklesText
                    text="Personalized Nutrition Guidance"
                    className="text-5xl md:text-6xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 mb-4"
                />
                <p
                    className="text-lg md:text-2xl mb-8 text-blue-800 max-w-2xl mx-auto"
                    style={{ fontFamily: "var(--font-open-sans), sans-serif" }}
                >
                    Get science-backed macro recommendations for your next workout.
                </p>
                <a href="#recommendation-form" className="inline-block">
                    <button className="px-8 py-3 rounded-xl bg-white text-blue-800 font-semibold shadow-xl hover:bg-blue-100 transition border border-blue-200">
                        Get Started
                    </button>
                </a>
            </section>

            {/* Recommendation Engine Anchor */}
            <section id="recommendation-form" className="min-h-screen w-full bg-background pt-12">
                {/* Features */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
                    <Card className="text-center">
                        <CardContent className="pt-6">
                            <div className="text-2xl mb-2">🎯</div>
                            <h3 className="font-semibold mb-2">Personalized</h3>
                            <p className="text-sm text-muted-foreground">
                                Recommendations tailored to your age, weight, and workout type
                            </p>
                        </CardContent>
                    </Card>
                    <Card className="text-center">
                        <CardContent className="pt-6">
                            <div className="text-2xl mb-2">🧠</div>
                            <h3 className="font-semibold mb-2">AI-Powered</h3>
                            <p className="text-sm text-muted-foreground">
                                Advanced AI analyzes your needs using scientific guidelines
                            </p>
                        </CardContent>
                    </Card>
                    <Card className="text-center">
                        <CardContent className="pt-6">
                            <div className="text-2xl mb-2">⚡</div>
                            <h3 className="font-semibold mb-2">Instant</h3>
                            <p className="text-sm text-muted-foreground">
                                Get detailed recommendations in seconds, not hours
                            </p>
                        </CardContent>
                    </Card>
                </div>

                {/* Form or Results */}
                {!results ? (
                    <NutritionForm onSubmit={handleSubmit} isLoading={isLoading} />
                ) : (
                    <div className="space-y-6">
                        <div className="flex justify-center">
                            <Button onClick={handleReset} variant="outline">
                                Get New Recommendations
                            </Button>
                        </div>
                        <NutritionResults results={results} />
                    </div>
                )}

                {/* Error Display */}
                {error && (
                    <Card className="border-red-200 bg-red-50">
                        <CardHeader>
                            <CardTitle className="text-red-800">Error</CardTitle>
                            <CardDescription className="text-red-600">{error}</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Button onClick={handleReset} variant="outline">
                                Try Again
                            </Button>
                        </CardContent>
                    </Card>
                )}
            </section>
        </main>
    );
}
