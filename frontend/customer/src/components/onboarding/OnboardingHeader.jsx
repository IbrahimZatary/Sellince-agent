import { Button } from "@/components/ui/button";
import SellinceLogo from "@/components/home/SellinceLogo";

/**
 * OnboardingHeader Component
 *
 * Header bar for the onboarding flow:
 * - Sellince brand logo.
 * - Current user avatar initials and account label.
 * - Sign out button trigger.
 */
function OnboardingHeader({ accountLabel, accountInitials, onSignOut }) {
  return (
    <header className="border-border/60 bg-background h-18 border-b md:h-20">
      <div className="flex size-full items-center justify-between px-5 md:px-8 lg:px-14">
        <SellinceLogo />

        <div className="flex items-center gap-2 sm:gap-3">
          <span
            className="bg-muted text-foreground flex size-10 items-center justify-center rounded-full text-sm font-medium"
            aria-hidden="true"
          >
            {accountInitials}
          </span>
          <span className="sr-only sm:not-sr-only sm:text-sm sm:font-medium">{accountLabel}</span>
          <Button
            type="button"
            variant="ghost"
            className="text-muted-foreground"
            onClick={onSignOut}
          >
            Sign out
          </Button>
        </div>
      </div>
    </header>
  );
}

export default OnboardingHeader;
