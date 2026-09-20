import { Link } from "react-router";

import conversationArtwork from "@/assets/images/sellince-conversation-hero.png";
import PillArrow from "@/components/home/PillArrow";
import { Button } from "@/components/ui/button";

/**
 * LandingHero Component
 *
 * Hero section of the marketing landing page:
 * - Brand eyebrow tag ("CONVERSATION INTELLIGENCE").
 * - Responsive display headline with controlled line wrapping.
 * - Supporting product value proposition.
 * - Primary CTA ("Start a conversation" -> `/login`) and secondary CTA ("See how it works").
 * - Hero conversation screenshot illustration with responsive positioning.
 */
function LandingHero() {
  return (
    <section aria-labelledby="landing-title" className="bg-background">
      <div className="grid min-h-[calc(100svh-6rem)] grid-cols-1 px-6 py-6 sm:px-8 sm:py-8 lg:grid-cols-[38%_62%] lg:items-center lg:gap-8 lg:px-12 lg:pt-16 lg:pb-20 xl:grid-cols-[36%_64%] xl:gap-12 xl:px-16">
        <div className="relative z-10 max-w-xl">
          <p className="text-primary tracking-label mb-6 text-sm font-semibold uppercase">
            Conversation intelligence
          </p>
          <h1
            id="landing-title"
            className="text-foreground text-hero md:text-hero-md xl:text-hero-xl 2xl:text-hero-2xl font-medium tracking-tighter text-balance"
          >
            <span className="lg:block">Understand the</span>{" "}
            <span className="lg:block">customer behind</span>{" "}
            <span className="lg:block">every message.</span>
          </h1>
          <p className="text-muted-foreground mt-6 max-w-[540px] text-lg leading-7 text-pretty lg:mt-7">
            Sellince turns questions, needs, and objections into relevant conversations that move
            customers forward.
          </p>
          <div className="mt-6 flex flex-col items-stretch gap-4 sm:flex-row sm:items-center lg:mt-7">
            <Button asChild className="h-13 gap-3 rounded-full py-1.5 pr-1.5 pl-7 text-base">
              <Link to="/login">
                Start a conversation
                <PillArrow />
              </Link>
            </Button>
            <Button type="button" variant="outline" className="h-13 rounded-full px-7 text-base">
              See how it works
            </Button>
          </div>
        </div>

        <div className="flex min-h-80 items-center justify-center sm:min-h-96 lg:min-h-0 lg:justify-end lg:self-center">
          <img
            src={conversationArtwork}
            alt=""
            data-testid="hero-artwork"
            className="w-hero sm:w-hero-sm lg:max-h-hero-max h-auto max-w-none object-contain lg:w-full lg:max-w-4xl"
          />
        </div>
      </div>
    </section>
  );
}

export default LandingHero;
