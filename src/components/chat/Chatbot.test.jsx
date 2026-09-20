import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import Chatbot from "@/components/chat/Chatbot";

describe("Chatbot", () => {
  it("opens the popup and focuses the composer", async () => {
    const user = userEvent.setup();
    render(<Chatbot />);

    await user.click(screen.getByRole("button", { name: "Chat with Us" }));

    expect(screen.getByRole("dialog", { name: "Sellince Assistant chat" })).toBeVisible();
    expect(screen.getByLabelText("Message Sellince Assistant")).toHaveFocus();
  });

  it("closes with Escape and restores focus to the launcher", async () => {
    const user = userEvent.setup();
    render(<Chatbot />);

    await user.click(screen.getByRole("button", { name: "Chat with Us" }));
    await user.keyboard("{Escape}");

    const launcher = screen.getByRole("button", { name: "Chat with Us" });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(launcher).toHaveFocus();
  });

  it("preserves the draft while the backend contract is unavailable", async () => {
    const user = userEvent.setup();
    render(<Chatbot defaultOpen />);

    const composer = screen.getByLabelText("Message Sellince Assistant");
    await user.type(composer, "Tell me about my plan");
    await user.click(screen.getByRole("button", { name: "Send message" }));

    expect(screen.getByRole("alert")).toHaveTextContent(
      "Messaging is not available yet. Please try again later.",
    );
    expect(composer).toHaveValue("Tell me about my plan");
    const messageLog = screen.getByRole("log", { name: "Conversation messages" });
    expect(within(messageLog).queryByText("Tell me about my plan")).not.toBeInTheDocument();
  });

  it("renders normalized messages returned by a connected adapter", async () => {
    const user = userEvent.setup();
    const handleMessageSend = vi.fn().mockResolvedValue("Here is the answer.");
    render(<Chatbot defaultOpen onMessageSend={handleMessageSend} />);

    const composer = screen.getByLabelText("Message Sellince Assistant");
    await user.type(composer, "My question");
    await user.click(screen.getByRole("button", { name: "Send message" }));

    expect(await screen.findByText("My question")).toBeVisible();
    expect(screen.getByText("Here is the answer.")).toBeVisible();
    expect(handleMessageSend).toHaveBeenCalledWith("My question");
    expect(composer).toHaveValue("");
  });

  it("shows a safe error and preserves the draft when sending fails", async () => {
    const user = userEvent.setup();
    const handleMessageSend = vi.fn().mockRejectedValue(new Error("Network details"));
    render(<Chatbot defaultOpen onMessageSend={handleMessageSend} />);

    const composer = screen.getByLabelText("Message Sellince Assistant");
    await user.type(composer, "Please retry this");
    await user.click(screen.getByRole("button", { name: "Send message" }));

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Your message could not be sent. Please try again.",
    );
    expect(composer).toHaveValue("Please retry this");
  });
});
