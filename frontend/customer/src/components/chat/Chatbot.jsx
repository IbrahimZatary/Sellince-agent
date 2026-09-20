import { useEffect, useRef } from "react";

import ChatButton from "@/components/chat/ChatButton";
import ChatHeader from "@/components/chat/ChatHeader";
import MessageInput from "@/components/chat/MessageInput";
import MessageList from "@/components/chat/MessageList";
import useChat from "@/hooks/useChat";
import { cn } from "@/lib/utils";

function Chatbot({ defaultOpen = false, onMessageSend, className }) {
  const launcherRef = useRef(null);
  const composerRef = useRef(null);
  const wasChatOpenRef = useRef(defaultOpen);
  const {
    conversationMessages,
    handleChatClose,
    handleChatToggle,
    handleMessageDraftChange,
    handleMessageSubmit,
    isChatOpen,
    isSendingMessage,
    messageDraft,
    messageSendError,
  } = useChat({ defaultOpen, onMessageSend });

  useEffect(() => {
    if (isChatOpen) {
      composerRef.current?.focus();

      function handleEscapeKey(event) {
        if (event.key === "Escape") {
          handleChatClose();
        }
      }

      document.addEventListener("keydown", handleEscapeKey);
      wasChatOpenRef.current = true;

      return () => document.removeEventListener("keydown", handleEscapeKey);
    }

    if (wasChatOpenRef.current) {
      launcherRef.current?.focus();
      wasChatOpenRef.current = false;
    }
  }, [handleChatClose, isChatOpen]);

  return (
    <div className={cn("relative", className)}>
      {isChatOpen ? (
        <section
          id="sellince-chat-dialog"
          role="dialog"
          aria-label="Sellince Assistant chat"
          className="border-border bg-chat shadow-float fixed right-3 bottom-3 z-50 flex h-[calc(100dvh-1.5rem)] max-h-[38rem] w-[calc(100vw-1.5rem)] flex-col overflow-hidden rounded-2xl border sm:right-6 sm:bottom-6 sm:h-[36rem] sm:w-[25rem]"
        >
          <ChatHeader onChatClose={handleChatClose} />
          <MessageList messages={conversationMessages} isSendingMessage={isSendingMessage} />
          <MessageInput
            composerRef={composerRef}
            isSendingMessage={isSendingMessage}
            messageDraft={messageDraft}
            messageSendError={messageSendError}
            onMessageDraftChange={handleMessageDraftChange}
            onMessageSubmit={handleMessageSubmit}
          />
        </section>
      ) : (
        <ChatButton launcherRef={launcherRef} onChatToggle={handleChatToggle} />
      )}
    </div>
  );
}

export default Chatbot;
