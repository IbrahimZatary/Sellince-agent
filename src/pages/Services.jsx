import {
  CircleHelp,
  ChevronRight,
  Gift,
  Globe2,
  Headphones,
  LifeBuoy,
  MessageCircle,
  ReceiptText,
  ShoppingBag,
  Smartphone,
  Sparkles,
  Store,
  WalletCards,
  Wifi,
} from "lucide-react";
import { ActionTile, SectionTitle } from "@/components/ServiceParts";

export function MyLine({ onUnavailable }) {
  const actions = [
    { label: "Bills & payments", Icon: ReceiptText },
    { label: "Recharge line", Icon: Smartphone },
    { label: "Internet", Icon: Wifi },
    { label: "More services", Icon: Sparkles },
  ];
  return (
    <main className="px-5 pt-6">
      <h1 className="text-3xl font-bold tracking-tight">My line</h1>
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
          Main services
        </SectionTitle>
        <div className="grid grid-cols-4 gap-3">
          {actions.map((action) => (
            <ActionTile key={action.label} {...action} onClick={onUnavailable} />
          ))}
        </div>
      </section>
      <div className="bg-lilac text-primary-foreground mt-8 rounded-2xl p-5">
        <p className="font-bold">Your opinion matters!</p>
        <p className="mt-1 text-sm leading-5">Tell us how we can make your experience better.</p>
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
      <h1 className="px-5 text-3xl font-bold tracking-tight">Marketplace</h1>
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
        <SectionTitle>Special offers</SectionTitle>
        <div className="hide-scrollbar flex gap-3 overflow-x-auto">
          <article className="border-border bg-background w-[80%] shrink-0 overflow-hidden rounded-2xl border">
            <div className="bg-primary text-primary-foreground flex h-36 items-end p-5">
              <div>
                <p className="text-[10px] font-bold tracking-widest">STAY CONNECTED</p>
                <p className="mt-2 text-2xl leading-tight font-extrabold">
                  More speed.
                  <br />
                  More possibilities.
                </p>
              </div>
            </div>
            <div className="p-4">
              <p className="font-bold">Discover fiber</p>
              <p className="text-muted-foreground mt-1 text-xs">Orange offers · Demo</p>
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
        <SectionTitle>Mobile subscriptions</SectionTitle>
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
      <h1 className="text-3xl font-bold tracking-tight">Rewards</h1>
      <section className="mt-8">
        <SectionTitle>Wheel of Fortune</SectionTitle>
        <button
          type="button"
          onClick={onUnavailable}
          className="bg-raised flex min-h-36 w-full items-center gap-5 overflow-hidden rounded-2xl p-5 text-left"
        >
          <span className="border-primary bg-yellow text-primary-foreground grid size-24 shrink-0 place-items-center rounded-full border-[10px]">
            <Gift size={35} />
          </span>
          <span className="flex-1">
            <span className="block text-xl leading-tight font-bold">
              Wheel of
              <br />
              Fortune
            </span>
            <span className="text-muted-foreground mt-2 block text-xs">
              Discover a little surprise
            </span>
          </span>
          <ChevronRight />
        </button>
      </section>
      <section className="border-border mt-8 border-t pt-7">
        <h2 className="text-xl font-bold">Orange Loyalty</h2>
        <p className="text-muted-foreground mt-2 text-sm leading-5">
          Turn your everyday moments into rewards and discover exclusive deals.
        </p>
        <div className="mt-5 grid grid-cols-2 gap-3">
          <button
            type="button"
            onClick={onUnavailable}
            className="bg-lilac text-primary-foreground flex min-h-52 flex-col justify-between rounded-2xl p-4 text-left"
          >
            <Gift size={38} />
            <span>
              <span className="block text-xl font-extrabold">
                Max it
                <br />
                Rewards
              </span>
              <span className="mt-2 block text-xs font-medium">More reasons to smile</span>
            </span>
          </button>
          <button
            type="button"
            onClick={onUnavailable}
            className="bg-mint text-primary-foreground flex min-h-52 flex-col justify-between rounded-2xl p-4 text-left"
          >
            <Sparkles size={38} />
            <span>
              <span className="block text-xl font-extrabold">
                Orange
                <br />
                Deals
              </span>
              <span className="mt-2 block text-xs font-medium">Discover everyday offers</span>
            </span>
          </button>
        </div>
      </section>
    </main>
  );
}

export function Assistance({ onNavigate, onUnavailable }) {
  const options = [
    { label: "Chat", Icon: MessageCircle, action: () => onNavigate("chat") },
    { label: "Report & track issues", Icon: CircleHelp, action: onUnavailable },
    { label: "FAQ", Icon: LifeBuoy, action: onUnavailable },
    { label: "Customer service", Icon: Headphones, action: onUnavailable },
    { label: "Orange Shops", Icon: Store, action: onUnavailable },
  ];
  return (
    <main className="px-5 pt-6">
      <h1 className="text-3xl font-bold tracking-tight">Assistance</h1>
      <div className="mt-8 flex flex-col gap-3">
        {options.map(({ label, Icon, action }) => (
          <button
            key={label}
            type="button"
            onClick={action}
            className="border-border bg-surface flex min-h-20 items-center gap-5 rounded-2xl border px-5 text-left"
          >
            <Icon size={24} className="text-primary" />
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
