import { cn } from "@/lib/utils";
import maxitLogo from "@/assets/maxit/maxit-logo.png";
import searchIcon from "@/assets/maxit/header-search.png";
import notificationIcon from "@/assets/maxit/header-notification.png";
import helpIcon from "@/assets/maxit/header-help.png";
import profileIcon from "@/assets/maxit/header-profile.png";
import homeIcon from "@/assets/maxit/nav-home.png";
import lineIcon from "@/assets/maxit/nav-line.png";
import shopIcon from "@/assets/maxit/nav-shop.png";
import moneyIcon from "@/assets/maxit/nav-money.png";
import rewardsIcon from "@/assets/maxit/nav-rewards.png";

const NAVIGATION = [
  { id: "home", label: "Home", icon: homeIcon },
  { id: "line", label: "My line", icon: lineIcon },
  { id: "marketplace", label: "Marketplace", icon: shopIcon },
  { id: "money", label: "Orange Money", icon: moneyIcon },
  { id: "rewards", label: "Rewards", icon: rewardsIcon },
];

export function MobileHeader({ onNavigate, onUnavailable, onSignOut }) {
  return (
    <header className="safe-top bg-background sticky top-0 z-10">
      <div className="flex h-14 items-center justify-between px-4">
        <button
          type="button"
          onClick={() => onNavigate("home")}
          aria-label="Go to home"
          className="size-7 shrink-0"
        >
          <img src={maxitLogo} alt="" className="size-full" />
        </button>
        <div className="text-foreground flex items-center gap-5">
          <button
            type="button"
            onClick={onUnavailable}
            aria-label="Search"
            className="grid size-9 place-items-center"
          >
            <img src={searchIcon} alt="" className="size-6" />
          </button>
          <button
            type="button"
            onClick={onUnavailable}
            aria-label="Notifications"
            className="grid size-9 place-items-center"
          >
            <img src={notificationIcon} alt="" className="size-6" />
          </button>
          <button
            type="button"
            onClick={() => onNavigate("assistance")}
            aria-label="Assistance"
            className="grid size-9 place-items-center"
          >
            <img src={helpIcon} alt="" className="size-6" />
          </button>
          <button
            type="button"
            onClick={onSignOut}
            aria-label="Exit preview"
            className="grid size-9 place-items-center rounded-full"
          >
            <img src={profileIcon} alt="" className="size-9" />
          </button>
        </div>
      </div>
    </header>
  );
}

export function BottomNavigation({ currentScreen, onNavigate }) {
  return (
    <nav
      aria-label="Main navigation"
      className="safe-bottom border-border bg-surface fixed inset-x-0 bottom-0 z-10 mx-auto w-full max-w-[480px] border-t"
    >
      <div className="grid grid-cols-5 items-start px-1 pt-2 pb-2">
        {NAVIGATION.map(({ id, label, icon }) => (
          <button
            key={id}
            type="button"
            onClick={() => onNavigate(id)}
            aria-label={label}
            aria-current={currentScreen === id ? "page" : undefined}
            className="text-foreground flex min-h-16 min-w-0 flex-col items-center gap-1 text-[9px] font-medium"
          >
            <span
              className={cn(
                "grid h-8 w-14 place-items-center rounded-full",
                currentScreen === id && "bg-raised text-primary",
              )}
            >
              <img src={icon} alt="" className={cn("size-6 max-w-full", currentScreen === id ? "maxit-icon-selected" : "maxit-icon")} />
            </span>
            <span className="max-w-full px-0.5 text-center leading-tight [overflow-wrap:anywhere]">{label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
}
