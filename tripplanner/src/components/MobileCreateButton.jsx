import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { MapPin } from 'lucide-react'

const MobileCreateButton = () => {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      // Show button when user scrolls down past hero section
      setIsVisible(window.scrollY > 500)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <div
      className={`fixed bottom-4 left-0 right-0 z-[90] flex justify-center md:hidden mobile-create-btn ${
        isVisible ? "visible" : ""
      }`}
    >
      <Link
        to="/naomi"
        className="flex w-fit items-center gap-2 rounded-full bg-accent-green px-3 py-2 text-white shadow-md btn-hover"
      >
        <MapPin className="mb-1 text-xl" size={20} />
        Create a new trip
      </Link>
    </div>
  );
}

export default MobileCreateButton