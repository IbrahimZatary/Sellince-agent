import { useState } from "react";
import { ArrowLeft, X } from "lucide-react";
import { MobileHeader, BottomNavigation } from "@/components/MobileShell";
import useChat from "@/hooks/useChat";
import Chat from "@/pages/Chat";
import Login from "@/pages/Login";
import Home from "@/pages/Home";
import { Assistance, Marketplace, Money, MyLine, Rewards } from "@/pages/Services";

export default function App() {
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  return isPreviewOpen ? (
    <MobilePreview onExit={() => setIsPreviewOpen(false)} />
  ) : (
    <Login onPreview={() => setIsPreviewOpen(true)} />
  );
}

function MobilePreview({ onExit }) {
  const chat = useChat();
  const [currentScreen, setCurrentScreen] = useState("home");
  const [isNoticeVisible, setIsNoticeVisible] = useState(false);
  const [isAssistantCardVisible, setIsAssistantCardVisible] = useState(true);
  const [chatReturnScreen, setChatReturnScreen] = useState("assistance");
  function handleNavigate(screen) {
    setIsNoticeVisible(false);
    if (screen === "chat") setChatReturnScreen(currentScreen);
    setCurrentScreen(screen);
    window.scrollTo(0, 0);
  }
  function handleUnavailable() {
    setIsNoticeVisible(true);
  }
  if (currentScreen === "chat")
    return (
      <div className="mx-auto min-h-dvh max-w-[480px]">
        <Chat
          backLabel={chatReturnScreen === "home" ? "Back to home" : "Back to assistance"}
          onBack={() => handleNavigate(chatReturnScreen)}
          messages={chat.conversationMessages}
          messageDraft={chat.messageDraft}
          messageSendError={chat.messageSendError}
          pendingMessage={chat.pendingMessage}
          isSendingMessage={chat.isSendingMessage}
          isInitializing={false}
          isChatReady
          isConnected={false}
          onDraftChange={chat.handleDraftChange}
          onMessageSubmit={chat.handleMessageSubmit}
        />
      </div>
    );
  return (
    <div className="bg-background text-foreground mx-auto min-h-dvh max-w-[480px] pb-[calc(8rem+env(safe-area-inset-bottom))]">
      {currentScreen === "assistance" ? (
        <header className="safe-top">
          <button
            type="button"
            onClick={() => handleNavigate("home")}
            aria-label="Back to home"
            className="m-4 grid size-10 place-items-center"
          >
            <ArrowLeft size={23} />
          </button>
        </header>
      ) : (
        <MobileHeader
          onNavigate={handleNavigate}
          onUnavailable={handleUnavailable}
          onSignOut={onExit}
        />
      )}
      {currentScreen === "home" && (
        <Home
          assistantSuggestion={chat.proactiveMessage}
          isAssistantCardVisible={isAssistantCardVisible}
          onAssistantCardDismiss={() => setIsAssistantCardVisible(false)}
          onNavigate={handleNavigate}
          onUnavailable={handleUnavailable}
        />
      )}
      {currentScreen === "line" && <MyLine onUnavailable={handleUnavailable} />}
      {currentScreen === "marketplace" && <Marketplace onUnavailable={handleUnavailable} />}
      {currentScreen === "rewards" && <Rewards onUnavailable={handleUnavailable} />}
      {currentScreen === "money" && <Money />}
      {currentScreen === "assistance" && (
        <Assistance onNavigate={handleNavigate} onUnavailable={handleUnavailable} />
      )}
      {isNoticeVisible && (
        <div
          role="status"
          className="border-border bg-raised fixed right-4 bottom-[calc(7rem+env(safe-area-inset-bottom))] left-4 z-20 mx-auto flex max-w-[448px] items-start gap-3 rounded-xl border p-4 text-sm shadow-lg"
        >
          <span className="flex-1">This service is not connected in the preview.</span>
          <button
            type="button"
            onClick={() => setIsNoticeVisible(false)}
            aria-label="Dismiss notice"
          >
            <X size={18} />
          </button>
        </div>
      )}
      {currentScreen !== "assistance" && (
        <BottomNavigation currentScreen={currentScreen} onNavigate={handleNavigate} />
      )}
    </div>
  );
}
