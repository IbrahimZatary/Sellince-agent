import { cn } from "@/lib/utils";

const LOGO_DOTS = [
  { dotId: "top", cx: 20, cy: 4, radius: 2.5 },
  { dotId: "upper-left", cx: 13, cy: 10, radius: 2.5 },
  { dotId: "upper-center", cx: 20, cy: 10, radius: 2.5 },
  { dotId: "upper-right", cx: 27, cy: 10, radius: 2.5 },
  { dotId: "middle-left-edge", cx: 6, cy: 17, radius: 2.5 },
  { dotId: "middle-left", cx: 13, cy: 17, radius: 2.5 },
  { dotId: "middle-center", cx: 20, cy: 17, radius: 3 },
  { dotId: "middle-right", cx: 27, cy: 17, radius: 2.5 },
  { dotId: "middle-right-edge", cx: 34, cy: 17, radius: 2.5 },
  { dotId: "lower-left", cx: 13, cy: 24, radius: 2.5 },
  { dotId: "lower-center", cx: 20, cy: 24, radius: 2.5 },
  { dotId: "lower-right", cx: 27, cy: 24, radius: 2.5 },
  { dotId: "bottom", cx: 20, cy: 31, radius: 2.5 },
];

/**
 * SellinceLogo Component
 *
 * Brand emblem and wordmark:
 * - SVG vector dot-grid symbol in brand primary orange.
 * - Bold typographic wordmark ("Sellince") with inverted (dark surface) support.
 * - Configurable wordmark visibility on inverse surfaces.
 */
function SellinceLogo({ className, isInverted = false, showWordmark = true, wordmarkClassName }) {
  return (
    <span className={cn("inline-flex items-center gap-3", className)}>
      <svg
        aria-hidden="true"
        className="text-primary h-[30px] w-[34px] shrink-0"
        viewBox="0 0 40 35"
      >
        {LOGO_DOTS.map((dot) => (
          <circle key={dot.dotId} cx={dot.cx} cy={dot.cy} r={dot.radius} fill="currentColor" />
        ))}
      </svg>
      {showWordmark ? (
        <span
          className={cn(
            "text-logo font-semibold tracking-tight",
            isInverted ? "text-inverse-foreground" : "text-foreground",
            wordmarkClassName,
          )}
        >
          Sellince
        </span>
      ) : null}
    </span>
  );
}

export default SellinceLogo;
