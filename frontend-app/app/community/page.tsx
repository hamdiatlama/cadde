"use client";

export default function CommunityPage() {
  const topics = [
    { title: "En iyi satıcı stratejileri 2026", replies: 24, author: "Ahmet42" },
    { title: "Yeni başlayanlar için öneriler", replies: 18, author: "ZeynepK" },
    { title: "Kargo firması tavsiyeleri", replies: 31, author: "SatıcıMehmet" },
    { title: "Ürün fotoğrafları için ipuçları", replies: 12, author: "FotoGrafik" },
    { title: "Düşük stok uyarıları nasıl yönetilir", replies: 8, author: "Stokçu" },
  ];

  return (
    <main className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Topluluk Forumu</h1>
          <p className="text-sm text-gray-500 mt-1">Tartışmalara katılın, bilgi paylaşın.</p>
        </div>
        <button className="bg-blue-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-blue-700 transition-colors">
          Yeni Konu
        </button>
      </div>
      <div className="space-y-2">
        {topics.map((t) => (
          <div key={t.title} className="bg-white border border-gray-200 rounded-lg p-4 flex items-center justify-between hover:shadow-md transition-shadow cursor-pointer">
            <div>
              <h3 className="font-medium text-gray-900 text-sm">{t.title}</h3>
              <p className="text-xs text-gray-400 mt-0.5">{t.author}</p>
            </div>
            <span className="text-xs text-gray-500">{t.replies} yanıt</span>
          </div>
        ))}
      </div>
    </main>
  );
}
