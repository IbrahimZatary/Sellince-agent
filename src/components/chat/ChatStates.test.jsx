// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";

afterEach(cleanup);

describe("chat interaction states", () => {
  it("shows loading and sending states without showing an empty conversation", () => {
    const { rerender } = render(
      <MessageList
        messages={[]}
        pendingMessage=""
        isSendingMessage={false}
        isInitializing
        onPromptSelect={() => {}}
      />,
    );
    expect(screen.getByRole("status").textContent).toContain("Preparing");
    expect(screen.queryByText("Your conversation will appear here.")).toBeNull();
    rerender(
      <MessageList
        messages={[]}
        pendingMessage="Hello"
        isSendingMessage
        isInitializing={false}
        onPromptSelect={() => {}}
      />,
    );
    expect(screen.getByText("Hello")).toBeTruthy();
    expect(screen.getByRole("status").textContent).toContain("replying");
  });

  it("submits on Enter but keeps Shift+Enter and IME composition for typing", () => {
    const onMessageSubmit = vi.fn();
    render(
      <MessageInput
        messageDraft="Hello"
        messageSendError=""
        isSendingMessage={false}
        isChatReady
        onDraftChange={() => {}}
        onMessageSubmit={onMessageSubmit}
      />,
    );
    const input = screen.getByRole("textbox", { name: "Message" });
    fireEvent.keyDown(input, { key: "Enter", shiftKey: true });
    expect(onMessageSubmit).not.toHaveBeenCalled();
    fireEvent.keyDown(input, { key: "Enter", isComposing: true });
    expect(onMessageSubmit).not.toHaveBeenCalled();
    fireEvent.keyDown(input, { key: "Enter" });
    expect(onMessageSubmit).toHaveBeenCalledTimes(1);
  });

  it("blocks submission while sending and exposes an error", () => {
    const onMessageSubmit = vi.fn();
    render(
      <MessageInput
        messageDraft="Hello"
        messageSendError="Please try again."
        isSendingMessage
        isChatReady
        onDraftChange={() => {}}
        onMessageSubmit={onMessageSubmit}
      />,
    );
    expect(screen.getByRole("alert").textContent).toBe("Please try again.");
    expect(screen.getByRole("button", { name: "Send message" }).disabled).toBe(true);
    fireEvent.keyDown(screen.getByRole("textbox", { name: "Message" }), { key: "Enter" });
    expect(onMessageSubmit).not.toHaveBeenCalled();
  });
});
