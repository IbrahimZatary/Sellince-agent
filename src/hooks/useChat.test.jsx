// @vitest-environment jsdom
import { act, cleanup, renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import useChat from "./useChat";

afterEach(cleanup);

describe("useChat", () => {
  it("keeps a supplied proactive message in the conversation without duplicates", () => {
    const { result } = renderHook(() => useChat());
    const message = { messageId: "suggestion-1", content: "Explore your options." };
    expect(result.current.proactiveMessage).toBeNull();
    act(() => result.current.receiveProactiveMessage(message));
    act(() => result.current.receiveProactiveMessage(message));
    expect(result.current.proactiveMessage.content).toBe(message.content);
    expect(result.current.conversationMessages).toEqual([
      { ...message, role: "assistant" },
    ]);
    act(() => result.current.receiveProactiveMessage({ messageId: "", content: "" }));
    expect(result.current.conversationMessages).toHaveLength(1);
  });
  it("keeps the draft and explains when the assistant is disconnected", async () => {
    const { result } = renderHook(() => useChat());
    act(() => result.current.handleDraftChange("Hello"));
    await act(() => result.current.handleMessageSubmit());
    expect(result.current.messageDraft).toBe("Hello");
    expect(result.current.messageSendError).toContain("isn’t connected");
    expect(result.current.conversationMessages).toHaveLength(1);
  });

  it("shows a pending message, prevents duplicate requests, and appends a real response", async () => {
    let resolveReply;
    const onMessageSend = vi.fn(
      () =>
        new Promise((resolve) => {
          resolveReply = resolve;
        }),
    );
    const { result } = renderHook(() => useChat({ onMessageSend }));
    act(() => result.current.handleDraftChange("Need a plan"));
    let request;
    act(() => {
      request = result.current.handleMessageSubmit();
    });
    expect(result.current.isSendingMessage).toBe(true);
    expect(result.current.pendingMessage).toBe("Need a plan");
    await act(() => result.current.handleMessageSubmit());
    expect(onMessageSend).toHaveBeenCalledTimes(1);
    act(() => result.current.handleDraftChange("Another question"));
    await act(async () => {
      resolveReply({ content: "Here are your options." });
      await request;
    });
    expect(result.current.isSendingMessage).toBe(false);
    expect(result.current.messageDraft).toBe("Another question");
    expect(result.current.conversationMessages.map((message) => message.content)).toEqual([
      "Hi! I can help you find an offer that fits your needs. Let’s explore your options together.",
      "Need a plan",
      "Here are your options.",
    ]);
    expect(
      new Set(result.current.conversationMessages.map((message) => message.messageId)).size,
    ).toBe(3);
  });

  it("preserves a failed message for a retry", async () => {
    const onMessageSend = vi
      .fn()
      .mockRejectedValueOnce(new Error("offline"))
      .mockResolvedValueOnce({ content: "I can help." });
    const { result } = renderHook(() => useChat({ onMessageSend }));
    act(() => result.current.handleDraftChange("Hello"));
    await act(() => result.current.handleMessageSubmit());
    expect(result.current.messageSendError).toContain("try again");
    expect(result.current.messageDraft).toBe("Hello");
    expect(result.current.conversationMessages).toHaveLength(1);
    await act(() => result.current.handleMessageSubmit());
    await waitFor(() => expect(result.current.conversationMessages).toHaveLength(3));
    expect(result.current.messageDraft).toBe("");
    expect(result.current.messageSendError).toBe("");
  });

  it("keeps draft edits made while a reply is pending", async () => {
    let resolveReply;
    const onMessageSend = () => new Promise((resolve) => { resolveReply = resolve; });
    const { result } = renderHook(() => useChat({ onMessageSend }));
    act(() => result.current.handleDraftChange("Hello"));
    let request;
    act(() => { request = result.current.handleMessageSubmit(); });
    act(() => result.current.handleDraftChange("Hello "));
    await act(async () => {
      resolveReply({ content: "Hi" });
      await request;
    });
    expect(result.current.messageDraft).toBe("Hello ");
  });

  it("does not display a malformed assistant response", async () => {
    const { result } = renderHook(() => useChat({ onMessageSend: async () => ({ content: " " }) }));
    act(() => result.current.handleDraftChange("Hello"));
    await act(() => result.current.handleMessageSubmit());
    expect(result.current.conversationMessages).toHaveLength(1);
    expect(result.current.messageDraft).toBe("Hello");
    expect(result.current.messageSendError).toContain("try again");
  });
});
