addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  url.hostname = 'monster-prices-extension.pages.dev'  // Replace with your Cloudflare Pages URL
  const newRequest = new Request(url, request)
  return fetch(newRequest)
}
