'use client';
import { useState } from 'react';

const notificationHistory = [
  { id: 1, title: 'Siparişiniz Kargolandı', message: '#ORD-2026-0421 numaralı siparişiniz kargoya verildi.', date: '2026-06-14 14:32', read: false, type: 'order' },
  { id: 2, title: 'Fırsat Alarmı!', message: 'Spor Ayakkabı %30 indirimde, kaçırmayın!', date: '2026-06-14 10:15', read: false, type: 'campaign' },
  { id: 3, title: 'Puan Kazandınız', message: 'Siparişinizden 120 puan kazandınız.', date: '2026-06-13 18:00', read: true, type: 'loyalty' },
  { id: 4, title: 'Yeni Mesaj', message: 'Satıcıdan yeni bir mesajınız var.', date: '2026-06-12 09:45', read: true, type: 'message' },
  { id: 5, title: 'Ödeme Hatırlatması', message: 'Bekleyen ödemeniz bulunmaktadır.', date: '2026-06-11 08:00', read: true, type: 'payment' },
  { id: 6, title: 'Seviye Atladınız!', message: 'Gümüş üyeliğe yükseldiniz!', date: '2026-06-10 20:30', read: false, type: 'loyalty' },
  { id: 7, title: 'İndirim Kuponu', message: 'Haftasonu özel %15 indirim kuponunuz hazır.', date: '2026-06-09 12:00', read: true, type: 'campaign' },
];

const channels = [
  { id: 'push', label: 'Push Bildirim', desc: 'Tarayıcı bildirimleri' },
  { id: 'email', label: 'E-posta', desc: 'E-posta bildirimleri' },
  { id: 'sms', label: 'SMS', desc: 'Kısa mesaj bildirimleri' },
];

const events = [
  { id: 'order_status', label: 'Sipariş Durumu' },
  { id: 'campaign', label: 'Kampanya & Fırsatlar' },
  { id: 'payment', label: 'Ödeme İşlemleri' },
  { id: 'loyalty', label: 'Sadakat & Puan' },
  { id: 'message', label: 'Mesajlar' },
  { id: 'stock', label: 'Stok Uyarıları' },
];

export default function PushNotificationsPage() {
  const [tab, setTab] = useState<'settings' | 'history'>('settings');
  const [settings, setSettings] = useState<Record<string, Record<string, boolean>>>({
    push: { order_status: true, campaign: true, payment: true, loyalty: true, message: false, stock: false },
    email: { order_status: true, campaign: true, payment: true, loyalty: true, message: true, stock: false },
    sms: { order_status: true, campaign: false, payment: true, loyalty: false, message: false, stock: true },
  });

  const toggle = (channel: string, event: string) => {
    setSettings(prev => ({
      ...prev,
      [channel]: { ...prev[channel], [event]: !prev[channel][event] },
    }));
  };

  const history = notificationHistory;
  const unread = history.filter(n => !n.read).length;

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Bildirim Ayarları</h1>
      <p className="text-gray-500 mb-6">Bildirim tercihlerinizi yönetin ve geçmişi görüntüleyin</p>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setTab('settings')}
          className={`px-4 py-1.5 rounded text-sm font-semibold ${tab === 'settings' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>Tercihler</button>
        <button onClick={() => setTab('history')}
          className={`relative px-4 py-1.5 rounded text-sm font-semibold ${tab === 'history' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
          Geçmiş
          {unread > 0 && (
            <span className="absolute -top-1.5 -right-1.5 bg-red-500 text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center">{unread}</span>
          )}
        </button>
      </div>

      {tab === 'settings' && (
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="text-left p-3 text-sm font-semibold">Bildirim</th>
                {channels.map(ch => (
                  <th key={ch.id} className="text-center p-3 text-sm font-semibold">{ch.label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {events.map(ev => (
                <tr key={ev.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 text-sm">{ev.label}</td>
                  {channels.map(ch => (
                    <td key={ch.id} className="p-3 text-center">
                      <button onClick={() => toggle(ch.id, ev.id)}
                        className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                          settings[ch.id][ev.id] ? 'bg-blue-600 border-blue-600' : 'border-gray-300 hover:border-gray-400'
                        }`}>
                        {settings[ch.id][ev.id] && <span className="text-white text-xs">✓</span>}
                      </button>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'history' && (
        <div className="space-y-2">
          {history.length === 0 ? (
            <p className="text-center text-gray-400 py-8">Bildirim bulunmuyor</p>
          ) : (
            history.map(n => (
              <div key={n.id} className={`border rounded-lg p-4 flex items-start gap-3 ${!n.read ? 'bg-blue-50 border-blue-200' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white ${
                  n.type === 'order' ? 'bg-blue-500' : n.type === 'campaign' ? 'bg-red-500' : n.type === 'loyalty' ? 'bg-purple-500' : n.type === 'message' ? 'bg-green-500' : 'bg-yellow-500'
                }`}>
                  {n.type === 'order' ? 'S' : n.type === 'campaign' ? 'K' : n.type === 'loyalty' ? 'P' : n.type === 'message' ? 'M' : 'Ö'}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-start">
                    <h3 className={`text-sm ${!n.read ? 'font-bold' : 'font-semibold'}`}>{n.title}</h3>
                    <span className="text-xs text-gray-400 ml-2 whitespace-nowrap">{n.date}</span>
                  </div>
                  <p className="text-xs text-gray-600 mt-0.5">{n.message}</p>
                </div>
                {!n.read && <div className="w-2 h-2 rounded-full bg-blue-600 mt-1.5 flex-shrink-0"></div>}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
