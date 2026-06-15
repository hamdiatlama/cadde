'use client';
import { useState } from 'react';

const availableIntegrations = [
  {
    id: 'microsoft-dynamics',
    name: 'Microsoft Dynamics 365',
    desc: 'ERP ve CRM entegrasyonu ile sipariş, stok ve müşteri yönetimi.',
    category: 'erp',
    status: 'not_connected',
    logo: 'D365',
    color: 'bg-blue-700',
  },
  {
    id: 'sap',
    name: 'SAP Business One',
    desc: 'SAP ERP ile finans, lojistik ve raporlama entegrasyonu.',
    category: 'erp',
    status: 'connected',
    logo: 'SAP',
    color: 'bg-blue-500',
  },
  {
    id: 'logo',
    name: 'Logo GO!',
    desc: 'Logo muhasebe ve fatura entegrasyonu.',
    category: 'erp',
    status: 'not_connected',
    logo: 'LOGO',
    color: 'bg-red-600',
  },
  {
    id: 'micro',
    name: 'Mikro ERP',
    desc: 'Mikro ERP ile stok ve sipariş senkronizasyonu.',
    category: 'erp',
    status: 'connected',
    logo: 'MIK',
    color: 'bg-green-700',
  },
  {
    id: 'nebim',
    name: 'Nebim ERP',
    desc: 'Nebim ile ürün, stok ve satış entegrasyonu.',
    category: 'erp',
    status: 'error',
    logo: 'NEB',
    color: 'bg-purple-600',
  },
  {
    id: 'etsy',
    name: 'Etsy',
    desc: 'Etsy mağazası ile ürün ve sipariş senkronizasyonu.',
    category: 'marketplace',
    status: 'not_connected',
    logo: 'ETS',
    color: 'bg-orange-500',
  },
  {
    id: 'trendyol',
    name: 'Trendyol',
    desc: 'Trendyol satıcı paneli ile entegre yönetim.',
    category: 'marketplace',
    status: 'connected',
    logo: 'TR',
    color: 'bg-yellow-600',
  },
  {
    id: 'hepsiburada',
    name: 'Hepsiburada',
    desc: 'Hepsiburada mağaza entegrasyonu.',
    category: 'marketplace',
    status: 'not_connected',
    logo: 'HB',
    color: 'bg-red-500',
  },
  {
    id: 'n11',
    name: 'n11',
    desc: 'n11 satıcı entegrasyonu.',
    category: 'marketplace',
    status: 'connected',
    logo: 'N11',
    color: 'bg-purple-500',
  },
  {
    id: 'facebook',
    name: 'Facebook & Instagram',
    desc: 'Sosyal medya mağaza ve reklam entegrasyonu.',
    category: 'marketing',
    status: 'connected',
    logo: 'Fb',
    color: 'bg-blue-600',
  },
  {
    id: 'google',
    name: 'Google Merchant Center',
    desc: 'Google alışveriş reklamları ve ürün feed yönetimi.',
    category: 'marketing',
    status: 'not_connected',
    logo: 'GMC',
    color: 'bg-blue-500',
  },
  {
    id: 'mailchimp',
    name: 'Mailchimp',
    desc: 'E-posta pazarlama ve otomasyon entegrasyonu.',
    category: 'marketing',
    status: 'connected',
    logo: 'MC',
    color: 'bg-yellow-500',
  },
  {
    id: 'kargomatik',
    name: 'Kargomatik',
    desc: 'Kargo takip ve gönderi yönetimi entegrasyonu.',
    category: 'logistics',
    status: 'not_connected',
    logo: 'KGM',
    color: 'bg-green-600',
  },
  {
    id: 'parasut',
    name: 'Paraşüt',
    desc: 'Online fatura ve muhasebe entegrasyonu.',
    category: 'erp',
    status: 'not_connected',
    logo: 'PŞT',
    color: 'bg-teal-600',
  },
];

const categories = [
  { id: 'all', label: 'Tümü' },
  { id: 'erp', label: 'ERP / Muhasebe' },
  { id: 'marketplace', label: 'Pazaryeri' },
  { id: 'marketing', label: 'Pazarlama' },
  { id: 'logistics', label: 'Lojistik' },
];

export default function IntegrationsPage() {
  const [filter, setFilter] = useState('all');
  const [integrations, setIntegrations] = useState(availableIntegrations);

  const filtered = filter === 'all' ? integrations : integrations.filter(i => i.category === filter);

  const connectToggle = (id: string) => {
    setIntegrations(prev => prev.map(i =>
      i.id === id ? { ...i, status: i.status === 'connected' ? 'not_connected' : 'connected' as const } : i
    ));
  };

  const statusBadge = (status: string) => {
    if (status === 'connected') return <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-semibold">Bağlı</span>;
    if (status === 'error') return <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full font-semibold">Hata</span>;
    return <span className="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded-full font-semibold">Bağlı Değil</span>;
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Entegrasyonlar</h1>
      <p className="text-gray-500 mb-6">ERP, pazaryeri ve servis entegrasyonlarını yönetin</p>

      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {categories.map(cat => (
          <button key={cat.id} onClick={() => setFilter(cat.id)}
            className={`whitespace-nowrap px-3 py-1.5 rounded text-sm font-semibold ${filter === cat.id ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {cat.label}
          </button>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {filtered.map(int => (
          <div key={int.id} className="border rounded-lg p-5 flex items-start gap-4">
            <div className={`w-12 h-12 rounded-lg ${int.color} flex items-center justify-center text-white text-xs font-bold flex-shrink-0`}>
              {int.logo}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2">
                <h3 className="font-semibold">{int.name}</h3>
                {statusBadge(int.status)}
              </div>
              <p className="text-sm text-gray-500 mt-1">{int.desc}</p>
              {int.status === 'error' && (
                <p className="text-xs text-red-600 mt-1">• Bağlantı hatası - API anahtarı geçersiz</p>
              )}
              <div className="flex gap-2 mt-3">
                <button onClick={() => connectToggle(int.id)}
                  className={`text-xs px-3 py-1 rounded font-semibold transition-colors ${
                    int.status === 'connected'
                      ? 'bg-red-50 text-red-600 hover:bg-red-100'
                      : 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                  }`}>
                  {int.status === 'connected' ? 'Bağlantıyı Kes' : 'Bağlan'}
                </button>
                <button className="text-xs px-3 py-1 rounded bg-gray-100 text-gray-600 hover:bg-gray-200 font-semibold">Yapılandır</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
