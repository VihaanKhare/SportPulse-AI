import { useNavigate } from "react-router-dom";
import "../index.css"; 
import { useAuth0 } from "@auth0/auth0-react";

export default function Header() {

  const navigate = useNavigate();
  const {user,isAuthenticated,logout} = useAuth0();

  function handleSignIn() {
    navigate("/login");
   }

  function logout_function() {
    console.log("Logging out...");
    logout();
  }


  return (
    <header className="chat_header">
      <div className="container mx-auto px-4 py-3 flex flex-col sm:flex-row justify-between items-center">
        <h1 className="font-bold text-3xl mb-3 sm:mb-0"><span>Sport</span>Stream</h1>
        <nav>
          <ul className="flex space-x-6">
            {isAuthenticated && user && (
              <li className="username text-white">Hi {user.name?.split(" ")[0]}</li>
            )}
            {!isAuthenticated || !user ?  <li><a onClick={handleSignIn} className="white_only hover:text-white transition-colors">Sign In</a></li>
            :<li><a onClick={logout_function} className="white_only hover:text-white transition-colors">Log Out</a></li>}
          </ul>
        </nav>
      </div>
    </header>
  );
}