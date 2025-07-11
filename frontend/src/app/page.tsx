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
    return (
        <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-100 flex flex-col">
            {/* Hero Section */}
            <section className="flex flex-col items-center justify-center flex-1 text-center px-4">
                <h1 className="text-5xl md:text-7xl font-extrabold tracking-tighter text-gray-950 mb-6 leading-tight">
                    Personalized Nutrition <br className="hidden md:inline" />
                    <span className="text-blue-600">Guidance</span>
                </h1>
                <p className="text-lg md:text-2xl text-gray-700 mb-8 max-w-2xl">
                    Get science-backed macro recommendations for your next workout. Built for athletes, fitness
                    enthusiasts, and anyone who wants to optimize their nutrition.
                </p>
                <a href="#recommendation-form">
                    <button className="px-8 py-3 rounded-xl bg-blue-600 text-white font-semibold shadow-lg hover:bg-blue-700 transition-colors text-lg">
                        Get Started
                    </button>
                </a>
            </section>

            {/* Features Section */}
            <section className="w-full max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 py-16 px-4">
                <div className="bg-white rounded-2xl shadow-lg p-8 flex flex-col items-center text-center">
                    <span className="text-4xl mb-4">🎯</span>
                    <h3 className="font-bold text-xl mb-2">Personalized</h3>
                    <p className="text-gray-600">Recommendations tailored to your age, weight, and workout type.</p>
                </div>
                <div className="bg-white rounded-2xl shadow-lg p-8 flex flex-col items-center text-center">
                    <span className="text-4xl mb-4">🧠</span>
                    <h3 className="font-bold text-xl mb-2">AI-Powered</h3>
                    <p className="text-gray-600">Advanced AI analyzes your needs using scientific guidelines.</p>
                </div>
                <div className="bg-white rounded-2xl shadow-lg p-8 flex flex-col items-center text-center">
                    <span className="text-4xl mb-4">⚡</span>
                    <h3 className="font-bold text-xl mb-2">Instant</h3>
                    <p className="text-gray-600">Get detailed recommendations in seconds, not hours.</p>
                </div>
            </section>

            {/* (Optional) Add more sections here, such as testimonials, logos, or a footer */}
        </main>
    );
}
