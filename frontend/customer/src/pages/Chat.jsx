import { useSearchParams } from "react-router";
import Chatbot from "@/components/chat/Chatbot";
import { requestAssistantReply } from "@/api/chat.api";

function Chat() {
  const [searchParams] = useSearchParams();
  const customerId = searchParams.get("customer_id") || localStorage.getItem("customer_id") || "1";

  const handleMessageSend = async (message) => {
    const response = await requestAssistantReply({
      customer_id: parseInt(customerId, 10),
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
