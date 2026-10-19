import { MessageCircleIcon } from "lucide-react";

import { Button } from "@/components/ui/button";

function ChatButton({ launcherRef, onChatToggle }) {
  return (
    <Button
      ref={launcherRef}
      type="button"
      aria-controls="sellince-chat-dialog"
      aria-expanded="false"
      className="shadow-launcher fixed right-4 bottom-4 z-50 h-13 gap-2 rounded-full px-6 text-base font-semibold sm:right-6 sm:bottom-6"
      onClick={onChatToggle}
    >
      <MessageCircleIcon aria-hidden="true" />
      <span>Chat with Us</span>
    </Button>
  );
}

export default ChatButton;
