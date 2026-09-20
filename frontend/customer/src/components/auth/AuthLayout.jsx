import { Link } from "react-router";

import SellinceLogo from "@/components/home/SellinceLogo";

/**
 * Provides the shared Sellince authentication layout for Login and Sign Up.
 */
function AuthLayout({
  title,
  description,
  children,
  footerPrompt,
  footerActionText,
  footerActionHref,
}) {
  const hasFooterAction = Boolean(footerPrompt && footerActionText && footerActionHref);

  return (
    <div className="bg-background flex min-h-dvh flex-col px-4 py-8 sm:px-6 lg:px-8">
      <header className="flex justify-center">
        <Link
          to="/"
          aria-label="Sellince home"
          className="focus-visible:ring-ring/50 rounded-md transition-opacity hover:opacity-90 focus-visible:ring-3 focus-visible:outline-none"
        >
          <SellinceLogo />
        </Link>
      </header>

      <main className="flex w-full flex-1 items-center justify-center py-6">
        <section
          aria-labelledby="auth-page-title"
          aria-describedby={description ? "auth-page-description" : undefined}
          className="bg-surface border-border shadow-card w-full max-w-md rounded-2xl border p-6 sm:p-8"
        >
          <div className="mb-6 space-y-1.5 text-left">
            <h1
              id="auth-page-title"
              className="text-foreground text-2xl font-semibold tracking-tight"
            >
              {title}
            </h1>

            {description ? (
              <p id="auth-page-description" className="text-muted-foreground text-sm">
                {description}
              </p>
            ) : null}
          </div>

          {children}

          {hasFooterAction ? (
            <div className="border-border mt-6 border-t pt-4 text-center text-sm">
              <span className="text-muted-foreground">{footerPrompt} </span>

              <Link
                to={footerActionHref}
                className="text-primary focus-visible:ring-ring/50 rounded-xs font-medium hover:underline focus-visible:ring-2 focus-visible:outline-none"
              >
                {footerActionText}
              </Link>
            </div>
          ) : null}
        </section>
      </main>

      <footer className="text-muted-foreground text-center text-xs">
        <p>&copy; {new Date().getFullYear()} Sellince Inc. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default AuthLayout;
