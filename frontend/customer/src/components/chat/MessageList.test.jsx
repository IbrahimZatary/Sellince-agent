import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import MessageList from "@/components/chat/MessageList";

describe("MessageList", () => {
  it("renders messages in an ordered live log", () => {
    render(
      <MessageList
        messages={[
          { messageId: "assistant-1", role: "assistant", content: "Welcome." },
          { messageId: "customer-1", role: "customer", content: "Hello." },
        ]}
        isSendingMessage={false}
      />,
    );

    const messageLog = screen.getByRole("log", { name: "Conversation messages" });
    expect(messageLog).toHaveAttribute("aria-live", "polite");
    expect(within(messageLog).getByText("Welcome.")).toBeVisible();
    expect(within(messageLog).getByText("Hello.")).toBeVisible();
  });

  it("renders its empty and sending states", () => {
    const { rerender } = render(<MessageList messages={[]} isSendingMessage={false} />);
    expect(screen.getByText("No messages yet")).toBeVisible();

    rerender(<MessageList messages={[]} isSendingMessage />);
    expect(screen.getByRole("status")).toHaveTextContent("Sellince Assistant is replying");
  });
});
