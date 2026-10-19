import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { describe, expect, it, vi } from "vitest";

import MessageInput from "@/components/chat/MessageInput";

function MessageInputHarness({
  isSendingMessage = false,
  messageSendError = "",
  onMessageSubmit = vi.fn(),
}) {
  const [messageDraft, setMessageDraft] = useState("");

  return (
    <MessageInput
      isSendingMessage={isSendingMessage}
      messageDraft={messageDraft}
      messageSendError={messageSendError}
      onMessageDraftChange={setMessageDraft}
      onMessageSubmit={onMessageSubmit}
    />
  );
}

describe("MessageInput", () => {
  it("disables whitespace-only and pending submissions", async () => {
    const user = userEvent.setup();
    const { rerender } = render(<MessageInputHarness />);

    const composer = screen.getByLabelText("Message Sellince Assistant");
    const sendButton = screen.getByRole("button", { name: "Send message" });
    expect(sendButton).toBeDisabled();

    await user.type(composer, "   ");
    expect(sendButton).toBeDisabled();

    rerender(<MessageInputHarness isSendingMessage />);
    expect(screen.getByRole("button", { name: "Sending message" })).toBeDisabled();
  });

  it("submits with Enter and keeps Shift+Enter as a newline", async () => {
    const user = userEvent.setup();
    const handleMessageSubmit = vi.fn();
    render(<MessageInputHarness onMessageSubmit={handleMessageSubmit} />);

    const composer = screen.getByLabelText("Message Sellince Assistant");
    await user.type(composer, "First line");
    await user.keyboard("{Shift>}{Enter}{/Shift}Second line");
    expect(composer).toHaveValue("First line\nSecond line");

    await user.keyboard("{Enter}");
    expect(handleMessageSubmit).toHaveBeenCalledOnce();
  });

  it("ignores Enter during IME composition and shows errors", () => {
    const handleMessageSubmit = vi.fn();
    render(
      <MessageInputHarness
        messageSendError="Messaging is not connected."
        onMessageSubmit={handleMessageSubmit}
      />,
    );

    const composer = screen.getByLabelText("Message Sellince Assistant");
    fireEvent.change(composer, { target: { value: "Composed text" } });
    fireEvent.keyDown(composer, { key: "Enter", isComposing: true });

    expect(handleMessageSubmit).not.toHaveBeenCalled();
    expect(screen.getByRole("alert")).toHaveTextContent("Messaging is not connected.");
  });
});
