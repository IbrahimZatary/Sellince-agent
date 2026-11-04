import {
  ArrowRight,
  Gift,
  Pencil,
  Smartphone,
  Truck,
  X,
} from "lucide-react";
import { ActionTile, SectionTitle } from "@/components/ServiceParts";
import SellinceMark from "@/components/chat/SellinceMark";
import topupIcon from "@/assets/maxit/quick-topup.png";
import lineIcon from "@/assets/maxit/quick-line.png";
import extraIcon from "@/assets/maxit/quick-extra.png";
import moneyIcon from "@/assets/maxit/quick-money.png";
import orangeLogo from "@/assets/maxit/orange-logo.png";
import scholarshipsCampaign from "@/assets/maxit/scholarships-campaign.jpg";

const QUICK_ACTIONS = [
  { label: "Recharge Line", imageSrc: topupIcon },
  { label: "Buy Mobile Line", imageSrc: lineIcon, badge: "Offer" },
  { label: "Orange Extra", imageSrc: extraIcon },
  { label: "Orange Money Transfer", imageSrc: moneyIcon },
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
        <h1 className="text-xl font-semibold">Welcome to Max it</h1>
        <div className="hide-scrollbar mt-5 flex gap-3 overflow-x-auto pb-1">
          <article className="bg-raised min-w-[46%] flex-1 rounded-2xl px-3 py-4">
            <div className="flex min-h-8 items-center gap-2"><Smartphone className="text-primary" size={20} /><span className="text-muted-foreground text-[10px]">Mobile line</span></div>
            <div className="mt-3 flex items-center gap-2"><p className="text-muted-foreground shrink-0 text-[10px] font-medium">My line balance</p><span className="bg-primary h-px min-w-0 flex-1" /></div>
            <p className="mt-2 text-base font-bold">
              — <span className="text-xs font-normal">JOD</span>
            </p>
          </article>
          <article className="bg-raised min-w-[46%] flex-1 rounded-2xl px-3 py-4">
            <div className="flex min-h-8 items-center gap-2"><img src={moneyIcon} alt="" className="size-7 object-contain" /><span className="text-[10px] leading-3 font-bold">Orange<br />Money</span></div>
            <div className="mt-3 flex items-center gap-2"><p className="text-muted-foreground shrink-0 text-[10px] font-medium">My Wallet</p><span className="bg-primary h-px min-w-0 flex-1" /></div>
            <p className="mt-2 text-base font-bold">
              — <span className="text-xs font-normal">JOD</span>
            </p>
          </article>
        </div>
      </section>
      {isAssistantCardVisible && (
        <section aria-label="Sellince suggestion" className="px-5 pt-6">
          <div className="border-border bg-surface flex items-start gap-3 rounded-2xl border p-3">
            <span className="bg-raised text-primary grid size-10 shrink-0 place-items-center rounded-xl">
              <SellinceMark />
            </span>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-bold">Sellince <span className="text-muted-foreground font-normal">· {assistantSuggestion ? "A suggestion for you" : "Chat preview"}</span></p>
              <p dir="auto" className="mt-1 text-xs leading-5">
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
        <SectionTitle action="Customize" onAction={onUnavailable} ActionIcon={Pencil}>
          Quick actions
        </SectionTitle>
        <div className="grid grid-cols-4 gap-3">
          {QUICK_ACTIONS.map((action) => (
            <ActionTile key={action.label} {...action} onClick={onUnavailable} />
          ))}
        </div>
      </section>
      <section className="px-5 pb-7">
        <SectionTitle action="Track Order" onAction={onUnavailable} ActionIcon={Truck}>
          Buy Now
        </SectionTitle>
        <button
          type="button"
          onClick={() => onNavigate("marketplace")}
          className="bg-raised flex min-h-20 w-full items-stretch overflow-hidden rounded-xl text-left"
        >
          <span className="bg-primary flex flex-1 items-center gap-2 rounded-r-[45%] px-4 py-3">
            <img src={lineIcon} alt="" className="size-9 shrink-0 object-contain" />
            <span><span className="block text-xs font-bold text-white">Mobile, Fiber, Devices & More</span><span className="mt-1 block text-[10px] font-semibold text-black">Explore options in Max it</span></span>
          </span>
          <span className="flex shrink-0 items-center gap-1 px-3 text-xs font-bold">
            Buy Now <ArrowRight size={18} />
          </span>
        </button>
      </section>
      <section className="bg-surface px-5 py-7">
        <SectionTitle action="See all" onAction={() => onNavigate("marketplace")}>
          Trending
        </SectionTitle>
        <div className="hide-scrollbar flex gap-3 overflow-x-auto pb-1">
          <article className="border-border bg-background flex min-h-36 w-[75%] shrink-0 overflow-hidden rounded-xl border">
            <img src={scholarshipsCampaign} alt="" className="w-1/2 object-cover object-right" />
            <div className="flex flex-1 flex-col justify-center gap-2 p-3">
              <h3 className="text-xs leading-tight font-bold">We’re bringing you one step closer</h3>
              <p className="text-[10px] leading-tight">Discover opportunities for students with <span className="text-primary">Orange</span>.</p>
            </div>
          </article>
          <article className="flex min-h-36 w-[60%] shrink-0 flex-col justify-between rounded-xl bg-white p-4 text-black">
            <img src={orangeLogo} alt="" className="size-7 object-contain" />
            <div>
              <h3 className="mt-1 text-base font-bold">Your next upgrade awaits</h3>
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
