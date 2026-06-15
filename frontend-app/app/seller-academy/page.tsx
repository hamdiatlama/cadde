"use client";

export default function SellerAcademyPage() {
  const courses = [
    { title: "Satışta İlk Adımlar", duration: "2 saat", lessons: 8, level: "Başlangıç" },
    { title: "Ürün Fotoğrafçılığı", duration: "3 saat", lessons: 12, level: "Orta" },
    { title: "Müşteri Yönetimi", duration: "1.5 saat", lessons: 6, level: "Başlangıç" },
    { title: "Pazarlama Stratejileri", duration: "4 saat", lessons: 16, level: "İleri" },
    { title: "Stok ve Envanter", duration: "2 saat", lessons: 10, level: "Orta" },
  ];

  return (
    <main className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Satıcı Akademisi</h1>
      <p className="text-sm text-gray-500 mb-6">Satış becerilerinizi geliştirecek kurslar.</p>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {courses.map((c) => (
          <div key={c.title} className="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
            <span className="text-xs font-medium text-blue-700 bg-blue-50 px-2 py-0.5 rounded">{c.level}</span>
            <h3 className="font-semibold text-gray-900 mt-3">{c.title}</h3>
            <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
              <span>{c.lessons} ders</span>
              <span>{c.duration}</span>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
