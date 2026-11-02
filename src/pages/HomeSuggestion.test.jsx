// @vitest-environment jsdom
import { useState } from "react";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";
import Home from "./Home";
import useChat from "../hooks/useChat";

afterEach(cleanup);

it("shows supplied suggestions, opens the conversation, and dismisses only the card", () => {
  function Preview() {
    const chat = useChat();
    const [isVisible, setIsVisible] = useState(true);
    const [isChatOpen, setIsChatOpen] = useState(false);
    return (
      <>
        <button onClick={() => chat.receiveProactiveMessage({ messageId: "one", content: "A useful suggestion." })}>
          Receive suggestion
        </button>
        {isChatOpen ? (
          <>
            <button onClick={() => setIsChatOpen(false)}>Back</button>
            {chat.conversationMessages.map((message) => <p key={message.messageId}>{message.content}</p>)}
          </>
        ) : (
          <Home assistantSuggestion={chat.proactiveMessage} isAssistantCardVisible={isVisible}
            onAssistantCardDismiss={() => setIsVisible(false)}
            onNavigate={() => setIsChatOpen(true)} onUnavailable={() => {}} />
        )}
        <button onClick={() => setIsChatOpen(true)}>Assistance chat</button>
      </>
    );
  }

  render(<Preview />);
  expect(screen.getByLabelText("Sellince suggestion").textContent).toContain("Chat is not connected yet.");
  fireEvent.click(screen.getByText("Open chat"));
  expect(screen.getByText(/Hi! I can help you find an offer/)).toBeTruthy();
  fireEvent.click(screen.getByText("Back"));
  fireEvent.click(screen.getByText("Receive suggestion"));
  expect(screen.getByLabelText("Sellince suggestion").textContent).toContain("A useful suggestion.");
  fireEvent.click(screen.getByText("View suggestion"));
  expect(screen.getByText("A useful suggestion.")).toBeTruthy();
  fireEvent.click(screen.getByText("Back"));
  fireEvent.click(screen.getByLabelText("Dismiss suggestion"));
  expect(screen.queryByLabelText("Sellince suggestion")).toBeNull();
  fireEvent.click(screen.getByText("Assistance chat"));
  expect(screen.getByText("A useful suggestion.")).toBeTruthy();
});
