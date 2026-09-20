import LandingHeader from "@/components/home/LandingHeader";
import LandingHero from "@/components/home/LandingHero";

/**
 * Home Page (Marketing Landing Page)
 *
 * Route entry point for `/`. Composes the responsive landing page header
 * with navigation capsule and CTA buttons, paired with the hero section
 * featuring headline typography, value proposition, and hero artwork.
 */
function Home() {
  return (
    <main className="bg-background min-h-dvh overflow-hidden">
      <LandingHeader />
      <LandingHero />
    </main>
  );
}

export default Home;
