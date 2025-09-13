import { useEffect, useRef, useState } from 'react'

const PartnerCarousel = () => {
  const [isVisible, setIsVisible] = useState(false)
  const sectionRef = useRef(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1, rootMargin: '50px' }
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  const partners = [
    {
      name: 'Booking',
      logo: 'https://tripplanner.ai/_next/image?url=%2Fshared%2Fplatforms%2Fbooking-logo.webp&w=640&q=75&dpl=dpl_3qP7RFTTn9SpXVLfWPH7mXJQkG1s'
    },
    {
      name: 'Viator',
      logo: 'https://tripplanner.ai/landing/images/affiliates/viator.svg'
    },
    {
      name: 'Get Your Guide',
      logo: 'https://tripplanner.ai/landing/images/affiliates/getyourguide.svg'
    },
    {
      name: 'Skyscanner',
      logo: 'https://tripplanner.ai/landing/images/affiliates/skyscanner.svg'
    }
  ]

  return (
    <div 
      ref={sectionRef}
      className={`lazy-element ${isVisible ? 'visible' : ''}`}
      id="partners-section"
    >
      <section className="">
        <div className="mx-auto pt-8">
          <div className="flex flex-col items-center justify-center lg:flex-row">
            <div className="flex flex-col items-center">
              <div className="mb-3">
                <h4 className="px-6 text-center lg:px-12">
                  8M+ trips planned <br /> 4.9 <span className="text-yellow-800">★</span> average
                </h4>
              </div>
              <div className="relative max-w-[20rem] cursor-grab py-10 sm:max-w-[40rem] md:py-20 lg:max-w-5xl">
                <div className="absolute z-[20] h-full w-full max-w-[1rem] bg-gradient-to-r from-white md:max-w-[5rem]"></div>
                <div className="absolute right-0 z-[20] h-full w-full max-w-[1rem] bg-gradient-to-l from-white md:max-w-[5rem]"></div>
                <div className="partner-carousel">
                  <div className="partner-track">
                    {/* Duplicate partners for seamless loop */}
                    {[...partners, ...partners, ...partners].map((partner, index) => (
                      <div key={index} className="partner-slide">
                        <img 
                          alt={partner.name} 
                          loading="lazy" 
                          width="200" 
                          height="200" 
                          className="h-[2rem] w-auto object-cover" 
                          src={partner.logo}
                        />
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default PartnerCarousel