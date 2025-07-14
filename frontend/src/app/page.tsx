import React from "react";

export default function NutriBoxLanding() {
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
                        <span className="text-xl font-semibold text-white">NutriBox AI</span>
                    </div>

                    <h1 className="text-5xl md:text-7xl font-bold text-white mb-16 leading-tight">
                        Digital Infrastructure
                        <br />
                        for Scaling Carbon
                        <br />
                        Removal
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
        </div>
    );
}
