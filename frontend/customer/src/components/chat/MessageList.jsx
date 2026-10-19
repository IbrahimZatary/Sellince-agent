import { useEffect, useRef } from "react";

import MessageBubble from "@/components/chat/MessageBubble";
import { Empty, EmptyDescription, EmptyHeader, EmptyTitle } from "@/components/ui/empty";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Spinner } from "@/components/ui/spinner";

function MessageList({ messages, isSendingMessage }) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [isSendingMessage, messages]);

  return (
    <ScrollArea className="min-h-0 flex-1">
      <div
        role="log"
        aria-label="Conversation messages"
        aria-live="polite"
        aria-relevant="additions text"
        className="flex min-h-full flex-col gap-4 p-4"
      >
        {messages.length > 0 ? (
          messages.map((message) => <MessageBubble key={message.messageId} message={message} />)
        ) : (
          <Empty>
            <EmptyHeader>
              <EmptyTitle>No messages yet</EmptyTitle>
              <EmptyDescription>Start a conversation when you are ready.</EmptyDescription>
            </EmptyHeader>
          </Empty>
        )}

        {isSendingMessage ? (
          <div role="status" className="text-muted-foreground flex items-center gap-2 text-sm">
            <Spinner aria-hidden="true" aria-label={undefined} role="presentation" />
            <span>Sellince Assistant is replying…</span>
          </div>
        ) : null}

        <div ref={messagesEndRef} aria-hidden="true" />
      </div>
    </ScrollArea>
  );
}

export default MessageList;
