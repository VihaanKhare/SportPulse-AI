import { useEffect, useState } from 'react';
import { Check, Info } from 'lucide-react';
import { sportCategories } from '../constants.ts';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth0, User } from '@auth0/auth0-react';
import { usePreference } from '../hooks/preferenceContext.tsx';



export default function Preferences() {

  const navigate = useNavigate();
  const [selectedSports, setSelectedSports] = useState<string[]>([]);
  const [showNotification, setShowNotification] = useState(false);
  const {user,getAccessTokenSilently,isAuthenticated} = useAuth0();
  const {preference,setPreference} = usePreference();
  
  async function fetchPreferences(user:User | null) {
    try {
      const token = await getAccessTokenSilently();
      console.log("Token:", token);
      console.log("Running fetchPreferences function")
      const response = await axios.get(`${import.meta.env.VITE_BASE_URL}/protected/signed_in`, 
        {withCredentials: true,
        headers: { email: user?.email , Authorization: `Bearer ${token}` },
      });
      console.log("luuuund lele")
      return response.data;
    } catch (error) {
      console.error('Error fetching preferences:', error);
    }
  }


  const toggleSport = (sportId: string) => {
    setSelectedSports(prev => 
      prev.includes(sportId)
        ? prev.filter(id => id !== sportId)
        : [...prev, sportId]
    );
  };

  const savePreferences = async () => {
    try {

      const token = await getAccessTokenSilently();
      
      console.log("Token:", token);
      const response = await axios.post(
        `${import.meta.env.VITE_BASE_URL}/protected/save_prefs`,
        { preferences: selectedSports },
        {
          headers: {
            email: user?.email,
            Authorization: `Bearer ${token}`
          },
          withCredentials: true
        }
      );

      if(response.status === 200) {
        setShowNotification(true);
        setTimeout(() => {
          setShowNotification(false);
          setPreference(true);
          localStorage.setItem('preferences', JSON.stringify(selectedSports));
          navigate("/chat");
        }, 2000);

      } else {
        console.error("Failed to save preferences:", response.statusText);
      }
    } catch (error) {
      console.error("Error saving preferences:", error);
      throw error;
    }
  };


  useEffect(() => {
    if(isAuthenticated === true && preference === null){
      console.log("User is authenticated and preferences are null, fetching preferences.");
      const response = fetchPreferences(user!);
      console.log("Response:", response);
      response.then((data) => {
        console.log("Response:", data);
        if (data.length === 0) {

          console.log("No preferences found, redirecting to preferences page.");
          setPreference(false)
          navigate('/preferences');

        } else {
          console.log("Preferences found:", data);
          console.log("Preferences found:", data);
          localStorage.setItem('preferences', JSON.stringify(data));
          setPreference(true);
          navigate('/chat');

        }
      });
    }else if(isAuthenticated === true && preference === false){
      console.log("User is authenticated but preferences are not set, redirecting to preferences page.");
      navigate('/preferences');
    } else if(isAuthenticated === true && preference === true){
      console.log("User is authenticated and preferences are set, redirecting to chat page.");
      navigate('/chat');
    }
    else{
      console.log("User is not authenticated, redirecting to auth page.");
      navigate('/');
    }
  }, []);


  return (
    <div style={{"height":"95vh"}} className="bg-gradient-to-b from-purple-900 to-black bg-neutral-900 rounded-xl text-gray-100 p-6 mb-6 scrollable mt-2 pt-10 overflow-y-auto">
      <div className="max-w-4xl mx-auto mb-8">
        <h1 className="text-3xl font-bold mb-2">Game Preferences</h1>
        <p className="text-gray-400">Select the sports you'd like to follow for personalized updates and content</p>
      </div>
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Available Sports</h2>
          <div className="grid  grid-cols-1 md:grid-cols-2 gap-4">
            {sportCategories.map(sport => (
              <div 
                key={sport.id}
                onClick={() => toggleSport(sport.id)}
                className={`flex bg-neutral-900 items-start p-4 rounded-lg cursor-pointer transition-all ${
                  selectedSports.includes(sport.id) 
                    ? 'bg-purple-900/40 border border-purple-500' 
                    : 'bg-gray-800 hover:bg-gray-700 border border-gray-700'
                }`}
              >
                <div className="flex-shrink-0 text-2xl mr-4">{sport.icon}</div>
                <div className="flex-grow">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium">{sport.name}</h3>
                    {selectedSports.includes(sport.id) && (
                      <Check className="h-5 w-5 text-purple-500" />
                    )}
                  </div>
                  <p className="text-sm text-gray-400 mt-1">{sport.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Information Box */}
        <div className="bg-gray-800 rounded-lg p-4 mb-8 flex items-start">
          <Info className="h-5 w-5 text-blue-400 mr-3 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-gray-300">
            Your sport preferences help us customize your feed and notifications. 
            You can change these settings anytime. We'll only send updates for the sports you select.
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-4">
          <button 
            className="px-4 py-2 rounded-md bg-gray-800 text-gray-300 hover:bg-gray-700 cursor-pointer transition-colors"
            onClick={() => setSelectedSports([])}
          >
            Reset
          </button>
          <button 
            className="px-4 py-2 rounded-md bg-purple-600 text-white hover:bg-purple-500 cursor-pointer transition-colors"
            onClick={savePreferences}
            disabled={selectedSports.length === 0}
          >
            Save Preferences
          </button>
        </div>
      </div>
      {showNotification && (
        <div className="fixed bottom-6 right-6 bg-green-900/90 text-green-100 px-4 py-3 rounded-lg shadow-lg flex items-center">
          <Check className="h-5 w-5 mr-2" />
          Preferences saved successfully!
        </div>
      )}
    </div>
  );
}