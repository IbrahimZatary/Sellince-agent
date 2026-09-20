import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { describe, expect, it, vi } from "vitest";

import * as apiClient from "@/api/client";
import App from "@/App";

describe("App routing and pages", () => {
  function renderApp(initialRoute = "/") {
    return render(
      <MemoryRouter initialEntries={[initialRoute]}>
        <App />
      </MemoryRouter>,
    );
  }

  describe("Landing Page (/)", () => {
    it("renders the landing-page message and artwork", () => {
      renderApp("/");

      expect(screen.getByText("Conversation intelligence")).toBeVisible();
      expect(
        screen.getByRole("heading", {
          level: 1,
          name: "Understand the customer behind every message.",
        }),
      ).toBeVisible();
      expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
      expect(screen.getByTestId("hero-artwork")).toBeInTheDocument();
    });

    it("renders navigation and the expected account links", () => {
      renderApp("/");

      expect(screen.getAllByRole("link", { name: "Log in" })[0]).toHaveAttribute("href", "/login");
      expect(screen.getAllByRole("link", { name: "Get started" })[0]).toHaveAttribute(
        "href",
        "/signup",
      );
      expect(screen.getByRole("link", { name: "Start a conversation" })).toHaveAttribute(
        "href",
        "/login",
      );
      expect(screen.getByRole("button", { name: "Open navigation menu" })).toBeInTheDocument();
      expect(screen.queryByRole("button", { name: "Chat with Us" })).not.toBeInTheDocument();
    });
  });

  describe("Login Page (/login)", () => {
    it("renders the login form elements", () => {
      renderApp("/login");

      expect(screen.getByRole("heading", { level: 1, name: "Welcome back" })).toBeVisible();
      expect(screen.getByLabelText("Email")).toBeInTheDocument();
      expect(screen.getByLabelText("Password")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Show password" })).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Log in" })).toBeInTheDocument();
      expect(screen.getByRole("link", { name: "Sign up" })).toHaveAttribute("href", "/signup");
    });

    it("toggles password visibility", async () => {
      const user = userEvent.setup();
      renderApp("/login");

      const passwordInput = screen.getByLabelText("Password");
      const toggleButton = screen.getByRole("button", { name: "Show password" });

      expect(passwordInput).toHaveAttribute("type", "password");
      await user.click(toggleButton);

      expect(passwordInput).toHaveAttribute("type", "text");
      expect(screen.getByRole("button", { name: "Hide password" })).toBeInTheDocument();
    });

    it("validates required fields and email format on submit", async () => {
      const user = userEvent.setup();
      renderApp("/login");

      await user.click(screen.getByRole("button", { name: "Log in" }));

      expect(screen.getByText("Email is required.")).toBeVisible();
      expect(screen.getByText("Password is required.")).toBeVisible();

      await user.type(screen.getByLabelText("Email"), "notanemail");
      await user.click(screen.getByRole("button", { name: "Log in" }));

      expect(screen.getByText("Please enter a valid email address.")).toBeVisible();
    });

    it("preserves credentials at the pending authentication boundary", async () => {
      const user = userEvent.setup();

      renderApp("/login");

      await user.type(screen.getByLabelText("Email"), "alex@company.com");
      await user.type(screen.getByLabelText("Password"), "SecretPassword123");
      await user.click(screen.getByRole("button", { name: "Log in" }));

      expect(await screen.findByRole("alert")).toHaveTextContent(
        "Login will be available when secure authentication is connected.",
      );
      expect(screen.getByLabelText("Email")).toHaveValue("alex@company.com");
      expect(screen.getByLabelText("Password")).toHaveValue("SecretPassword123");
    });
  });

  describe("SignUp Page (/signup)", () => {
    it("renders the signup form elements", () => {
      renderApp("/signup");

      expect(screen.getByRole("heading", { level: 1, name: "Create your account" })).toBeVisible();
      expect(screen.getByLabelText("Full name")).toBeInTheDocument();
      expect(screen.getByLabelText("Work email")).toBeInTheDocument();
      expect(screen.getByLabelText("Password")).toBeInTheDocument();
      expect(screen.getByLabelText("Company name")).toBeInTheDocument();
      expect(screen.getByLabelText("Sector")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Create account" })).toBeInTheDocument();
      expect(screen.getByRole("link", { name: "Log in" })).toHaveAttribute("href", "/login");
    });

    it("validates required fields and password length", async () => {
      const user = userEvent.setup();
      renderApp("/signup");

      await user.click(screen.getByRole("button", { name: "Create account" }));

      expect(screen.getByText("Full name is required.")).toBeVisible();
      expect(screen.getByText("Email is required.")).toBeVisible();
      expect(screen.getByText("Password is required.")).toBeVisible();
      expect(screen.getByText("Company name is required.")).toBeVisible();
      expect(screen.getByText("Please select your sector.")).toBeVisible();

      await user.type(screen.getByLabelText("Password"), "short");
      await user.click(screen.getByRole("button", { name: "Create account" }));
      expect(screen.getByText("Password must be at least 8 characters.")).toBeVisible();
    });

    it("calls registerUser on valid submit and handles error safely", async () => {
      const user = userEvent.setup();
      const registerSpy = vi.spyOn(apiClient, "registerUser").mockRejectedValueOnce({
        response: { data: { message: "Account already exists." } },
      });

      renderApp("/signup");

      await user.type(screen.getByLabelText("Full name"), "Sarah Connor");
      await user.type(screen.getByLabelText("Work email"), "sarah@cyberdyne.com");
      await user.type(screen.getByLabelText("Password"), "StrongPassword123");
      await user.type(screen.getByLabelText("Company name"), "Cyberdyne Systems");

      const sectorTrigger = screen.getByLabelText("Sector");
      await user.click(sectorTrigger);
      const option = await screen.findByRole("option", { name: "Technology & Software" });
      await user.click(option);

      await user.click(screen.getByRole("button", { name: "Create account" }));

      expect(registerSpy).toHaveBeenCalledWith({
        name: "Sarah Connor",
        email: "sarah@cyberdyne.com",
        password: "StrongPassword123",
        companyName: "Cyberdyne Systems",
        sector: "technology",
      });

      expect(await screen.findByRole("alert")).toHaveTextContent("Account already exists.");
      expect(screen.getByLabelText("Full name")).toHaveValue("Sarah Connor");
      expect(screen.getByLabelText("Work email")).toHaveValue("sarah@cyberdyne.com");

      registerSpy.mockRestore();
    });
  });

  describe("Onboarding and Chat Pages", () => {
    it("renders onboarding on /onboarding", () => {
      renderApp("/onboarding");

      expect(
        screen.getByRole("heading", {
          level: 1,
          name: "How would you like Sellince to help?",
        }),
      ).toBeVisible();
    });

    it("renders the floating chatbot host on /chat", () => {
      renderApp("/chat");

      expect(screen.getByRole("dialog", { name: "Sellince Assistant chat" })).toBeVisible();
      expect(screen.getByRole("heading", { level: 2, name: "Sellince Assistant" })).toBeVisible();
    });
  });
});
