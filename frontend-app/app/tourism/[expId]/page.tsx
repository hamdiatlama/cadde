"use client";
import { useParams, useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

export default function TourismDetail() {
  const { expId } = useParams();
  const router = useRouter();
  const [exp, setExp] = useState<any>(null);
  const [schedules, setSchedules] = useState<any[]>([]);
  const [selectedSchedule, setSelectedSchedule] = useState<number | null>(null);
  const [participants, setParticipants] = useState(1);
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [booking, setBooking] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const [expRes, schedRes] = await Promise.all([
          fetch(`${API}/tourism/experiences/${expId}`),
          fetch(`${API}/tourism/schedules?experience_id=${expId}`),
        ]);
        setExp(await expRes.json());
        const schedData = await schedRes.json();
        setSchedules(Array.isArray(schedData) ? schedData : []);
      } catch (_) {}
    }
    load();
  }, [expId]);

  async function handleBook() {
    if (!selectedSchedule) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/tourism/bookings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          schedule_id: selectedSchedule,
          user_id: 1,
          participant_count: participants,
          total_price: (schedules.find(s => s.id === selectedSchedule)?.price || exp?.base_price || 0) * participants,
          customer_name: name,
          customer_phone: phone,
          customer_email: email,
        }),
      });
      const data = await res.json();
      setBooking(data);
    } catch (_) {}
    setLoading(false);
  }

  if (!exp) return <div className="p-4">Yükleniyor...</div>;

  const schedule = schedules.filter(s => s.is_active !== false && s.available > 0);

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <button onClick={() => router.back()} className="text-blue-600 mb-4">&larr; Geri</button>
      {exp.cover_photo_url && (
        <img src={exp.cover_photo_url} alt={exp.name} className="w-full h-64 object-cover rounded-lg mb-4" />
      )}
      <h1 className="text-2xl font-bold">{exp.name}</h1>
      <p className="text-gray-600">{exp.city}{exp.district ? ` / ${exp.district}` : ""}</p>
      {exp.duration_minutes && <p className="text-sm text-gray-500">Süre: {exp.duration_minutes} dk</p>}
      <p className="text-blue-600 font-bold text-xl mt-2">{exp.base_price?.toLocaleString()} {exp.currency}</p>
      {exp.description && <p className="mt-4">{exp.description}</p>}
      {exp.includes && <div className="mt-4"><h3 className="font-semibold">Dahil Olanlar:</h3><p>{exp.includes}</p></div>}

      <div className="mt-6 border-t pt-4">
        <h2 className="text-lg font-bold mb-2">Rezervasyon</h2>
        <select value={selectedSchedule || ""} onChange={e => setSelectedSchedule(Number(e.target.value))}
          className="border p-2 rounded w-full mb-2">
          <option value="">Tarih Seçin</option>
          {schedule.map(s => (
            <option key={s.id} value={s.id}>
              {s.date} {s.time} - {s.available} kişilik yer
            </option>
          ))}
        </select>
        <input type="number" min={1} value={participants}
          onChange={e => setParticipants(Number(e.target.value))}
          placeholder="Kişi sayısı" className="border p-2 rounded w-full mb-2" />
        <input value={name} onChange={e => setName(e.target.value)}
          placeholder="Ad Soyad" className="border p-2 rounded w-full mb-2" />
        <input value={phone} onChange={e => setPhone(e.target.value)}
          placeholder="Telefon" className="border p-2 rounded w-full mb-2" />
        <input value={email} onChange={e => setEmail(e.target.value)}
          placeholder="E-posta" className="border p-2 rounded w-full mb-2" />

        <button onClick={handleBook} disabled={loading || !selectedSchedule}
          className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 w-full">
          {loading ? "Rezervasyon yapılıyor..." : "Rezervasyon Yap"}
        </button>

        {booking && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded">
            <p className="font-bold text-green-700">Rezervasyon Başarılı!</p>
            <p>Rezervasyon No: {booking.booking_no}</p>
            <p>Toplam: {booking.total_price?.toLocaleString()} {booking.currency}</p>
          </div>
        )}
      </div>
    </div>
  );
}
