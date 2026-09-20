import { useState } from "react";
import { useNavigate } from "react-router";

import AuthLayout from "@/components/auth/AuthLayout";
import PasswordField from "@/components/auth/PasswordField";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { authenticateUser } from "@/api/auth.api";

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/**
 * Login Component
 *
 * Provides end-user and operator authentication:
 * - Controlled email and password inputs with field-level validation.
 * - Password show/hide toggle via PasswordField.
 * - Accessible error messages (`role="alert"` and `aria-invalid`).
 * - Calls authenticateUser API and redirects on success.
 */
function Login() {
  const navigate = useNavigate();
  const [loginFormValues, setLoginFormValues] = useState({
    email: "",
    password: "",
  });
  const [loginFormErrors, setLoginFormErrors] = useState({});
  const [loginRequestError, setLoginRequestError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function validateLoginForm(values) {
    const nextErrors = {};

    if (!values.email.trim()) {
      nextErrors.email = "Email is required.";
    } else if (!EMAIL_REGEX.test(values.email.trim())) {
      nextErrors.email = "Please enter a valid email address.";
    }

    if (!values.password) {
      nextErrors.password = "Password is required.";
    }

    return nextErrors;
  }

  function handleLoginFieldChange(event) {
    const { name, value } = event.target;

    setLoginFormValues((previousValues) => ({
      ...previousValues,
      [name]: value,
    }));

    if (loginFormErrors[name]) {
      setLoginFormErrors((previousErrors) => {
        const nextErrors = { ...previousErrors };
        delete nextErrors[name];
        return nextErrors;
      });
    }

    if (loginRequestError) {
      setLoginRequestError(null);
    }
  }

  async function handleLoginSubmit(event) {
    event.preventDefault();

    const formValidationErrors = validateLoginForm(loginFormValues);
    if (Object.keys(formValidationErrors).length > 0) {
      setLoginFormErrors(formValidationErrors);
      return;
    }

    setLoginFormErrors({});
    setLoginRequestError(null);
    setIsSubmitting(true);

    try {
      await authenticateUser({
        email: loginFormValues.email.trim(),
        password: loginFormValues.password,
      });
      // On success, navigate to onboarding or chat
      navigate("/onboarding", { replace: true });
    } catch (error) {
      const serverMessage =
        error.response?.data?.message ||
        "Unable to log in. Please check your credentials and try again.";
      setLoginRequestError(serverMessage);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthLayout
      title="Welcome back"
      description="Enter your email and password to log in to your account."
      footerPrompt="Don't have an account?"
      footerActionText="Sign up"
      footerActionHref="/signup"
    >
      <form onSubmit={handleLoginSubmit} noValidate className="space-y-4">
        {loginRequestError ? (
          <Alert variant="destructive">
            <AlertDescription>{loginRequestError}</AlertDescription>
          </Alert>
        ) : null}

        <div className="space-y-1.5 text-left">
          <Label htmlFor="login-email">Email</Label>
          <Input
            id="login-email"
            name="email"
            type="email"
            value={loginFormValues.email}
            onChange={handleLoginFieldChange}
            placeholder="name@company.com"
            autoComplete="email"
            aria-invalid={Boolean(loginFormErrors.email)}
            aria-describedby={loginFormErrors.email ? "login-email-error" : undefined}
            className="h-11 text-base md:text-sm"
            disabled={isSubmitting}
          />
          {loginFormErrors.email ? (
            <p id="login-email-error" role="alert" className="text-destructive text-xs">
              {loginFormErrors.email}
            </p>
          ) : null}
        </div>

        <div className="space-y-1.5 text-left">
          <Label htmlFor="login-password">Password</Label>
          <PasswordField
            id="login-password"
            name="password"
            value={loginFormValues.password}
            onChange={handleLoginFieldChange}
            placeholder="Enter your password"
            autoComplete="current-password"
            aria-invalid={Boolean(loginFormErrors.password)}
            aria-describedby={loginFormErrors.password ? "login-password-error" : undefined}
            disabled={isSubmitting}
          />
          {loginFormErrors.password ? (
            <p id="login-password-error" role="alert" className="text-destructive text-xs">
              {loginFormErrors.password}
            </p>
          ) : null}
        </div>

        <Button
          type="submit"
          disabled={isSubmitting}
          className="h-11 w-full rounded-lg text-base font-medium transition-all"
        >
          {isSubmitting ? "Logging in..." : "Log in"}
        </Button>
      </form>
    </AuthLayout>
  );
}

export default Login;
