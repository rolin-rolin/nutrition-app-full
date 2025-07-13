import Image from "next/image";
import styles from "./page.module.css";
import Header from "./Header";

export default function Home() {
    return (
        <div className={styles.page}>
            <Header />
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
