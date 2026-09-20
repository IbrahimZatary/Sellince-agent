import { useState } from "react";
import { EyeIcon, EyeOffIcon } from "lucide-react";

import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

/**
 * PasswordField Component
 *
 * Reusable password input with show/hide visibility toggle:
 * - Switches between `type="password"` and `type="text"`.
 * - Accessible toggle button with descriptive `aria-label`.
 * - Forwards accessibility props (`aria-invalid`, `aria-describedby`).
 */
function PasswordField({
  id,
  name = "password",
  value,
  onChange,
  onBlur,
  placeholder = "Enter your password",
  autoComplete = "current-password",
  disabled = false,
  className,
  "aria-invalid": ariaInvalid,
  "aria-describedby": ariaDescribedBy,
  ...props
}) {
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);

  function handlePasswordVisibilityToggle() {
    setIsPasswordVisible((previousIsVisible) => !previousIsVisible);
  }

  return (
    <div className="relative flex items-center">
      <Input
        id={id}
        name={name}
        type={isPasswordVisible ? "text" : "password"}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        placeholder={placeholder}
        autoComplete={autoComplete}
        disabled={disabled}
        aria-invalid={ariaInvalid}
        aria-describedby={ariaDescribedBy}
        className={cn("h-11 pr-10 text-base md:text-sm", className)}
        {...props}
      />
      <button
        type="button"
        onClick={handlePasswordVisibilityToggle}
        disabled={disabled}
        aria-label={isPasswordVisible ? "Hide password" : "Show password"}
        className="text-muted-foreground hover:text-foreground focus-visible:ring-ring/50 absolute right-2 flex size-7 items-center justify-center rounded-md transition-colors focus-visible:ring-2 focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50"
      >
        {isPasswordVisible ? (
          <EyeOffIcon className="size-4.5" aria-hidden="true" />
        ) : (
          <EyeIcon className="size-4.5" aria-hidden="true" />
        )}
      </button>
    </div>
  );
}

export default PasswordField;
