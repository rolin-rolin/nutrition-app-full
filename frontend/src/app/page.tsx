"use client";

import { useState } from "react";
import { NutritionForm } from "@/components/NutritionForm";
import { NutritionResults } from "@/components/NutritionResults";
import { getMacroTargets, ApiError } from "@/lib/api";
import { MacroTargetRequest, MacroTargetResponse, NutritionFormData } from "@/types/nutrition";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

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
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            {/* Header */}
            <header className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">NutriFit</h1>
                            <p className="text-gray-600">AI-Powered Nutrition Recommendations</p>
                        </div>
                        <div className="flex items-center space-x-2">
                            <Badge variant="outline">Powered by AI</Badge>
                            <Badge variant="secondary">Local RAG</Badge>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="space-y-8">
                    {/* Hero Section */}
                    <div className="text-center space-y-4">
                        <h2 className="text-4xl font-bold text-gray-900">Get Personalized Nutrition Advice</h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Tell us about your workout and receive tailored macronutrient recommendations powered by AI
                            and backed by scientific nutrition guidelines.
                        </p>
                    </div>

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
                </div>
            </main>

            {/* Footer */}
            <footer className="bg-white border-t mt-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <div className="text-center text-gray-600">
                        <p>Built with Next.js, Tailwind CSS, and shadcn/ui</p>
                        <p className="text-sm mt-2">
                            Powered by local RAG pipeline with sentence-transformers and Chroma
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    );
}
