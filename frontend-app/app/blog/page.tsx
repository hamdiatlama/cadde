'use client';
import { useState } from 'react';

const posts = [
  { id: 1, title: '2026 Yaz Trendleri: Bu Sezon Neler Giymeli?', excerpt: 'Yaz aylarına girerken gardırobunuzu yenilemek için en trend parçaları derledik.', author: 'Elif Demir', date: '2026-06-14', readTime: '5 dk', category: 'Moda', image: null },
  { id: 2, title: 'Akıllı Ev Teknolojileri 2026', excerpt: 'Evinizi akıllı cihazlarla donatmak için kapsamlı bir rehber.', author: 'Can Tekin', date: '2026-06-12', readTime: '7 dk', category: 'Teknoloji', image: null },
  { id: 3, title: 'Sürdürülebilir Alışveriş İpuçları', excerpt: 'Çevre dostu alışveriş yapmak için pratik öneriler.', author: 'Zeynep Yılmaz', date: '2026-06-10', readTime: '4 dk', category: 'Yaşam', image: null },
  { id: 4, title: 'İkinci El Ürün Alırken Dikkat Edilmesi Gerekenler', excerpt: 'Yenilenmiş ürün satın alırken kaliteyi nasıl anlarsınız?', author: 'Mehmet Kaya', date: '2026-06-08', readTime: '6 dk', category: 'Alışveriş', image: null },
  { id: 5, title: 'Ev Ofis İçin En İyi Ekipmanlar 2026', excerpt: 'Verimliliğinizi artıracak ofis malzemeleri ve teknolojileri.', author: 'Ayşe Kara', date: '2026-06-05', readTime: '8 dk', category: 'Teknoloji', image: null },
  { id: 6, title: 'Yaz Tatili İçin Seyahat Çantası Hazırlama Rehberi', excerpt: 'Tatil öncesi valizinizi hazırlarken ihtiyacınız olan her şey.', author: 'Elif Demir', date: '2026-06-03', readTime: '3 dk', category: 'Seyahat', image: null },
];

const categories = [...new Set(posts.map(p => p.category))];

export default function BlogPage() {
  const [categoryFilter, setCategoryFilter] = useState('Tümü');

  const filtered = categoryFilter === 'Tümü' ? posts : posts.filter(p => p.category === categoryFilter);

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">Blog</h1>
      <p className="text-gray-500 mb-6">Alışveriş ipuçları, trendler ve daha fazlası</p>

      <div className="flex gap-2 mb-6 flex-wrap">
        {['Tümü', ...categories].map(c => (
          <button key={c} onClick={() => setCategoryFilter(c)}
            className={`px-3 py-1.5 rounded text-sm font-semibold ${categoryFilter === c ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
            {c}
          </button>
        ))}
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filtered.map(p => (
          <article key={p.id} className="border rounded-lg shadow-sm hover:shadow-md overflow-hidden cursor-pointer">
            <div className="h-36 bg-gradient-to-br from-blue-50 to-indigo-50 flex items-center justify-center text-gray-400 text-sm">
              {p.image || 'Blog Görseli'}
            </div>
            <div className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded font-semibold">{p.category}</span>
                <span className="text-xs text-gray-400">{p.readTime}</span>
              </div>
              <h2 className="font-semibold text-base mb-2 line-clamp-2">{p.title}</h2>
              <p className="text-sm text-gray-500 mb-3 line-clamp-2">{p.excerpt}</p>
              <div className="flex items-center justify-between text-xs text-gray-400">
                <span>{p.author}</span>
                <span>{p.date}</span>
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
