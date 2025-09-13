// TripPlanner.ai Clone - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all interactive features
    initLazyLoading();
    initScrollAnimations();
    initPartnerCarousel();
    initSmoothScrolling();
    initMobileMenu();
    initImageLoading();
    initHoverEffects();
});

// Lazy loading animation observer
function initLazyLoading() {
    const lazyElements = document.querySelectorAll('.lazy-div');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateX(0) translateZ(0)';
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px'
    });

    lazyElements.forEach(element => {
        observer.observe(element);
    });
}

// Scroll animations for various elements
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll, .fade-in-up, .fade-in-left, .fade-in-right');

    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                scrollObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '30px'
    });

    animatedElements.forEach(element => {
        scrollObserver.observe(element);
    });
}

// Partner carousel functionality
function initPartnerCarousel() {
    const carousel = document.getElementById('partner-carousel');
    if (!carousel) return;

    const track = carousel.querySelector('.partner-track');
    if (!track) return;

    // Clone slides for seamless loop
    const slides = track.querySelectorAll('.partner-slide');
    slides.forEach(slide => {
        const clone = slide.cloneNode(true);
        track.appendChild(clone);
    });

    // Pause animation on hover
    carousel.addEventListener('mouseenter', () => {
        track.style.animationPlayState = 'paused';
    });

    carousel.addEventListener('mouseleave', () => {
        track.style.animationPlayState = 'running';
    });
}

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Mobile menu functionality (if needed)
function initMobileMenu() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            mobileMenuButton.classList.toggle('active');
        });
    }
}

// Image loading optimization
function initImageLoading() {
    const images = document.querySelectorAll('img[loading="lazy"]');

    images.forEach(img => {
        img.addEventListener('load', () => {
            img.classList.add('loaded');
        });

        // Fallback for already loaded images
        if (img.complete) {
            img.classList.add('loaded');
        }
    });
}

// Enhanced hover effects
function initHoverEffects() {
    // Trip cards hover effects
    const tripCards = document.querySelectorAll('.trip-card');
    tripCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('hover-active');
        });

        card.addEventListener('mouseleave', () => {
            card.classList.remove('hover-active');
        });
    });

    // Feature cards hover effects
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Button hover effects
    const buttons = document.querySelectorAll('button, .btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-2px)';
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translateY(0)';
        });
    });
}

// Header scroll effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('.fixed.top-0');
    if (!header) return;

    if (window.scrollY > 50) {
        header.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        header.style.backdropFilter = 'blur(12px)';
        header.style.borderBottom = '1px solid rgba(229, 231, 235, 0.5)';
    } else {
        header.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        header.style.backdropFilter = 'blur(10px)';
        header.style.borderBottom = '1px solid rgba(229, 231, 235, 0.3)';
    }
});

// Mobile create trip button scroll behavior
function initMobileButton() {
    const mobileButton = document.querySelector('.fixed.bottom-4');
    if (!mobileButton) return;

    let lastScrollY = window.scrollY;
    let ticking = false;

    function updateButtonPosition() {
        const scrollY = window.scrollY;
        const scrollDirection = scrollY > lastScrollY ? 'down' : 'up';

        if (scrollDirection === 'down' && scrollY > 100) {
            mobileButton.style.transform = 'translateY(100px) translateZ(0px)';
        } else {
            mobileButton.style.transform = 'translateY(0) translateZ(0px)';
        }

        lastScrollY = scrollY;
        ticking = false;
    }

    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(updateButtonPosition);
            ticking = true;
        }
    });
}

// Initialize mobile button behavior
initMobileButton();

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimized scroll handler
const optimizedScrollHandler = debounce(() => {
    // Any additional scroll-based functionality can go here
}, 16); // ~60fps

window.addEventListener('scroll', optimizedScrollHandler);

// Preload critical images
function preloadImages() {
    const criticalImages = [
        'https://tripplanner.ai/_next/image?url=%2Flogo%2Flogo.webp&w=64&q=75&dpl=dpl_3qP7RFTTn9SpXVLfWPH7mXJQkG1s',
        'https://tripplanner.ai/logo/logo.svg'
    ];

    criticalImages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

// Initialize preloading
preloadImages();

// Error handling for images
document.addEventListener('error', (e) => {
    if (e.target.tagName === 'IMG') {
        console.warn('Image failed to load:', e.target.src);
        // You could add a fallback image here
        // e.target.src = '/fallback-image.jpg';
    }
}, true);

// Analytics and tracking (placeholder)
function trackEvent(eventName, properties = {}) {
    // Placeholder for analytics tracking
    console.log('Track event:', eventName, properties);

    // Example: Google Analytics 4
    // gtag('event', eventName, properties);

    // Example: Custom analytics
    // analytics.track(eventName, properties);
}

// Track button clicks
document.addEventListener('click', (e) => {
    if (e.target.matches('a[href*="layla.ai"], button')) {
        const elementText = e.target.textContent.trim();
        trackEvent('button_click', {
            button_text: elementText,
            button_location: e.target.closest('section')?.id || 'unknown'
        });
    }
});

// Track scroll depth
let maxScrollDepth = 0;
window.addEventListener('scroll', debounce(() => {
    const scrollDepth = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
    if (scrollDepth > maxScrollDepth) {
        maxScrollDepth = scrollDepth;
        if (maxScrollDepth % 25 === 0) { // Track at 25%, 50%, 75%, 100%
            trackEvent('scroll_depth', { depth: maxScrollDepth });
        }
    }
}, 500));

// Page visibility API for performance
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Pause animations or reduce activity when page is hidden
        document.querySelectorAll('.partner-track').forEach(track => {
            track.style.animationPlayState = 'paused';
        });
    } else {
        // Resume animations when page becomes visible
        document.querySelectorAll('.partner-track').forEach(track => {
            track.style.animationPlayState = 'running';
        });
    }
});

// Keyboard navigation support
document.addEventListener('keydown', (e) => {
    // Add keyboard navigation for interactive elements
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', () => {
    document.body.classList.remove('keyboard-navigation');
});

// Touch device detection and optimization
function isTouchDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

if (isTouchDevice()) {
    document.body.classList.add('touch-device');

    // Optimize for touch devices
    const hoverElements = document.querySelectorAll('.hover\\:scale-105, .hover-lift');
    hoverElements.forEach(element => {
        element.addEventListener('touchstart', () => {
            element.classList.add('touch-active');
        });

        element.addEventListener('touchend', () => {
            setTimeout(() => {
                element.classList.remove('touch-active');
            }, 150);
        });
    });
}

// Reduced motion support
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.body.classList.add('reduced-motion');

    // Disable or reduce animations for users who prefer reduced motion
    const animatedElements = document.querySelectorAll('[style*="animation"], .animate-');
    animatedElements.forEach(element => {
        element.style.animation = 'none';
    });
}

// Service Worker registration (for PWA features if needed)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment if you want to add PWA features
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    });
}

// Intersection Observer polyfill fallback
if (!window.IntersectionObserver) {
    // Fallback for older browsers
    const lazyElements = document.querySelectorAll('.lazy-div');
    lazyElements.forEach(element => {
        element.style.opacity = '1';
        element.style.transform = 'translateX(0) translateZ(0)';
    });
}

// Console welcome message
console.log('%c🚀 TripPlanner.ai Clone', 'color: #10b981; font-size: 20px; font-weight: bold;');
console.log('%cBuilt with modern web technologies', 'color: #6b7280; font-size: 14px;');

// Export functions for potential external use
window.TripPlannerClone = {
    trackEvent,
    initLazyLoading,
    initScrollAnimations,
    initPartnerCarousel
};