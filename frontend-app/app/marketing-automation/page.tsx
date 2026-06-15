'use client';
import { useState } from 'react';

const workflows = [
  {
    id: 1,
    name: 'Hoş Geldin Serisi',
    desc: 'Yeni kayıt olan kullanıcılara otomatik hoş geldin e-postası ve %10 indirim kuponu gönderimi.',
    trigger: 'Yeni kayıt',
    actions: ['E-posta gönder', 'Kupon oluştur'],
    status: 'active',
    runs: 1240,
    conversion: '24%',
  },
  {
    id: 2,
    name: 'Sepet Terk Kurtarma',
    desc: 'Sepetini terk eden kullanıcılara 1 saat sonra hatırlatma e-postası, 24 saat sonra SMS.',
    trigger: 'Sepet terk',
    actions: ['E-posta gönder', 'SMS gönder'],
    status: 'active',
    runs: 3420,
    conversion: '15%',
  },
  {
    id: 3,
    name: 'Doğum Günü Kampanyası',
    desc: 'Doğum gününde kullanıcılara özel indirim kuponu ve kutlama mesajı.',
    trigger: 'Doğum günü',
    actions: ['E-posta gönder', 'Kupon oluştur', 'Push bildirim'],
    status: 'active',
    runs: 890,
    conversion: '38%',
  },
  {
    id: 4,
    name: 'Alışveriş Sonrası Teşekkür',
    desc: 'Sipariş teslimattan 3 gün sonra ürün değerlendirme davetiyesi.',
    trigger: 'Teslimat',
    actions: ['E-posta gönder'],
    status: 'active',
    runs: 5670,
    conversion: '12%',
  },
  {
    id: 5,
    name: 'VIP Müşteri Ödülü',
    desc: 'Yüksek harcama yapan müşterilere özel teklif ve öncelikli destek.',
    trigger: 'Harcama eşiği',
    actions: ['E-posta gönder', 'Özel teklif oluştur'],
    status: 'inactive',
    runs: 450,
    conversion: '42%',
  },
  {
    id: 6,
    name: 'Stok Tekrar Bildirimi',
    desc: 'Tükenen ürünler stoklara girdiğinde bekleyen kullanıcılara bildirim.',
    trigger: 'Stok girişi',
    actions: ['E-posta gönder', 'Push bildirim'],
    status: 'inactive',
    runs: 2340,
    conversion: '31%',
  },
  {
    id: 7,
    name: 'Aylık Haber Bülteni',
    desc: 'Kayıtlı kullanıcılara aylık kampanya ve yenilik bülteni gönderimi.',
    trigger: 'Zamanlayıcı (Aylık)',
    actions: ['E-posta gönder'],
    status: 'active',
    runs: 8900,
    conversion: '8%',
  },
  {
    id: 8,
    name: 'Yeniden Etkileşim',
    desc: '90 gündür aktif olmayan kullanıcılara geri kazanım kampanyası.',
    trigger: 'Pasiflik süresi',
    actions: ['E-posta gönder', 'SMS gönder', 'Push bildirim'],
    status: 'inactive',
    runs: 1200,
    conversion: '5%',
  },
];

export default function MarketingAutomationPage() {
  const [filter, setFilter] = useState<'all' | 'active' | 'inactive'>('all');
  const [wf, setWf] = useState(workflows);

  const toggleStatus = (id: number) => {
    setWf(prev => prev.map(w => w.id === id ? { ...w, status: w.status === 'active' ? 'inactive' : 'active' } : w));
  };

  const filtered = filter === 'all' ? wf : wf.filter(w => w.status === filter);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Pazarlama Otomasyonu</h1>
      <p className="text-gray-500 mb-6">Otomatik pazarlama akışları oluşturun ve yönetin</p>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setFilter('all')}
          className={`px-4 py-1.5 rounded text-sm font-semibold ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Tümü ({wf.length})</button>
        <button onClick={() => setFilter('active')}
          className={`px-4 py-1.5 rounded text-sm font-semibold ${filter === 'active' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Aktif ({wf.filter(w => w.status === 'active').length})</button>
        <button onClick={() => setFilter('inactive')}
          className={`px-4 py-1.5 rounded text-sm font-semibold ${filter === 'inactive' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Pasif ({wf.filter(w => w.status === 'inactive').length})</button>
        <div className="flex-1"></div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded text-sm font-semibold transition-colors">+ Yeni Akış</button>
      </div>

      <div className="space-y-4">
        {filtered.map(w => (
          <div key={w.id} className="border rounded-lg p-5 hover:shadow-sm transition-shadow">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold">{w.name}</h3>
                  <button onClick={() => toggleStatus(w.id)}
                    className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                      w.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
                    }`}>
                    {w.status === 'active' ? 'Aktif' : 'Pasif'}
                  </button>
                </div>
                <p className="text-sm text-gray-500 mt-1">{w.desc}</p>
                <div className="flex flex-wrap gap-2 mt-3">
                  <span className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded font-semibold">
                    Tetikleyici: {w.trigger}
                  </span>
                  {w.actions.map((a, i) => (
                    <span key={i} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">{a}</span>
                  ))}
                </div>
              </div>
              <div className="text-right flex-shrink-0">
                <p className="text-sm font-bold">{w.runs.toLocaleString()}</p>
                <p className="text-xs text-gray-400">çalışma</p>
                <p className="text-sm font-bold text-green-600 mt-1">{w.conversion}</p>
                <p className="text-xs text-gray-400">dönüşüm</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
