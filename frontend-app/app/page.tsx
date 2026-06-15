"use client";
import { useRouter } from "next/navigation";
import { useState } = from "react";

const Logo = ({ router }: { router: any }) => (
  <div style={{display:"inline-flex",alignItems:"flex-start",lineHeight:1,cursor:"pointer"}} onClick={()=>router.push("/")}>
    <span style={{fontSize:18,fontWeight:700,color:"#1A2B4A",letterSpacing:-0.8}}>cadd</span>
    <div style={{position:"relative",display:"inline-block"}}>
      <span style={{fontSize:18,fontWeight:700,color:"#1A2B4A",letterSpacing:-0.8}}>e</span>
      <span style={{position:"absolute",top:-2,right:-7,fontSize:7,fontWeight:700,color:"#4A7FD4",letterSpacing:-0.2}}>cc</span>
    </div>
  </div>
);

export default function Home() {
  const router = useRouter();
  const [query, setQuery] = useState("");

  function handleSearch() {
    router.push(`/search?q=${encodeURIComponent(query.trim() || "")}`);
  }

  return (
    <main style={{fontFamily:"'Space Grotesk',sans-serif",background:"#EEF4FF",minHeight:"100vh",color:"#1A2B4A"}}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>

      {/* NAV */}
      <nav style={{height:56,background:"#fff",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",padding:"0 32px"}}>
        <div style={{marginRight:40}}><Logo router={router}/></div>
        <div style={{display:"flex",gap:28,flex:1}}>
          {["Keşfet","İşletmeler","Kurumlar","Hakkında"].map(l=>(
            <span key={l} className="nav-link" style={{fontSize:13,color:"#5A7499",cursor:"pointer",fontWeight:500}}>{l}</span>
          ))}
        </div>
        <div style={{display:"flex",alignItems:"center",gap:10}}>
          <button onClick={()=>router.push("/login")} style={{fontSize:13,color:"#5A7499",background:"none",border:"1px solid #D6E4FA",borderRadius:6,padding:"7px 14px",cursor:"pointer",fontFamily:"inherit",fontWeight:500}}>Giriş yap</button>
          <button onClick={()=>router.push("/login")} style={{fontSize:13,color:"#fff",background:"#4A7FD4",border:"none",borderRadius:6,padding:"7px 16px",cursor:"pointer",fontFamily:"inherit",fontWeight:600}}>Üye ol</button>
        </div>
      </nav>

      {/* HERO */}
      <div style={{background:"#fff",borderBottom:"1px solid #D6E4FA",display:"grid",gridTemplateColumns:"1.1fr 0.9fr"}}>
        <div style={{padding:"52px 36px",borderRight:"1px solid #D6E4FA"}}>
          <div style={{display:"inline-flex",alignItems:"center",gap:6,background:"#EEF4FF",border:"1px solid #D6E4FA",borderRadius:20,padding:"5px 12px",marginBottom:24}}>
            <div style={{width:6,height:6,borderRadius:"50%",background:"#4A7FD4"}}/>
            <span style={{fontSize:11,fontWeight:600,color:"#4A7FD4",letterSpacing:0.5,textTransform:"uppercase"}}>{"Türkiye'nin süper uygulaması"}</span>
          </div>
          <h1 style={{fontSize:40,fontWeight:700,lineHeight:1.1,letterSpacing:-1.5,color:"#1A2B4A",marginBottom:14}}>
            {"Hayatında ne"}<br/>{"lazımsa,"}<br/><span style={{color:"#4A7FD4"}}>{"burada."}</span>
          </h1>
          <p style={{fontSize:14,color:"#5A7499",lineHeight:1.65,maxWidth:320,marginBottom:28}}>
            {"Usta, market, taksi, otel, çiftçi — hepsi tek platformda, yakınında."}
          </p>
          <div style={{display:"flex",gap:24}}>
            {[{n:"24K",l:"Aktif üye"},{n:"6K+",l:"İşletme"},{n:"81",l:"İl"},{n:"4.8★",l:"Puan"}].map(s=>(
              <div key={s.l}>
                <div style={{fontSize:20,fontWeight:700,color:"#4A7FD4",letterSpacing:-0.5}}>{s.n}</div>
                <div style={{fontSize:11,color:"#8FAAC8",marginTop:1}}>{s.l}</div>
              </div>
            ))}
          </div>
        </div>
        <div style={{padding:"52px 32px",background:"#EEF4FF",display:"flex",flexDirection:"column",justifyContent:"center",gap:16}}>
          <div style={{fontSize:11,fontWeight:600,color:"#8FAAC8",textTransform:"uppercase",letterSpacing:1.2}}>{"Hızlı arama"}</div>
          <div style={{display:"flex",alignItems:"center",background:"#fff",border:"1.5px solid #D6E4FA",borderRadius:8,overflow:"hidden"}}>
            <i className="ti ti-search" style={{padding:"0 12px",color:"#8FAAC8",fontSize:18}}/>
            <input type="text" placeholder="Ne arıyorsunuz?" value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==="Enter"&&handleSearch()} style={{flex:1,border:"none",outline:"none",background:"transparent",fontFamily:"inherit",fontSize:14,color:"#1A2B4A",padding:"12px 0"}}/>
            <div style={{width:1,height:28,background:"#D6E4FA"}}/>
            <span style={{display:"flex",alignItems:"center",gap:4,padding:"0 12px",fontSize:12,color:"#4A7FD4",fontWeight:600,cursor:"pointer",whiteSpace:"nowrap"}}>
              <i className="ti ti-map-pin" style={{fontSize:14}}/> {"Kahramanmaraş"}
            </span>
            <button onClick={handleSearch} style={{padding:"12px 20px",background:"#4A7FD4",color:"#fff",border:"none",fontFamily:"inherit",fontSize:13,fontWeight:600,cursor:"pointer"}}>Ara</button>
          </div>
          <div style={{display:"flex",flexWrap:"wrap",gap:6}}>
            {[{icon:"ti-tools",l:"Usta"},{icon:"ti-car",l:"Taksi"},{icon:"ti-tools-kitchen-2",l:"Yemek"},{icon:"ti-plant",l:"Çiftçi"},{icon:"ti-bed",l:"Otel"},{icon:"ti-briefcase",l:"Proje"}].map(t=>(
              <span key={t.l} onClick={()=>router.push(`/search?q=${t.l}`)} className="qtag" style={{display:"inline-flex",alignItems:"center",gap:5,padding:"6px 12px",background:"#fff",border:"1px solid #D6E4FA",borderRadius:20,fontSize:12,color:"#5A7499",cursor:"pointer",fontWeight:500,transition:"all .15s"}}>
                <i className={`ti ${t.icon}`} style={{fontSize:14,color:"#4A7FD4"}}/> {t.l}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* BODY */}
      <div style={{padding:"28px 32px"}}>
        <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:16}}>
          <span style={{fontSize:12,fontWeight:700,color:"#5A7499",textTransform:"uppercase",letterSpacing:1.2}}>Kategoriler</span>
          <span onClick={()=>router.push("/search")} style={{fontSize:12,color:"#4A7FD4",cursor:"pointer",fontWeight:600}}>{"Tümünü gör →"}</span>
        </div>
        <div style={{display:"grid",gridTemplateColumns:"repeat(6,1fr)",gap:8,marginBottom:32}}>
          {[
            {icon:"ti-tools",n:"Ustalar",s:"Tadilat, tamir"},
            {icon:"ti-building-store",n:"Mağazalar",s:"Yerel alışveriş"},
            {icon:"ti-plant",n:"Çiftçiler",s:"Taze ürünler"},
            {icon:"ti-car",n:"Taksi",s:"Anlık ulaşım"},
            {icon:"ti-bed",n:"Oteller",s:"Konaklama"},
            {icon:"ti-tools-kitchen-2",n:"Yemek",s:"Sipariş ver"},
            {icon:"ti-briefcase",n:"Projeler",s:"Freelance, iş"},
            {icon:"ti-building",n:"Kurumlar",s:"Dernek, okul"},
            {icon:"ti-home",n:"Emlak",s:"Kiralık, satılık"},
            {icon:"ti-stethoscope",n:"Sağlık",s:"Klinik, doktor"},
            {icon:"ti-school",n:"Eğitim",s:"Kurs, özel ders"},
            {icon:"ti-car-garage",n:"Araç Servis",s:"Bakım, tamir"},
          ].map(c=>(
            <div key={c.n} onClick={()=>router.push(`/search?q=${c.n}`)} className="cat-card" style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:"18px 10px",textAlign:"center",cursor:"pointer",transition:"all .15s"}}>
              <div className="cat-icon-wrap" style={{width:44,height:44,background:"#EEF4FF",borderRadius:10,display:"flex",alignItems:"center",justifyContent:"center",margin:"0 auto 10px",transition:"all .15s"}}>
                <i className={`ti ${c.icon} cat-icon`} style={{fontSize:22,color:"#4A7FD4",transition:"all .15s"}}/>
              </div>
              <div className="cn" style={{fontSize:12,fontWeight:600,color:"#1A2B4A",transition:"all .15s"}}>{c.n}</div>
              <div className="cs" style={{fontSize:10,color:"#8FAAC8",marginTop:2,transition:"all .15s"}}>{c.s}</div>
            </div>
          ))}
        </div>

        <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:16}}>
          <span style={{fontSize:12,fontWeight:700,color:"#5A7499",textTransform:"uppercase",letterSpacing:1.2}}>{"Kahramanmaraş'ta öne çıkanlar"}</span>
          <span onClick={()=>router.push("/search")} style={{fontSize:12,color:"#4A7FD4",cursor:"pointer",fontWeight:600}}>{"Tümünü gör →"}</span>
        </div>
        <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10}}>
          {[
            {icon:"ti-tools",n:"Mehmet Usta",c:"Elektrik & Tesisat",r:"4.9",d:"1.2 km",j:"147 iş"},
            {icon:"ti-plant",n:"Doğal Bahçem",c:"Üretici · Sebze & meyve",r:"4.7",d:"3.5 km",j:"89 satış"},
            {icon:"ti-bed",n:"Maraş Grand Otel",c:"Konaklama · Kahvaltı dahil",r:"4.8",d:"0.8 km",j:"312 konaklama"},
            {icon:"ti-car",n:"Ahmet Şoför",c:"Taksi · Şu an aktif",r:"4.6",d:"Anlık",j:"1.2K yolcu"},
          ].map(b=>(
            <div key={b.n} onClick={()=>router.push("/profile")} className="biz-card" style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:16,display:"flex",alignItems:"flex-start",gap:12,cursor:"pointer",transition:"border-color .15s"}}>
              <div style={{width:44,height:44,borderRadius:8,background:"#EEF4FF",border:"1px solid #D6E4FA",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>
                <i className={`ti ${b.icon}`} style={{fontSize:22,color:"#4A7FD4"}}/>
              </div>
              <div style={{flex:1}}>
                <div style={{fontSize:13,fontWeight:600,color:"#1A2B4A",letterSpacing:-0.3,display:"flex",alignItems:"center",gap:5}}>
                  {b.n}<div style={{width:6,height:6,borderRadius:"50%",background:"#4A7FD4"}}/>
                </div>
                <div style={{fontSize:11,color:"#8FAAC8",marginTop:2}}>{b.c}</div>
                <div style={{display:"flex",alignItems:"center",gap:6,marginTop:10}}>
                  <span style={{fontSize:12,fontWeight:700,color:"#4A7FD4"}}>★ {b.r}</span>
                  <span style={{fontSize:10,fontWeight:600,padding:"2px 8px",borderRadius:20,background:"#EEF4FF",color:"#4A7FD4"}}>{b.j}</span>
                  <span style={{fontSize:11,color:"#8FAAC8"}}>{b.d}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}
