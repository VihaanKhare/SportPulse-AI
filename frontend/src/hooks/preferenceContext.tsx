import { PreferenceContextType } from '@/types/types';
import React, { createContext, useContext, useState, ReactNode } from 'react';


const PreferenceContext = createContext<PreferenceContextType | undefined>(undefined);

export const PreferenceProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [preference, setPreference] = useState<boolean|null>(null);

  return (
    <PreferenceContext.Provider value={{ preference, setPreference }}>
      {children}
    </PreferenceContext.Provider>
  );
};

export const usePreference = (): PreferenceContextType => {
  const context = useContext(PreferenceContext);
  if (!context) {
    throw new Error('usePreference must be used within a PreferenceProvider');
  }
  return context;
};