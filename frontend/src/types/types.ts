export type HistoryItem = {
  id: number;
  title: string;
  time: string;
}

export interface Banner {
  id: string;
  type: "info" | "warning" | "promo" | "update";
  title: string;
  message: string;
  isNew?: boolean;
  actionText?: string;
}

export interface BannerProps {
  title: string;
  description: string;

}

export interface ChatBubbleProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
}


export type PreferenceContextType = {
  preference: boolean|null;
  setPreference: (value: boolean|null) => void;
};

export interface HistorySidebarProps {
  func_to_fetch_History: (id: number) => Promise<any>;
}

export interface Message {
  message: string;
  isUser: boolean;
  timestamp?: string;
}

export type HistoryEntry = {
  id:number;
  title: string;
  messages: Message;
  timestamp?:string;
};

type CareerStatistics = Record<string, Record<string, string>>;
type InfoBoxSection = Record<string, string>;

export interface PlayerApiResponse {
  bio: string;
  career_statistics: CareerStatistics;
  infobox: {
    [section: string]: InfoBoxSection;
  };
  url: string;
}