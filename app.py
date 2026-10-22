HTML

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sales Analytics Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/xlsx/dist/xlsx.full.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif;background:#f2f5fa;color:#202b3c}
header{background:#172554;color:white;padding:22px}
header h1{margin:0 0 8px;font-size:25px}
header p{margin:0;color:#dbeafe}
main{padding:18px;max-width:1200px;margin:auto}
.panel,.metric{background:white;padding:17px;border-radius:12px;
box-shadow:0 3px 12px #17255412;margin-bottom:16px}
.upload{border:2px dashed #93a8c9;text-align:center}
input,select,button{padding:11px;border:1px solid #ccd5e2;
border-radius:7px;background:white;max-width:100%}
button{background:#1d4ed8;color:white;border:0;cursor:pointer}
.filters,.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:12px}
.metric small{color:#64748b}
.metric h2{font-size:23px;margin:10px 0 0;overflow-wrap:anywhere}
.chartgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.chartbox{height:320px;position:relative}
h3{margin-top:0}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{text-align:left;padding:10px;border-bottom:1px solid #e5e7eb}
th{background:#eff6ff}
.tablewrap{overflow:auto;max-height:400px}
.status{color:#475569;font-size:14px}
</style>
</head>
<body>
<header>
<h1>Sales Analytics Dashboard</h1>
<p>Product Performance • Revenue • Sales Trends</p>
</header>
<main>
<div class="panel upload">
<h3>Upload Your Excel Sales File</h3>
<p>Upload nbd_sales_cleaning.xlsx or another compatible Excel file.</p>
<input type="file" id="file" accept=".xlsx,.xls,.csv">
<p id="status" class="status">Please select your data file.</p>
</div>

<div class="panel">
<h3>Filters</h3>
<div class="filters">
<div><label>Category</label><br><select id="category"><option value="">All Categories</option></select></div>
<div><label>Brand</label><br><select id="brand"><option value="">All Brands</option></select></div>
<div><label>State</label><br><select id="state"><option value="">All States</option></select></div>
<div><label>Shop Type</label><br><select id="shop"><option value="">All Shops</option></select></div>
<div><label>Month</label><br><select id="month"><option value="">All Months</option></select></div>
</div>
<br><button onclick="resetFilters()">Reset Filters</button>
</div>

<div class="cards">
<div class="metric"><small>Total Sales (₹)</small><h2 id="revenue">₹0</h2></div>
<div class="metric"><small>Units / Volume (kg)</small><h2 id="volume">0</h2></div>
<div class="metric"><small>Cases Sold</small><h2 id="cases">0</h2></div>
<div class="metric"><small>Products Listed</small><h2 id="products">0</h2></div>
<div class="metric"><small>Top-Selling Product</small><h2 id="top">—</h2></div>
<div class="metric"><small>Lowest-Selling Product</small><h2 id="low">—</h2></div>
</div>

<div class="chartgrid">
<div class="panel"><h3>Top 10 Products by Sales Value</h3><div class="chartbox"><canvas id="productChart"></canvas></div></div>
<div class="panel"><h3>Sales by Category</h3><div class="chartbox"><canvas id="categoryChart"></canvas></div></div>
<div class="panel"><h3>Monthly Sales Trend</h3><div class="chartbox"><canvas id="monthChart"></canvas></div></div>
<div class="panel"><h3>Sales by Shop Type</h3><div class="chartbox"><canvas id="shopChart"></canvas></div></div>
</div>

<div class="panel">
<h3>Product Performance Table</h3>
<input id="search" placeholder="Search product..." oninput="render()">
<br><br>
<div class="tablewrap"><table>
<thead><tr><th>Product</th><th>Category</th><th>Sales (₹)</th><th>Volume (kg)</th><th>Cases</th></tr></thead>
<tbody id="tbody"></tbody>
</table></div>
<p id="rows" class="status"></p>
</div>
</main>

<script>
let data=[], charts={};
const $=id=>document.getElementById(id);
const num=v=>Number(v)||0;
const money=v=>"₹"+Math.round(v).toLocaleString("en-IN");
const sum=(a,k)=>a.reduce((s,r)=>s+num(r[k]),0);
const clean=v=>String(v??"").trim();
function get(r,k){return clean(r[k]);}

$("file").addEventListener("change",async e=>{
 const file=e.target.files[0];
 if(!file)return;
 $("status").textContent="Reading file...";
 try{
  const buf=await file.arrayBuffer();
  const wb=XLSX.read(buf,{type:"array",cellDates:true});
  const sheet=wb.Sheets[wb.SheetNames[0]];
  data=XLSX.utils.sheet_to_json(sheet,{defval:""});
  if(!data.length)throw Error("No data rows found.");
  const first=data[0];
  ["value_rs","volume_kg","cases","category","brand_code",
   "base_pack","month","buyer_state","shop_type"].forEach(k=>{
    if(!(k in first))throw Error("Required column missing: "+k);
   });
  data=data.map(r=>{
   let d={...r};
   if(d.month instanceof Date){
    d.month=d.month.getFullYear()+"-"+String(d.month.getMonth()+1).padStart(2,"0");
   }else{
    let dt=new Date(d.month);
    d.month=!isNaN(dt)?dt.getFullYear()+"-"+String(dt.getMonth()+1).padStart(2,"0"):clean(d.month);
   }
   return d;
  });
  ["category","brand","state","shop","month"].forEach(k=>{
   const map={category:"category",brand:"brand_code",state:"buyer_state",shop:"shop_type",month:"month"};
   const sel=$(k),old=sel.value;
   sel.innerHTML='<option value="">All</option>';
   [...new Set(data.map(r=>get(r,map[k])).filter(Boolean))].sort()
    .forEach(v=>sel.add(new Option(v,v)));
   sel.value=old;
  });
  $("status").textContent=data.length.toLocaleString()+" rows loaded successfully.";
  render();
 }catch(err){$("status").textContent="Error: "+err.message;}
});
["category","brand","state","shop","month"].forEach(id=>$(id).addEventListener("change",render));
function resetFilters(){
 ["category","brand","state","shop","month"].forEach(id=>$(id).value="");
 $("search").value="";render();
}
function filtered(){
 return data.filter(r=>
  (! $("category").value||get(r,"category")===$("category").value)&&
  (! $("brand").value||get(r,"brand_code")===$("brand").value)&&
  (! $("state").value||get(r,"buyer_state")===$("state").value)&&
  (! $("shop").value||get(r,"shop_type")===$("shop").value)&&
  (! $("month").value||get(r,"month")===$("month").value)
 );
}
function aggregate(arr,key){
 const m=new Map();
 arr.forEach(r=>{
  let k=get(r,key)||"Unknown";
  if(!m.has(k))m.set(k,{name:k,sales:0,volume:0,cases:0});
  let a=m.get(k);
  a.sales+=num(r.value_rs);a.volume+=num(r.volume_kg);a.cases+=num(r.cases);
 });
 return [...m.values()].sort((a,b)=>b.sales-a.sales);
}
function draw(id,type,labels,values,horizontal=false){
 if(charts[id])charts[id].destroy();
 charts[id]=new Chart($(id),{
  type,
  data:{labels,datasets:[{label:"Sales (₹)",data:values,
   backgroundColor:["#2563eb","#0d9488","#f59e0b","#8b5cf6","#ec4899",
    "#64748b","#14b8a6","#f97316","#6366f1","#84cc16"],
   borderColor:"#2563eb",borderWidth:1,borderRadius:4}]},
  options:{responsive:true,maintainAspectRatio:false,indexAxis:horizontal?"y":"x",
   plugins:{legend:{display:type==="doughnut"}},
   scales:type==="doughnut"?{}:{y:{beginAtZero:true}}
  }
 });
}
function render(){
 if(!data.length)return;
 const a=filtered(),p=aggregate(a,"base_pack");
 $("revenue").textContent=money(sum(a,"value_rs"));
 $("volume").textContent=sum(a,"volume_kg").toLocaleString("en-IN",{maximumFractionDigits:2});
 $("cases").textContent=sum(a,"cases").toLocaleString("en-IN",{maximumFractionDigits:2});
 $("products").textContent=p.length.toLocaleString();
 $("top").textContent=p[0]?.name||"—";
 $("low").textContent=p.length?p[p.length-1].name:"—";
 draw("productChart","bar",p.slice(0,10).map(x=>x.name),p.slice(0,10).map(x=>x.sales),true);
 const c=aggregate(a,"category");
 draw("categoryChart","doughnut",c.map(x=>x.name),c.map(x=>x.sales));
 const m=aggregate(a,"month").sort((x,y)=>x.name.localeCompare(y.name));
 draw("monthChart","line",m.map(x=>x.name),m.map(x=>x.sales));
 const s=aggregate(a,"shop_type").slice(0,10);
 draw("shopChart","bar",s.map(x=>x.name),s.map(x=>x.sales),true);
 const q=$("search").value.toLowerCase();
 const list=p.filter(x=>x.name.toLowerCase().includes(q));
 $("tbody").innerHTML=list.slice(0,300).map(x=>
 `<tr><td>${esc(x.name)}</td><td>${esc((a.find(r=>get(r,"base_pack")===x.name)||{}).category||"")}</td><td>${money(x.sales)}</td><td>${x.volume.toFixed(2)}</td><td>${x.cases.toFixed(2)}</td></tr>`
 ).join("");
 $("rows").textContent="Showing "+Math.min(list.length,300)+" of "+list.length+" products.";
}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
</script>
</body>
</html>
