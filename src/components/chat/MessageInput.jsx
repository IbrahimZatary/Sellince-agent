import { SendIcon } from "lucide-react";

import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

function MessageInput({
  composerRef,
  isSendingMessage,
  messageDraft,
  messageSendError,
  onMessageDraftChange,
  onMessageSubmit,
}) {
  const canSubmitMessage = messageDraft.trim().length > 0 && !isSendingMessage;

  function handleMessageDraftChange(event) {
    onMessageDraftChange(event.target.value);
  }

  function handleMessageKeyDown(event) {
    if (event.key !== "Enter" || event.shiftKey || event.nativeEvent.isComposing) {
      return;
    }

    event.preventDefault();

    if (canSubmitMessage) {
      onMessageSubmit();
    }
  }

  function handleMessageSubmit(event) {
    event.preventDefault();

    if (canSubmitMessage) {
      onMessageSubmit();
    }
  }

  return (
    <form className="border-border bg-surface shrink-0 border-t p-3" onSubmit={handleMessageSubmit}>
      {messageSendError ? (
        <Alert variant="destructive" className="mb-3">
          <AlertDescription>{messageSendError}</AlertDescription>
        </Alert>
      ) : null}

      <div className="flex items-end gap-2">
        <Label htmlFor="chat-message" className="sr-only">
          Message Sellince Assistant
        </Label>
        <Textarea
          ref={composerRef}
          id="chat-message"
          rows={1}
          value={messageDraft}
          placeholder="Type your message…"
          className="max-h-28 min-h-11 resize-none"
          disabled={isSendingMessage}
          onChange={handleMessageDraftChange}
          onKeyDown={handleMessageKeyDown}
        />
        <Button
          type="submit"
          size="icon-lg"
          className="shrink-0 rounded-full"
          disabled={!canSubmitMessage}
          aria-label={isSendingMessage ? "Sending message" : "Send message"}
        >
          <SendIcon aria-hidden="true" />
        </Button>
      </div>
    </form>
  );
}

export default MessageInput;
