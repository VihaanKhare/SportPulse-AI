import { BannerProps } from "@/types/types";
import { useState } from "react";

export function ExpandableBanner({ title, description}: BannerProps) {
  const [isHovered, setIsHovered] = useState(false);

  // const renderIcon = () => {
  //   switch (icon) {
  //     case 'star':
  //       return <Star className="text-yellow-300" size={20} />;
  //     case 'info':
  //       return <Info className="text-blue-400" size={20}  />;
  //     case 'warning':
  //       return <AlertTriangle className="text-yellow-400" size={20} />;
  //     case 'promo':
  //       return <Tag className="text-purple-400" size={20} />;
  //     case 'update':
  //       return <Bell className="text-green-400" size={20} />;
  //     default:
  //       return <Star className="text-yellow-300" size={20} />;
  //   }
  // };

  return (
    <div 
      className={`banner p-4 rounded-xl transition-all duration-300 cursor-pointer ${isHovered ? 'transform scale-105 shadow-lg' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-center space-x-2">
        <h3 className="text-white font-bold text-l">{title}</h3>
      </div>
      <p className={`text-sm  text-white/80 mt-2 transition-all duration-300 ${isHovered ? 'opacity-100 max-h-40' : 'opacity-70 max-h-20 truncate'}`}>
        {description}
      </p>
    </div>
  );
}