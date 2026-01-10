import React, { useState } from "react";
import { User, Bot, Copy, CheckCheck } from "lucide-react";
import { ChatBubbleProps } from "@/types/types";

export const ChatBubble: React.FC<ChatBubbleProps> = ({
  message,
  isUser,
  timestamp,
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`w-full py-4 ${isUser ? "bg-transparent" : "bg-gray-100/70 rounded-lg dark:bg-gray-700/30"}`}>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 flex gap-3">
        {/* Avatar - Using flex-shrink-0 to prevent it from shrinking */}
        <div 
          className="h-10 w-10 flex-shrink-0 flex items-center justify-center rounded-full"
          style={{ backgroundColor: "rgb(84, 42, 186)" }}
        >
          {isUser ? (
            <User size={20} className="text-white" />
          ) : (
            <Bot size={20} className="text-white" />
          )}
        </div>

        {/* Message and Info - Using min-width-0 to allow proper text wrapping */}
        <div className="flex-1 min-w-0 flex flex-col">
          {/* Name and Timestamp */}
          <div className="flex items-center gap-2 mb-1">
            <p className="font-semibold text-sm text-gray-800 dark:text-gray-200">
              {isUser ? "You" : "SportBot"}
            </p>
            {timestamp && (
              <span className="text-xs text-gray-500">{timestamp}</span>
            )}
          </div>

          {/* Message Content - Using break-words to handle long content */}
          <div
  className="text-sm leading-relaxed text-gray-700 dark:text-gray-300 prose dark:prose-invert max-w-none break-words"
  dangerouslySetInnerHTML={{
    __html: message.replace(/\\n/g, "<br/>"), // Replace literal '\n' with <br />
  }}
/>

        </div>

        {/* Copy Button - Using flex-shrink-0 to prevent it from shrinking */}
        {!isUser && (
          <button
            onClick={handleCopy}
            className="flex-shrink-0 self-start text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 transition-colors p-1 rounded"
            aria-label="Copy message"
          >
            {copied ? (
              <CheckCheck size={18} className="text-green-400" />
            ) : (
              <Copy size={18} />
            )}
          </button>
        )}
      </div>
    </div>
  );
};

export default ChatBubble;