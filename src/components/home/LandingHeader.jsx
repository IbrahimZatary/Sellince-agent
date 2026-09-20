import { MenuIcon } from "lucide-react";
import { Link } from "react-router";

import PillArrow from "@/components/home/PillArrow";
import SellinceLogo from "@/components/home/SellinceLogo";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

/**
 * Navigation items for page sections.
 * Only fragment links with existing section targets (e.g. id="product") are included.
 * Kept empty until corresponding section targets are implemented.
 */
const NAVIGATION_ITEMS = [];

/**
 * Renders the responsive public navigation.
 * Uses real links, closes mobile sheet upon navigation, and keeps CTA styles consistent.
 */
function LandingHeader() {
  return (
    <header className="bg-background py-4">
      <div className="grid grid-cols-2 items-center px-6 sm:px-8 lg:grid-cols-3 lg:px-12 xl:px-16">
        <Link
          to="/"
          aria-label="Sellince home"
          className="focus-visible:ring-ring/50 w-fit rounded-md focus-visible:ring-3 focus-visible:outline-none"
        >
          <SellinceLogo />
        </Link>

        {NAVIGATION_ITEMS.length > 0 ? (
          <nav
            aria-label="Primary navigation"
            className="bg-muted hidden h-13 items-center gap-6 justify-self-center rounded-full px-6 lg:flex xl:gap-8"
          >
            {NAVIGATION_ITEMS.map(({ label, href }) => (
              <a
                key={href}
                href={href}
                className="text-foreground hover:text-primary focus-visible:ring-ring/50 rounded-sm text-base font-medium whitespace-nowrap transition-colors focus-visible:ring-3 focus-visible:outline-none"
              >
                {label}
              </a>
            ))}
          </nav>
        ) : (
          <div className="hidden lg:block" aria-hidden="true" />
        )}

        <div className="hidden items-center justify-self-end gap-3 lg:flex xl:gap-4">
          <Button asChild variant="outline" className="h-12 rounded-full px-7 text-base">
            <Link to="/login">Log in</Link>
          </Button>

          <Button asChild className="h-12 rounded-full py-1.5 pr-1.5 pl-7 text-base">
            <Link to="/signup" className="gap-3">
              Get started
              <PillArrow />
            </Link>
          </Button>
        </div>

        <Sheet>
          <SheetTrigger asChild>
            <Button
              type="button"
              variant="outline"
              size="icon-lg"
              aria-label="Open navigation menu"
              className="justify-self-end rounded-full lg:hidden"
            >
              <MenuIcon aria-hidden="true" />
            </Button>
          </SheetTrigger>

          <SheetContent className="bg-background flex flex-col">
            <SheetHeader>
              <SheetTitle>Navigation</SheetTitle>
              <SheetDescription>Explore Sellince or continue to your account.</SheetDescription>
            </SheetHeader>

            {NAVIGATION_ITEMS.length > 0 ? (
              <nav aria-label="Mobile navigation" className="flex flex-col gap-1 px-4">
                {NAVIGATION_ITEMS.map(({ label, href }) => (
                  <SheetClose key={href} asChild>
                    <a
                      href={href}
                      className="text-foreground hover:bg-muted focus-visible:ring-ring/50 rounded-lg px-3 py-3 text-left text-base font-medium focus-visible:ring-3 focus-visible:outline-none"
                    >
                      {label}
                    </a>
                  </SheetClose>
                ))}
              </nav>
            ) : null}

            <div className="mt-auto flex flex-col gap-3 p-4">
              <SheetClose asChild>
                <Button asChild variant="outline" className="h-12 rounded-full text-base">
                  <Link to="/login">Log in</Link>
                </Button>
              </SheetClose>

              <SheetClose asChild>
                <Button asChild className="h-12 rounded-full py-1.5 pr-1.5 pl-7 text-base">
                  <Link to="/signup" className="gap-3">
                    Get started
                    <PillArrow />
                  </Link>
                </Button>
              </SheetClose>
            </div>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}

export default LandingHeader;
