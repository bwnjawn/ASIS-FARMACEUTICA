// Service Worker ASIS Farmacéutica
// RNF04: El módulo de alarmas debe funcionar sin conexión a internet

const CACHE_NAME = 'asis-farmaceutica-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
];

// Instalar y cachear assets estáticos
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activar y limpiar caches antiguos
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Estrategia: Network-first para API, Cache-first para assets estáticos
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // API calls: network first, sin cache
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() =>
        new Response(JSON.stringify({ error: 'Sin conexión. Las alarmas siguen activas.' }), {
          headers: { 'Content-Type': 'application/json' },
          status: 503,
        })
      )
    );
    return;
  }

  // Assets estáticos: cache first
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => caches.match('/index.html'));
    })
  );
});

// Notificaciones push (para alertas al cuidador cuando la app está cerrada)
self.addEventListener('push', event => {
  const data = event.data?.json() || {};
  const title = data.title || 'ASIS Farmacéutica';
  const body = data.body || 'Recordatorio de medicamento';

  event.waitUntil(
    self.registration.showNotification(title, {
      body,
      icon: '/icon-192.png',
      badge: '/icon-192.png',
      vibrate: [500, 200, 500],
      actions: [
        { action: 'confirm', title: '✅ Confirmar toma' },
        { action: 'snooze', title: '⏱ En 10 min' },
      ],
      requireInteraction: true,
    })
  );
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  if (event.action === 'confirm') {
    event.waitUntil(
      clients.matchAll({ type: 'window' }).then(windowClients => {
        if (windowClients.length > 0) {
          windowClients[0].focus();
          windowClients[0].postMessage({ type: 'CONFIRM_DOSE', alarmId: event.notification.data?.alarmId });
        } else {
          clients.openWindow('/');
        }
      })
    );
  }
});
