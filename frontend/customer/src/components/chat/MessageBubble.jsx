import { cn } from "@/lib/utils";

function MessageBubble({ message }) {
  const isCustomerMessage = message.role === "customer";

  return (
    <div className={cn("flex", isCustomerMessage ? "justify-end" : "justify-start")}>
      <p
        className={cn(
          "max-w-[82%] rounded-2xl px-4 py-3 text-sm leading-6 break-words whitespace-pre-wrap",
          isCustomerMessage
            ? "bg-inverse text-inverse-foreground rounded-br-sm"
            : "bg-surface text-foreground border-border rounded-bl-sm border",
        )}
      >
        {message.content}
      </p>
    </div>
  );
}

export default MessageBubble;
