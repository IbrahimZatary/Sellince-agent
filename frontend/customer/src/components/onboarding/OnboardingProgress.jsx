import { CheckIcon, CircleIcon } from "lucide-react";

/**
 * Stages in the user onboarding funnel.
 */
const ONBOARDING_STAGES = [
  { stageId: "account-created", label: "ACCOUNT CREATED", state: "completed" },
  { stageId: "choose-workspace", label: "CHOOSE WORKSPACE", state: "current" },
  { stageId: "start", label: "START", state: "upcoming" },
];

/**
 * OnboardingProgress Component
 *
 * Visual stepper tracking progress through registration and workspace configuration:
 * - Shows completed, current, and upcoming stages.
 * - Screen-reader accessible step indicators using `aria-current="step"`.
 */
function OnboardingProgress() {
  return (
    <nav aria-label="Onboarding progress">
      <ol className="text-micro tracking-step sm:tracking-step-wide flex max-w-xl items-center gap-1 font-medium sm:gap-3 sm:text-xs">
        {ONBOARDING_STAGES.map((stage, stageIndex) => (
          <li key={stage.stageId} className="contents">
            <span
              className={
                stage.state === "current"
                  ? "text-primary flex shrink-0 items-center gap-1 sm:gap-1.5"
                  : "text-muted-foreground flex shrink-0 items-center gap-1 sm:gap-1.5"
              }
              aria-current={stage.state === "current" ? "step" : undefined}
            >
              {stage.label}
              {stage.state === "completed" ? (
                <span className="border-muted-foreground flex size-3.5 items-center justify-center rounded-full border sm:size-4">
                  <CheckIcon className="size-2.5" aria-hidden="true" />
                </span>
              ) : (
                <CircleIcon
                  className={stage.state === "current" ? "fill-primary size-3" : "size-3"}
                  aria-hidden="true"
                />
              )}
            </span>

            {stageIndex < ONBOARDING_STAGES.length - 1 ? (
              <span className="bg-border h-px min-w-2 flex-1 sm:min-w-10" aria-hidden="true" />
            ) : null}
          </li>
        ))}
      </ol>
    </nav>
  );
}

export default OnboardingProgress;
