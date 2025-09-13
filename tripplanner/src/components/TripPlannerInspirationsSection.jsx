import React from 'react';

const inspirations = [
  {
    href: "https://www.tripplanner.ai/public-trips/ff989e43-ce8f-403f-869b-3017630a23a4",
    imgSrc: "https://tripplanner.ai/_next/image?url=https%3A%2F%2Fimages.pexels.com%2Fphotos%2F2389171%2Fpexels-photo-2389171.jpeg%3Fauto%3Dcompress%26cs%3Dtinysrgb%26w%3D1260%26h%3D750%26dpr%3D1&w=2048&q=75&dpl=dpl_BVqXPdBxWjNVA6pzJR2huFbe68ST",
    imgAlt: "Trip to Tokyo",
    user: {
      name: "Ivanner Mora",
      avatarSrc: "https://tripplanner.ai/_next/image?url=%2Flanding%2Fimages%2Fpublic-plans%2Fuser1.jpg&w=64&q=75&dpl=dpl_BVqXPdBxWjNVA6pzJR2huFbe68ST",
    },
    title: "Trip to Tokyo",
    description: "Join me on an exciting 10-day journey through Tokyo, where we'll visit iconic landmarks, indulge in delicious cuisine, and immerse ourselves in the vibrant culture of Japan's capital city.",
    heightClass: "md:h-[16rem]",
  },
  {
    href: "https://www.tripplanner.ai/public-trips/ffb140e8-f654-4ea9-8b03-2632ccd7184b",
    imgSrc: "https://tripplanner.ai/_next/image?url=https%3A%2F%2Fimages.pexels.com%2Fphotos%2F3873672%2Fpexels-photo-3873672.jpeg%3Fauto%3Dcompress%26cs%3Dtinysrgb%26w%3D600&w=2048&q=75&dpl=dpl_BVqXPdBxWjNVA6pzJR2huFbe68ST",
    imgAlt: "Trip to Dubai",
    user: {
      name: "john mathew",
      avatarSrc: "https://tripplanner.ai/_next/image?url=%2Flanding%2Fimages%2Fpublic-plans%2Fuser3.jpg&w=64&q=75&dpl=dpl_BVqXPdBxWjNVA6pzJR2huFbe68ST",
    },
    title: "Trip to Dubai",
    description: "Embark on a thrilling 6-day journey through Dubai, United Arab Emirates. Explore vibrant souks, iconic landmarks, world-class shopping, and enchanting attractions. Join us as we uncover the hidden gems and unforgettable experiences that Dubai has to offer.",
    heightClass: "md:h-[25rem]",
  },
  {
    href: "https://www.tripplanner.ai/public-trips/ff4437a1-5d04-461e-ba95-7c72932247ea",
    imgSrc: "https://tripplanner.ai/_next/image?url=https%3A%2F%2Fimages.pexels.com%2Fphotos%2F944690%2Fpexels-photo-944690.jpeg%3Fauto%3Dcompress%26cs%3Dtinysrgb%26w%3D1260%26h%3D750%26dpr%3D1&w=2048&q=75&dpl=dpl_BVqXPdBxWjNVA6pzJR2huFbe68ST",
    imgAlt: "Trip to New York",
    user: {
      name: "Pablo Guzman",
      avatarSrc: "https://tripplanner.ai/_next/image?url=%2Flanding%2Fimages%2Fpublic-plans%2Fuser2.webp&w=64&q=75&dpl=dpl_BVqXPdBxWjNVA6pzJR2huFbe68ST",
    },
    title: "Trip to New York",
    description: "Experience the best of New York City in just 7 days! Explore iconic landmarks, indulge in delicious meals, and immerse yourself in the vibrant culture of the city that never sleeps.",
    heightClass: "md:h-[25rem]",
  },
  {
    href: "https://www.tripplanner.ai/public-trips/ffcf5eb5-03bd-4ca6-b412-6d2e3afee111",
    imgSrc: "https://tripplanner.ai/_next/image?url=https%3A%2F%2Fimages.pexels.com%2Fphotos%2F532263%2Fpexels-photo-532263.jpeg%3Fauto%3Dcompress%26cs%3Dtinysrgb%26w%3D1260%26h%3D750%26dpr%3D1&w=2048&q=75&dpl=dpl_BVqXPdBxWjNVA6pzJR2huFbe68ST",
    imgAlt: "Trip to Rome",
    user: {
      name: "Rosarinho Alves",
      avatarSrc: "https://tripplanner.ai/_next/image?url=%2Flanding%2Fimages%2Fpublic-plans%2Fuser4.jpg&w=64&q=75&dpl=dpl_BVqXPdBxWjNVA6pzJR2huFbe68ST",
    },
    title: "Trip to Rome",
    description: "Join me on a thrilling 5-day adventure in Rome, where we'll explore ancient ruins, marvel at stunning architecture, and indulge in mouthwatering pizza. Get ready for an unforgettable experience!",
    heightClass: "md:h-[18rem]",
  },
];

const TripPlannerInspirationsSection = () => {
  return (
    <div className="mx-auto mt-3 w-full max-w-screen-2xl md:mt-14">
      <h2 className="px-6 text-center text-3xl font-bold md:text-4xl lg:px-12 xl:text-5xl">Journey Inspirations from Travelers</h2>
      <p className="mx-auto mt-10 max-w-3xl px-6 text-center text-base lg:px-12 lg:text-lg">Dive into unique <a className="text-accent-red-2 underline" href="https://tripplanner.ai/public-trips">trip itineraries</a> crafted by our global travelers. Find your next adventure and share your own journey with fellow explorers.</p>
      <div className="mx-auto mt-12 flex max-w-6xl flex-col gap-5 px-6 md:flex-row lg:gap-12 lg:px-12">
        <div className="flex flex-auto flex-col gap-5 lg:gap-12">
          {inspirations.slice(0, 2).map((inspiration, index) => (
            <div key={index} className={`group relative items-end overflow-hidden rounded-xl md:rounded-3xl flex h-[15rem] max-w-[50rem] ${inspiration.heightClass}`} style={{transform: "none"}}>
              <a className="h-full w-full" href={inspiration.href}>
                <div className="absolute right-0 top-0 z-[20] h-full w-full bg-gradient-to-t from-black/70 via-transparent via-40% to-black/40"></div>
                <div className="absolute right-0 top-0 z-[20] h-full w-full bg-transparent transition-colors duration-700 group-hover:bg-black/50"></div>
                <img alt={inspiration.imgAlt} loading="lazy" width="1000" height="1000" decoding="async" data-nimg="1" className="object-cover transition-all duration-700 group-hover:scale-110 absolute h-full w-full" style={{color:"transparent"}} src={inspiration.imgSrc} />
                <div className="relative z-[22] flex h-full flex-col justify-between p-4 md:p-7 lg:p-8">
                  <div className="absolute right-5 top-5 z-[20] rounded-lg bg-white ring ring-white ring-offset-2 transition-all duration-300 ease-in-out hover:bg-gray-200 group-hover:text-gray-700 md:right-8 md:top-[-58px] md:p-1 md:group-hover:top-8 xl:group-hover:top-8">
                    <svg xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" className="text-gray-700 iconify iconify--material-symbols" width="1em" height="1em" viewBox="0 0 24 24">
                      <path fill="currentColor" d="m16 8.4l-8.9 8.9q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7L14.6 7H7q-.425 0-.712-.288T6 6t.288-.712T7 5h10q.425 0 .713.288T18 6v10q0 .425-.288.713T17 17t-.712-.288T16 16z"></path>
                    </svg>
                  </div>
                  <div className="flex items-center gap-2">
                    <img alt={inspiration.user.name} loading="lazy" width="26" height="26" decoding="async" data-nimg="1" className="h-5 w-5 rounded-full ring ring-white/70 md:h-6 md:w-6" style={{color:"transparent"}} src={inspiration.user.avatarSrc} />
                    <span className="text-sm font-medium text-white md:text-base">{inspiration.user.name}</span>
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-white md:text-3xl">{inspiration.title}</h2>
                    <p className="mt-2 line-clamp-2 text-sm text-white md:mt-5 md:text-base undefined">{inspiration.description}</p>
                  </div>
                </div>
              </a>
            </div>
          ))}
        </div>
        <div className="flex-2 hidden flex-col gap-5 md:flex lg:gap-12">
            {inspirations.slice(2, 4).map((inspiration, index) => (
                <div key={index} className={`group relative items-end overflow-hidden rounded-xl md:rounded-3xl flex h-[15rem] max-w-[50rem] ${inspiration.heightClass}`} style={{transform: "none"}}>
                <a className="h-full w-full" href={inspiration.href}>
                    <div className="absolute right-0 top-0 z-[20] h-full w-full bg-gradient-to-t from-black/70 via-transparent via-40% to-black/40"></div>
                    <div className="absolute right-0 top-0 z-[20] h-full w-full bg-transparent transition-colors duration-700 group-hover:bg-black/50"></div>
                    <img alt={inspiration.imgAlt} loading="lazy" width="1000" height="1000" decoding="async" data-nimg="1" className="object-cover transition-all duration-700 group-hover:scale-110 absolute h-full w-full" style={{color:"transparent"}} src={inspiration.imgSrc} />
                    <div className="relative z-[22] flex h-full flex-col justify-between p-4 md:p-7 lg:p-8">
                    <div className="absolute right-5 top-5 z-[20] rounded-lg bg-white ring ring-white ring-offset-2 transition-all duration-300 ease-in-out hover:bg-gray-200 group-hover:text-gray-700 md:right-8 md:top-[-58px] md:p-1 md:group-hover:top-8 xl:group-hover:top-8">
                        <svg xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" className="text-gray-700 iconify iconify--material-symbols" width="1em" height="1em" viewBox="0 0 24 24">
                        <path fill="currentColor" d="m16 8.4l-8.9 8.9q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7L14.6 7H7q-.425 0-.712-.288T6 6t.288-.712T7 5h10q.425 0 .713.288T18 6v10q0 .425-.288.713T17 17t-.712-.288T16 16z"></path>
                        </svg>
                    </div>
                    <div className="flex items-center gap-2">
                        <img alt={inspiration.user.name} loading="lazy" width="26" height="26" decoding="async" data-nimg="1" className="h-5 w-5 rounded-full ring ring-white/70 md:h-6 md:w-6" style={{color:"transparent"}} src={inspiration.user.avatarSrc} />
                        <span className="text-sm font-medium text-white md:text-base">{inspiration.user.name}</span>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-white md:text-3xl">{inspiration.title}</h2>
                        <p className="mt-2 line-clamp-2 text-sm text-white md:mt-5 md:text-base undefined">{inspiration.description}</p>
                    </div>
                    </div>
                </a>
                </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default TripPlannerInspirationsSection;