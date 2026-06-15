"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState("yorumlar");

  const Logo = () => (
    <div style={{display:"inline-flex",alignItems:"flex-start",lineHeight:1,cursor:"pointer"}} onClick={()=>router.push("/")}>
      <span style={{fontSize:18,fontWeight:700,color:"#1A2B4A",letterSpacing:-0.8}}>cadd</span>
      <div style={{position:"relative",display:"inline-block"}}>
        <span style={{fontSize:18,fontWeight:700,color:"#1A2B4A",letterSpacing:-0.8}}>e</span>
        <span style={{position:"absolute",top:-2,right:-7,fontSize:7,fontWeight:700,color:"#4A7FD4",letterSpacing:-0.2}}>cc</span>
      </div>
    </div>
  );

  return (
    <main style={{fontFamily:"'Space Grotesk',sans-serif",background:"#EEF4FF",minHeight:"100vh",color:"#1A2B4A"}}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css"/>

      {/* NAV */}
      <nav style={{height:56,background:"#fff",borderBottom:"1px solid #D6E4FA",display:"flex",alignItems:"center",padding:"0 24px",gap:12}}>
        <Logo/>
        <div style={{display:"flex",alignItems:"center",gap:8,marginLeft:"auto"}}>
          <button onClick={()=>router.push("/login")} style={{fontSize:12,color:"#5A7499",background:"none",border:"1px solid #D6E4FA",borderRadius:6,padding:"6px 12px",cursor:"pointer",fontFamily:"inherit"}}>Giriş yap</button>
          <button onClick={()=>router.push("/login")} style={{fontSize:12,color:"#fff",background:"#4A7FD4",border:"none",borderRadius:6,padding:"6px 12px",cursor:"pointer",fontFamily:"inherit",fontWeight:600}}>Üye ol</button>
        </div>
      </nav>

      {/* COVER */}
      <div style={{height:160,background:"linear-gradient(135deg,#4A7FD4 0%,#2C5FAA 100%)",position:"relative"}}>
        <div style={{width:80,height:80,borderRadius:12,background:"#fff",border:"3px solid #fff",position:"absolute",bottom:-40,left:32,display:"flex",alignItems:"center",justifyContent:"center",boxShadow:"0 4px 12px rgba(74,127,212,0.15)"}}>
          <i className="ti ti-tools" style={{fontSize:36,color:"#4A7FD4"}}/>
        </div>
        <button style={{position:"absolute",top:12,right:12,padding:"7px 14px",background:"rgba(255,255,255,0.2)",color:"#fff",border:"1px solid rgba(255,255,255,0.3)",borderRadius:6,fontSize:12,fontWeight:600,cursor:"pointer",fontFamily:"inherit",backdropFilter:"blur(4px)"}}>
          <i className="ti ti-edit" style={{fontSize:13}}/> Profili Düzenle
        </button>
      </div>

      {/* LAYOUT */}
      <div style={{display:"grid",gridTemplateColumns:"280px 1fr",gap:16,padding:"56px 24px 24px",maxWidth:1000,margin:"0 auto"}}>

        {/* SOL */}
        <div style={{display:"flex",flexDirection:"column",gap:10}}>
          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:16}}>
            <div style={{fontSize:18,fontWeight:700,color:"#1A2B4A",letterSpacing:-0.5,display:"flex",alignItems:"center",gap:6}}>
              Mehmet Yılmaz
              <div style={{width:8,height:8,borderRadius:"50%",background:"#4A7FD4"}}/>
            </div>
            <div style={{fontSize:12,color:"#8FAAC8",marginTop:3}}>Elektrik & Tesisat Ustası · Bireysel</div>
            <div style={{display:"flex",alignItems:"center",gap:4,fontSize:12,color:"#5A7499",marginTop:8}}>
              <i className="ti ti-map-pin" style={{fontSize:14,color:"#8FAAC8"}}/> Kahramanmaraş, Türkiye
            </div>
            <div style={{height:1,background:"#EEF4FF",margin:"12px 0"}}/>
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:8,textAlign:"center"}}>
              {[{n:"4.9",l:"★ Puan"},{n:"147",l:"Yorum"},{n:"312",l:"İş"}].map(s=>(
                <div key={s.l}>
                  <div style={{fontSize:18,fontWeight:700,color:"#1A2B4A",letterSpacing:-0.5}}>{s.n}</div>
                  <div style={{fontSize:10,color:"#8FAAC8",marginTop:2}}>{s.l}</div>
                </div>
              ))}
            </div>
          </div>

          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:16}}>
            <div style={{fontSize:11,fontWeight:700,color:"#8FAAC8",textTransform:"uppercase",letterSpacing:1,marginBottom:10}}>Uzmanlıklar</div>
            <div style={{display:"flex",flexWrap:"wrap",gap:5}}>
              {["Elektrik","Tesisat","Pano Montaj","Aydınlatma","Kombi","7/24 Servis"].map(t=>(
                <span key={t} style={{fontSize:11,fontWeight:600,padding:"4px 10px",borderRadius:20,background:"#EEF4FF",color:"#4A7FD4",border:"1px solid #D6E4FA"}}>{t}</span>
              ))}
            </div>
          </div>

          <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:16}}>
            <div style={{fontSize:11,fontWeight:700,color:"#8FAAC8",textTransform:"uppercase",letterSpacing:1,marginBottom:10}}>Bilgiler</div>
            {[
              {icon:"ti-clock",label:"Deneyim",val:"10 yıl"},
              {icon:"ti-calendar",label:"Üyelik",val:"Ocak 2024"},
              {icon:"ti-clock-hour-4",label:"Yanıt süresi",val:"~30 dakika"},
              {icon:"ti-map-2",label:"Hizmet bölgesi",val:"Kahramanmaraş merkez"},
            ].map(r=>(
              <div key={r.label} style={{display:"flex",alignItems:"center",gap:8,padding:"6px 0",borderBottom:"1px solid #EEF4FF"}}>
                <i className={`ti ${r.icon}`} style={{fontSize:16,color:"#8FAAC8",flexShrink:0}}/>
                <div>
                  <div style={{fontSize:11,color:"#8FAAC8"}}>{r.label}</div>
                  <div style={{fontSize:12,color:"#1A2B4A",fontWeight:500}}>{r.val}</div>
                </div>
              </div>
            ))}
          </div>

          <div style={{background:"#4A7FD4",borderRadius:8,padding:20,textAlign:"center"}}>
            <div style={{fontSize:15,fontWeight:700,color:"#fff",marginBottom:6}}>İletişime Geç</div>
            <div style={{fontSize:12,color:"rgba(255,255,255,0.75)",marginBottom:16}}>Mehmet Usta ile hızlıca iletişime geçin</div>
            <button style={{width:"100%",padding:10,background:"#fff",color:"#4A7FD4",border:"none",borderRadius:6,fontSize:13,fontWeight:700,cursor:"pointer",fontFamily:"inherit"}}>
              <i className="ti ti-message" style={{fontSize:14}}/> Mesaj Gönder
            </button>
          </div>
        </div>

        {/* SAĞ */}
        <div style={{display:"flex",flexDirection:"column",gap:12}}>
          <div style={{display:"flex",gap:0,background:"#EEF4FF",borderRadius:8,padding:4}}>
            {[{k:"yorumlar",l:"Değerlendirmeler"},{k:"portfolio",l:"Portföy"},{k:"hakkinda",l:"Hakkında"}].map(t=>(
              <div key={t.k} onClick={()=>setActiveTab(t.k)} style={{flex:1,padding:8,textAlign:"center",fontSize:12,fontWeight:600,cursor:"pointer",borderRadius:6,transition:"all .15s",background:activeTab===t.k?"#fff":"transparent",color:activeTab===t.k?"#1A2B4A":"#8FAAC8",boxShadow:activeTab===t.k?"0 1px 4px rgba(74,127,212,0.1)":"none"}}>
                {t.l}
              </div>
            ))}
          </div>

          {activeTab === "yorumlar" && (
            <>
              {[
                {name:"Ahmet K.",date:"2 gün önce",rating:"5.0",text:"Çok hızlı geldi, işini eksiksiz yaptı. Elektrik panosunu değiştirdi, temiz ve düzenli çalışıyor. Kesinlikle tavsiye ederim."},
                {name:"Fatma S.",date:"1 hafta önce",rating:"5.0",text:"Kombi arızamı kısa sürede çözdü. Fiyatı da uygundu. Teşekkürler Mehmet usta!"},
                {name:"Mustafa T.",date:"2 hafta önce",rating:"4.0",text:"İşini iyi yapıyor. Biraz geç geldi ama kaliteli iş çıkardı."},
              ].map(r=>(
                <div key={r.name} style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:14}}>
                  <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:8}}>
                    <div style={{width:32,height:32,borderRadius:6,background:"#EEF4FF",display:"flex",alignItems:"center",justifyContent:"center"}}>
                      <i className="ti ti-user" style={{fontSize:16,color:"#4A7FD4"}}/>
                    </div>
                    <div>
                      <div style={{fontSize:13,fontWeight:600,color:"#1A2B4A"}}>{r.name}</div>
                      <div style={{fontSize:11,color:"#8FAAC8"}}>{r.date}</div>
                    </div>
                    <div style={{marginLeft:"auto",fontSize:12,fontWeight:700,color:"#4A7FD4"}}>★ {r.rating}</div>
                  </div>
                  <div style={{fontSize:12,color:"#5A7499",lineHeight:1.55}}>{r.text}</div>
                </div>
              ))}
            </>
          )}

          {activeTab === "portfolio" && (
            <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:16}}>
              <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:8}}>
                {[...Array(6)].map((_,i)=>(
                  <div key={i} style={{aspectRatio:"1",background:"#EEF4FF",border:"1px solid #D6E4FA",borderRadius:8,display:"flex",alignItems:"center",justifyContent:"center"}}>
                    <i className={i===5?"ti ti-plus":"ti ti-photo"} style={{fontSize:28,color:"#C4D4E8"}}/>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === "hakkinda" && (
            <div style={{background:"#fff",border:"1px solid #D6E4FA",borderRadius:8,padding:16}}>
              <p style={{fontSize:13,color:"#5A7499",lineHeight:1.7}}>
                10 yılı aşkın deneyimimle Kahramanmaraş ve çevresinde elektrik tesisatı, pano montajı, aydınlatma sistemleri, kombi bakım ve onarımı konularında profesyonel hizmet sunuyorum. Müşteri memnuniyetini her zaman ön planda tutarak işimi titizlikle yapıyorum. 7/24 acil servis hizmeti vermekteyim.
              </p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
