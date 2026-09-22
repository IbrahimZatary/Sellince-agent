import { useCallback, useRef, useState } from "react";

const INITIAL_ASSISTANT_MESSAGE = {
  messageId: "initial-assistant-message",
  role: "assistant",
  content: "Hi! I’m the Sellince Assistant. How can I help you today?",
};

const CHAT_UNAVAILABLE_MESSAGE = "Messaging is not available yet. Please try again later.";

const CHAT_ERROR_MESSAGE = "Your message could not be sent. Please try again.";

let fallbackMessageSequence = 0;

function createMessage(role, content, action) {
  const fallbackMessageId = `${role}-${Date.now()}-${fallbackMessageSequence++}`;

  return {
    messageId: globalThis.crypto?.randomUUID?.() ?? fallbackMessageId,
    role,
    content,
    action,
  };
}

/**
 * Owns the chatbot state and exposes its UI actions.
 * Connect onMessageSend after the authenticated chat contract is confirmed.
 */
function useChat({ defaultOpen = false, onMessageSend } = {}) {
  const [isChatOpen, setIsChatOpen] = useState(defaultOpen);
  const [conversationMessages, setConversationMessages] = useState([INITIAL_ASSISTANT_MESSAGE]);
  const [messageDraft, setMessageDraft] = useState("");
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const [messageSendError, setMessageSendError] = useState("");

  const isSubmissionPendingRef = useRef(false);

  function handleChatToggle() {
    setIsChatOpen((currentState) => !currentState);
  }

  const handleChatClose = useCallback(() => {
    setIsChatOpen(false);
  }, []);

  function handleMessageDraftChange(nextDraft) {
    setMessageDraft(nextDraft);

    if (messageSendError) {
      setMessageSendError("");
    }
  }

  async function handleMessageSubmit() {
    const submittedMessage = messageDraft.trim();

    if (!submittedMessage || isSubmissionPendingRef.current) {
      return false;
    }

    if (typeof onMessageSend !== "function") {
      setMessageSendError(CHAT_UNAVAILABLE_MESSAGE);
      return false;
    }

    isSubmissionPendingRef.current = true;
    setIsSendingMessage(true);
    setMessageSendError("");

    try {
      const assistantReply = await onMessageSend(submittedMessage);

      const assistantText =
        typeof assistantReply === "string" ? assistantReply : assistantReply?.response || "";
      const assistantAction =
        typeof assistantReply === "object" && assistantReply !== null
          ? assistantReply.action
          : undefined;
      if (!assistantText.trim()) {
        throw new Error("Invalid assistant reply");
      }

      setConversationMessages((currentMessages) => [
        ...currentMessages,
        createMessage("customer", submittedMessage),
        createMessage("assistant", assistantText.trim(), assistantAction),
      ]);

      // Do not erase text entered while the request was pending.
      setMessageDraft((currentDraft) =>
        currentDraft.trim() === submittedMessage ? "" : currentDraft,
      );

      return true;
    } catch {
      setMessageSendError(CHAT_ERROR_MESSAGE);
      return false;
    } finally {
      isSubmissionPendingRef.current = false;
      setIsSendingMessage(false);
    }
  }

  return {
    conversationMessages,
    isChatOpen,
    isSendingMessage,
    messageDraft,
    messageSendError,
    handleChatClose,
    handleChatToggle,
    handleMessageDraftChange,
    handleMessageSubmit,
  };
}

export default useChat;
