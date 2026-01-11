function Landing() {
  return (
    <div className="min-h-screen bg-[#FFFFFF]">
      {/* Top Section - Two Equal Blocks */}
      <section className="flex flex-col md:flex-row w-full">
        {/* Left Block - Yellow */}
        <div className="w-full md:w-1/2 bg-[#FDE047] border-2 border-[#000000] p-4 md:p-8 flex items-center">
          <p className="text-[#000000] text-base md:text-2xl">
            An AI-powered classroom companion offering real-time listening,
            instant crisis support, smart pre-class planning, activity ideas and
            multilingual help.
          </p>
        </div>

        {/* Right Block - Light Purple */}
        <div className="w-full md:w-1/2 bg-[#DDD6FE] border-2 border-[#000000] p-4 md:p-8 flex flex-col md:flex-row items-center gap-4 md:gap-8">
          <img
            src="/fav_icon_chanakya.png"
            alt="Chanakya Character"
            className="w-48 h-48 md:w-71 md:h-71 object-contain"
          />
          <p className="text-[#000000] text-base md:text-2xl">
            An AI-powered classroom companion offering real-time listening,
            instant crisis support, smart pre-class planning, activity ideas and
            multilingual help.
          </p>
        </div>
      </section>

      {/* Bottom Section - Full Width */}
      <section className="w-full bg-[#B2CFB1] border-2 border-[#000000] p-2 md:p-4 flex flex-col md:flex-row items-center gap-4 md:gap-8">
        <img
          src="/chan_winking.png"
          alt="Chanakya Character"
          className="w-48 h-48 md:w-72 md:h-72 object-contain"
        />
        <div>
          <h2 className="text-3xl md:text-5xl font-bold text-[#000000] mb-1">
            <span className="text-[#F97316]">NOT</span> JUST AN ASSISTANT.
          </h2>
          <p className="text-[#000000] text-base md:text-2xl">
            An EdTech solution focused on providing continuous support for
            teachers' day-to-day academic and classroom activities.
          </p>
        </div>
      </section>

      {/* Feature Buttons Section */}
      <section className="w-full bg-[#FCF4AC] border-2 border-[#000000] p-8 md:p-16">
        <div className="max-w-7xl mx-auto">
          {/* Top Row - 4 Buttons */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
            <button className="bg-white border-2 border-[#000000] px-4 md:px-6 py-3 md:py-4 text-black font-bold text-sm md:text-base shadow-[4px_4px_0px_0px_#000000] hover:shadow-[2px_2px_0px_0px_#000000] hover:translate-x-1 hover:translate-y-1 transition-all">
              Crisis-Handling Mode
            </button>
            <button className="bg-white border-2 border-[#000000] px-4 md:px-6 py-3 md:py-4 text-black font-bold text-sm md:text-base shadow-[4px_4px_0px_0px_#000000] hover:shadow-[2px_2px_0px_0px_#000000] hover:translate-x-1 hover:translate-y-1 transition-all">
              Active-Listening Mode
            </button>
            <button className="bg-white border-2 border-[#000000] px-4 md:px-6 py-3 md:py-4 text-black font-bold text-sm md:text-base shadow-[4px_4px_0px_0px_#000000] hover:shadow-[2px_2px_0px_0px_#000000] hover:translate-x-1 hover:translate-y-1 transition-all">
              Pre-class-Module Mode
            </button>
            <button className="bg-white border-2 border-[#000000] px-4 md:px-6 py-3 md:py-4 text-black font-bold text-sm md:text-base shadow-[4px_4px_0px_0px_#000000] hover:shadow-[2px_2px_0px_0px_#000000] hover:translate-x-1 hover:translate-y-1 transition-all">
              Activity-Generator
            </button>
          </div>

          {/* Bottom Row - 3 Buttons */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 max-w-4xl mx-auto">
            <button className="bg-white border-2 border-[#000000] px-4 md:px-6 py-3 md:py-4 text-black font-bold text-sm md:text-base shadow-[4px_4px_0px_0px_#000000] hover:shadow-[2px_2px_0px_0px_#000000] hover:translate-x-1 hover:translate-y-1 transition-all">
              Post-class Feedback
            </button>
            <button className="bg-white border-2 border-[#000000] px-4 md:px-6 py-3 md:py-4 text-black font-bold text-sm md:text-base shadow-[4px_4px_0px_0px_#000000] hover:shadow-[2px_2px_0px_0px_#000000] hover:translate-x-1 hover:translate-y-1 transition-all">
              Multilingual Support
            </button>
            <button className="bg-white border-2 border-[#000000] px-4 md:px-6 py-3 md:py-4 text-black font-bold text-sm md:text-base shadow-[4px_4px_0px_0px_#000000] hover:shadow-[2px_2px_0px_0px_#000000] hover:translate-x-1 hover:translate-y-1 transition-all">
              Personalised
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Landing;
