"use client";

import { MacroTargetResponse } from "@/types/nutrition";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";

interface NutritionResultsProps {
    results: MacroTargetResponse;
}

export function NutritionResults({ results }: NutritionResultsProps) {
    const totalCalories = results.target_calories;
    const proteinCalories = results.target_protein * 4; // 4 calories per gram
    const carbsCalories = results.target_carbs * 4; // 4 calories per gram
    const fatCalories = results.target_fat * 9; // 9 calories per gram

    const proteinPercentage = totalCalories > 0 ? (proteinCalories / totalCalories) * 100 : 0;
    const carbsPercentage = totalCalories > 0 ? (carbsCalories / totalCalories) * 100 : 0;
    const fatPercentage = totalCalories > 0 ? (fatCalories / totalCalories) * 100 : 0;

    return (
        <div className="space-y-6 w-full max-w-4xl mx-auto">
            {/* Main Results Card */}
            <Card>
                <CardHeader>
                    <CardTitle className="text-2xl font-bold text-center">Your Nutrition Recommendations</CardTitle>
                    <CardDescription className="text-center">
                        Personalized macronutrient targets for your workout
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Total Calories */}
                    <div className="text-center">
                        <div className="text-4xl font-bold text-primary">{Math.round(totalCalories)} kcal</div>
                        <div className="text-sm text-muted-foreground">Total Calories</div>
                    </div>

                    <Separator />

                    {/* Macro Breakdown */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Protein */}
                        <div className="space-y-3">
                            <div className="flex items-center justify-between">
                                <span className="font-medium">Protein</span>
                                <Badge variant="secondary">{Math.round(results.target_protein)}g</Badge>
                            </div>
                            <Progress value={proteinPercentage} className="h-2" />
                            <div className="text-xs text-muted-foreground">
                                {Math.round(proteinPercentage)}% of total calories
                            </div>
                        </div>

                        {/* Carbs */}
                        <div className="space-y-3">
                            <div className="flex items-center justify-between">
                                <span className="font-medium">Carbohydrates</span>
                                <Badge variant="secondary">{Math.round(results.target_carbs)}g</Badge>
                            </div>
                            <Progress value={carbsPercentage} className="h-2" />
                            <div className="text-xs text-muted-foreground">
                                {Math.round(carbsPercentage)}% of total calories
                            </div>
                        </div>

                        {/* Fat */}
                        <div className="space-y-3">
                            <div className="flex items-center justify-between">
                                <span className="font-medium">Fat</span>
                                <Badge variant="secondary">{Math.round(results.target_fat)}g</Badge>
                            </div>
                            <Progress value={fatPercentage} className="h-2" />
                            <div className="text-xs text-muted-foreground">
                                {Math.round(fatPercentage)}% of total calories
                            </div>
                        </div>
                    </div>

                    {/* Electrolytes */}
                    {results.target_electrolytes > 0 && (
                        <>
                            <Separator />
                            <div className="text-center">
                                <div className="text-lg font-medium">Electrolytes</div>
                                <div className="text-2xl font-bold text-blue-600">{results.target_electrolytes}g</div>
                            </div>
                        </>
                    )}
                </CardContent>
            </Card>

            {/* Timing Breakdown */}
            {(results.pre_workout_macros || results.during_workout_macros || results.post_workout_macros) && (
                <Card>
                    <CardHeader>
                        <CardTitle>Timing Breakdown</CardTitle>
                        <CardDescription>When to consume your nutrients for optimal performance</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {/* Pre-workout */}
                            {results.pre_workout_macros && (
                                <div className="space-y-3 p-4 border rounded-lg">
                                    <div className="font-medium text-green-600">Pre-workout</div>
                                    <div className="space-y-1 text-sm">
                                        <div>Carbs: {results.pre_workout_macros.carbs}g</div>
                                        <div>Protein: {results.pre_workout_macros.protein}g</div>
                                        <div>Fat: {results.pre_workout_macros.fat}g</div>
                                        <div className="font-medium">
                                            Calories: {results.pre_workout_macros.calories}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* During workout */}
                            {results.during_workout_macros && (
                                <div className="space-y-3 p-4 border rounded-lg">
                                    <div className="font-medium text-blue-600">During workout</div>
                                    <div className="space-y-1 text-sm">
                                        <div>Carbs: {results.during_workout_macros.carbs}g</div>
                                        <div>Protein: {results.during_workout_macros.protein}g</div>
                                        <div>Electrolytes: {results.during_workout_macros.electrolytes}g</div>
                                    </div>
                                </div>
                            )}

                            {/* Post-workout */}
                            {results.post_workout_macros && (
                                <div className="space-y-3 p-4 border rounded-lg">
                                    <div className="font-medium text-orange-600">Post-workout</div>
                                    <div className="space-y-1 text-sm">
                                        <div>Carbs: {results.post_workout_macros.carbs}g</div>
                                        <div>Protein: {results.post_workout_macros.protein}g</div>
                                        <div>Fat: {results.post_workout_macros.fat}g</div>
                                        <div className="font-medium">
                                            Calories: {results.post_workout_macros.calories}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* AI Reasoning */}
            <Card>
                <CardHeader>
                    <CardTitle>AI Analysis</CardTitle>
                    <CardDescription>How the recommendations were generated based on your input</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        <div className="p-4 bg-muted rounded-lg">
                            <div className="text-sm font-medium mb-2">Reasoning:</div>
                            <div className="text-sm text-muted-foreground">{results.reasoning}</div>
                        </div>

                        {results.rag_context && (
                            <div className="p-4 bg-muted rounded-lg">
                                <div className="text-sm font-medium mb-2">Sources Used:</div>
                                <div className="text-sm text-muted-foreground max-h-32 overflow-y-auto">
                                    {results.rag_context.substring(0, 500)}...
                                </div>
                            </div>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
