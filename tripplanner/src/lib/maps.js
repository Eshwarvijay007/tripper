export function loadGoogleMaps(apiKey) {
  return new Promise((resolve, reject) => {
    if (typeof window !== 'undefined' && window.google && window.google.maps) {
      resolve(window.google.maps);
      return;
    }
    if (!apiKey) {
      reject(new Error('Missing VITE_GOOGLE_MAPS_API_KEY'));
      return;
    }
    const existing = document.querySelector('script[data-google-maps-loader]');
    if (existing) {
      existing.addEventListener('load', () => resolve(window.google.maps));
      existing.addEventListener('error', reject);
      return;
    }
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&v=weekly`;
    script.async = true;
    script.defer = true;
    script.setAttribute('data-google-maps-loader', 'true');
    script.onload = () => resolve(window.google.maps);
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

