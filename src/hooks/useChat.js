import { useRef, useState } from "react";

const INITIAL_ASSISTANT_MESSAGE = {
  messageId: "assistant-welcome",
  role: "assistant",
  content: "Hi! I can help you find an offer that fits your needs. Let’s explore your options together.",
};

let messageSequence = 0;

function createMessage(role, content) {
  const messageId = globalThis.crypto?.randomUUID?.() ?? `message-${++messageSequence}`;
  return { messageId, role, content };
}

// The backend team can supply a callback that returns a UI message with a content string.
export default function useChat({ onMessageSend } = {}) {
  const [conversationMessages, setConversationMessages] = useState([INITIAL_ASSISTANT_MESSAGE]);
  const [messageDraft, setMessageDraft] = useState("");
  const [messageSendError, setMessageSendError] = useState("");
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const [pendingMessage, setPendingMessage] = useState("");
  const [proactiveMessage, setProactiveMessage] = useState(null);
  const isSubmissionPending = useRef(false);

  function receiveProactiveMessage(message) {
    if (typeof message?.messageId !== "string" || !message.messageId.trim() ||
        typeof message.content !== "string" || !message.content.trim()) return;

    const assistantMessage = {
      messageId: message.messageId,
      role: "assistant",
      content: message.content.trim(),
    };
    setProactiveMessage(assistantMessage);
    setConversationMessages((messages) => {
      if (messages.some((existingMessage) => existingMessage.messageId === assistantMessage.messageId)) {
        return messages.map((existingMessage) =>
          existingMessage.messageId === assistantMessage.messageId ? assistantMessage : existingMessage,
        );
      }
      if (messages.length === 1 && messages[0].messageId === INITIAL_ASSISTANT_MESSAGE.messageId) {
        return [assistantMessage];
      }
      return [...messages, assistantMessage];
    });
  }

  function handleDraftChange(nextDraft) {
    setMessageDraft(nextDraft);
    setMessageSendError("");
  }

  async function handleMessageSubmit() {
    const submittedMessage = messageDraft.trim();
    if (!submittedMessage || isSubmissionPending.current) return;
    if (typeof onMessageSend !== "function") {
      setMessageSendError("Chat isn’t connected yet. Your message is saved in the box below.");
      return;
    }
    isSubmissionPending.current = true;
    setIsSendingMessage(true);
    setPendingMessage(submittedMessage);
    setMessageSendError("");
    try {
      const assistantMessage = await onMessageSend(submittedMessage);
      if (typeof assistantMessage?.content !== "string" || !assistantMessage.content.trim()) {
        throw new Error("Invalid assistant message");
      }
      const customerMessage = createMessage("customer", submittedMessage);
      const replyMessage = createMessage("assistant", assistantMessage.content.trim());
      setConversationMessages((messages) => [...messages, customerMessage, replyMessage]);
      setMessageDraft((draft) => (draft.trim() === submittedMessage ? "" : draft));
    } catch {
      setMessageSendError("Your message couldn’t be sent. Please try again.");
    } finally {
      isSubmissionPending.current = false;
      setIsSendingMessage(false);
      setPendingMessage("");
    }
  }

  return {
    conversationMessages,
    messageDraft,
    messageSendError,
    isSendingMessage,
    pendingMessage,
    proactiveMessage,
    receiveProactiveMessage,
    handleDraftChange,
    handleMessageSubmit,
  };
}
