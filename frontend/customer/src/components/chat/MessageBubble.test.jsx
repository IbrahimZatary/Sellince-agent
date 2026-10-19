import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import MessageBubble from "@/components/chat/MessageBubble";

describe("MessageBubble", () => {
  it.each([
    ["assistant", "How can I help?"],
    ["customer", "Tell me about Sellince."],
  ])("renders a %s message", (role, content) => {
    render(<MessageBubble message={{ messageId: `${role}-1`, role, content }} />);
    expect(screen.getByText(content)).toBeVisible();
  });

  it("renders content as text rather than HTML", () => {
    render(
      <MessageBubble
        message={{
          messageId: "unsafe-message",
          role: "assistant",
          content: "<img src=x onerror=alert(1)>",
        }}
      />,
    );

    expect(screen.getByText("<img src=x onerror=alert(1)>")).toBeVisible();
    expect(document.querySelector("img")).not.toBeInTheDocument();
  });
});
