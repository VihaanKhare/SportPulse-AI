import "../index.css"; // Import your CSS file for styling

export const Footer = () =>{
  return (
    <footer className="chat_footer  text-white py-0 w-full">
      <div className="container mx-auto px-4 text-center">
        <p>&copy; {new Date().getFullYear()} SportStream. All rights reserved.</p>
      </div>
    </footer>
  );
}