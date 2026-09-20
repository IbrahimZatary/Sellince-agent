import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { createRef } from "react";
import { describe, expect, it, vi } from "vitest";

import ChatButton from "@/components/chat/ChatButton";

describe("ChatButton", () => {
  it("labels and connects the popup launcher accessibly", async () => {
    const user = userEvent.setup();
    const handleChatToggle = vi.fn();
    const launcherRef = createRef();

    render(<ChatButton launcherRef={launcherRef} onChatToggle={handleChatToggle} />);

    const launcher = screen.getByRole("button", { name: "Chat with Us" });
    expect(launcher).toHaveAttribute("aria-controls", "sellince-chat-dialog");
    expect(launcher).toHaveAttribute("aria-expanded", "false");
    expect(launcherRef.current).toBe(launcher);

    await user.click(launcher);
    expect(handleChatToggle).toHaveBeenCalledOnce();
  });
});
