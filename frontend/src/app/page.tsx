import styles from "./page.module.css";
import Header from "./Header";

export default function Home() {
    return (
        <div className="bg-white min-h-screen">
            <Header />
            {/* Hero Section */}
            <section className="w-full min-h-[50vh] flex items-center justify-center bg-[#4B0D7A]">
                <h1 className="text-5xl md:text-6xl font-bold text-white text-center leading-tight">
                    Digital Infrastructure
                    <br />
                    for Scaling Carbon Removal
                </h1>
            </section>
        </div>
    );
}
