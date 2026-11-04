import {
  ChevronRight,
  Globe2,
  ShoppingBag,
  Smartphone,
  Sparkles,
  WalletCards,
} from "lucide-react";
import { ActionTile, SectionTitle } from "@/components/ServiceParts";
import billIcon from "@/assets/maxit/quick-bill.png";
import topupIcon from "@/assets/maxit/quick-topup.png";
import safeIcon from "@/assets/maxit/quick-safe.png";
import wheelImage from "@/assets/maxit/reward-wheel.png";
import pointsImage from "@/assets/maxit/reward-points.png";
import dealsImage from "@/assets/maxit/reward-deals.png";
import chatIcon from "@/assets/maxit/assist-chat.png";
import helpIcon from "@/assets/maxit/assist-help.png";
import faqIcon from "@/assets/maxit/assist-faq.png";
import serviceIcon from "@/assets/maxit/assist-service.png";
import shopsIcon from "@/assets/maxit/assist-shops.png";
import fiberCampaign from "@/assets/maxit/fiber-campaign.jpg";
import orangeLogo from "@/assets/maxit/orange-logo.png";

export function MyLine({ onUnavailable }) {
  const actions = [
    { label: "Bills & Orange Taqseet", imageSrc: billIcon },
    { label: "Recharge Line", imageSrc: topupIcon },
    { label: "Safe Internet", imageSrc: safeIcon },
    { label: "OSN", Icon: Sparkles },
  ];
  return (
    <main className="px-5 pt-6">
      <h1 className="text-2xl font-bold tracking-tight">My line</h1>
      <div className="mt-8 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="bg-raised grid size-12 place-items-center rounded-xl">
            <Smartphone size={23} />
          </span>
          <div>
            <p className="text-sm font-bold">Your mobile line</p>
            <p className="text-muted-foreground text-xs">Demo account</p>
          </div>
        </div>
        <button type="button" onClick={onUnavailable} className="text-xs font-semibold">
          Other lines <span aria-hidden="true">⌄</span>
        </button>
      </div>
      <div className="bg-surface mt-8 rounded-2xl p-6 text-center">
        <p className="text-muted-foreground text-sm">Main balance</p>
        <p className="mt-2 text-3xl font-bold">
          — <span className="text-sm font-medium">JOD</span>
        </p>
        <p className="text-muted-foreground mt-2 text-xs">Account not connected</p>
      </div>
      <section className="mt-8">
        <SectionTitle action="See all" onAction={onUnavailable}>
          Main Services
        </SectionTitle>
        <div className="grid grid-cols-4 gap-3">
          {actions.map((action) => (
            <ActionTile key={action.label} {...action} onClick={onUnavailable} />
          ))}
        </div>
      </section>
      <div className="bg-lilac text-primary-foreground mt-8 rounded-2xl p-5">
        <p className="font-bold">Your opinion matters!</p>
        <p className="mt-1 text-sm leading-5">Please take one minute from your time to answer this short survey to improve the services and meet your expectations.</p>
      </div>
      <section className="mt-8">
        <SectionTitle>Remaining balance</SectionTitle>
        <p className="border-border text-muted-foreground rounded-2xl border p-5 text-sm">
          Your usage will appear here when your account is connected.
        </p>
      </section>
    </main>
  );
}

export function Marketplace({ onUnavailable }) {
  return (
    <main className="pt-6">
      <h1 className="px-5 text-2xl font-bold tracking-tight">Marketplace</h1>
      <div className="hide-scrollbar mt-6 flex gap-2 overflow-x-auto px-5 pb-1">
        <span className="bg-foreground text-background shrink-0 rounded-full px-5 py-2 text-sm font-semibold">
          Discover
        </span>
        <button
          type="button"
          onClick={onUnavailable}
          className="border-border bg-surface shrink-0 rounded-full border px-5 py-2 text-sm font-semibold"
        >
          Orange offers
        </button>
        <button
          type="button"
          onClick={onUnavailable}
          className="border-border bg-surface shrink-0 rounded-full border px-5 py-2 text-sm font-semibold"
        >
          Mobile services
        </button>
      </div>
      <div className="px-5 py-7">
        <div className="border-primary bg-raised grid size-16 place-items-center rounded-full border-2">
          <ShoppingBag size={27} />
        </div>
        <p className="mt-2 text-xs font-medium">
          Discover
          <br />
          more
        </p>
      </div>
      <section className="bg-surface px-5 py-7">
        <SectionTitle>Special Offers</SectionTitle>
        <div className="hide-scrollbar flex gap-3 overflow-x-auto">
          <article className="border-border bg-surface w-[75%] shrink-0 overflow-hidden rounded-xl border">
            <div className="bg-background flex h-40 overflow-hidden">
              <img src={fiberCampaign} alt="" className="h-full w-[42%] object-cover object-right" />
              <div className="flex min-w-0 flex-1 flex-col justify-center gap-2 p-3">
                <img src={orangeLogo} alt="" className="size-6 object-contain" />
                <p className="text-primary text-xs leading-tight font-bold">Spending time at home just got better</p>
                <p className="text-[10px] leading-tight font-medium">Discover Orange Fiber offers for your home.</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-4">
              <span className="bg-primary grid size-10 shrink-0 place-items-center rounded-lg"><img src={safeIcon} alt="" className="size-7 object-contain" /></span>
              <span><span className="block text-sm font-semibold">Fiber offers</span><span className="mt-1 block text-xs">Orange Offers</span></span>
            </div>
          </article>
          <article className="border-border bg-background w-[65%] shrink-0 overflow-hidden rounded-2xl border">
            <div className="bg-lilac text-primary-foreground grid h-36 place-items-center">
              <Smartphone size={54} />
            </div>
            <div className="p-4">
              <p className="font-bold">Mobile offers</p>
              <p className="text-muted-foreground mt-1 text-xs">Orange offers · Demo</p>
            </div>
          </article>
        </div>
      </section>
      <section className="px-5 py-7">
        <SectionTitle>Mobile Subscriptions Content</SectionTitle>
        <div className="bg-raised flex items-center gap-4 rounded-2xl p-5">
          <Globe2 size={26} className="text-primary" />
          <div>
            <p className="font-semibold">Discover more with Max it</p>
            <p className="text-muted-foreground mt-1 text-xs">
              Services for every day, all in one place.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}

export function Rewards({ onUnavailable }) {
  return (
    <main className="px-5 pt-6">
      <h1 className="text-2xl font-bold tracking-tight">Rewards</h1>
      <section className="mt-8">
        <SectionTitle>Wheel Of Fortune 🎡</SectionTitle>
        <button
          type="button"
          onClick={onUnavailable}
          className="w-full overflow-hidden rounded-2xl text-left"
        >
          <img src={wheelImage} alt="Wheel of Fortune" className="block w-full" />
        </button>
      </section>
      <section className="border-border mt-8 border-t pt-7">
        <h2 className="text-xl font-bold">Orange Loyalty</h2>
        <p className="mt-2 text-sm leading-5">
          Turn your spending into rewards with Max it Rewards and discover Orange partner deals.
        </p>
        <div className="mt-5 grid grid-cols-2 gap-3">
          <button
            type="button"
            onClick={onUnavailable}
            className="overflow-hidden rounded-2xl text-left"
          >
            <img src={pointsImage} alt="Max it Rewards" className="block w-full" />
          </button>
          <button
            type="button"
            onClick={onUnavailable}
            className="overflow-hidden rounded-2xl text-left"
          >
            <img src={dealsImage} alt="Orange Deals" className="block w-full" />
          </button>
        </div>
      </section>
    </main>
  );
}

export function Assistance({ onNavigate, onUnavailable }) {
  const options = [
    { label: "Chat", icon: chatIcon, action: () => onNavigate("chat") },
    { label: "Report & track issues", icon: helpIcon, action: onUnavailable },
    { label: "FAQ", icon: faqIcon, action: onUnavailable },
    { label: "Customer service", icon: serviceIcon, action: onUnavailable },
    { label: "Orange Shops", icon: shopsIcon, action: onUnavailable },
  ];
  return (
    <main className="px-5 pt-6">
      <h1 className="text-2xl font-bold tracking-tight">Assistance</h1>
      <div className="mt-8 flex flex-col gap-3">
        {options.map(({ label, icon, action }) => (
          <button
            key={label}
            type="button"
            onClick={action}
            className="border-border bg-surface flex min-h-20 items-center gap-5 rounded-2xl border px-5 text-left"
          >
            <img src={icon} alt="" className="size-7 shrink-0 object-contain" />
            <span className="flex-1 text-base font-semibold">{label}</span>
            <ChevronRight size={20} />
          </button>
        ))}
      </div>
    </main>
  );
}

export function Money() {
  return (
    <main className="px-5 pt-6">
      <h1 className="text-3xl font-bold tracking-tight">Orange Money</h1>
      <div className="bg-surface mt-8 rounded-2xl p-6">
        <WalletCards size={30} className="text-primary" />
        <h2 className="mt-5 text-xl font-bold">Your wallet, in one place</h2>
        <p className="text-muted-foreground mt-2 text-sm leading-6">
          Wallet services are not connected in this demo.
        </p>
      </div>
    </main>
  );
}
