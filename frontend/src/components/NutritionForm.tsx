"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { NutritionFormData } from "@/types/nutrition";

interface NutritionFormProps {
    onSubmit: (data: NutritionFormData) => void;
    isLoading: boolean;
}

export function NutritionForm({ onSubmit, isLoading }: NutritionFormProps) {
    const [formData, setFormData] = useState<NutritionFormData>({
        user_query: "",
        age: "",
        weight_kg: "",
        sex: "",
        exercise_type: "",
        exercise_duration_minutes: "",
        exercise_intensity: "",
        timing: "",
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    };

    const handleInputChange = (field: keyof NutritionFormData, value: string) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
    };

    const quickQueries = [
        "I just finished a 45-minute weights workout",
        "I'm about to do 30 minutes of cardio",
        "I completed a 90-minute strength training session",
        "I'm going for a 60-minute run",
    ];

    const handleQuickQuery = (query: string) => {
        setFormData((prev) => ({ ...prev, user_query: query }));
    };

    return (
        <Card className="w-full max-w-2xl mx-auto">
            <CardHeader>
                <CardTitle className="text-2xl font-bold text-center">Get Personalized Nutrition Advice</CardTitle>
                <CardDescription className="text-center">
                    Tell us about your workout and get tailored macronutrient recommendations
                </CardDescription>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Quick Query Suggestions */}
                    <div className="space-y-3">
                        <label className="text-sm font-medium">Quick Start</label>
                        <div className="flex flex-wrap gap-2">
                            {quickQueries.map((query, index) => (
                                <Badge
                                    key={index}
                                    variant="outline"
                                    className="cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors"
                                    onClick={() => handleQuickQuery(query)}
                                >
                                    {query}
                                </Badge>
                            ))}
                        </div>
                    </div>

                    {/* User Query */}
                    <div className="space-y-2">
                        <label htmlFor="user_query" className="text-sm font-medium">
                            Describe your workout
                        </label>
                        <Textarea
                            id="user_query"
                            placeholder="e.g., I just finished a 45-minute weights workout and I'm looking for post-workout nutrition advice..."
                            value={formData.user_query}
                            onChange={(e) => handleInputChange("user_query", e.target.value)}
                            className="min-h-[100px]"
                            required
                        />
                    </div>

                    {/* Personal Details */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="space-y-2">
                            <label htmlFor="age" className="text-sm font-medium">
                                Age
                            </label>
                            <Input
                                id="age"
                                type="number"
                                placeholder="25"
                                value={formData.age}
                                onChange={(e) => handleInputChange("age", e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <label htmlFor="weight" className="text-sm font-medium">
                                Weight (kg)
                            </label>
                            <Input
                                id="weight"
                                type="number"
                                placeholder="70"
                                value={formData.weight_kg}
                                onChange={(e) => handleInputChange("weight_kg", e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <label htmlFor="sex" className="text-sm font-medium">
                                Sex
                            </label>
                            <Select value={formData.sex} onValueChange={(value) => handleInputChange("sex", value)}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="male">Male</SelectItem>
                                    <SelectItem value="female">Female</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    {/* Workout Details */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="space-y-2">
                            <label htmlFor="exercise_type" className="text-sm font-medium">
                                Exercise Type
                            </label>
                            <Input
                                id="exercise_type"
                                placeholder="weights, cardio, running..."
                                value={formData.exercise_type}
                                onChange={(e) => handleInputChange("exercise_type", e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <label htmlFor="duration" className="text-sm font-medium">
                                Duration (minutes)
                            </label>
                            <Input
                                id="duration"
                                type="number"
                                placeholder="45"
                                value={formData.exercise_duration_minutes}
                                onChange={(e) => handleInputChange("exercise_duration_minutes", e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <label htmlFor="intensity" className="text-sm font-medium">
                                Intensity
                            </label>
                            <Select
                                value={formData.exercise_intensity}
                                onValueChange={(value) => handleInputChange("exercise_intensity", value)}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="low">Low</SelectItem>
                                    <SelectItem value="moderate">Moderate</SelectItem>
                                    <SelectItem value="high">High</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    {/* Timing */}
                    <div className="space-y-2">
                        <label htmlFor="timing" className="text-sm font-medium">
                            Nutrition Timing
                        </label>
                        <Select value={formData.timing} onValueChange={(value) => handleInputChange("timing", value)}>
                            <SelectTrigger>
                                <SelectValue placeholder="Select timing" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="pre-workout">Pre-workout</SelectItem>
                                <SelectItem value="during-workout">During workout</SelectItem>
                                <SelectItem value="post-workout">Post-workout</SelectItem>
                                <SelectItem value="general">General advice</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    {/* Submit Button */}
                    <Button type="submit" className="w-full" disabled={isLoading || !formData.user_query.trim()}>
                        {isLoading ? "Generating Recommendations..." : "Get Nutrition Advice"}
                    </Button>
                </form>
            </CardContent>
        </Card>
    );
}
