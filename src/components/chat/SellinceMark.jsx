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

export default function SellinceMark({ className = "h-5 w-6" }) {
  return (
    <svg aria-hidden="true" className={className} viewBox="0 0 40 35">
      {LOGO_DOTS.map((dot) => (
        <circle key={dot.dotId} cx={dot.cx} cy={dot.cy} r={dot.radius} fill="currentColor" />
      ))}
    </svg>
  );
}
