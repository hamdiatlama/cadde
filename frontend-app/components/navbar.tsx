'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const pathname = usePathname();

  const links = [
    { href: '/', label: 'Ana Sayfa' },
    { href: '/search', label: 'Arama' },
    // Alışveriş
    { href: '/orders', label: 'Siparişler' },
    { href: '/marketplace', label: 'Pazaryeri' },
    { href: '/bundles', label: 'Paketler' },
    { href: '/pre-order', label: 'Ön Sipariş' },
    { href: '/guest-checkout', label: 'Misafir Ödeme' },
    { href: '/gift-cards', label: 'Hediye Çeki' },
    { href: '/gift-registry', label: 'Hediye Listesi' },
    // Satıcı
    { href: '/seller/dashboard', label: 'Satıcı Paneli' },
    { href: '/seller-apply', label: 'Satıcı Ol' },
    { href: '/seller-academy', label: 'Satıcı Akademisi' },
    { href: '/commission', label: 'Komisyon' },
    { href: '/warehouse', label: 'Depo' },
    { href: '/pos', label: 'POS' },
    { href: '/dynamic-pricing', label: 'Fiyatlama' },
    { href: '/analytics', label: 'Analytics' },
    { href: '/integrations', label: 'Entegrasyon' },
    { href: '/marketing-automation', label: 'Otomasyon' },
    // Hesap
    { href: '/profile', label: 'Profil' },
    { href: '/wishlist', label: 'Favoriler' },
    { href: '/wallet', label: 'Cüzdan' },
    { href: '/loyalty', label: 'Sadakat' },
    { href: '/invoices', label: 'Faturalar' },
    { href: '/saved-cards', label: 'Kartlarım' },
    { href: '/payout-schedule', label: 'Ödeme Takvimi' },
    { href: '/push-notifications', label: 'Bildirimler' },
    // Destek
    { href: '/chat', label: 'Mesajlar' },
    { href: '/qna', label: 'Soru & Cevap' },
    { href: '/help-center', label: 'Yardım' },
    { href: '/community', label: 'Topluluk' },
    { href: '/returns', label: 'İade' },
    // Keşfet
    { href: '/auctions', label: 'Açık Artırma' },
    { href: '/live-shopping', label: 'Canlı Alışveriş' },
    { href: '/refurbished', label: 'Yenilenmiş' },
    { href: '/custom-orders', label: 'Özel Sipariş' },
    { href: '/b2b', label: 'B2B' },
    { href: '/blog', label: 'Blog' },
    // Konaklama
    { href: '/hotels', label: 'Konaklama' },
    { href: '/bookings', label: 'Rezervasyonlar' },
    { href: '/hotels/dashboard', label: 'Otel Paneli' },
    { href: '/channel-manager', label: 'OTA Kanallar' },
    { href: '/hotel-revenue', label: 'Gelir Yönetimi' },
    { href: '/payment-gateway', label: 'Ödemeler' },
    { href: '/multi-property', label: 'Grup Yönetimi' },
    { href: '/mobile-checkin', label: 'Mobil Giriş' },
    { href: '/reputation', label: 'İtibar Yönetimi' },
    { href: '/upselling', label: 'Ek Satış' },
    { href: '/website-builder', label: 'Web Sitesi' },
    { href: '/digital-compendium', label: 'Dijital Rehber' },
    { href: '/ai-concierge', label: 'AI Danışman' },
    { href: '/iot-manager', label: 'Akıllı Oda' },
    { href: '/energy-manager', label: 'Enerji' },
    // Acente & Turizm
    { href: '/agency', label: 'Acente' },
    { href: '/tourism', label: 'Turizm' },
    { href: '/rental', label: 'Kiralama' },
    // Seyahat
    { href: '/trip-planner', label: 'Rota Oluştur' },
    // Diğer
    { href: '/delivery-slots', label: 'Teslimat' },
    { href: '/variants', label: 'Varyantlar' },
    { href: '/developer', label: 'Geliştirici' },
    { href: '/compliance', label: 'Uyumluluk' },
  ];

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center h-12 gap-2 overflow-x-auto">
          <Link href="/" className="font-bold text-lg text-blue-700 mr-4 whitespace-nowrap">cadde</Link>
          {links.map(l => (
            <Link
              key={l.href}
              href={l.href}
              className={`whitespace-nowrap text-sm px-3 py-1.5 rounded transition-colors ${
                pathname === l.href ? 'bg-blue-100 text-blue-700 font-semibold' : 'text-gray-600 hover:text-blue-600 hover:bg-gray-50'
              }`}
            >
              {l.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
