import ChatHeader from "@/components/chat/ChatHeader";
import MessageList from "@/components/chat/MessageList";
import MessageInput from "@/components/chat/MessageInput";

export default function Chat({
  backLabel,
  onBack,
  messages,
  messageDraft,
  messageSendError,
  pendingMessage,
  isSendingMessage,
  isInitializing,
  isChatReady,
  isConnected,
  onDraftChange,
  onMessageSubmit,
}) {
  return (
    <main className="safe-top bg-chat flex h-dvh flex-col">
      <ChatHeader backLabel={backLabel} onBack={onBack} isConnected={isConnected} />
      <MessageList
        messages={messages}
        pendingMessage={pendingMessage}
        isSendingMessage={isSendingMessage}
        isInitializing={isInitializing}
        onPromptSelect={onDraftChange}
      />
      <MessageInput
        messageDraft={messageDraft}
        messageSendError={messageSendError}
        isSendingMessage={isSendingMessage}
        isChatReady={isChatReady}
        onDraftChange={onDraftChange}
        onMessageSubmit={onMessageSubmit}
      />
    </main>
  );
}
