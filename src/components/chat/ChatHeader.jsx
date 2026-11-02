import { ArrowLeft } from "lucide-react";
import SellinceMark from "./SellinceMark";

export default function ChatHeader({ backLabel, onBack, isConnected }) {
  return (
    <header className="border-border bg-background text-foreground flex min-h-18 shrink-0 items-center gap-3 border-b px-4">
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
        <p className="text-muted-foreground mt-0.5 text-xs" role="status">
          {isConnected ? "Ready to help" : "Preview · Not connected"}
        </p>
      </div>
    </header>
  );
}
