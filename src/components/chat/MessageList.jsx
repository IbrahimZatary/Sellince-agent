import { useEffect, useRef } from "react";
import SellinceMark from "./SellinceMark";

export default function MessageList({
  messages,
  pendingMessage,
  isSendingMessage,
  isInitializing,
  onPromptSelect,
}) {
  const listRef = useRef(null);
  const shouldScrollToBottom = useRef(true);
  useEffect(() => {
    const list = listRef.current;
    if (list && shouldScrollToBottom.current) list.scrollTop = list.scrollHeight;
  }, [messages, pendingMessage, isInitializing]);
  return (
    <section
      ref={listRef}
      onScroll={(event) => {
        const list = event.currentTarget;
        shouldScrollToBottom.current = list.scrollHeight - list.scrollTop - list.clientHeight < 48;
      }}
      aria-label="Conversation"
      className="bg-chat flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto overscroll-contain px-4 py-6"
    >
      <p className="text-center text-xs font-medium text-neutral-600">Your conversation</p>
      <div aria-live="polite" aria-relevant="additions text" className="flex flex-col gap-4">
        {isInitializing && (
          <div role="status" className="flex items-center gap-3 text-sm text-neutral-600">
            <span className="bg-surface text-primary grid size-8 shrink-0 place-items-center rounded-full">
              <SellinceMark className="h-4 w-4" />
            </span>
            Preparing your conversation…
          </div>
        )}
        {!isInitializing && messages.length === 0 && (
          <p className="my-auto py-8 text-center text-sm text-neutral-600">
            Your conversation will appear here.
          </p>
        )}
        {messages.map((message) => (
          <div
            key={message.messageId}
            className={message.role === "customer" ? "flex justify-end" : "flex items-end gap-2"}
          >
            {message.role === "assistant" && (
              <span
                aria-hidden="true"
                className="bg-surface text-primary grid size-8 shrink-0 place-items-center rounded-full"
              >
                <SellinceMark className="h-4 w-4" />
              </span>
            )}
            <div
              dir="auto"
              className={
                message.role === "customer"
                  ? "bg-primary text-primary-foreground max-w-[85%] rounded-2xl rounded-br-sm px-4 py-3 text-sm leading-5 break-words whitespace-pre-wrap"
                  : "text-background max-w-[85%] rounded-2xl rounded-bl-sm bg-white px-4 py-3 text-sm leading-5 break-words whitespace-pre-wrap"
              }
            >
              {message.content}
            </div>
          </div>
        ))}
        {pendingMessage && (
          <div className="flex justify-end">
            <div
              dir="auto"
              className="bg-primary text-primary-foreground max-w-[85%] rounded-2xl rounded-br-sm px-4 py-3 text-sm leading-5 break-words whitespace-pre-wrap"
            >
              {pendingMessage}
            </div>
          </div>
        )}
        {isSendingMessage && (
          <div role="status" className="flex items-center gap-2 text-xs text-neutral-600">
            <span className="bg-surface text-primary grid size-8 shrink-0 place-items-center rounded-full">
              <SellinceMark className="h-4 w-4" />
            </span>
            Sellince is replying…
          </div>
        )}
      </div>
      {!isInitializing && messages.length === 1 && !pendingMessage && (
        <div className="ml-10 flex flex-wrap gap-2" aria-label="Suggested questions">
          <button
            type="button"
            onClick={() => onPromptSelect("What offers are available?")}
            className="border-border text-background rounded-full border bg-white px-3 py-2 text-xs font-medium"
          >
            Explore offers
          </button>
          <button
            type="button"
            onClick={() => onPromptSelect("Help me choose a plan.")}
            className="border-border text-background rounded-full border bg-white px-3 py-2 text-xs font-medium"
          >
            Help me choose
          </button>
        </div>
      )}
    </section>
  );
}
