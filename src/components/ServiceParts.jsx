import { ChevronRight } from "lucide-react";

export function SectionTitle({ children, action, onAction, ActionIcon = ChevronRight }) {
  return (
    <div className="mb-4 flex items-center justify-between gap-4">
      <h2 className="text-xl font-bold tracking-tight">{children}</h2>
      {action && (
        <button
          type="button"
          onClick={onAction}
          className="flex items-center gap-1 text-xs font-semibold"
        >
          {action}
          <ActionIcon size={16} />
        </button>
      )}
    </div>
  );
}

export function ActionTile({ Icon, imageSrc, label, badge, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="flex min-w-0 flex-col items-center gap-2 text-center text-[10px] leading-tight font-medium"
    >
      <span className="bg-raised text-primary relative grid aspect-square w-full max-w-20 place-items-center rounded-2xl">
        {imageSrc ? <img src={imageSrc} alt="" className="size-10 object-contain" /> : <Icon size={28} strokeWidth={1.8} />}
        {badge && <span className="bg-mint absolute right-2 bottom-1 left-2 rounded-sm text-center text-[9px] leading-3 font-bold text-white">{badge}</span>}
      </span>
      <span className="line-clamp-2">{label}</span>
    </button>
  );
}

export function DemoBanner() {
  return (
    <div className="bg-raised text-muted-foreground flex items-center justify-between gap-3 px-5 py-2 text-[10px]">
      <span>DEMO EXPERIENCE</span>
      <span>Preview · Not connected</span>
    </div>
  );
}
