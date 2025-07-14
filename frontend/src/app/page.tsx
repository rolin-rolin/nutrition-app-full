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

            {/* Why Choose OA Packs AI Section */}
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
        </div>
    );
}
