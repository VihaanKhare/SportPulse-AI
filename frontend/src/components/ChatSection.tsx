import "../../public/styles/ChatSection.css";
import Input from "@mui/joy/Input";
import { ChevronRight, Mic, MicOff } from "lucide-react";
import { Button } from "../components/ui/button";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";
import { useState, useRef, useEffect } from "react";
import ChatBubble from "./ChatBubble";
import supabase from "../utils/supabase";
import gemini from "../services/llm/gemini";
interface Message {
  message: string;
  isUser: boolean;
  timestamp?: string;
}
interface ChatSectionProps {
  historyMessages?: Message[]|null;
  clearChat?: () => void;
}
export const ChatSection = ({ historyMessages }: ChatSectionProps) => {
  const { getAccessTokenSilently } = useAuth0();
  const [query, setQuery] = useState<string>("");
  const [currentMessages, setCurrentMessages] = useState<Message[]>([]);
  const [, setLoading] = useState<boolean>(false);
  const [buttonDisabled, setButtonDisabled] = useState(false);
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [, setAudioBlob] = useState<Blob | null>(null);
  const [, setUrl] = useState<string>("");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [currentMessages]);
  // Load history messages when they change
  useEffect(() => {
    if (historyMessages && historyMessages.length > 0) {
      setCurrentMessages(historyMessages);
    }
  }, [historyMessages]);
  async function messageSend() {
    if (!query.trim()) return;
    const userMessage: Message = {
      message: query,
      isUser: true,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };
    setCurrentMessages((prev) => [...prev, userMessage]);
    setQuery("");
    setLoading(true);
    setButtonDisabled(true);
    try {
      // const token = await getAccessTokenSilently();
      // const response = await axios.post(
      //   `${import.meta.env.VITE_BACKEND_BASE_URL}/query`,
      //   { query: query },
      //   {
      //     headers: {
      //       Authorization: `Bearer ${token}`,
      //     },
      //   }
      // );
      const result = await gemini(query);
      const llmMessage: Message = {
        message: result,
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setCurrentMessages((prev) => [...prev, llmMessage]);
      // Save conversation if it's the first message
      if (currentMessages.length === 0) {
        saveConversationTitle(query);
      }
    } catch (error) {
      const errorMessage: Message = {
        message: `Error fetching response! Error: ${error}`,
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setCurrentMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setTimeout(() => {
        setButtonDisabled(false);
      }, 5000);
    }
  }
  const saveConversationTitle = async (firstQuery: string) => {
    try {
      const title = firstQuery.split(" ").slice(0, 5).join(" ");
      const token = await getAccessTokenSilently();
      const { user } = useAuth0();
      await axios.post(
        `${import.meta.env.VITE_BACKEND_BASE_URL}/api/titles`,
        {
          email: user?.email,
          title: title
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
    } catch (error) {
      console.error("Error saving conversation title:", error);
    }
  };
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !buttonDisabled && !isRecording) {
      messageSend();
    }
  };
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setAudioBlob(audioBlob);
        await handleAudioStop(audioBlob);
      };
      mediaRecorder.start();
      setIsRecording(true);
      setQuery("Recording...");
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setQuery("");
    }
  };
  const handleAudioInputToggle = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };
  const handleAudioStop = async (audioBlob: Blob) => {
    const fileExt = 'webm';
    const fileName = `${Math.random()}.${fileExt}`;
    const filePath = `${fileName}`;
    try {
      const { data, error } = await supabase.storage
        .from("gcaudios")
        .upload(filePath, audioBlob, {
          cacheControl: '3600',
          upsert: false,
        });
      if (error) throw error;
      const { data: { publicUrl } } = supabase.storage
        .from('gcaudios')
        .getPublicUrl(filePath);
      console.log('Uploaded to:', publicUrl);
      setUrl(publicUrl);
      const audioMessage: Message = {
        message: `Audio uploaded`,
        isUser: true,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setCurrentMessages((prev) => [...prev, audioMessage]);
    } catch (error) {
      console.error('Error uploading audio:', error);
    }
  };
  return (
    <div id="chat" className="chat flex flex-col bg-neutral-900 p-4 h-full">
      <div
        ref={chatContainerRef}
        className="flex flex-col overflow-y-auto hide-scrollbar flex-1 mb-4"
      >
        {currentMessages.map((msg, idx) => (
          <ChatBubble
            key={idx}
            message={msg.message}
            isUser={msg.isUser}
            timestamp={msg.timestamp}
          />
        ))}
      </div>
      <div className="flex gap-2">
        <Input
          id="chat_prompt"
          className="w-full chat_input"
          color="neutral"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder={isRecording ? "Recording..." : "Let's Chat"}
          variant="soft"
          disabled={isRecording}
        />
        <Button
          className="prompt_btn"
          size="icon"
          onClick={messageSend}
          disabled={buttonDisabled || isRecording}
        >
          <ChevronRight />
        </Button>
        <Button
          className="mic_btn"
          size="icon"
          variant={!isRecording ? "destructive" : "default"}
          onClick={handleAudioInputToggle}
          style={{"cursor":"pointer"}}
        >
          {!isRecording ? <MicOff /> : <Mic />}
        </Button>
      </div>
    </div>
  );
};