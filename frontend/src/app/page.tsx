"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Variants } from "framer-motion";
import Image from "next/image";
import { AuroraText } from "@/components/magicui/aurora-text";
import { Particles } from "@/components/magicui/particles";

// TypeScript interfaces for type safety
interface MacroTargets {
    target_calories?: number;
    target_protein?: number;
    target_carbs?: number;
    target_fat?: number;
    target_electrolytes?: number;
}

interface Product {
    id: number;
    name: string;
    brand: string;
    flavor?: string;
    texture?: string;
    form?: string;
    price_usd?: number;
    protein_g?: number;
    carbs_g?: number;
    fat_g?: number;
    calories?: number;
    electrolytes_mg?: number;
    image_url?: string;
    link?: string;
    description?: string;
    protein?: number;
    carbs?: number;
    fat?: number;
}

interface BundleStats {
    total_protein: number;
    total_carbs: number;
    total_fat: number;
    total_calories: number;
    total_electrolytes: number;
}

interface PreferenceInfo {
    soft_prefs: string[];
    hard_filters: string[];
}

interface RecommendationResult {
    macro_targets?: MacroTargets;
    user_profile?: {
        age?: number;
        weight_kg?: number;
        height_cm?: number;
        activity_level?: string;
        fitness_goal?: string;
        age_display?: string;
        weight_display?: string;
        exercise_display?: string;
    };
    recommended_products: Product[];
    bundle_stats: BundleStats;
    applied_preferences: PreferenceInfo;
    key_principles: string[];
    recommendation_reasoning: string;
    preferences?: {
        soft_preferences?: string[];
        hard_filters?: string[];
    };
    reasoning?: string;
    timing_breakdown?: {
        pre_workout?: {
            carbs?: number;
            protein?: number;
            fat?: number;
            calories?: number;
        };
        during_workout?: {
            carbs?: number;
            protein?: number;
            electrolytes?: number;
            calories?: number;
        };
        post_workout?: {
            carbs?: number;
            protein?: number;
            fat?: number;
            calories?: number;
        };
        general?: string[];
    };
}

const fadeInUp: Variants = {
    hidden: {
        opacity: 0,
        y: 20,
    },
    visible: {
        opacity: 1,
        y: 0,
        transition: {
            duration: 0.6,
            ease: "easeOut",
        },
    },
};

const staggerChildren: Variants = {
    hidden: {},
    visible: {
        transition: {
            staggerChildren: 0.1,
        },
    },
};

export default function OARecsLanding() {
    // State for textarea, loading, error, and result
    const [userQuery, setUserQuery] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<RecommendationResult | null>(null);

    // Handler for Generate Recommendation
    const handleGenerate = async () => {
        setLoading(true);
        setError(null);
        setResult(null);
        try {
            const backendUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

            const response = await fetch(`${backendUrl}/api/v1/recommend/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_query: userQuery }),
            });

            if (!response.ok) {
                const err = await response.json().catch(() => ({}));
                throw new Error(err.detail || "Failed to get recommendation");
            }

            const data: RecommendationResult = await response.json();
            setResult(data);
        } catch (err: unknown) {
            const errorMessage = err instanceof Error ? err.message : "Unknown error";
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    // Handler for Clear
    const handleClear = () => {
        setUserQuery("");
        setResult(null);
        setError(null);
    };

    return (
        <div className="min-h-screen bg-white">
            {/* Hero Section */}

            <div className="min-h-screen bg-white relative">
                {/* Particles Background */}
                <Particles className="absolute inset-0 z-0" quantity={150} ease={75} color="#8B5CF6" size={2} refresh />

                {/* Hero Section */}
                <main className="relative overflow-hidden h-[500px] w-full flex flex-col items-center justify-center min-h-screen px-6 text-center z-10">
                    <div className="max-w-4xl">
                        {/* Logo - Centered and Large, with fade-in animation */}
                        <motion.div
                            className="flex items-center justify-center mb-2"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0 }}
                        >
                            <Image src="/transparent.png" alt="OA Recs Logo" className="w-90 h-60 object-contain" />
                        </motion.div>

                        {/* Animated Hero Text */}
                        <motion.h1
                            className="text-5xl md:text-7xl font-bold mb-8 leading-tight"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 1 }}
                        >
                            Fuel Your Workout
                            <br />
                            in{" "}
                            <em>
                                <AuroraText>Seconds</AuroraText>
                            </em>
                        </motion.h1>

                        <motion.p
                            className="text-xl text-black mb-16 max-w-2xl mx-auto leading-relaxed"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 2.0, duration: 0.5 }}
                        >
                            Get personalized nutrition box recommendations based on your workout routine, dietary
                            preferences, and fitness goals.
                        </motion.p>

                        <motion.div
                            className="flex flex-col sm:flex-row gap-6 justify-center"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 2.0, duration: 0.5 }}
                        >
                            <button
                                className="border-3 border-purple-700 text-purple-700 px-12 py-5 rounded-full font-bold hover:bg-purple-700 hover:text-white transition-colors"
                                onClick={() => {
                                    document.getElementById("recommendation-section")?.scrollIntoView({
                                        behavior: "smooth",
                                        block: "center",
                                    });
                                }}
                            >
                                Get your Recommendation
                            </button>
                            <button
                                className="border-3 border-purple-700 text-purple-700 px-12 py-5 rounded-full font-bold hover:bg-purple-700 hover:text-white transition-colors"
                                onClick={() => {
                                    document.getElementById("how-it-works-section")?.scrollIntoView({
                                        behavior: "smooth",
                                        block: "center",
                                    });
                                }}
                            >
                                How it works
                            </button>
                        </motion.div>
                    </div>
                </main>
            </div>

            {/* Why Choose OA Recs Section */}
            <section className="py-20 bg-gray-50">
                <div className="max-w-6xl mx-auto px-6">
                    <motion.div
                        className="text-center mb-16"
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        viewport={{ once: true }}
                    >
                        <h2 className="text-4xl md:text-5xl font-bold text-purple-700 mb-6">Why Choose OA Recs?</h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            OA Recs uses International Society of Sports Nutrition (ISSN) guidelines (science!) to
                            calculate <b>exact</b> macronutrient targets that you should hit.
                        </p>
                    </motion.div>

                    <div className="flex flex-col md:flex-row gap-8">
                        {/* AI-Powered Analysis */}
                        <motion.div
                            className="bg-white rounded-lg p-8 shadow-lg text-center flex-1"
                            initial={{ opacity: 0, y: 50 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.5 }}
                            viewport={{ once: true }}
                            whileHover={{
                                y: -10,
                                scale: 1.05,
                                transition: {
                                    duration: 0.2,
                                    type: "spring",
                                    stiffness: 800,
                                    damping: 40,
                                },
                            }}
                        >
                            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                <div className="w-8 h-8 bg-purple-700 rounded-full flex items-center justify-center">
                                    <div className="w-4 h-4 bg-white rounded-full"></div>
                                </div>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-4">Macronutrient Analysis</h3>
                            <p className="text-gray-600 leading-relaxed">
                                Get concrete macronutrient targets you should hit through our research-backed
                                &quot;macro-targeting&quot; algorithm.
                            </p>
                        </motion.div>

                        {/* Personalized Boxes */}
                        <motion.div
                            className="bg-white rounded-lg p-8 shadow-lg text-center flex-1"
                            initial={{ opacity: 0, y: 50 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 1 }}
                            viewport={{ once: true }}
                            whileHover={{
                                y: -10,
                                scale: 1.05,
                                transition: {
                                    duration: 0.2,
                                    type: "spring",
                                    stiffness: 800,
                                    damping: 40,
                                },
                            }}
                        >
                            <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                <div className="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center">
                                    <div className="w-4 h-4 bg-white rounded-full"></div>
                                </div>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-4">Personalized Boxes</h3>
                            <p className="text-gray-600 leading-relaxed">
                                Receive curated nutrition boxes that, together, hit your targets and follow your
                                preferences.
                            </p>
                        </motion.div>

                        {/* Workout Optimization */}
                        <motion.div
                            className="bg-white rounded-lg p-8 shadow-lg text-center flex-1"
                            initial={{ opacity: 0, y: 50 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 1.5 }}
                            viewport={{ once: true }}
                            whileHover={{
                                y: -10,
                                scale: 1.05,
                                transition: {
                                    duration: 0.2,
                                    type: "spring",
                                    stiffness: 800,
                                    damping: 40,
                                },
                            }}
                        >
                            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                <div className="w-8 h-8 bg-blue-400 rounded-full flex items-center justify-center">
                                    <div className="w-4 h-4 bg-white rounded-full"></div>
                                </div>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-4">Workout Optimization</h3>
                            <p className="text-gray-600 leading-relaxed">
                                Maximize your workout results with nutrition that complements your specific exercise
                                routine.
                            </p>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section id="how-it-works-section" className="py-20 bg-white">
                <div className="max-w-8xl mx-auto px-12">
                    <motion.div
                        className="text-center mb-16"
                        initial={{ opacity: 0, scale: 0.8 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.8, type: "spring", bounce: 0.3 }}
                        viewport={{ once: true }}
                    >
                        <h2 className="text-4xl md:text-5xl font-bold text-purple-700 mb-6">How It Works</h2>
                        <p className="text-xl text-gray-600">
                            Four simple steps to get your personalized nutrition recommendations.
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
                        {/* Step 1 */}
                        <motion.div
                            className="bg-gray-50 rounded-lg p-6 shadow-lg border text-center max-w-lg mx-auto"
                            initial={{ opacity: 0, scale: 0.8 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            transition={{
                                duration: 0.8,
                                delay: 0.2,
                                type: "spring",
                                bounce: 0.3,
                            }}
                            viewport={{ once: true }}
                            whileHover={{
                                y: -10,
                                scale: 1.05,
                                transition: {
                                    duration: 0.3,
                                    type: "spring",
                                    stiffness: 700,
                                    damping: 25,
                                },
                            }}
                        >
                            <div className="w-16 h-16 bg-purple-700 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-white font-bold text-xl">1</span>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-3">AI-Powered Consultation</h3>
                            <p className="text-gray-600 leading-relaxed mb-4">
                                Tell us about yourself, your workout routine, and preferences for snacks just as you
                                would to a real dietitian.
                            </p>
                            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto">
                                <svg className="w-6 h-6 text-purple-700" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                </svg>
                            </div>
                        </motion.div>

                        {/* Step 2 */}
                        <motion.div
                            className="bg-gray-50 rounded-lg p-6 shadow-lg border text-center max-w-lg mx-auto"
                            initial={{ opacity: 0, scale: 0.8 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            transition={{
                                duration: 0.8,
                                delay: 0.4,
                                type: "spring",
                                bounce: 0.3,
                            }}
                            viewport={{ once: true }}
                            whileHover={{
                                y: -10,
                                scale: 1.05,
                                transition: {
                                    duration: 0.3,
                                    type: "spring",
                                    stiffness: 700,
                                    damping: 25,
                                },
                            }}
                        >
                            <div className="w-16 h-16 bg-purple-700 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-white font-bold text-xl">2</span>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-3">Macronutrient Targets</h3>
                            <p className="text-gray-600 leading-relaxed mb-4">
                                Our algorithm calculates your exact macronutrient targets based on your age, weight,
                                exercise, and snack preferences.
                            </p>
                            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto">
                                <svg className="w-6 h-6 text-purple-700" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M13 7H7v6h6V7z" />
                                    <path
                                        fillRule="evenodd"
                                        d="M7 2a1 1 0 012 0v1h2V2a1 1 0 112 0v1h2a2 2 0 012 2v2h1a1 1 0 110 2h-1v2h1a1 1 0 110 2h-1v2a2 2 0 01-2 2h-2v1a1 1 0 11-2 0v-1H9v1a1 1 0 11-2 0v-1H5a2 2 0 01-2-2v-2H2a1 1 0 110-2h1V9H2a1 1 0 010-2h1V5a2 2 0 012-2h2V2zM5 5v10h10V5H5z"
                                        clipRule="evenodd"
                                    />
                                </svg>
                            </div>
                        </motion.div>

                        {/* Step 3 */}
                        <motion.div
                            className="bg-gray-50 rounded-lg p-6 shadow-lg border text-center max-w-lg mx-auto"
                            initial={{ opacity: 0, scale: 0.8 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            transition={{
                                duration: 0.8,
                                delay: 0.6,
                                type: "spring",
                                bounce: 0.3,
                            }}
                            viewport={{ once: true }}
                            whileHover={{
                                y: -10,
                                scale: 1.05,
                                transition: {
                                    duration: 0.3,
                                    type: "spring",
                                    stiffness: 700,
                                    damping: 25,
                                },
                            }}
                        >
                            <div className="w-16 h-16 bg-purple-700 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-white font-bold text-xl">3</span>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-3">Recommendation Engine</h3>
                            <p className="text-gray-600 leading-relaxed mb-4">
                                The engine takes in your targets and preferences and does a similarity search against
                                its product database.
                            </p>
                            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto">
                                <svg className="w-6 h-6 text-purple-700" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M5 4a2 2 0 00-2 2v1h14V6a2 2 0 00-2-2H5zM3 9v6a2 2 0 002 2h10a2 2 0 002-2V9H3z" />
                                </svg>
                            </div>
                        </motion.div>

                        {/* Step 4 */}
                        <motion.div
                            className="bg-gray-50 rounded-lg p-6 shadow-lg border text-center max-w-lg mx-auto"
                            initial={{ opacity: 0, scale: 0.8 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            transition={{
                                duration: 0.8,
                                delay: 0.8,
                                type: "spring",
                                bounce: 0.3,
                            }}
                            viewport={{ once: true }}
                            whileHover={{
                                y: -10,
                                scale: 1.05,
                                transition: {
                                    duration: 0.3,
                                    type: "spring",
                                    stiffness: 700,
                                    damping: 25,
                                },
                            }}
                        >
                            <div className="w-16 h-16 bg-purple-700 rounded-full flex items-center justify-center mx-auto mb-4">
                                <span className="text-white font-bold text-xl">4</span>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-3">Enjoy Your Personalized Nutrition</h3>
                            <p className="text-gray-600 leading-relaxed mb-4">
                                Get an assortment of snacks that hit your macronutrient targets and fit your
                                preferences!
                            </p>
                            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto">
                                <svg className="w-6 h-6 text-purple-700" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                        fillRule="evenodd"
                                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                        clipRule="evenodd"
                                    />
                                </svg>
                            </div>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* Get Your Personalized Recommendation Section */}
            <section id="recommendation-section" className="min-h-screen bg-gray-50 flex items-center">
                <div className="max-w-screen-lg mx-auto px-4 sm:px-6 lg:px-8 w-full py-12">
                    <div className="text-center mb-12">
                        <h2 className="text-4xl md:text-5xl font-bold text-purple-700 mb-6">
                            Get Your Personalized Recommendation
                        </h2>
                        <p className="text-xl text-gray-600 mb-8">
                            Tell me about you and your next workout! Be sure to enter:
                        </p>

                        <div className="flex flex-col items-center text-center gap-4 md:grid md:grid-cols-2 md:text-left md:items-start max-w-2xl mx-auto mb-12">
                            <div className="flex items-center space-x-3">
                                <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                        fillRule="evenodd"
                                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                        clipRule="evenodd"
                                    />
                                </svg>
                                <span className="text-gray-700">What workout/exercise you&apos;re doing</span>
                            </div>
                            <div className="flex items-center space-x-3">
                                <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                        fillRule="evenodd"
                                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                        clipRule="evenodd"
                                    />
                                </svg>
                                <span className="text-gray-700">Duration of workout</span>
                            </div>
                            <div className="flex items-center space-x-3">
                                <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                        fillRule="evenodd"
                                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                        clipRule="evenodd"
                                    />
                                </svg>
                                <span className="text-gray-700">Age and Bodyweight</span>
                            </div>
                            <div className="flex items-center space-x-3">
                                <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                        fillRule="evenodd"
                                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                        clipRule="evenodd"
                                    />
                                </svg>
                                <span className="text-gray-700">Dietary restrictions and/or taste preferences</span>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg shadow-lg p-8">
                        <label className="block text-gray-700 text-lg font-semibold mb-4">
                            Describe your workout routine:
                        </label>
                        <textarea
                            className="w-full h-40 p-4 border border-gray-300 rounded-lg resize-none text-black focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent placeholder-gray-400"
                            placeholder="I do strength training 3 times a week focusing on upper body and legs. I also run 5km twice a week and practice yoga on Sundays..."
                            value={userQuery}
                            onChange={(e) => setUserQuery(e.target.value)}
                        />

                        <div className="flex flex-col sm:flex-row gap-4 mt-6">
                            <button
                                className="bg-purple-700 text-white px-8 py-3 rounded-full font-semibold hover:bg-purple-800 transition-colors flex items-center justify-center disabled:opacity-60"
                                onClick={handleGenerate}
                                disabled={loading || !userQuery.trim()}
                            >
                                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                </svg>
                                {loading ? "Generating..." : "Generate Recommendation"}
                            </button>
                            <button
                                className="border border-gray-300 text-gray-700 px-8 py-3 rounded-full font-semibold hover:bg-gray-50 transition-colors flex items-center justify-center"
                                onClick={handleClear}
                                disabled={loading && !userQuery}
                            >
                                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path
                                        fillRule="evenodd"
                                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                        clipRule="evenodd"
                                    />
                                </svg>
                                Clear
                            </button>
                        </div>

                        {/* Error Message */}
                        {error && <div className="mt-6 text-red-600 font-semibold text-center">{error}</div>}

                        {/* Result Display */}
                        {result && (
                            <motion.div
                                className="mt-10 space-y-6"
                                initial="hidden"
                                animate="visible"
                                variants={staggerChildren}
                            >
                                {/* User Profile */}
                                {result.user_profile ? (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">Your Profile</h3>
                                        <motion.div
                                            className="grid grid-cols-2 md:grid-cols-4 gap-4 text-gray-950"
                                            variants={staggerChildren}
                                            initial="hidden"
                                            whileInView="visible"
                                            viewport={{ once: true }}
                                        >
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold text-sm">Age:</div>
                                                <div>{result.user_profile.age_display}</div>
                                            </motion.div>
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold text-sm">Weight:</div>
                                                <div>{result.user_profile.weight_display}</div>
                                            </motion.div>
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold text-sm">Exercise:</div>
                                                <div>{result.user_profile.exercise_display}</div>
                                            </motion.div>
                                        </motion.div>
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">Your Profile</h3>
                                        <div className="text-sm text-gray-600">No profile data available</div>
                                    </motion.div>
                                )}

                                {/* Macro Targets */}
                                {result.macro_targets ? (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">
                                            Your Macro Targets
                                            {result.timing_breakdown && (
                                                <span className="ml-2 text-sm font-normal text-purple-600">
                                                    (ℹ️ Hover for timing breakdown)
                                                </span>
                                            )}
                                        </h3>
                                        <motion.div
                                            className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-4 text-gray-950"
                                            variants={staggerChildren}
                                            initial="hidden"
                                            whileInView="visible"
                                            viewport={{ once: true }}
                                        >
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold">Calories:</div>
                                                <div>{result.macro_targets.target_calories ?? "-"}</div>
                                            </motion.div>
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold">Protein:</div>
                                                <div>{result.macro_targets.target_protein ?? "-"} g</div>
                                            </motion.div>
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold">Carbs:</div>
                                                <div>{result.macro_targets.target_carbs ?? "-"} g</div>
                                            </motion.div>
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold">Fat:</div>
                                                <div>{result.macro_targets.target_fat ?? "-"} g</div>
                                            </motion.div>
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold">Electrolytes:</div>
                                                <div>{result.macro_targets.target_electrolytes ?? "-"} mg</div>
                                            </motion.div>
                                        </motion.div>

                                        {/* Timing Breakdown Tooltip */}
                                        {result.timing_breakdown && (
                                            <motion.div
                                                className="mt-4 p-4 bg-white rounded-lg border border-purple-300"
                                                initial={{ opacity: 0 }}
                                                whileInView={{ opacity: 1 }}
                                                viewport={{ once: true }}
                                                transition={{ duration: 0.5, delay: 0.2 }}
                                            >
                                                <h4 className="font-semibold text-purple-700 mb-2">
                                                    Timing Breakdown:
                                                </h4>
                                                <motion.div
                                                    className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm"
                                                    variants={staggerChildren}
                                                    initial="hidden"
                                                    whileInView="visible"
                                                    viewport={{ once: true }}
                                                >
                                                    {result.timing_breakdown.pre_workout && (
                                                        <motion.div variants={fadeInUp}>
                                                            <div className="font-semibold text-green-700">
                                                                Pre-workout:
                                                            </div>
                                                            <div className="text-gray-700">
                                                                {result.timing_breakdown.pre_workout.carbs &&
                                                                    `${result.timing_breakdown.pre_workout.carbs}g carbs, `}
                                                                {result.timing_breakdown.pre_workout.protein &&
                                                                    `${result.timing_breakdown.pre_workout.protein}g protein, `}
                                                                {result.timing_breakdown.pre_workout.fat &&
                                                                    `${result.timing_breakdown.pre_workout.fat}g fat, `}
                                                                {result.timing_breakdown.pre_workout.calories &&
                                                                    `${result.timing_breakdown.pre_workout.calories} cals`}
                                                            </div>
                                                        </motion.div>
                                                    )}
                                                    {result.timing_breakdown.during_workout && (
                                                        <motion.div variants={fadeInUp}>
                                                            <div className="font-semibold text-blue-700">
                                                                During workout:
                                                            </div>
                                                            <div className="text-gray-700">
                                                                {result.timing_breakdown.during_workout.carbs &&
                                                                    `${result.timing_breakdown.during_workout.carbs}g carbs, `}
                                                                {result.timing_breakdown.during_workout.protein &&
                                                                    `${result.timing_breakdown.during_workout.protein}g protein, `}
                                                                {result.timing_breakdown.during_workout.electrolytes &&
                                                                    `${result.timing_breakdown.during_workout.electrolytes}mg electrolytes, `}
                                                                {result.timing_breakdown.during_workout.calories &&
                                                                    `${result.timing_breakdown.during_workout.calories} cals`}
                                                            </div>
                                                        </motion.div>
                                                    )}
                                                    {result.timing_breakdown.post_workout && (
                                                        <motion.div variants={fadeInUp}>
                                                            <div className="font-semibold text-orange-700">
                                                                Post-workout:
                                                            </div>
                                                            <div className="text-gray-700">
                                                                {result.timing_breakdown.post_workout.carbs &&
                                                                    `${result.timing_breakdown.post_workout.carbs}g carbs, `}
                                                                {result.timing_breakdown.post_workout.protein &&
                                                                    `${result.timing_breakdown.post_workout.protein}g protein, `}
                                                                {result.timing_breakdown.post_workout.fat &&
                                                                    `${result.timing_breakdown.post_workout.fat}g fat, `}
                                                                {result.timing_breakdown.post_workout.calories &&
                                                                    `${result.timing_breakdown.post_workout.calories} cals`}
                                                            </div>
                                                        </motion.div>
                                                    )}
                                                </motion.div>
                                            </motion.div>
                                        )}
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">Your Macro Targets</h3>
                                        <div className="text-sm text-gray-600">No macro targets available</div>
                                    </motion.div>
                                )}

                                {/* Bundle Stats */}
                                {result.bundle_stats ? (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">Bundle Summary</h3>
                                        <motion.div
                                            className="grid grid-cols-2 md:grid-cols-5 gap-4 text-gray-950"
                                            variants={staggerChildren}
                                            initial="hidden"
                                            whileInView="visible"
                                            viewport={{ once: true }}
                                        >
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold">Total Calories:</div>
                                                <div>{result.bundle_stats.total_calories}</div>
                                            </motion.div>
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold">Total Protein:</div>
                                                <div>{result.bundle_stats.total_protein} g</div>
                                            </motion.div>
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold">Total Carbs:</div>
                                                <div>{result.bundle_stats.total_carbs} g</div>
                                            </motion.div>
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold">Total Fat:</div>
                                                <div>{result.bundle_stats.total_fat} g</div>
                                            </motion.div>
                                            <motion.div variants={fadeInUp}>
                                                <div className="font-semibold">Total Electrolytes:</div>
                                                <div>{result.bundle_stats.total_electrolytes} mg</div>
                                            </motion.div>
                                        </motion.div>
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">Bundle Summary</h3>
                                        <div className="text-sm text-gray-600">No bundle stats available</div>
                                    </motion.div>
                                )}

                                {/* Recommended Products */}
                                {result.recommended_products && result.recommended_products.length > 0 && (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">
                                            Recommended Products ({result.recommended_products.length})
                                        </h3>
                                        <motion.div
                                            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
                                            variants={staggerChildren}
                                            initial="hidden"
                                            whileInView="visible"
                                            viewport={{ once: true }}
                                        >
                                            {result.recommended_products.map((product, index) => (
                                                <motion.div
                                                    key={index}
                                                    className="bg-white p-4 rounded-lg border border-gray-200"
                                                    variants={fadeInUp}
                                                >
                                                    {/* Product Image */}
                                                    {product.image_url && (
                                                        <div className="mb-3">
                                                            <Image
                                                                src={product.image_url}
                                                                alt={product.name}
                                                                className="w-full h-32 object-contain rounded-lg"
                                                                onError={(e) => {
                                                                    e.currentTarget.style.display = "none";
                                                                }}
                                                            />
                                                        </div>
                                                    )}

                                                    <h4 className="font-semibold text-gray-800 mb-2">{product.name}</h4>
                                                    <div className="text-sm text-gray-700 mb-2">
                                                        {product.description}
                                                    </div>
                                                    <div className="grid grid-cols-2 gap-2 text-xs text-gray-700">
                                                        <div>
                                                            <span className="font-semibold">Protein:</span>{" "}
                                                            {product.protein}g
                                                        </div>
                                                        <div>
                                                            <span className="font-semibold">Carbs:</span>{" "}
                                                            {product.carbs}g
                                                        </div>
                                                        <div>
                                                            <span className="font-semibold">Fat:</span> {product.fat}g
                                                        </div>
                                                        <div>
                                                            <span className="font-semibold">Calories:</span>{" "}
                                                            {product.calories}
                                                        </div>
                                                        <div className="col-span-2">
                                                            <span className="font-semibold">Electrolytes:</span>{" "}
                                                            {product.electrolytes_mg ?? "-"} mg
                                                        </div>
                                                    </div>

                                                    {/* Product Link */}
                                                    {product.link && (
                                                        <div className="mt-3 text-blue-600 hover:text-blue-800 text-xs font-semibold underline">
                                                            <a
                                                                href={product.link}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                            >
                                                                View Product →
                                                            </a>
                                                        </div>
                                                    )}
                                                </motion.div>
                                            ))}
                                        </motion.div>
                                    </motion.div>
                                )}

                                {/* Preferences */}
                                {result.preferences ? (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">Applied Preferences</h3>
                                        <div className="space-y-2">
                                            {result.preferences.soft_preferences &&
                                            result.preferences.soft_preferences.length > 0 ? (
                                                <div>
                                                    <div className="font-semibold text-sm text-indigo-600">
                                                        Soft Preferences:
                                                    </div>
                                                    <div className="text-sm text-gray-700">
                                                        {result.preferences.soft_preferences.join(", ")}
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="text-sm text-gray-600">No soft preferences applied</div>
                                            )}
                                            {result.preferences.hard_filters &&
                                            result.preferences.hard_filters.length > 0 ? (
                                                <div>
                                                    <div className="font-semibold text-sm text-indigo-600">
                                                        Hard Filters:
                                                    </div>
                                                    <div className="text-sm text-gray-700">
                                                        {result.preferences.hard_filters.join(", ")}
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="text-sm text-gray-600">No hard filters applied</div>
                                            )}
                                        </div>
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">Applied Preferences</h3>
                                        <div className="text-sm text-gray-600">No preferences data available</div>
                                    </motion.div>
                                )}

                                {/* Key Principles */}
                                {result.key_principles && result.key_principles.length > 0 ? (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">
                                            Key Nutrition Principles
                                        </h3>
                                        <motion.div
                                            className="space-y-2"
                                            variants={staggerChildren}
                                            initial="hidden"
                                            whileInView="visible"
                                            viewport={{ once: true }}
                                        >
                                            {result.key_principles.map((principle, index) => (
                                                <motion.div
                                                    key={index}
                                                    className="flex items-start space-x-2"
                                                    variants={fadeInUp}
                                                >
                                                    <div className="w-2 h-2 bg-pink-400 rounded-full mt-2 flex-shrink-0"></div>
                                                    <div className="text-sm text-gray-700">{principle}</div>
                                                </motion.div>
                                            ))}
                                        </motion.div>
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">
                                            Key Nutrition Principles
                                        </h3>
                                        <div className="text-sm text-gray-600">
                                            No key principles available for this recommendation.
                                        </div>
                                    </motion.div>
                                )}

                                {/* Reasoning */}
                                {result.reasoning && (
                                    <motion.div
                                        className="p-6 rounded-lg bg-white border border-gray-200"
                                        variants={fadeInUp}
                                        whileInView="visible"
                                        initial="hidden"
                                        viewport={{ once: true, margin: "-50px" }}
                                    >
                                        <h3 className="text-xl font-bold text-gray-800 mb-4">
                                            Recommendation Reasoning
                                        </h3>
                                        <div className="text-gray-700 whitespace-pre-line">{result.reasoning}</div>
                                    </motion.div>
                                )}
                            </motion.div>
                        )}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-gray-800 text-white py-6">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="text-center">
                        <div className="flex items-center justify-center space-x-2 mb-2">
                            <div className="w-20 h-20 flex items-center justify-center">
                                <Image src="/transparent.png" alt="OA Recs Logo" className="w-20 h-20 object-contain" />
                            </div>
                        </div>
                        <p className="text-gray-400 text-sm mb-3">
                            Personalized nutrition recommendations for your fitness goals.
                        </p>
                        <p className="text-gray-400 text-sm">&copy; 2025 OA Packs. All rights reserved.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
}
