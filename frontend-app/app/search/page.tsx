"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

const RESULTS = [
  { icon: "ti-bolt", name: "Mehmet Usta", cat: "Elektrik & Tesisat · Bireysel · 10 yıl deneyim", desc: "10 yıllık deneyimle elektrik tesisatı, pano montajı, aydınlatma sistemleri kurulum ve bakım hizmetleri sunuyorum. 7/24 acil servis.", tags: ["Elektrik","Tesisat","Pano","Aydınlatma"], rating: "4.9", reviews: 147, dist: "1.2 km" },
  { icon: "ti-hammer", name: "Ali Usta", cat: "Marangoz & Tadilat · Bireysel · 8 yıl deneyim", desc: "Mutfak dolabı, parke, laminant zemin döşeme, alçıpan asma tavan ve iç dekorasyon işleri yapıyorum.", tags: ["Marangoz","Parke","Alçıpan","Dekorasyon"], rating: "4.7", reviews: 89, dist: "2.4 km" },
  { icon: "ti-droplet", name: "Hasan Tesisatçı", cat: "Su Tesisatı · Bireysel · 15 yıl deneyim", desc: "Su tesisatı, doğalgaz tesisatı, kombi bakım ve onarımı, banyo tadilat işleri konusunda hizmet veriyorum.", tags: ["Su Tesisatı","Doğalgaz","Kombi","Banyo"], rating: "4.8", reviews: 203, dist: "0.8 km" },
  { icon: "ti-paint", name: "Kadir Boyacı", cat: "Boya & Badana · Bireysel · 12 yıl deneyim", desc: "İç ve dış cephe boya, dekoratif boya, badana, saten alçı, duvar kağıdı uygulamaları yapıyorum.", tags: ["Boya","Badana","Saten","Dekoratif"], rating: "4.6", reviews: 64, dist: "3.1 km" },
];

const CATS = [
  { icon: "ti-tools", label: "Ustalar" },
  { icon: "ti-bolt", label: "Elektrik" },
  { icon: "ti-droplet", label: "Tesisat" },
  { icon: "ti-paint", label: "Boyacı" },
  { icon: "ti-hammer", label: "Marangoz" },
  { icon: "ti-air-conditioning", label: "Klima" },
];

export default function SearchPage() {
  const router = useRouter();
  const [activeChip, setActiveChip] = useState("Ustalar");
  const [query, setQuery] = useState("usta");

  return (
    <main style={{ fontFamily: "'Space Grotesk',sans-serif", background: "#EEF4FF", minHeight: "100vh", color: "#1A2B4A" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>

      {/* NAV */}
      <nav style={{ height: 56, background: "#fff", borderBottom: "1px solid #D6E4FA", display: "flex", alignItems: "center", padding: "0 24px", gap: 12, position: "sticky", top: 0, zIndex: 10 }}>
        <div onClick={() => router.push("/")} style={{ display: "flex", alignItems: "center", gap: 7, marginRight: 16, cursor: "pointer", flexShrink: 0 }}>
          <div style={{ width: 26, height: 26, background: "#4A7FD4", borderRadius: 6, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ color: "#fff", fontSize: 13, fontWeight: 700 }}>C</span>
          </div>
          <span style={{ fontSize: 16, fontWeight: 700, color: "#1A2B4A" }}>cadde</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", flex: 1, background: "#f8faff", border: "1px solid #D6E4FA", borderRadius: 8, overflow: "hidden", maxWidth: 500 }}>
          <i className="ti ti-search" style={{ padding: "0 10px", color: "#8FAAC8", fontSize: 16 }}/>
          <input value={query} onChange={e => setQuery(e.target.value)} type="text" style={{ flex: 1, border: "none", outline: "none", background: "transparent", fontFamily: "inherit", fontSize: 13, color: "#1A2B4A", padding: "10px 0" }}/>
          <div style={{ width: 1, height: 24, background: "#D6E4FA" }}/>
          <span style={{ display: "flex", alignItems: "center", gap: 4, padding: "0 10px", fontSize: 12, color: "#4A7FD4", fontWeight: 600, cursor: "pointer", whiteSpace: "nowrap" }}>
            <i className="ti ti-map-pin" style={{ fontSize: 12 }}/> Kahramanmaraş
          </span>
          <button style={{ padding: "10px 16px", background: "#4A7FD4", color: "#fff", border: "none", fontFamily: "inherit", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>Ara</button>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginLeft: "auto" }}>
          <button onClick={() => router.push("/login")} style={{ fontSize: 12, color: "#5A7499", background: "none", border: "1px solid #D6E4FA", borderRadius: 6, padding: "6px 12px", cursor: "pointer", fontFamily: "inherit" }}>Giriş yap</button>
          <button onClick={() => router.push("/login")} style={{ fontSize: 12, color: "#fff", background: "#4A7FD4", border: "none", borderRadius: 6, padding: "6px 12px", cursor: "pointer", fontFamily: "inherit", fontWeight: 600 }}>Üye ol</button>
        </div>
      </nav>

      <div style={{ display: "grid", gridTemplateColumns: "220px 1fr", gap: 16, padding: "16px 24px", maxWidth: 1100, margin: "0 auto" }}>

        {/* FİLTRE */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {[
            { title: "Kategori", items: [{ l: "Tüm Ustalar", n: 48, on: true }, { l: "Elektrik", n: 15 }, { l: "Tesisat", n: 18 }, { l: "Alçı & Sıva", n: 11 }, { l: "Boya", n: 12 }, { l: "Marangoz", n: 9 }] },
            { title: "Puan", items: [{ l: "4.5 ve üzeri", on: true }, { l: "4.0 ve üzeri" }, { l: "Tümü" }] },
            { title: "Mesafe", items: [{ l: "5 km içinde", on: true }, { l: "10 km içinde" }, { l: "Tüm şehir" }, { l: "Tüm Türkiye" }] },
            { title: "Durum", items: [{ l: "Onaylı üye", on: true }, { l: "Şu an aktif" }, { l: "Müsait" }] },
          ].map(f => (
            <div key={f.title} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 14 }}>
              <div style={{ fontSize: 11, fontWeight: 700, color: "#8FAAC8", textTransform: "uppercase", letterSpacing: 1, marginBottom: 10 }}>{f.title}</div>
              {f.items.map(item => (
                <div key={item.l} style={{ display: "flex", alignItems: "center", gap: 8, padding: "5px 0", cursor: "pointer" }}>
                  <div style={{ width: 16, height: 16, border: `1.5px solid ${(item as any).on ? "#4A7FD4" : "#D6E4FA"}`, borderRadius: 4, background: (item as any).on ? "#4A7FD4" : "transparent", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                    {(item as any).on && <i className="ti ti-check" style={{ fontSize: 10, color: "#fff" }}/>}
                  </div>
                  <span style={{ fontSize: 12, color: "#5A7499" }}>{item.l}</span>
                  {(item as any).n && <span style={{ fontSize: 10, color: "#C4D4E8", marginLeft: "auto" }}>{(item as any).n}</span>}
                </div>
              ))}
            </div>
          ))}
        </div>

        {/* SONUÇLAR */}
        <div>
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 10 }}>
            {CATS.map(c => (
              <span key={c.label} onClick={() => setActiveChip(c.label)} style={{ display: "inline-flex", alignItems: "center", gap: 5, padding: "5px 12px", background: activeChip === c.label ? "#4A7FD4" : "#fff", border: `1px solid ${activeChip === c.label ? "#4A7FD4" : "#D6E4FA"}`, borderRadius: 20, fontSize: 12, color: activeChip === c.label ? "#fff" : "#5A7499", cursor: "pointer", fontWeight: 500, transition: "all .15s" }}>
                <i className={`ti ${c.icon}`} style={{ fontSize: 13 }}/> {c.label}
              </span>
            ))}
          </div>

          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
            <div style={{ fontSize: 13, color: "#5A7499" }}><b style={{ color: "#1A2B4A" }}>48</b> sonuç — Kahramanmaraş</div>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <select style={{ fontSize: 12, color: "#1A2B4A", border: "1px solid #D6E4FA", borderRadius: 6, padding: "5px 10px", background: "#fff", fontFamily: "inherit", cursor: "pointer", outline: "none" }}>
                <option>Önerilen</option>
                <option>En yakın</option>
                <option>En yüksek puan</option>
                <option>En çok iş</option>
              </select>
            </div>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {RESULTS.map(r => (
              <div key={r.name} style={{ background: "#fff", border: "1px solid #D6E4FA", borderRadius: 8, padding: 16, display: "flex", gap: 14, cursor: "pointer" }}>
                <div style={{ width: 52, height: 52, borderRadius: 8, background: "#EEF4FF", border: "1px solid #D6E4FA", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                  <i className={`ti ${r.icon}`} style={{ fontSize: 24, color: "#4A7FD4" }}/>
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 8 }}>
                    <div>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#1A2B4A", letterSpacing: -0.3, display: "flex", alignItems: "center", gap: 6 }}>
                        {r.name}
                        <div style={{ width: 6, height: 6, borderRadius: "50%", background: "#4A7FD4", flexShrink: 0 }}/>
                      </div>
                      <div style={{ fontSize: 11, color: "#8FAAC8", marginTop: 2 }}>{r.cat}</div>
                    </div>
                    <div style={{ textAlign: "right", flexShrink: 0, display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 3 }}>
                      <div style={{ fontSize: 16, fontWeight: 700, color: "#1A2B4A", letterSpacing: -0.5 }}>{r.rating}</div>
                      <div style={{ fontSize: 11, color: "#8FAAC8" }}>★ {r.reviews} değerlendirme</div>
                      <div style={{ fontSize: 11, color: "#8FAAC8" }}>📍 {r.dist}</div>
                      <button style={{ padding: "7px 16px", background: "#4A7FD4", color: "#fff", border: "none", borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", marginTop: 4 }}>İletişim</button>
                    </div>
                  </div>
                  <div style={{ fontSize: 12, color: "#5A7499", marginTop: 8, lineHeight: 1.55 }}>{r.desc}</div>
                  <div style={{ display: "flex", gap: 5, marginTop: 8, flexWrap: "wrap" }}>
                    {r.tags.map(t => (
                      <span key={t} style={{ fontSize: 10, fontWeight: 600, padding: "3px 8px", borderRadius: 20, background: "#EEF4FF", color: "#4A7FD4", border: "1px solid #D6E4FA" }}>{t}</span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 6, marginTop: 16 }}>
            {["‹", "1", "2", "3", "...", "8", "›"].map((p, i) => (
              <div key={i} style={{ width: 32, height: 32, border: "1px solid #D6E4FA", borderRadius: 6, background: p === "1" ? "#4A7FD4" : "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, color: p === "1" ? "#fff" : "#5A7499", cursor: "pointer", fontWeight: 500 }}>{p}</div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
