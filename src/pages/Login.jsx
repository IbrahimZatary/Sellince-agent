import { useState } from "react";
import {
  ArrowLeft,
  ChevronDown,
  ChevronRight,
  Eye,
  EyeOff,
  Globe2,
  LockKeyhole,
  MessageSquare,
  ShoppingBag,
  Smartphone,
} from "lucide-react";
import welcomeArt from "@/assets/auth-welcome.png";
import signInArt from "@/assets/auth-sign-in.png";

function BackButton({ onBack }) {
  return (
    <button
      type="button"
      onClick={onBack}
      aria-label="Go back"
      className="grid size-11 place-items-center"
    >
      <ArrowLeft size={25} />
    </button>
  );
}

function PasswordInput({ id, value, onChange, placeholder, autoComplete }) {
  const [isVisible, setIsVisible] = useState(false);
  return (
    <div className="relative">
      <label htmlFor={id} className="sr-only">
        {placeholder}
      </label>
      <input
        id={id}
        type={isVisible ? "text" : "password"}
        autoComplete={autoComplete}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="auth-input pr-14"
      />
      <button
        type="button"
        onClick={() => setIsVisible(!isVisible)}
        aria-label={isVisible ? "Hide password" : "Show password"}
        className="absolute inset-y-0 right-2 grid w-11 place-items-center"
      >
        {isVisible ? <EyeOff size={22} /> : <Eye size={22} />}
      </button>
    </div>
  );
}

function AuthWelcome({ onSignIn, onPreview }) {
  return (
    <main className="safe-top bg-background text-foreground mx-auto min-h-dvh max-w-[480px] px-4 pb-8">
      <div className="flex justify-end pt-4">
        <button
          type="button"
          className="border-border flex h-10 items-center gap-2 rounded-full border px-3 text-sm font-semibold"
          disabled
          aria-label="Language: English"
        >
          <Globe2 size={19} className="text-primary" /> English <ChevronDown size={18} />
        </button>
      </div>
      <img src={welcomeArt} alt="" className="mx-auto mt-5 h-44 w-full object-contain" />
      <div className="mt-8 text-center">
        <h1 className="text-xl font-bold">Welcome to Max it</h1>
        <p className="mx-auto mt-3 max-w-80 text-sm leading-5">
          If you have an Orange mobile line you can login using these two methods
        </p>
      </div>
      <div className="mt-9 grid grid-cols-2 gap-4">
        <button
          type="button"
          disabled
          className="border-border bg-surface flex min-h-36 flex-col items-start justify-between rounded-xl border p-4 text-left opacity-80"
        >
          <Smartphone className="text-primary" size={26} />
          <span>
            <span className="block text-xs">SIM Card</span>
            <span className="mt-1 block text-sm font-semibold">Mobile Data</span>
          </span>
        </button>
        <button
          type="button"
          disabled
          className="border-border bg-surface flex min-h-36 flex-col items-start justify-between rounded-xl border p-4 text-left opacity-80"
        >
          <MessageSquare className="text-primary" size={26} />
          <span>
            <span className="block text-xs">Mobile connect</span>
            <span className="mt-1 block text-sm font-semibold">SMS</span>
          </span>
        </button>
      </div>
      <div className="my-6 flex items-center gap-3 text-sm">
        <span className="bg-border h-px flex-1" />
        OR
        <span className="bg-border h-px flex-1" />
      </div>
      <button
        type="button"
        onClick={onSignIn}
        className="border-border bg-surface flex min-h-24 w-full items-center gap-4 rounded-xl border px-5 text-left"
      >
        <LockKeyhole className="text-primary shrink-0" size={30} />
        <span className="flex-1">
          <span className="block text-base font-semibold">Sign in/ Sign up</span>
          <span className="mt-1 block text-xs leading-5">Using your email or mobile number</span>
        </span>
        <ChevronRight size={22} />
      </button>
      <button
        type="button"
        onClick={onPreview}
        className="border-border bg-surface mt-4 flex min-h-24 w-full items-center gap-4 rounded-xl border px-5 text-left"
      >
        <ShoppingBag className="text-primary shrink-0" size={30} />
        <span className="flex-1">
          <span className="block text-base font-semibold">Continue as a guest</span>
          <span className="mt-1 block text-xs leading-5">Explore the UI without signing in</span>
        </span>
        <ChevronRight size={22} />
      </button>
      <p className="text-muted-foreground mt-4 text-center text-xs">
        Sign-in and account services will be connected later.
      </p>
    </main>
  );
}

function AuthSecondary({ page, onBack }) {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const isRegistration = page === "signup";
  return (
    <main className="safe-top bg-background text-foreground mx-auto flex min-h-dvh max-w-[480px] flex-col px-4 pb-8">
      <div className="pt-3">
        <BackButton onBack={onBack} />
      </div>
      <h1 className="mt-8 text-2xl font-bold">
        {isRegistration ? "Create your account" : "Forgot your password ?"}
      </h1>
      <div className="mt-14 flex flex-col gap-4">
        <label className="sr-only" htmlFor="secondary-identifier">
          Email or mobile number
        </label>
        <input
          id="secondary-identifier"
          value={identifier}
          onChange={(event) => setIdentifier(event.target.value)}
          autoComplete="username"
          placeholder="Email or mobile number *"
          className="auth-input"
        />
        {isRegistration && (
          <>
            <PasswordInput
              id="new-password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Create password *"
              autoComplete="new-password"
            />
            <p className="text-muted-foreground -mt-2 px-4 text-xs">
              Minimum of 8 characters, with upper and lowercase letters.
            </p>
          </>
        )}
      </div>
      <div className="mt-auto pt-10">
        {isRegistration && (
          <label className="mb-8 flex items-center gap-4 text-sm">
            <input type="checkbox" disabled className="size-5" /> I agree with the terms &
            conditions
          </label>
        )}
        <button
          type="button"
          disabled
          className="bg-surface text-muted-foreground h-12 w-full rounded-xl font-semibold"
        >
          {isRegistration ? "Next" : "Reset password"}
        </button>
        <p className="text-muted-foreground mt-3 text-center text-xs">
          {isRegistration ? "Account creation" : "Password recovery"} is not available in this demo.
        </p>
      </div>
    </main>
  );
}

export default function Login({ onPreview }) {
  const [page, setPage] = useState("welcome");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  function handleLoginSubmit(event) {
    event.preventDefault();
    setLoginError("Sign-in is not connected yet.");
  }
  function handleLeaveSignIn(nextPage) {
    setPassword("");
    setLoginError("");
    setPage(nextPage);
  }
  if (page === "welcome")
    return <AuthWelcome onPreview={onPreview} onSignIn={() => setPage("signin")} />;
  if (page === "signup" || page === "recovery")
    return <AuthSecondary key={page} page={page} onBack={() => setPage("signin")} />;
  return (
    <main className="safe-top bg-background text-foreground mx-auto min-h-dvh max-w-[480px] px-4 pb-10">
      <div className="pt-3">
        <BackButton onBack={() => handleLeaveSignIn("welcome")} />
      </div>
      <img src={signInArt} alt="" className="bg-surface mt-4 h-32 w-full object-contain" />
      <h1 className="mt-7 text-center text-xl font-bold">Sign in with your account</h1>
      <form onSubmit={handleLoginSubmit} className="mt-12">
        <label className="sr-only" htmlFor="phone">
          Mobile number
        </label>
        <input
          id="phone"
          type="tel"
          autoComplete="tel"
          value={phone}
          onChange={(event) => setPhone(event.target.value)}
          placeholder="Mobile number *"
          className="auth-input"
        />
        <div className="mt-4">
          <PasswordInput
            id="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Password *"
            autoComplete="current-password"
          />
        </div>
        <button
          type="button"
          onClick={() => handleLeaveSignIn("recovery")}
          className="text-auth-link mt-8 px-4 text-sm"
        >
          Forgot your password?
        </button>
        {loginError && (
          <p role="alert" className="mt-4 text-sm">
            {loginError}
          </p>
        )}
        <button
          type="submit"
          disabled={!phone.trim() || !password}
          className="border-border bg-primary text-primary-foreground disabled:bg-background disabled:text-muted-foreground mt-10 h-11 w-full rounded-lg border font-semibold"
        >
          Sign in
        </button>
      </form>
      <p className="mt-12 text-center text-sm font-semibold">
        Not a member?{" "}
        <button type="button" onClick={() => handleLeaveSignIn("signup")} className="text-auth-link">
          Create account
        </button>
      </p>
      <p className="text-muted-foreground mt-6 text-center text-xs">
        Sign-in is not connected yet.
      </p>
    </main>
  );
}
