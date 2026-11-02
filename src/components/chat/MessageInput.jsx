import { Send } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function MessageInput({
  messageDraft,
  messageSendError,
  isSendingMessage,
  isChatReady,
  onDraftChange,
  onMessageSubmit,
}) {
  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey && !event.nativeEvent.isComposing) {
      event.preventDefault();
      if (isChatReady && !isSendingMessage && messageDraft.trim()) onMessageSubmit();
    }
  }
  return (
    <div className="safe-bottom shrink-0 bg-white px-4 pt-3">
      {messageSendError && (
        <div
          role="alert"
          className="border-border mb-3 rounded-xl border px-3 py-2 text-sm text-neutral-700"
        >
          {messageSendError}
        </div>
      )}
      <form
        onSubmit={(event) => {
          event.preventDefault();
          onMessageSubmit();
        }}
        className="flex items-end gap-3 pb-4"
      >
        <label className="sr-only" htmlFor="message">
          Message
        </label>
        <textarea
          id="message"
          rows={1}
          value={messageDraft}
          onChange={(event) => onDraftChange(event.target.value)}
          onKeyDown={handleKeyDown}
          disabled={!isChatReady}
          placeholder="Write a message..."
          className="text-background max-h-28 min-h-12 min-w-0 flex-1 resize-y rounded-2xl border border-neutral-300 bg-white px-4 py-3 text-base leading-6 placeholder:text-neutral-500 disabled:opacity-60"
        />
        <Button
          type="submit"
          disabled={!isChatReady || isSendingMessage || !messageDraft.trim()}
          aria-label="Send message"
          className="bg-background text-foreground size-12 shrink-0 rounded-full"
        >
          <Send />
        </Button>
      </form>
    </div>
  );
}
