import {
  ArrowRight,
  CircleDollarSign,
  Gift,
  Globe2,
  Play,
  Smartphone,
  Sparkles,
  WalletCards,
  X,
} from "lucide-react";
import { ActionTile, SectionTitle } from "@/components/ServiceParts";
import SellinceMark from "@/components/chat/SellinceMark";

const QUICK_ACTIONS = [
  { label: "Recharge line", Icon: CircleDollarSign },
  { label: "Buy mobile line", Icon: Smartphone },
  { label: "Orange Extra", Icon: Play },
  { label: "Money transfer", Icon: WalletCards },
];

export default function Home({
  assistantSuggestion,
  isAssistantCardVisible,
  onAssistantCardDismiss,
  onNavigate,
  onUnavailable,
}) {
  return (
    <main>
      <section className="bg-surface px-5 pt-6 pb-7">
        <p className="text-muted-foreground text-xs font-medium">YOUR SPACE, ALL IN ONE PLACE</p>
        <h1 className="mt-1 text-2xl font-bold tracking-tight">Welcome to Max it</h1>
        <p className="text-muted-foreground mt-1 text-xs">Your everyday essentials, together.</p>
        <div className="hide-scrollbar mt-5 flex gap-3 overflow-x-auto pb-1">
          <article className="bg-raised min-w-[46%] flex-1 rounded-2xl p-4">
            <Smartphone className="text-primary" size={22} />
            <p className="mt-4 text-sm font-semibold">My line balance</p>
            <p className="mt-2 text-lg font-bold">
              — <span className="text-xs font-normal">JOD</span>
            </p>
            <p className="text-muted-foreground mt-1 text-[10px]">Demo account</p>
          </article>
          <article className="bg-raised min-w-[46%] flex-1 rounded-2xl p-4">
            <WalletCards className="text-primary" size={22} />
            <p className="mt-4 text-sm font-semibold">My wallet</p>
            <p className="mt-2 text-lg font-bold">
              — <span className="text-xs font-normal">JOD</span>
            </p>
            <p className="text-muted-foreground mt-1 text-[10px]">Not connected</p>
          </article>
        </div>
      </section>
      {isAssistantCardVisible && (
        <section aria-label="Sellince suggestion" className="px-5 pt-6">
          <div className="border-border bg-surface flex items-start gap-3 rounded-2xl border p-4">
            <span className="bg-raised text-primary grid size-11 shrink-0 place-items-center rounded-xl">
              <SellinceMark />
            </span>
            <div className="min-w-0 flex-1">
              <p className="text-sm font-bold">Sellince <span className="text-muted-foreground font-normal">· {assistantSuggestion ? "A suggestion for you" : "Chat preview"}</span></p>
              <p dir="auto" className="mt-2 text-sm leading-5">
                {assistantSuggestion ? assistantSuggestion.content : "Explore the assistant. Chat is not connected yet."}
              </p>
              <button
                type="button"
                onClick={() => onNavigate("chat")}
                className="text-primary mt-2 text-xs font-bold disabled:opacity-50"
              >
                {assistantSuggestion ? "View suggestion" : "Open chat"} <span aria-hidden="true">→</span>
              </button>
            </div>
            <button
              type="button"
              onClick={onAssistantCardDismiss}
              aria-label="Dismiss suggestion"
              className="text-muted-foreground grid size-8 shrink-0 place-items-center rounded-full"
            >
              <X size={16} />
            </button>
          </div>
        </section>
      )}
      <section className="px-5 py-7">
        <SectionTitle action="Customize" onAction={onUnavailable}>
          Quick actions
        </SectionTitle>
        <div className="grid grid-cols-4 gap-3">
          {QUICK_ACTIONS.map((action) => (
            <ActionTile key={action.label} {...action} onClick={onUnavailable} />
          ))}
        </div>
      </section>
      <section className="px-5 pb-7">
        <SectionTitle action="Track order" onAction={onUnavailable}>
          Buy now
        </SectionTitle>
        <button
          type="button"
          onClick={() => onNavigate("marketplace")}
          className="bg-primary text-primary-foreground flex min-h-24 w-full items-center justify-between gap-3 overflow-hidden rounded-2xl px-5 text-left"
        >
          <span>
            <span className="block text-lg leading-tight font-extrabold">
              Mobile, fiber,
              <br />
              devices & more.
            </span>
            <span className="mt-1 block text-xs font-medium">
              Explore what’s possible with Max it
            </span>
          </span>
          <span className="bg-background text-foreground grid size-10 shrink-0 place-items-center rounded-full">
            <ArrowRight size={20} />
          </span>
        </button>
      </section>
      <section className="bg-surface px-5 py-7">
        <SectionTitle action="See all" onAction={() => onNavigate("marketplace")}>
          Trending
        </SectionTitle>
        <div className="hide-scrollbar flex gap-3 overflow-x-auto pb-1">
          <article className="border-border bg-background flex min-h-36 w-[78%] shrink-0 flex-col justify-between rounded-2xl border p-4">
            <Sparkles size={26} className="text-primary" />
            <div>
              <p className="text-primary text-[10px] font-bold tracking-widest">MADE FOR YOU</p>
              <h3 className="mt-1 text-base leading-tight font-bold">
                More of what
                <br />
                keeps you connected.
              </h3>
              <p className="text-muted-foreground mt-2 text-xs">Discover our latest offers</p>
            </div>
          </article>
          <article className="bg-lilac text-primary-foreground flex min-h-36 w-[60%] shrink-0 flex-col justify-between rounded-2xl p-4">
            <Globe2 size={27} />
            <div>
              <p className="text-[10px] font-bold tracking-widest">EXPLORE MORE</p>
              <h3 className="mt-1 text-base font-bold">
                A world of
                <br />
                possibilities.
              </h3>
            </div>
          </article>
        </div>
      </section>
      <section className="px-5 py-7">
        <div className="border-border flex items-center justify-between gap-4 rounded-2xl border p-4">
          <div>
            <p className="text-sm font-bold">A little something for you</p>
            <p className="text-muted-foreground mt-1 text-xs">Discover rewards and surprises.</p>
          </div>
          <button
            type="button"
            onClick={() => onNavigate("rewards")}
            aria-label="Explore rewards"
            className="bg-raised text-primary grid size-11 shrink-0 place-items-center rounded-full"
          >
            <Gift size={21} />
          </button>
        </div>
      </section>
    </main>
  );
}
