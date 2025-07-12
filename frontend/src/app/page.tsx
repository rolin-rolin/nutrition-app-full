import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
    return (
        <div className={styles.page}>
            {/* Navbar/Header */}
            <nav className={styles.navbar}>
                <div className={styles.navLeft}>
                    <Image src="/apple.svg" alt="NutriBox AI Logo" width={40} height={40} className={styles.navLogo} />
                    <span className={styles.navBrand}>NutriBox AI</span>
                </div>
                <div className={styles.navLinks}>
                    <a href="#features" className={styles.navLink}>
                        Features
                    </a>
                    <a href="#how" className={styles.navLink}>
                        How It Works
                    </a>
                    <a href="#pricing" className={styles.navLink}>
                        Pricing
                    </a>
                    <a href="#contact" className={styles.navLink}>
                        Contact
                    </a>
                </div>
                <div className={styles.navAuth}>
                    <button className={styles.navLogin}>Log In</button>
                    <button className={styles.navSignUp}>Sign Up</button>
                    <button className={styles.navDarkToggle} aria-label="Toggle dark mode">
                        🌙
                    </button>
                </div>
            </nav>

            {/* Hero Section */}
            <section className={styles.hero}>
                <div className={styles.heroContent}>
                    <h1 className={styles.heroTitle}>
                        AI-Powered Nutrition
                        <br />
                        Tailored to Your Workout Needs
                    </h1>
                    <div className={styles.heroSubtitle}>
                        Get personalized nutrition box recommendations based on your workout routine, dietary
                        preferences, and fitness goals.
                    </div>
                    <div className={styles.heroButtons}>
                        <button className={styles.heroPrimaryBtn}>
                            <span role="img" aria-label="magic">
                                ✨
                            </span>{" "}
                            Get Your Recommendation
                        </button>
                        <button className={styles.heroSecondaryBtn}>
                            <span role="img" aria-label="play">
                                ▶️
                            </span>{" "}
                            How It Works
                        </button>
                    </div>
                </div>
                <div className={styles.heroImage}>
                    {/* Placeholder for hero image */}
                    <Image src="/file.svg" alt="Nutrition Box" width={320} height={320} />
                </div>
            </section>
        </div>
    );
}
