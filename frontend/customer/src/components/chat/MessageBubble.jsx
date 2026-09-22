import { Link } from "react-router";

import { cn } from "@/lib/utils";

function MessageBubble({ message }) {
  const isCustomerMessage = message.role === "customer";

  return (
    <div className={cn("flex", isCustomerMessage ? "justify-end" : "justify-start")}>
      <div
        className={cn(
          "max-w-[82%] rounded-2xl px-4 py-3 text-sm leading-6 break-words whitespace-pre-wrap",
          isCustomerMessage
            ? "bg-inverse text-inverse-foreground rounded-br-sm"
            : "bg-surface text-foreground border-border rounded-bl-sm border",
        )}
      >
        <p>{message.content}</p>

        {message.action && typeof message.action === "object" ? (
          <Link
            to={message.action.url}
            className="bg-primary text-primary-foreground mt-3 inline-flex w-full items-center justify-center rounded-lg px-3 py-2 font-medium transition hover:opacity-90"
          >
            {message.action.label || "Continue"}
          </Link>
        ) : null}
      </div>
    </div>
  );
}

export default MessageBubble;
