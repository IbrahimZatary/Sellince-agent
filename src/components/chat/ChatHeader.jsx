import { ArrowLeft } from "lucide-react";
import SellinceMark from "./SellinceMark";

export default function ChatHeader({ backLabel, onBack, isConnected }) {
  return (
    <header className="flex min-h-18 shrink-0 items-center gap-3 border-b border-neutral-300 bg-white px-4 text-black">
      <button
        type="button"
        onClick={onBack}
        aria-label={backLabel}
        className="grid size-11 shrink-0 place-items-center rounded-full"
      >
        <ArrowLeft size={22} />
      </button>
      <span className="bg-surface text-primary grid size-10 shrink-0 place-items-center rounded-full">
        <SellinceMark />
      </span>
      <div className="min-w-0">
        <h1 className="text-base font-bold">Sellince assistant</h1>
        <p className="mt-0.5 text-xs text-neutral-600" role="status">
          {isConnected ? "Ready to help" : "Preview · Not connected"}
        </p>
      </div>
    </header>
  );
}
