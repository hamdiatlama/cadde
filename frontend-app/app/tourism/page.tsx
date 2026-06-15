"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const CATEGORIES = [
  { value: "", label: "Tümü" },
  { value: "balloon", label: "Uçan Balon" },
  { value: "safari", label: "Safari" },
  { value: "diving", label: "Dalış" },
  { value: "museum", label: "Müze" },
  { value: "zoo", label: "Hayvanat Bahçesi" },
  { value: "theme_park", label: "Tema Park" },
  { value: "aquarium", label: "Akvaryum" },
  { value: "city_tour", label: "Şehir Turu" },
  { value: "boat_tour", label: "Tekne Turu" },
  { value: "national_park", label: "Milli Park" },
  { value: "adventure", label: "Macera" },
  { value: "cultural", label: "Kültürel" },
  { value: "hiking", label: "Doğa Yürüyüşü" },
  { value: "horse_riding", label: "At Binme" },
  { value: "fishing", label: "Balık Tutma" },
  { value: "camping", label: "Kamp" },
  { value: "workshop", label: "Atölye" },
  { value: "spa", label: "Spa" },
  { value: "cooking", label: "Yemek Atölyesi" },
  { value: "wine_tasting", label: "Şarap Tadımı" },
  { value: "other", label: "Diğer" },
];

export default function TourismPage() {
  const router = useRouter();
  const [category, setCategory] = useState("");
  const [city, setCity] = useState("");
  const [experiences, setExperiences] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  async function search() {
    setLoading(true);
    setSearched(true);
    try {
      const params = new URLSearchParams();
      if (category) params.set("category", category);
      if (city) params.set("city", city);
      const res = await fetch(`${API}/tourism/experiences?${params}`);
      const data = await res.json();
      setExperiences(Array.isArray(data) ? data : []);
    } catch (_) { setExperiences([]); }
    setLoading(false);
  }

  useEffect(() => { search(); }, []);

  return (
    <div className="p-4 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Deneyim & Aktivite</h1>
      <div className="flex gap-2 mb-4 flex-wrap">
        <select value={category} onChange={e => setCategory(e.target.value)}
          className="border p-2 rounded flex-1 min-w-[180px]">
          {CATEGORIES.map(c => <option key={c.value} value={c.value}>{c.label}</option>)}
        </select>
        <input value={city} onChange={e => setCity(e.target.value)}
          placeholder="Şehir" className="border p-2 rounded flex-1 min-w-[150px]" />
        <button onClick={search} disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          {loading ? "Aranıyor..." : "Ara"}
        </button>
      </div>

      {loading && <p className="text-gray-500">Yükleniyor...</p>}

      {!loading && searched && experiences.length === 0 && (
        <p className="text-gray-500">Sonuç bulunamadı.</p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {experiences.map(exp => (
          <div key={exp.id}
            className="border rounded-lg overflow-hidden shadow hover:shadow-md cursor-pointer"
            onClick={() => router.push(`/tourism/${exp.id}`)}>
            {exp.cover_photo_url && (
              <img src={exp.cover_photo_url} alt={exp.name} className="w-full h-48 object-cover" />
            )}
            <div className="p-3">
              <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                {CATEGORIES.find(c => c.value === exp.category)?.label || exp.category}
              </span>
              <h3 className="font-semibold mt-1">{exp.name}</h3>
              <p className="text-sm text-gray-600">{exp.city}{exp.district ? ` / ${exp.district}` : ""}</p>
              <p className="text-sm text-gray-500 mt-1 line-clamp-2">{exp.short_description}</p>
              <p className="text-blue-600 font-bold mt-2">
                {exp.base_price?.toLocaleString()} {exp.currency || "TRY"}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
