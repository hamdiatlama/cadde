'use client';
import { useState } from 'react';

const timeSlots = [
  { id: 1, date: '2026-06-16', day: 'Yarın', slots: ['09:00-12:00', '12:00-15:00', '15:00-18:00', '18:00-21:00'] },
  { id: 2, date: '2026-06-17', day: '17 Haziran Çarşamba', slots: ['09:00-12:00', '12:00-15:00', '15:00-18:00', '18:00-21:00'] },
  { id: 3, date: '2026-06-18', day: '18 Haziran Perşembe', slots: ['09:00-12:00', '12:00-15:00', '15:00-18:00', '18:00-21:00'] },
  { id: 4, date: '2026-06-19', day: '19 Haziran Cuma', slots: ['09:00-12:00', '12:00-15:00', '15:00-18:00'] },
  { id: 5, date: '2026-06-20', day: '20 Haziran Cumartesi', slots: ['10:00-14:00', '14:00-18:00'] },
];

export default function DeliverySlotsPage() {
  const [selectedDate, setSelectedDate] = useState(timeSlots[0].id);
  const [selectedSlot, setSelectedSlot] = useState('');
  const [expressEnabled, setExpressEnabled] = useState(false);

  const currentDate = timeSlots.find(d => d.id === selectedDate);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Teslimat Zamanı Seçimi</h1>
      <p className="text-gray-500 mb-6">Size uygun gün ve saat aralığını seçin</p>

      <div className="mb-6 bg-gradient-to-r from-orange-50 to-red-50 border border-orange-200 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-lg">Ekspres Teslimat</h3>
            <p className="text-sm text-gray-600">2 saat içinde kapınızda, sadece 49 TL</p>
          </div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" checked={expressEnabled} onChange={e => setExpressEnabled(e.target.checked)} className="sr-only peer" />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-orange-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-orange-500"></div>
          </label>
        </div>
      </div>

      {expressEnabled ? (
        <div className="border rounded-lg p-6 text-center">
          <p className="text-xl font-bold text-orange-600 mb-2">Ekspres Teslimat Aktif</p>
          <p className="text-sm text-gray-500 mb-4">Siparişiniz 2 saat içinde teslim edilmek üzere hazırlanıyor.</p>
          <div className="inline-block bg-orange-50 border border-orange-200 rounded-lg p-4">
            <p className="text-sm text-gray-600">Teslimat ücreti: <strong className="text-orange-600">49 TL</strong></p>
            <p className="text-xs text-gray-400">Tahmini varış: 2 saat</p>
          </div>
        </div>
      ) : (
        <>
          <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
            {timeSlots.map(d => (
              <button key={d.id} onClick={() => { setSelectedDate(d.id); setSelectedSlot(''); }}
                className={`px-4 py-3 rounded-lg border text-sm whitespace-nowrap ${selectedDate === d.id ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-700 border-gray-300 hover:border-blue-400'}`}>
                <div className="font-semibold">{d.day}</div>
                <div className="text-xs opacity-80">{d.date}</div>
              </button>
            ))}
          </div>

          {currentDate && (
            <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
              {currentDate.slots.map(slot => {
                const isSelected = selectedSlot === slot;
                return (
                  <button key={slot} onClick={() => setSelectedSlot(slot)}
                    className={`border rounded-lg p-4 text-center ${isSelected ? 'bg-blue-600 text-white border-blue-600' : 'hover:border-blue-400'}`}>
                    <p className="font-semibold">{slot}</p>
                    <p className={`text-xs mt-1 ${isSelected ? 'text-blue-200' : 'text-gray-400'}`}>
                      {isSelected ? 'Seçildi' : 'Müsait'}
                    </p>
                  </button>
                );
              })}
            </div>
          )}

          {selectedSlot && (
            <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-4 text-center">
              <p className="font-semibold text-green-800">Teslimat aralığı seçildi</p>
              <p className="text-sm text-green-600">{currentDate?.day} {selectedSlot} aralığında teslim edilecek</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
