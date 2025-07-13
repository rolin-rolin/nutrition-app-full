import Image from "next/image";
// import { Moon } from "lucide-react"; // Uncomment if lucide-react is installed

export default function Header() {
    return (
        <header className="w-full bg-white shadow-sm">
            <div className="max-w-screen-xl mx-auto px-6 h-16 flex items-center justify-between">
                {/* Left: Logo */}
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-[#3D005E] rounded-full flex items-center justify-center">
                        <Image src="/apple.svg" alt="NutriBox AI Logo" width={20} height={20} />
                    </div>
                    <span className="text-lg font-semibold text-[#3D005E]">NutriBox AI</span>
                </div>

                {/* Center: Navigation */}
                <nav className="hidden md:flex gap-6 text-gray-800 font-medium">
                    <a href="#features" className="hover:text-[#3D005E]">
                        Features
                    </a>
                    <a href="#how-it-works" className="hover:text-[#3D005E]">
                        How It Works
                    </a>
                    <a href="#pricing" className="hover:text-[#3D005E]">
                        Pricing
                    </a>
                    <a href="#contact" className="hover:text-[#3D005E]">
                        Contact
                    </a>
                </nav>

                {/* Right: Auth buttons + toggle */}
                <div className="flex items-center gap-4">
                    <a href="/login" className="text-gray-800 hover:text-[#3D005E]">
                        Log In
                    </a>
                    <a href="/signup" className="bg-[#3D005E] text-white px-4 py-2 rounded-md hover:opacity-90">
                        Sign Up
                    </a>
                    <button className="text-gray-800 hover:text-[#3D005E]">
                        {/* <Moon size={18} /> */}
                        <span role="img" aria-label="moon">
                            🌙
                        </span>
                    </button>
                </div>
            </div>
        </header>
    );
}
