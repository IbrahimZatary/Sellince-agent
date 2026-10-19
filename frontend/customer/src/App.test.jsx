import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { beforeEach, describe, expect, it, vi } from "vitest";

import * as authApi from "@/api/auth.api";
import App from "@/App";

// jsdom in this repo does not expose localStorage; the app reads it
// (customer session + ProtectedRoute), so stub a minimal version here.
function createLocalStorageStub() {
  let store = {};
  return {
    getItem: (key) => (key in store ? store[key] : null),
    setItem: (key, value) => {
      store[key] = String(value);
    },
    removeItem: (key) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
}

vi.stubGlobal("localStorage", createLocalStorageStub());

describe("App routing and pages", () => {
  function renderApp(initialRoute = "/") {
    return render(
      <MemoryRouter initialEntries={[initialRoute]}>
        <App />
      </MemoryRouter>,
    );
  }

  beforeEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

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
      expect(screen.getByLabelText("Phone number")).toBeInTheDocument();
      expect(screen.getByLabelText("Password")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Show password" })).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Log in" })).toBeInTheDocument();
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

    it("validates required fields and phone format on submit", async () => {
      const user = userEvent.setup();
      renderApp("/login");

      await user.click(screen.getByRole("button", { name: "Log in" }));

      expect(screen.getByText("Phone number is required.")).toBeVisible();
      expect(screen.getByText("Password is required.")).toBeVisible();

      await user.type(screen.getByLabelText("Phone number"), "abc");
      await user.click(screen.getByRole("button", { name: "Log in" }));

      expect(screen.getByText("Please enter a valid phone number.")).toBeVisible();
    });

    it("stores the session and navigates to chat on valid submit", async () => {
      const user = userEvent.setup();
      const loginSpy = vi.spyOn(authApi, "loginCustomer").mockResolvedValueOnce({
        customer_id: 4,
        name: "Noor Ibrahim",
        access_token: "test-token",
      });

      renderApp("/login");

      await user.type(screen.getByLabelText("Phone number"), "0784444444");
      await user.type(screen.getByLabelText("Password"), "Sellince123!");
      await user.click(screen.getByRole("button", { name: "Log in" }));

      expect(loginSpy).toHaveBeenCalledWith({
        phone: "0784444444",
        password: "Sellince123!",
      });
      expect(localStorage.getItem("customer_id")).toBe("4");
      expect(localStorage.getItem("customer_access_token")).toBe("test-token");
      expect(await screen.findByRole("dialog", { name: "Sellince Assistant chat" })).toBeVisible();
    });

    it("preserves credentials when login fails", async () => {
      const user = userEvent.setup();
      vi.spyOn(authApi, "loginCustomer").mockRejectedValueOnce({
        response: { data: { message: "Invalid phone number or password" } },
      });

      renderApp("/login");

      await user.type(screen.getByLabelText("Phone number"), "0784444444");
      await user.type(screen.getByLabelText("Password"), "WrongPassword1");
      await user.click(screen.getByRole("button", { name: "Log in" }));

      expect(await screen.findByRole("alert")).toHaveTextContent(
        "Invalid phone number or password",
      );
      expect(screen.getByLabelText("Phone number")).toHaveValue("0784444444");
      expect(screen.getByLabelText("Password")).toHaveValue("WrongPassword1");
    });
  });

  describe("Chat and Checkout Pages", () => {
    it("redirects /chat to /login when unauthenticated", () => {
      renderApp("/chat");

      expect(screen.getByRole("heading", { level: 1, name: "Welcome back" })).toBeVisible();
    });

    it("renders the assistant chat on /chat when authenticated", () => {
      localStorage.setItem("customer_id", "4");
      localStorage.setItem("customer_access_token", "test-token");
      renderApp("/chat");

      expect(screen.getByRole("dialog", { name: "Sellince Assistant chat" })).toBeVisible();
      expect(screen.getByRole("heading", { level: 2, name: "Sellince Assistant" })).toBeVisible();
    });

    it("renders the checkout page on /checkout", () => {
      renderApp("/checkout?customer_id=4&product_name=20GB%20Mobile%204G&price=15.00");

      expect(
        screen.getByRole("heading", { level: 1, name: "Complete your purchase" }),
      ).toBeVisible();
    });
  });
});
