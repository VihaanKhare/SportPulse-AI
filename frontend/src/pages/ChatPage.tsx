import { useState } from "react";
import HistorySidebar from "../components/HistorySidebar.tsx";
import { Footer } from "../components/Footer.tsx";
import Header from "../components/Header.tsx";
import BannersSidebar from "../components/BannersSidebar.tsx";
import { ChatSection } from "../components/ChatSection.tsx";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";
interface Message {
  message: string;
  isUser: boolean;
  timestamp?: string;
}
export const ChatPage = () => {
  const { user, getAccessTokenSilently } = useAuth0();
  const [historyMessages, setHistoryMessages] = useState<Message[] | null>(null);
  async function fetchHistory(email: string, title: string) {
    try {
      const token = await getAccessTokenSilently();
      const response = await axios.get(
        `${import.meta.env.VITE_BACKEND_BASE_URL}/api/messages/${email}/${title}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          },
        }
      );
      // Transform the messages to the format needed by ChatSection
      const formattedMessages = response.data.messages.map((msg: any) => ({
        message: msg.content,
        isUser: msg.role === "user",
        timestamp: new Date(msg.timestamp).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit"
        })
      }));
      setHistoryMessages(formattedMessages);
      return formattedMessages;
    } catch (error) {
      console.error(`Error fetching history:`, error);
      throw error;
    }
  }
  const handleHistorySelect = (messages: Message[]) => {
    setHistoryMessages(messages);
  };
  const handleNewChat = () => {
    setHistoryMessages([]);
  };
  return (
    <>
      <Header />
      <main className="flex flex-row gap-4 py-4">
        <HistorySidebar
          func_to_fetch_History={fetchHistory}
          onHistorySelect={handleHistorySelect}
          onNewChat={handleNewChat}
        />
        <ChatSection historyMessages={historyMessages} />
        <BannersSidebar />
      </main>
      <Footer />
    </>
  );
};
export default ChatPage;