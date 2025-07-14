import React from "react";

export default function OARecsLanding() {
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

                    <h1 className="text-5xl md:text-7xl font-bold text-white mb-16 leading-tight">
                        Fuel Your Workout
                        <br />
                        in Seconds
                    </h1>

                    <p className="text-xl text-purple-100 mb-16 max-w-2xl mx-auto leading-relaxed">
                        Get personalized nutrition box recommendations based on your workout routine, dietary
                        preferences, and fitness goals.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-6 justify-center">
                        <button className="bg-yellow-400 text-purple-900 px-12 py-5 rounded-full font-semibold hover:bg-yellow-300 transition-colors">
                            Get your Recommendation
                        </button>
                        <button className="border-2 border-white text-white px-12 py-5 rounded-full font-semibold hover:bg-white hover:text-purple-900 transition-colors">
                            How it works
                        </button>
                    </div>
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
                <div className="max-w-8xl mx-auto px-10">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl md:text-5xl font-bold text-purple-700 mb-6">How It Works</h2>
                        <p className="text-xl text-gray-600">
                            Three simple steps to get your personalized nutrition recommendations
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {/* Step 1 */}
                        <div className="bg-gray-50 rounded-lg p-8 text-center">
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
                        <div className="bg-gray-50 rounded-lg p-8 text-center">
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
                        <div className="bg-gray-50 rounded-lg p-8 text-center">
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
        </div>
    );
}
