import { PreferenceProvider } from "./hooks/preferenceContext"
import { Routes_ } from "./router/Routes_"

export const App = () => {  
  return(
    <PreferenceProvider>
    <Routes_ />
    </PreferenceProvider>
  )
}