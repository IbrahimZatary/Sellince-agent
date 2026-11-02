import {
  Bell,
  CircleHelp,
  Gift,
  House,
  Search,
  ShoppingBag,
  Smartphone,
  LogOut,
  WalletCards,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAVIGATION = [
  { id: "home", label: "Home", Icon: House },
  { id: "line", label: "My line", Icon: Smartphone },
  { id: "marketplace", label: "Shop", accessibleLabel: "Marketplace", Icon: ShoppingBag },
  { id: "money", label: "Money", accessibleLabel: "Orange Money", Icon: WalletCards },
  { id: "rewards", label: "Rewards", Icon: Gift },
];

export function MobileHeader({ onNavigate, onUnavailable, onSignOut }) {
  return (
    <header className="safe-top bg-background sticky top-0 z-10">
      <div className="flex h-16 items-center justify-between px-5">
        <button
          type="button"
          onClick={() => onNavigate("home")}
          aria-label="Go to home"
          className="bg-primary text-primary-foreground flex size-10 items-end rounded-sm p-1 text-[9px] font-bold tracking-tight whitespace-nowrap"
        >
          Max it
        </button>
        <div className="text-foreground flex items-center gap-5">
          <button
            type="button"
            onClick={onUnavailable}
            aria-label="Search"
            className="grid size-9 place-items-center"
          >
            <Search size={23} />
          </button>
          <button
            type="button"
            onClick={onUnavailable}
            aria-label="Notifications"
            className="grid size-9 place-items-center"
          >
            <Bell size={23} />
          </button>
          <button
            type="button"
            onClick={() => onNavigate("assistance")}
            aria-label="Assistance"
            className="grid size-9 place-items-center"
          >
            <CircleHelp size={23} />
          </button>
          <button
            type="button"
            onClick={onSignOut}
            aria-label="Exit preview"
            className="bg-raised grid size-9 place-items-center rounded-full"
          >
            <LogOut size={21} />
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
        {NAVIGATION.map(({ id, label, accessibleLabel, Icon }) => (
          <button
            key={id}
            type="button"
            onClick={() => onNavigate(id)}
            aria-label={accessibleLabel || label}
            aria-current={currentScreen === id ? "page" : undefined}
            className="text-foreground flex min-h-16 min-w-0 flex-col items-center gap-1 text-[10px] font-medium"
          >
            <span
              className={cn(
                "grid h-8 w-14 place-items-center rounded-full",
                currentScreen === id && "bg-raised text-primary",
              )}
            >
              <Icon size={22} strokeWidth={2} />
            </span>
            <span className="max-w-full px-0.5 text-center leading-tight [overflow-wrap:anywhere]">{label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
}
