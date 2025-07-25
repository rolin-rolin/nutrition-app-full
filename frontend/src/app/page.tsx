"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";

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
            const response = await fetch("http://localhost:8000/api/v1/macro-targets/", {
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
        <div className="min-h-screen bg-gradient-to-br from-purple-700 to-purple-900">
            {/* Hero Section */}
            <main className="flex flex-col items-center justify-center min-h-screen px-6 text-center">
                <div className="max-w-4xl">
                    {/* Logo */}
                    <div className="flex items-center justify-center space-x-2 mb-16">
                        <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                            <div className="w-4 h-4 bg-purple-700 rounded-full"></div>
                        </div>
                        <span className="text-xl font-semibold text-white">OA Recs</span>
                    </div>

                    {/* Animated Hero Text */}
                    <motion.h1
                        className="text-5xl md:text-7xl font-bold text-white mb-16 leading-tight"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1 }}
                    >
                        Fuel Your Workout
                        <br />
                        in Seconds
                    </motion.h1>

                    <motion.p
                        className="text-xl text-purple-100 mb-16 max-w-2xl mx-auto leading-relaxed"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4, duration: 1 }}
                    >
                        Get personalized nutrition box recommendations based on your workout routine, dietary
                        preferences, and fitness goals.
                    </motion.p>

                    <motion.div
                        className="flex flex-col sm:flex-row gap-6 justify-center"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.8, duration: 1 }}
                    >
                        <button className="bg-yellow-400 text-purple-900 px-12 py-5 rounded-full font-semibold hover:bg-yellow-300 transition-colors">
                            Get your Recommendation
                        </button>
                        <button className="border-2 border-white text-white px-12 py-5 rounded-full font-semibold hover:bg-white hover:text-purple-900 transition-colors">
                            How it works
                        </button>
                    </motion.div>
                </div>
            </main>

            {/* Why Choose OA Recs Section */}
            <section className="py-20 bg-gray-50">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl md:text-5xl font-bold text-purple-700 mb-6">Why Choose OA Recs?</h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Our AI-powered platform analyzes your workout data and creates nutrition recommendations
                            specifically designed for your body and goals.
                        </p>
                    </div>

                    <div className="flex flex-col md:flex-row gap-8">
                        {/* AI-Powered Analysis */}
                        <div className="bg-white rounded-lg p-8 shadow-lg text-center flex-1">
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
                        </div>

                        {/* Personalized Boxes */}
                        <div className="bg-white rounded-lg p-8 shadow-lg text-center flex-1">
                            <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-6">
                                <div className="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center">
                                    <div className="w-4 h-4 bg-white rounded-full"></div>
                                </div>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-800 mb-4">Personalized Boxes</h3>
                            <p className="text-gray-600 leading-relaxed">
                                Receive curated nutrition boxes with pre-portioned supplements and meal ingredients.
                            </p>
                        </div>

                        {/* Workout Optimization */}
                        <div className="bg-white rounded-lg p-8 shadow-lg text-center flex-1">
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
                        </div>
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section className="py-20 bg-white">
                <div className="max-w-8xl mx-auto px-12">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl md:text-5xl font-bold text-purple-700 mb-6">How It Works</h2>
                        <p className="text-xl text-gray-600">
                            Three simple steps to get your personalized nutrition recommendations
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {/* Step 1 */}
                        <div className="bg-gray-50 rounded-lg p-8 shadow-lg border text-center">
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
                        </div>
                        {/* Step 2 */}
                        <div className="bg-gray-50 rounded-lg p-8 shadow-lg border text-center">
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
                        </div>
                        {/* Step 3 */}
                        <div className="bg-gray-50 rounded-lg p-8 shadow-lg border text-center">
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
                        </div>
                    </div>
                </div>
            </section>

            {/* Get Your Personalized Recommendation Section */}
            <section className="py-20 bg-gray-50">
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
                            <div className="mt-10 p-6 rounded-lg bg-purple-50 border border-purple-200">
                                <h3 className="text-2xl font-bold text-purple-700 mb-4">Your Macro Recommendation</h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 text-gray-950">
                                    <div>
                                        <div className="font-semibold">Calories:</div>
                                        <div>{result.target_calories ?? "-"} kcal</div>
                                    </div>
                                    <div>
                                        <div className="font-semibold">Protein:</div>
                                        <div>{result.target_protein ?? "-"} g</div>
                                    </div>
                                    <div>
                                        <div className="font-semibold">Carbs:</div>
                                        <div>{result.target_carbs ?? "-"} g</div>
                                    </div>
                                    <div>
                                        <div className="font-semibold">Fat:</div>
                                        <div>{result.target_fat ?? "-"} g</div>
                                    </div>
                                    <div>
                                        <div className="font-semibold">Electrolytes:</div>
                                        <div>{result.target_electrolytes ?? "-"} g</div>
                                    </div>
                                </div>
                                {result.reasoning && (
                                    <div className="mt-4 text-gray-950">
                                        <div className="font-semibold mb-1">Reasoning:</div>
                                        <div className="whitespace-pre-line text-sm">{result.reasoning}</div>
                                    </div>
                                )}
                                {result.rag_context && (
                                    <div className="mt-4 text-gray-950">
                                        <div className="font-semibold mb-1">Context Used:</div>
                                        <div className="whitespace-pre-line text-xs">{result.rag_context}</div>
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
