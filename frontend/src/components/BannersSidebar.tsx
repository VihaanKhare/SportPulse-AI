import React, { useState } from "react";
import "../../public/styles/BannersSidebar.css";
import { Bell } from "lucide-react";
import { Banner } from "@/types/types";
import { ExpandableBanner } from "../components/Banner.tsx";

export const BannersSidebar: React.FC = () => {
  const [banners, setBanners] = useState<Banner[]>([
    {
      id: "banner1",
      type: "promo",
      title: "SRH vs MI  SRH:162-5 (20.0)  MI:158-6 (17.2)",
      message: "Get live updates on the match between SRH and MI.",
    },
    {
      id: "banner2",
      type: "update",
      title: "Karachi vs Quetta",
      message: "Catch the live action of Karachi vs Quetta.",
    },
    {
      id: "banner3",
      type: "warning",
      title: "Reaction of Preity Zinta on PBKS win",
      message: "Preity Zinta shares her thoughts on PBKS's recent victory.",
    },
  ]);

  // const handleCloseBanner = (bannerId: string) => {
  //   setBanners(banners!.filter(banner => banner.id !== bannerId));
  // };
  // const handleCloseBanner = (bannerId: string) => {
  //   setBanners(banners.filter(banner => banner.id !== bannerId));
  // };

  return (
    <div id="bannersSB" className="bannersSB flex flex-col bg-neutral-900 p-4 space-y-4 overflow-auto">
      <div className="flex justify-between items-center mb-2">
        <h2 className="top_picks text-xl font-bold text-white flex items-center py-3">
          <Bell size={20} className="mr-2" />
          Top Picks
        </h2>
        {banners!.length > 0 && (
          <button 

            className="clear_all cursor-pointer text-sm font-bold text-neutral-400 hover:text-white transition-colors"
            onClick={() => setBanners([])}
          >
            Clear all
          </button>
        )}
      </div>
      
      {banners!.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-40 text-neutral-500">
          <Bell size={20} className="mb-2 opacity-50" />
          <p>No notifications</p>
        </div>
      ) : (
        <div className="space-y-3">
          {banners!.map((banner) => (
            <div key={banner.id} className="relative">
              {banner.isNew && (
                <span className="absolute -top-1 -right-1 z-10 bg-red-500 rounded-full w-3 h-3"></span>
              )}
              <div className="relative">
                <ExpandableBanner
                  title={banner.title}
                  description={banner.message}
                
                />
                
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BannersSidebar;