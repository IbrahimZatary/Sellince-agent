import { useState } from "react";

import { registerUser } from "@/api/client";
import AuthLayout from "@/components/auth/AuthLayout";
import PasswordField from "@/components/auth/PasswordField";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Spinner } from "@/components/ui/spinner";

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// TODO: Replace temporary sector options once the product owner provides the official sector list.
const SECTOR_OPTIONS = [
  { value: "technology", label: "Technology & Software" },
  { value: "ecommerce", label: "E-Commerce & Retail" },
  { value: "finance", label: "Financial Services" },
  { value: "healthcare", label: "Healthcare & Life Sciences" },
  { value: "education", label: "Education & EdTech" },
  { value: "manufacturing", label: "Manufacturing & Logistics" },
  { value: "other", label: "Other" },
];

/**
 * SignUp Component
 *
 * Registration interface for new Sellince accounts:
 * - Collects full name, work email, password (min 8 chars), company name, and sector.
 * - Accessible Radix select dropdown for sector options.
 * - Loading spinner during API submission and disabled controls to prevent duplicate submits.
 * - Calls `registerUser` API endpoint and safely handles response errors.
 */
function SignUp() {
  const [signUpFormValues, setSignUpFormValues] = useState({
    name: "",
    email: "",
    password: "",
    companyName: "",
    sector: "",
  });
  const [signUpFormErrors, setSignUpFormErrors] = useState({});
  const [isSignUpSubmitting, setIsSignUpSubmitting] = useState(false);
  const [signUpRequestError, setSignUpRequestError] = useState(null);

  function validateSignUpForm(values) {
    const nextErrors = {};

    if (!values.name.trim()) {
      nextErrors.name = "Full name is required.";
    }

    if (!values.email.trim()) {
      nextErrors.email = "Email is required.";
    } else if (!EMAIL_REGEX.test(values.email.trim())) {
      nextErrors.email = "Please enter a valid email address.";
    }

    if (!values.password) {
      nextErrors.password = "Password is required.";
    } else if (values.password.length < 8) {
      nextErrors.password = "Password must be at least 8 characters.";
    }

    if (!values.companyName.trim()) {
      nextErrors.companyName = "Company name is required.";
    }

    if (!values.sector) {
      nextErrors.sector = "Please select your sector.";
    }

    return nextErrors;
  }

  function handleSignUpFieldChange(event) {
    const { name, value } = event.target;

    setSignUpFormValues((previousValues) => ({
      ...previousValues,
      [name]: value,
    }));

    if (signUpFormErrors[name]) {
      setSignUpFormErrors((previousErrors) => {
        const nextErrors = { ...previousErrors };
        delete nextErrors[name];
        return nextErrors;
      });
    }

    if (signUpRequestError) {
      setSignUpRequestError(null);
    }
  }

  function handleSignUpSectorChange(selectedSector) {
    setSignUpFormValues((previousValues) => ({
      ...previousValues,
      sector: selectedSector,
    }));

    if (signUpFormErrors.sector) {
      setSignUpFormErrors((previousErrors) => {
        const nextErrors = { ...previousErrors };
        delete nextErrors.sector;
        return nextErrors;
      });
    }

    if (signUpRequestError) {
      setSignUpRequestError(null);
    }
  }

  async function handleSignUpSubmit(event) {
    event.preventDefault();

    const formValidationErrors = validateSignUpForm(signUpFormValues);
    if (Object.keys(formValidationErrors).length > 0) {
      setSignUpFormErrors(formValidationErrors);
      return;
    }

    setSignUpFormErrors({});
    setSignUpRequestError(null);
    setIsSignUpSubmitting(true);

    try {
      await registerUser({
        name: signUpFormValues.name.trim(),
        email: signUpFormValues.email.trim(),
        password: signUpFormValues.password,
        companyName: signUpFormValues.companyName.trim(),
        sector: signUpFormValues.sector,
      });

      // TODO: When backend authentication contract is available, handle registration response and onboarding flow.
    } catch (error) {
      const serverMessage =
        error.response?.data?.message ||
        "Unable to create account. Please check your information or try again later.";
      setSignUpRequestError(serverMessage);
    } finally {
      setIsSignUpSubmitting(false);
    }
  }

  return (
    <AuthLayout
      title="Create your account"
      description="Start understanding the customer behind every message with Sellince."
      footerPrompt="Already have an account?"
      footerActionText="Log in"
      footerActionHref="/login"
    >
      <form onSubmit={handleSignUpSubmit} noValidate className="space-y-4">
        {signUpRequestError ? (
          <Alert variant="destructive">
            <AlertDescription>{signUpRequestError}</AlertDescription>
          </Alert>
        ) : null}

        <div className="space-y-1.5 text-left">
          <Label htmlFor="signup-name">Full name</Label>
          <Input
            id="signup-name"
            name="name"
            type="text"
            value={signUpFormValues.name}
            onChange={handleSignUpFieldChange}
            placeholder="Jane Doe"
            autoComplete="name"
            disabled={isSignUpSubmitting}
            aria-invalid={Boolean(signUpFormErrors.name)}
            aria-describedby={signUpFormErrors.name ? "signup-name-error" : undefined}
            className="h-11 text-base md:text-sm"
          />
          {signUpFormErrors.name ? (
            <p id="signup-name-error" role="alert" className="text-destructive text-xs">
              {signUpFormErrors.name}
            </p>
          ) : null}
        </div>

        <div className="space-y-1.5 text-left">
          <Label htmlFor="signup-email">Work email</Label>
          <Input
            id="signup-email"
            name="email"
            type="email"
            value={signUpFormValues.email}
            onChange={handleSignUpFieldChange}
            placeholder="jane@company.com"
            autoComplete="email"
            disabled={isSignUpSubmitting}
            aria-invalid={Boolean(signUpFormErrors.email)}
            aria-describedby={signUpFormErrors.email ? "signup-email-error" : undefined}
            className="h-11 text-base md:text-sm"
          />
          {signUpFormErrors.email ? (
            <p id="signup-email-error" role="alert" className="text-destructive text-xs">
              {signUpFormErrors.email}
            </p>
          ) : null}
        </div>

        <div className="space-y-1.5 text-left">
          <Label htmlFor="signup-password">Password</Label>
          <PasswordField
            id="signup-password"
            name="password"
            value={signUpFormValues.password}
            onChange={handleSignUpFieldChange}
            placeholder="At least 8 characters"
            autoComplete="new-password"
            disabled={isSignUpSubmitting}
            aria-invalid={Boolean(signUpFormErrors.password)}
            aria-describedby={signUpFormErrors.password ? "signup-password-error" : undefined}
          />
          {signUpFormErrors.password ? (
            <p id="signup-password-error" role="alert" className="text-destructive text-xs">
              {signUpFormErrors.password}
            </p>
          ) : null}
        </div>

        <div className="space-y-1.5 text-left">
          <Label htmlFor="signup-company">Company name</Label>
          <Input
            id="signup-company"
            name="companyName"
            type="text"
            value={signUpFormValues.companyName}
            onChange={handleSignUpFieldChange}
            placeholder="Acme Corp"
            autoComplete="organization"
            disabled={isSignUpSubmitting}
            aria-invalid={Boolean(signUpFormErrors.companyName)}
            aria-describedby={signUpFormErrors.companyName ? "signup-company-error" : undefined}
            className="h-11 text-base md:text-sm"
          />
          {signUpFormErrors.companyName ? (
            <p id="signup-company-error" role="alert" className="text-destructive text-xs">
              {signUpFormErrors.companyName}
            </p>
          ) : null}
        </div>

        <div className="space-y-1.5 text-left">
          <Label htmlFor="signup-sector">Sector</Label>
          <Select
            value={signUpFormValues.sector}
            onValueChange={handleSignUpSectorChange}
            disabled={isSignUpSubmitting}
          >
            <SelectTrigger
              id="signup-sector"
              aria-invalid={Boolean(signUpFormErrors.sector)}
              aria-describedby={signUpFormErrors.sector ? "signup-sector-error" : undefined}
              className="h-11 w-full text-base md:text-sm"
            >
              <SelectValue placeholder="Select your industry sector" />
            </SelectTrigger>
            <SelectContent>
              {SECTOR_OPTIONS.map((sectorOption) => (
                <SelectItem key={sectorOption.value} value={sectorOption.value}>
                  {sectorOption.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {signUpFormErrors.sector ? (
            <p id="signup-sector-error" role="alert" className="text-destructive text-xs">
              {signUpFormErrors.sector}
            </p>
          ) : null}
        </div>

        <Button
          type="submit"
          disabled={isSignUpSubmitting}
          className="h-11 w-full rounded-lg text-base font-medium transition-all"
        >
          {isSignUpSubmitting ? (
            <span className="flex items-center gap-2">
              <Spinner />
              Creating account...
            </span>
          ) : (
            "Create account"
          )}
        </Button>
      </form>
    </AuthLayout>
  );
}

export default SignUp;
