import { useAuth } from "@/components/auth/AuthContext";
import Chatbot from "@/components/chat/Chatbot";
import { requestAssistantReply } from "@/api/chat.api";

function Chat() {
  const { user } = useAuth();

  const handleMessageSend = async (message) => {
    if (!user?.customer_id) {
      throw new Error("Customer ID not available. Please complete onboarding.");
    }
    const response = await requestAssistantReply({
      customer_id: user.customer_id,
      message,
    });
    return response.response;
  };

  return (
    <main className="bg-background min-h-dvh">
      <Chatbot defaultOpen onMessageSend={handleMessageSend} />
    </main>
  );
}

export default Chat;
