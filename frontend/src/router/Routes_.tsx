import { Routes,Route, BrowserRouter } from "react-router-dom";
import { ChatPage } from "../pages/ChatPage.tsx";
import  { AuthPage }  from "../pages/AuthBanner.tsx";
import Preferences from "../pages/Preferences.tsx";
import { useAuth0 } from "@auth0/auth0-react";
import { usePreference } from "../hooks/preferenceContext.tsx";
import { Navigate } from "react-router-dom";

export const Routes_ = () => {

  const {isAuthenticated} = useAuth0()
  const {preference} = usePreference()

  return (
    <BrowserRouter> 
    <Routes>
      <Route path="/" element={isAuthenticated ? <Navigate to="/login"/> : <AuthPage />} />
      <Route path="/chat" element={isAuthenticated  ? <ChatPage /> : <AuthPage />} />
      <Route path="/preferences" element={!isAuthenticated ?  <AuthPage/>:!preference || preference==null ? <Preferences/>:<ChatPage/>} />
      <Route path="/login" element={!isAuthenticated ? <AuthPage/>: preference==true ? <ChatPage/> : <Preferences/> } /> 
    </Routes>
    </BrowserRouter>)
}