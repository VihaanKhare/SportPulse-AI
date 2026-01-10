import { useEffect, useState } from "react";
import { Clock, Trash2 } from "lucide-react";
import { Button } from "./ui/button.tsx";
import { Card } from "./ui/card.tsx";
import { cn } from "../lib/utils.ts";
import "../../public/styles/HistorySidebar.css"
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";
import { HistorySidebarProps } from "@/types/types.ts";
export const HistorySidebar: React.FC<HistorySidebarProps> = ({
  func_to_fetch_History,
  onHistorySelect,
  onNewChat
}) => {
  const [hoveredItem, setHoveredItem] = useState<number | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [selectedHistoryId, setSelectedHistoryId] = useState<number | null>(null);
  const { user, getAccessTokenSilently } = useAuth0();
  async function getTitles(email: string) {
    try {
      const url = import.meta.env.VITE_BACKEND_BASE_URL;
      const token = await getAccessTokenSilently();
      const response = await axios.get(`${url}/api/titles/${email}`, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "ngrok-skip-browser-warning": true
        },withCredentials:true
      });
      return response.data.titles;
    } catch (error) {
      console.error("Error fetching titles:", error);
      throw error;
    }
  }
  const handleHistoryClick = async (id: number, title: string) => {
    setSelectedHistoryId(id);
    try {
      if (user?.email) {
        const historyData = await func_to_fetch_History(user.email, title);
        onHistorySelect(historyData);
      }
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };
  const handleNewChat = () => {
    setSelectedHistoryId(null);
    onNewChat();
  };
  const deleteHistory = async ()=>{
    try{
      const token = await getAccessTokenSilently();
    const response = await axios.delete(`${import.meta.env.VITE_BACKEND_BASE_URL}/api/conversation`,{
      headers:{"Authorization": `Bearer ${token}`},
    })
    console.log(response)
  }
  catch(e){
    throw e;
  }
  }
  useEffect(() => {
    if (user?.email) {
      (async () => {
        console.log('yaha hu bsdk')
        const titles = await getTitles(user.email as string);
        console.log(titles)
        setHistory(titles);
      })();
    }
  }, [user?.email]);
  return (
    <div id="history" className="history flex flex-col bg-neutral-900 p-4">
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center text-yellow-50">
          <Clock size={20} className="mr-2" />
          <h2 className="text-xl font-bold">History</h2>
        </div>
        <Button variant="ghost" size="icon" className="cursor-pointer text-neutral-400 hover:text-neutral-200">
          <Trash2 size={30} onClick={deleteHistory} />
        </Button>
      </div>
      <div className="flex flex-col space-y-2 flex-grow overflow-auto">
        {history?.map((item) => (
          <Card
            key={item.id}
            className={cn(
              "p-4 rounded-lg cursor-pointer border-0 transition-all duration-200",
              selectedHistoryId === item.id
                ? "bg-neutral-600 text-neutral-100"
                : hoveredItem === item.id
                  ? "bg-neutral-800 text-neutral-100"
                  : "bg-neutral-700 text-neutral-100"
            )}
            onMouseEnter={() => setHoveredItem(item.id)}
            onMouseLeave={() => setHoveredItem(null)}
            onClick={() => handleHistoryClick(item.id, item[item.id])}
          >
            <h3 className="text-l p-0 m-0">{item[item.id]}</h3>
          </Card>
        ))}
      </div>
      <Button
        className="w-full newChat mt-4 py-5"
        onClick={handleNewChat}
      >
        New Chat
      </Button>
    </div>
  );
};
export default HistorySidebar;  