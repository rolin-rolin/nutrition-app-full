"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import { AuroraText } from "@/components/magicui/aurora-text";
import { Particles } from "@/components/magicui/particles";

export default function OARecsLanding() {
    // State for textarea, loading, error, and result
    const [userQuery, setUserQuery] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<any>(null);

    // Handler for Generate Recommendation
    const handleGenerate = async () => {
        setLoading(true);
        setError(null);
        setResult(null);
        try {
            const response = await fetch("http://localhost:8000/api/v1/recommend/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_query: userQuery }),
            });

            if (!response.ok) {
                const err = await response.json().catch(() => ({}));
                throw new Error(err.detail || "Failed to get recommendation");
            }

            const data = await response.json();
            setResult(data);
        } catch (err: any) {
            setError(err.message || "Unknown error");
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
                <Particles className="absolute inset-0 z-0" quantity={100} ease={70} color="#8B5CF6" size={2} refresh />

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
                            <img src="/just-lion.png" alt="OA Recs Logo" className="w-90 h-60 object-contain" />
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
                            className="text-xl text-purple-600 mb-16 max-w-2xl mx-auto leading-relaxed font-semibold"
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
                            Our AI-powered platform analyzes your workout data and creates nutrition recommendations
                            specifically designed for your body and goals.
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
                            <h3 className="text-2xl font-bold text-gray-800 mb-4">AI-Powered Analysis</h3>
                            <p className="text-gray-600 leading-relaxed">
                                Our advanced algorithms analyze your workout data to create perfectly balanced nutrition
                                plans.
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
                                Receive curated nutrition boxes with pre-portioned supplements and meal ingredients.
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
                            Three simple steps to get your personalized nutrition recommendations
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {/* Step 1 */}
                        <motion.div
                            className="bg-gray-50 rounded-lg p-8 shadow-lg border text-center"
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
                            <div className="w-16 h-16 bg-purple-700 rounded-full flex items-center justify-center mx-auto mb-6">
                                <span className="text-white font-bold text-xl">1</span>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-4">Smart Consultation</h3>
                            <p className="text-gray-600 leading-relaxed mb-6">
                                Tell us about yourself, your workout routine, and preferences for snacks.
                            </p>
                            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto">
                                <svg className="w-6 h-6 text-purple-700" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                </svg>
                            </div>
                        </motion.div>

                        {/* Step 2 */}
                        <motion.div
                            className="bg-gray-50 rounded-lg p-8 shadow-lg border text-center"
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
                            <div className="w-16 h-16 bg-purple-700 rounded-full flex items-center justify-center mx-auto mb-6">
                                <span className="text-white font-bold text-xl">2</span>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-4">Macronutrient Targets</h3>
                            <p className="text-gray-600 leading-relaxed mb-6">
                                Our AI analyzes your input and generates Macronutrient Targets for you to hit.
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
                            className="bg-gray-50 rounded-lg p-8 shadow-lg border text-center"
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
                            <div className="w-16 h-16 bg-purple-700 rounded-full flex items-center justify-center mx-auto mb-6">
                                <span className="text-white font-bold text-xl">3</span>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-4">Get Your Snack Recommendations</h3>
                            <p className="text-gray-600 leading-relaxed mb-6">
                                Get an assortment of snacks that hit your macronutrient targets and fit your
                                preferences!
                            </p>
                            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto">
                                <svg className="w-6 h-6 text-purple-700" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M5 4a2 2 0 00-2 2v1h14V6a2 2 0 00-2-2H5zM3 9v6a2 2 0 002 2h10a2 2 0 002-2V9H3z" />
                                </svg>
                            </div>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* Get Your Personalized Recommendation Section */}
            <section id="recommendation-section" className="py-20 bg-gray-50">
                <div className="max-w-screen-lg mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-12">
                        <h2 className="text-4xl md:text-5xl font-bold text-purple-700 mb-6">
                            Get Your Personalized Recommendation
                        </h2>
                        <p className="text-xl text-gray-600 mb-8">
                            Tell me about you and your next workout! Include information about:
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
                                <span className="text-gray-700">What workout/exercise you're doing</span>
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
                                <span className="text-gray-700">Dietary restrictions or taste preferences</span>
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
                            <div className="mt-10 space-y-6">
                                {/* User Profile */}
                                {result.user_profile ? (
                                    <div className="p-6 rounded-lg bg-blue-50 border border-blue-200">
                                        <h3 className="text-xl font-bold text-blue-700 mb-4">Your Profile</h3>
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-gray-950">
                                            <div>
                                                <div className="font-semibold text-sm">Age:</div>
                                                <div>{result.user_profile.age_display}</div>
                                            </div>
                                            <div>
                                                <div className="font-semibold text-sm">Weight:</div>
                                                <div>{result.user_profile.weight_display}</div>
                                            </div>
                                            <div>
                                                <div className="font-semibold text-sm">Exercise:</div>
                                                <div>{result.user_profile.exercise_display}</div>
                                            </div>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="p-6 rounded-lg bg-blue-50 border border-blue-200">
                                        <h3 className="text-xl font-bold text-blue-700 mb-4">Your Profile</h3>
                                        <div className="text-sm text-gray-600">No profile data available</div>
                                    </div>
                                )}

                                {/* Macro Targets */}
                                {result.macro_targets ? (
                                    <div className="p-6 rounded-lg bg-purple-50 border border-purple-200">
                                        <h3 className="text-xl font-bold text-purple-700 mb-4">
                                            Your Macro Targets
                                            {result.timing_breakdown && (
                                                <span className="ml-2 text-sm font-normal text-purple-600">
                                                    (ℹ️ Hover for timing breakdown)
                                                </span>
                                            )}
                                        </h3>
                                        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-4 text-gray-950">
                                            <div>
                                                <div className="font-semibold">Calories:</div>
                                                <div>{result.macro_targets.target_calories ?? "-"}</div>
                                            </div>
                                            <div>
                                                <div className="font-semibold">Protein:</div>
                                                <div>{result.macro_targets.target_protein ?? "-"} g</div>
                                            </div>
                                            <div>
                                                <div className="font-semibold">Carbs:</div>
                                                <div>{result.macro_targets.target_carbs ?? "-"} g</div>
                                            </div>
                                            <div>
                                                <div className="font-semibold">Fat:</div>
                                                <div>{result.macro_targets.target_fat ?? "-"} g</div>
                                            </div>
                                            <div>
                                                <div className="font-semibold">Electrolytes:</div>
                                                <div>{result.macro_targets.target_electrolytes ?? "-"} mg</div>
                                            </div>
                                        </div>

                                        {/* Timing Breakdown Tooltip */}
                                        {result.timing_breakdown && (
                                            <div className="mt-4 p-4 bg-white rounded-lg border border-purple-300">
                                                <h4 className="font-semibold text-purple-700 mb-2">
                                                    Timing Breakdown:
                                                </h4>
                                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                                                    {result.timing_breakdown.pre_workout && (
                                                        <div>
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
                                                        </div>
                                                    )}
                                                    {result.timing_breakdown.during_workout && (
                                                        <div>
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
                                                        </div>
                                                    )}
                                                    {result.timing_breakdown.post_workout && (
                                                        <div>
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
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                ) : (
                                    <div className="p-6 rounded-lg bg-purple-50 border border-purple-200">
                                        <h3 className="text-xl font-bold text-purple-700 mb-4">Your Macro Targets</h3>
                                        <div className="text-sm text-gray-600">No macro targets available</div>
                                    </div>
                                )}

                                {/* Recommended Products */}
                                {result.recommended_products && result.recommended_products.length > 0 && (
                                    <div className="p-6 rounded-lg bg-green-50 border border-green-200">
                                        <h3 className="text-xl font-bold text-green-700 mb-4">
                                            Recommended Products ({result.recommended_products.length})
                                        </h3>
                                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                            {result.recommended_products.map((product: any, index: number) => (
                                                <div
                                                    key={index}
                                                    className="bg-white p-4 rounded-lg border border-green-300"
                                                >
                                                    {/* Product Image */}
                                                    {product.image_url && (
                                                        <div className="mb-3">
                                                            <img
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
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Bundle Stats */}
                                {result.bundle_stats ? (
                                    <div className="p-6 rounded-lg bg-yellow-50 border border-yellow-200">
                                        <h3 className="text-xl font-bold text-yellow-700 mb-4">Bundle Summary</h3>
                                        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-gray-950">
                                            <div>
                                                <div className="font-semibold">Total Calories:</div>
                                                <div>{result.bundle_stats.total_calories}</div>
                                            </div>
                                            <div>
                                                <div className="font-semibold">Total Protein:</div>
                                                <div>{result.bundle_stats.total_protein} g</div>
                                            </div>
                                            <div>
                                                <div className="font-semibold">Total Carbs:</div>
                                                <div>{result.bundle_stats.total_carbs} g</div>
                                            </div>
                                            <div>
                                                <div className="font-semibold">Total Fat:</div>
                                                <div>{result.bundle_stats.total_fat} g</div>
                                            </div>
                                            <div>
                                                <div className="font-semibold">Total Electrolytes:</div>
                                                <div>{result.bundle_stats.total_electrolytes} mg</div>
                                            </div>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="p-6 rounded-lg bg-yellow-50 border border-yellow-200">
                                        <h3 className="text-xl font-bold text-yellow-700 mb-4">Bundle Summary</h3>
                                        <div className="text-sm text-gray-600">No bundle stats available</div>
                                    </div>
                                )}

                                {/* Preferences */}
                                {result.preferences ? (
                                    <div className="p-6 rounded-lg bg-indigo-50 border border-indigo-200">
                                        <h3 className="text-xl font-bold text-indigo-700 mb-4">Applied Preferences</h3>
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
                                    </div>
                                ) : (
                                    <div className="p-6 rounded-lg bg-indigo-50 border border-indigo-200">
                                        <h3 className="text-xl font-bold text-indigo-700 mb-4">Applied Preferences</h3>
                                        <div className="text-sm text-gray-600">No preferences data available</div>
                                    </div>
                                )}

                                {/* Key Principles */}
                                {result.key_principles && result.key_principles.length > 0 ? (
                                    <div className="p-6 rounded-lg bg-pink-50 border border-pink-200">
                                        <h3 className="text-xl font-bold text-pink-700 mb-4">
                                            Key Nutrition Principles
                                        </h3>
                                        <div className="space-y-2">
                                            {result.key_principles.map((principle: any, index: number) => (
                                                <div key={index} className="flex items-start space-x-2">
                                                    <div className="w-2 h-2 bg-pink-400 rounded-full mt-2 flex-shrink-0"></div>
                                                    <div className="text-sm text-gray-700">{principle.principle}</div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ) : (
                                    <div className="p-6 rounded-lg bg-pink-50 border border-pink-200">
                                        <h3 className="text-xl font-bold text-pink-700 mb-4">
                                            Key Nutrition Principles
                                        </h3>
                                        <div className="text-sm text-gray-600">
                                            No key principles available for this recommendation.
                                        </div>
                                    </div>
                                )}

                                {/* Reasoning */}
                                {result.reasoning && (
                                    <div className="p-6 rounded-lg bg-gray-50 border border-gray-200">
                                        <h3 className="text-xl font-bold text-gray-700 mb-4">
                                            Recommendation Reasoning
                                        </h3>
                                        <div className="text-gray-700 whitespace-pre-line">{result.reasoning}</div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-gray-800 text-white py-12">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="text-center">
                        <div className="flex items-center justify-center space-x-2 mb-4">
                            <div className="w-8 h-8 bg-purple-700 rounded-full flex items-center justify-center">
                                <div className="w-4 h-4 bg-white rounded-full"></div>
                            </div>
                            <span className="text-xl font-semibold">OA Recs</span>
                        </div>
                        <p className="text-gray-400 mb-8">
                            AI-powered nutrition recommendations for your fitness goals.
                        </p>
                    </div>

                    <div className="border-t border-gray-700 pt-8 text-center text-gray-400">
                        <p>&copy; 2025 OA Recs. All rights reserved.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
}
