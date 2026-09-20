import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router";
import { describe, expect, it } from "vitest";

import Onboarding from "@/pages/Onboarding";

function renderOnboarding() {
  return render(
    <MemoryRouter initialEntries={["/onboarding"]}>
      <Routes>
        <Route path="/onboarding" element={<Onboarding />} />
        <Route path="/chat" element={<p>Chat destination</p>} />
        <Route path="/dashboard" element={<p>Chat destination</p>} />
        <Route path="/login" element={<p>Login destination</p>} />
      </Routes>
    </MemoryRouter>,
  );
}

describe("Onboarding", () => {
  it("renders the approved content and accessible progress", () => {
    renderOnboarding();

    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "How would you like Sellince to help?",
      }),
    ).toBeVisible();
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getAllByRole("radio")).toHaveLength(2);
    expect(screen.getByText("AI Sales Assistant")).toBeVisible();
    expect(screen.getByText("Opportunity Intelligence")).toBeVisible();
    expect(
      screen.getByText(
        "Start relevant customer conversations and guide every customer toward the right offer.",
      ),
    ).toBeVisible();
    expect(
      screen.getByText("Explore customer signals and identify the strongest sales opportunities."),
    ).toBeVisible();
    expect(screen.getByText("ACCOUNT CREATED")).toBeVisible();
    expect(screen.getByText("CHOOSE WORKSPACE")).toHaveAttribute("aria-current", "step");
    expect(screen.getByText("START")).toBeVisible();
  });

  it("selects exactly one product at a time", async () => {
    const user = userEvent.setup();
    renderOnboarding();

    const assistantProduct = screen.getByRole("radio", { name: "AI Sales Assistant" });
    const intelligenceProduct = screen.getByRole("radio", {
      name: "Opportunity Intelligence",
    });

    expect(assistantProduct).toBeChecked();
    expect(intelligenceProduct).not.toBeChecked();

    await user.click(intelligenceProduct);

    expect(assistantProduct).not.toBeChecked();
    expect(intelligenceProduct).toBeChecked();
    expect(screen.getAllByRole("radio", { checked: true })).toHaveLength(1);
  });

  it("continues from AI Sales Assistant to the dashboard", async () => {
    const user = userEvent.setup();
    renderOnboarding();

    await user.click(screen.getByRole("button", { name: "Continue with Assistant" }));

    expect(screen.getByText("Chat destination")).toBeVisible();
  });

  it("keeps Intelligence selected and announces that it is unavailable", async () => {
    const user = userEvent.setup();
    renderOnboarding();

    const intelligenceProduct = screen.getByRole("radio", {
      name: "Opportunity Intelligence",
    });
    await user.click(intelligenceProduct);
    await user.click(screen.getByRole("button", { name: "Open Intelligence" }));

    expect(intelligenceProduct).toBeChecked();
    expect(screen.getByRole("status")).toHaveTextContent(
      "Opportunity Intelligence is being prepared and will be available soon.",
    );
    expect(screen.queryByText("Chat destination")).not.toBeInTheDocument();
  });

  it("returns to login through the navigation-only sign-out action", async () => {
    const user = userEvent.setup();
    renderOnboarding();

    await user.click(screen.getByRole("button", { name: "Sign out" }));

    expect(screen.getByText("Login destination")).toBeVisible();
  });
});
