import { ArrowRightIcon } from "lucide-react";

import { cn } from "@/lib/utils";

/**
 * PillArrow Component
 *
 * Decorative circular arrow badge embedded inside pill-shaped CTA buttons.
 */
function PillArrow({ className }) {
  return (
    <span
      className={cn(
        "bg-surface text-primary flex size-10 shrink-0 items-center justify-center rounded-full",
        className,
      )}
    >
      <ArrowRightIcon data-icon="inline-end" />
    </span>
  );
}

export default PillArrow;
