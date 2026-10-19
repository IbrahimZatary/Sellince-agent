import { XIcon } from "lucide-react";

import { Button } from "@/components/ui/button";

function ChatHeader({ onChatClose }) {
  return (
    <header className="border-border bg-surface flex shrink-0 items-center justify-between border-b px-4 py-3">
      <div>
        <h2 className="text-foreground font-semibold">Sellince Assistant</h2>
        <p className="text-muted-foreground text-xs">Ready to help</p>
      </div>
      <Button
        type="button"
        variant="ghost"
        size="icon"
        aria-label="Close assistant chat"
        onClick={onChatClose}
      >
        <XIcon aria-hidden="true" />
      </Button>
    </header>
  );
}

export default ChatHeader;
