import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { usePreference } from '../hooks/preferenceContext';
// import { useNavigate } from 'react-router-dom';


export const AuthPage: React.FC = () => {

  const {preference}=usePreference();
  const { loginWithRedirect,isAuthenticated } = useAuth0();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-black text-white flex flex-col items-center justify-center mt-2 rounded-lg">
      <div className="max-w-4xl w-full text-center">
        <h1 className="text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
          Welcome to SportStream
        </h1>
        
        <p className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto">
          Your personalized gateway to live scores, highlights, and updates from all your favorite sports around the world.
        </p>
        
        <div className="relative mb-16">
          {isAuthenticated === true && preference === null ?<button
            className="cursor-pointer relative bg-gray-900 hover:bg-gray-800 text-white font-semibold py-3 px-8 rounded-lg text-lg transition duration-300 ease-in-out transform hover:scale-105 hover:bg-purple-500"
            onClick={() => loginWithRedirect()}
          >
            Signing In...
          </button>:<button
            className="cursor-pointer relative bg-gray-900 hover:bg-gray-800 text-white font-semibold py-3 px-8 rounded-lg text-lg transition duration-300 ease-in-out transform hover:scale-105 hover:bg-purple-500"
            onClick={() => loginWithRedirect()}
          >
            Sign In
          </button>}
          
        </div>
      
        
        <div className="mt-16 text-gray-400 text-sm flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          Join now to customize your feed with the sports you love
        </div>
      </div>
    </div>
  );
};


