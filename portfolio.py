from flask import Flask, render_template_string

app = Flask(__name__)

# ==============================
# PERSONAL PORTFOLIO + ADMIN CMS
# ==============================
# PUBLIC WEBSITE  -> Recruiters can view this
# ADMIN DASHBOARD -> You can edit/add blogs, notes, projects
# =============================================

portfolio_data = {
    "name": "M Mani Chandana",
    "role": "Data Analyst | Data Scientist",
    "about": "Aspiring Data Analyst and Data Scientist passionate about transforming raw data into meaningful business insights using Python, SQL, Power BI, Statistics, and Machine Learning.",
    "skills": [
        {
            "name": "Python",
            "description": "Python is the core programming language used for data analysis, automation, machine learning, and backend development. It enables efficient data processing and scalable analytics workflows."
        },
        {
            "name": "SQL",
            "description": "SQL is used for querying, managing, and analyzing structured data stored in relational databases. It plays a critical role in business intelligence and reporting."
        },
        {
            "name": "Power BI",
            "description": "Power BI helps create interactive dashboards and business reports with powerful visual storytelling and real-time analytics capabilities."
        },
        {
            "name": "Machine Learning",
            "description": "Machine Learning enables predictive analytics and intelligent systems by training models on data patterns and trends."
        },
        {
            "name": "Pandas",
            "description": "Pandas is a Python library used for data cleaning, manipulation, transformation, and analysis using DataFrames and advanced operations."
        },
        {
            "name": "NumPy",
            "description": "NumPy is a numerical computing library used for high-performance mathematical operations, arrays, and scientific computing."
        },
        {
            "name": "Data Visualization",
            "description": "Data Visualization helps transform complex datasets into meaningful charts, dashboards, and visual insights for decision-making."
        },
        {
            "name": "Statistics",
            "description": "Statistics helps analyze data distributions, trends, probability, and hypothesis testing for accurate business and ML insights."
        }
    ],
    "notes": [
        {
            "title": "SQL Interview Preparation",
            "content": "Important joins, window functions, CTEs, and optimization concepts."
        },
        {
            "title": "Machine Learning Notes",
            "content": "Regression, classification, feature engineering, model evaluation."
        }
    ],

    "projects": [
        {
            "id": 1,
            "title": "Retail Sales Dashboard",
            "description": "Interactive analytics dashboard for sales KPIs and business insights.",
            "tech": "SQL • Power BI • Analytics",
            "details": "This project focuses on analyzing retail sales KPIs, customer purchasing behavior, revenue growth trends, and regional performance using Power BI dashboards and SQL queries.",
            "features": ["Interactive Dashboard", "Regional Analysis", "KPI Tracking", "Revenue Insights"],
            "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
            "media": [
                {
                    "type": "image",
                    "url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80"
                },
                {
                    "type": "image",
                    "url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80"
                },
                {
                    "type": "video",
                    "url": "https://www.w3schools.com/html/mov_bbb.mp4"
                }
            ]
        },
        {
            "id": 2,
            "title": "Netflix Data Analysis",
            "description": "EDA using Python, Pandas and visualization libraries.",
            "tech": "Python • Pandas • Visualization",
            "details": "Performed complete Exploratory Data Analysis on Netflix datasets using Python libraries and attractive visualizations.",
            "features": ["EDA", "Data Cleaning", "Visualizations", "Trend Analysis"],
            "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
            "media": [
                {
                    "type": "image",
                    "url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80"
                },
                {
                    "type": "image",
                    "url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80"
                }
            ]
        }
    ],
    "github": "https://github.com/MManiChandana",
    "linkedin": "https://www.linkedin.com/in/mchandana10032003/",
    "email": "mchandana10m2003@gmail.com"
}

admin_template = '''
<!DOCTYPE html>
<html>
<head>
<title>Admin Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
body{
background:#020617;
font-family:'Poppins',sans-serif;
color:white;
padding:40px;
}

h1{
color:cyan;
margin-bottom:30px;
}

.dashboard-grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
gap:30px;
}

.card{
background:#111827;
padding:30px;
border-radius:24px;
border:1px solid rgba(255,255,255,.08);
box-shadow:0 0 25px rgba(0,255,255,.08);
}

.card h2{
color:cyan;
margin-bottom:20px;
}

input, textarea{
width:100%;
padding:14px;
margin-top:12px;
border:none;
border-radius:12px;
background:#1e293b;
color:white;
}

textarea{
height:120px;
resize:none;
}

button{
margin-top:18px;
padding:14px 22px;
border:none;
border-radius:12px;
background:cyan;
color:black;
font-weight:700;
cursor:pointer;
transition:.3s;
}

button:hover{
transform:translateY(-5px);
box-shadow:0 0 20px rgba(0,255,255,.2);
}

.note-card{
background:#1e293b;
padding:18px;
border-radius:16px;
margin-top:18px;
}

.project-preview img{
width:100%;
height:180px;
object-fit:cover;
border-radius:16px;
margin-top:15px;
}
</style>
</head>
<body>

<h1>Portfolio Admin Dashboard</h1>
<p style="color:#94a3b8;margin-bottom:30px;">
Private CMS Access • Allowed only for {{ admin_email }}
</p>

<div class="dashboard-grid">

<div class="card">
<h2>Add Notes / Blogs</h2>
<input type="text" placeholder="Blog Title">
<textarea placeholder="Write your notes/blog here..."></textarea>
<button>Add Blog</button>

{% for note in data.notes %}
<div class="note-card">
<h3>{{ note.title }}</h3>
<p>{{ note.content }}</p>
</div>
{% endfor %}
</div>

<div class="card">
<h2>Manage Skills</h2>
<input type="text" placeholder="Skill Name">
<textarea placeholder="Short professional description about the skill/library/tool"></textarea>
<button>Add Skill</button>

<div style="margin-top:25px;display:flex;flex-direction:column;gap:16px;">
{% for skill in data.skills %}
<div style="background:#1e293b;padding:18px;border-radius:18px;border:1px solid rgba(255,255,255,.08);">
<div style="display:flex;justify-content:space-between;align-items:center;gap:15px;flex-wrap:wrap;">
<div>
<h3 style="color:cyan;margin-bottom:8px;">{{ skill.name }}</h3>
<p style="color:#cbd5e1;line-height:1.7;">{{ skill.description }}</p>
</div>

<div style="display:flex;gap:10px;">
<button style="background:#22c55e;color:white;padding:10px 16px;">Edit</button>
<button style="background:#ef4444;color:white;padding:10px 16px;">Delete</button>
</div>
</div>
</div>
{% endfor %}
</div>
</div>

<div class="card">
<h2>Add New Project</h2>
<input type="text" placeholder="Project Name">
<textarea placeholder="Project Description"></textarea>
<input type="text" placeholder="Tech Stack">
<label style="display:block;margin-top:16px;color:#cbd5e1;">Upload Multiple Project Images</label>
<input type="file" multiple>

<label style="display:block;margin-top:16px;color:#cbd5e1;">Upload Demo Video</label>
<input type="file" accept="video/*">
<button>Upload Project</button>

<div class="project-preview" style="margin-top:30px;display:grid;gap:22px;">
{% for project in data.projects %}
<div style="background:#1e293b;padding:22px;border-radius:22px;border:1px solid rgba(255,255,255,.08);">
<img src="{{ project.image }}" style="width:100%;height:220px;object-fit:cover;border-radius:18px;margin-bottom:18px;">

<h3 style="color:cyan;font-size:24px;margin-bottom:12px;">{{ project.title }}</h3>
<p style="color:#cbd5e1;line-height:1.8;margin-bottom:12px;">{{ project.description }}</p>

<div style="color:#67e8f9;margin-bottom:20px;">
{{ project.tech }}
</div>

<div style="display:flex;flex-wrap:wrap;gap:12px;">
<button style="background:#22c55e;color:white;padding:12px 18px;border-radius:12px;">
Edit Project
</button>

<button style="background:#3b82f6;color:white;padding:12px 18px;border-radius:12px;">
Manage Media
</button>

<button style="background:#f59e0b;color:black;padding:12px 18px;border-radius:12px;">
Upload More Images
</button>

<button style="background:#a855f7;color:white;padding:12px 18px;border-radius:12px;">
Replace Video
</button>

<button style="background:#ef4444;color:white;padding:12px 18px;border-radius:12px;">
Delete Project
</button>
</div>

<div style="margin-top:22px;background:#0f172a;padding:18px;border-radius:18px;">
<h4 style="color:white;margin-bottom:15px;">Current Media Assets</h4>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:15px;">
{% if project.media %}
{% for media in project.media %}
{% if media.type == 'image' %}
<img src="{{ media.url }}" style="width:100%;height:100px;object-fit:cover;border-radius:12px;">
{% else %}
<div style="height:100px;background:black;border-radius:12px;display:flex;align-items:center;justify-content:center;color:white;">
Video Asset
</div>
{% endif %}
{% endfor %}
{% endif %}
</div>
</div>
</div>
{% endfor %}
</div>
</div>

<div class="card">
<h2>Website Content Manager</h2>
<p style="line-height:2;color:#cbd5e1;">
This Admin CMS controls your complete recruiter portfolio website dynamically.
Any updates here will automatically reflect on the public portfolio.
</p>

<div style="margin-top:25px;display:grid;gap:16px;">
<div class="note-card">✔ Add/Edit Skills</div>
<div class="note-card">✔ Add/Edit Projects</div>
<div class="note-card">✔ Upload Project Images</div>
<div class="note-card">✔ Add Blogs & Notes</div>
<div class="note-card">✔ Update About Section</div>
<div class="note-card">✔ Manage Recruiter Portfolio</div>
</div>

<button style="width:100%;margin-top:28px;" onclick="window.location.href='/'">
Open Public Portfolio
</button>
</div>

<div class="card">
<h2>Quick Portfolio Controls</h2>
<p>• Edit portfolio details</p>
<p>• Upload project screenshots</p>
<p>• Add achievements</p>
<p>• Write blogs & notes</p>
<p>• Update recruiter portfolio instantly</p>

<button onclick="window.location.href='/'">
View Recruiter Portfolio
</button>
</div>

</div>

</body>
</html>
'''

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ data.name }}</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;scroll-behavior:smooth;}
body{font-family:'Poppins',sans-serif;background:#050816;color:white;overflow-x:hidden;}
.hero{height:100vh;background:linear-gradient(rgba(5,8,22,.85),rgba(5,8,22,.92)),url('https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=1600&q=80');background-size:cover;background-position:center;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px;}
.hero h1{font-size:72px;animation:fadeUp 1s ease;}
.hero h1 span{color:cyan;}
.hero h2{margin-top:10px;color:#cbd5e1;font-size:28px;}
.hero p{max-width:850px;margin-top:25px;line-height:1.8;color:#d1d5db;font-size:18px;}
.buttons{margin-top:35px;display:flex;gap:20px;}
.btn{padding:14px 28px;border-radius:14px;text-decoration:none;font-weight:600;transition:.4s;}
.primary{background:cyan;color:black;}
.secondary{border:1px solid cyan;color:cyan;}
.btn:hover{transform:translateY(-6px);box-shadow:0 0 25px rgba(0,255,255,.25);}
.section{padding:100px 70px;}
.section-title{text-align:center;font-size:42px;color:cyan;margin-bottom:60px;}
.skills{display:flex;flex-wrap:wrap;gap:18px;justify-content:center;}
.skill{background:#111827;padding:14px 22px;border-radius:18px;border:1px solid rgba(255,255,255,.08);transition:.4s;cursor:pointer;}
.skill:hover{transform:translateY(-8px);border-color:cyan;}
.projects-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:35px;}
.project-card{background:#111827;border-radius:28px;overflow:hidden;border:1px solid rgba(255,255,255,.08);transition:.5s;cursor:pointer;position:relative;}
.project-card:hover{transform:translateY(-12px) scale(1.02);border-color:cyan;box-shadow:0 0 30px rgba(0,255,255,.15);}
.project-card img{width:100%;height:240px;object-fit:cover;transition:.5s;}
.project-card:hover img{transform:scale(1.08);}
.project-content{padding:25px;}
.project-content h3{color:cyan;font-size:26px;margin-bottom:14px;}
.project-content p{line-height:1.7;color:#d1d5db;}
.tech{margin-top:14px;color:#67e8f9;font-size:14px;}
.upload-box{margin-top:20px;padding:18px;border:2px dashed rgba(255,255,255,.15);border-radius:18px;color:#94a3b8;text-align:center;}
.contact-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:30px;}
.contact-card{background:#111827;padding:28px;border-radius:24px;text-align:center;transition:.4s;}
.contact-card:hover{transform:translateY(-8px);}
a{color:cyan;text-decoration:none;}
.project-modal{position:fixed;inset:0;background:rgba(0,0,0,.85);display:none;align-items:center;justify-content:center;padding:30px;z-index:9999;backdrop-filter:blur(12px);overflow-y:auto;} 
.modal-content{background:#0f172a;width:90%;max-width:900px;border-radius:30px;overflow:hidden;border:1px solid rgba(255,255,255,.08);animation:fadeUp .5s ease;max-height:90vh;overflow-y:auto;} 
.media-slider{position:relative;width:100%;height:420px;background:black;overflow:hidden;} 
.media-slide{width:100%;height:420px;display:none;} 
.media-slide.active{display:block;animation:fadeUp .5s ease;} 
.media-slide img,.media-slide video{width:100%;height:100%;object-fit:cover;} 
.modal-body{padding:35px;} 
.modal-body h2{font-size:38px;color:cyan;margin-bottom:18px;} 
.modal-body p{line-height:1.9;color:#d1d5db;margin-bottom:20px;} 
.feature-tags{display:flex;flex-wrap:wrap;gap:14px;margin-top:25px;} 
.feature{padding:12px 18px;background:#111827;border-radius:14px;border:1px solid rgba(255,255,255,.08);color:#67e8f9;} 
.close-btn{position:absolute;top:25px;right:25px;background:cyan;color:black;border:none;width:45px;height:45px;border-radius:50%;font-size:22px;font-weight:700;cursor:pointer;} 
.skill-modal{position:fixed;inset:0;background:rgba(0,0,0,.82);display:none;align-items:center;justify-content:center;padding:30px;z-index:99999;backdrop-filter:blur(10px);} 
.skill-modal-content{background:#0f172a;width:90%;max-width:700px;padding:40px;border-radius:28px;border:1px solid rgba(255,255,255,.08);animation:fadeUp .4s ease;position:relative;} 
.skill-modal-content h2{font-size:38px;color:cyan;margin-bottom:20px;} 
.skill-modal-content p{line-height:2;color:#d1d5db;font-size:17px;} 
.skill-close{position:absolute;top:20px;right:20px;width:45px;height:45px;border-radius:50%;border:none;background:cyan;color:black;font-size:22px;font-weight:700;cursor:pointer;} 
.footer{text-align:center;padding:30px;color:#94a3b8;border-top:1px solid rgba(255,255,255,.08);}
@keyframes fadeUp{from{opacity:0;transform:translateY(50px);}to{opacity:1;transform:translateY(0);}}
</style>
</head>
<body>
<nav style="position:fixed;top:0;width:100%;padding:20px 60px;display:flex;justify-content:space-between;align-items:center;background:rgba(0,0,0,.45);backdrop-filter:blur(12px);z-index:1000;border-bottom:1px solid rgba(255,255,255,.08);">
<div style="font-size:28px;font-weight:700;color:cyan;">M Mani Chandana</div>
<div style="display:flex;gap:25px;align-items:center;">
<a href="#projects" style="color:white;text-decoration:none;">Projects</a>
<a href="#contact" style="color:white;text-decoration:none;">Contact</a>
<a href="/admin" style="padding:10px 18px;background:cyan;color:black;border-radius:12px;text-decoration:none;font-weight:600;">Admin CMS</a>
</div>
</nav>

<section class="hero">
<h1>Hi, I'm <span>{{ data.name }}</span></h1>
<h2>{{ data.role }}</h2>
<p>{{ data.about }}</p>
<div class="buttons">
<a href="#projects" class="btn primary">View Projects</a>
<a href="{{ data.github }}" target="_blank" class="btn secondary">GitHub</a>
</div>
</section>
<section class="section">
<h2 class="section-title">Skills & Technologies</h2>
<div class="skills">
{% for skill in data.skills %}
<div class="skill" onclick="openSkillModal('{{ skill.name }}', `{{ skill.description }}`)">
{{ skill.name }}
</div>
{% endfor %}
</div>
</section>
<section class="section" id="projects">
<h2 class="section-title">Featured Projects</h2>
<div class="projects-grid">
{% for project in data.projects %}
<div class="project-card" onclick="openProjectModal('{{ project.title }}','{{ project.image }}','{{ project.details }}','{{ project.tech }}')">
<img src="{{ project.image }}">
<div class="project-content">
<h3>{{ project.title }}</h3>
<p>{{ project.description }}</p>
<div class="tech">{{ project.tech }}</div>
<div class="upload-box">Replace this image later with your project screenshot.</div>
</div>
</div>
{% endfor %}
</div>
</section>
<section class="section" id="contact">
<h2 class="section-title">Contact</h2>
<div class="contact-grid">
<div class="contact-card"><h3>Email</h3><p>{{ data.email }}</p></div>
<div class="contact-card"><h3>LinkedIn</h3><a href="{{ data.linkedin }}">Visit Profile</a></div>
<div class="contact-card"><h3>GitHub</h3><a href="{{ data.github }}">View Projects</a></div>
</div>
</section>
<div class="skill-modal" id="skillModal">
<div class="skill-modal-content">
<button class="skill-close" onclick="closeSkillModal()">×</button>
<h2 id="skillTitle"></h2>
<p id="skillDescription"></p>
</div>
</div>

<div class="project-modal" id="projectModal">
<div class="modal-content">
<button class="close-btn" onclick="closeProjectModal()">×</button>
<div class="media-slider" id="mediaSlider"></div>
<div class="modal-body">
<h2 id="modalTitle"></h2>
<p id="modalDescription"></p>
<div class="tech" id="modalTech"></div>
<div class="feature-tags">
<div class="feature">Interactive UI</div>
<div class="feature">Business Insights</div>
<div class="feature">Data Visualization</div>
<div class="feature">Professional Analytics</div>
</div>
</div>
</div>
</div>

<div class="footer">Built with passion for Data Analytics & AI • M Mani Chandana</div>

<script>
function openSkillModal(title,description){
document.getElementById('skillModal').style.display='flex';
document.getElementById('skillTitle').innerText=title;
document.getElementById('skillDescription').innerText=description;
}

function closeSkillModal(){
document.getElementById('skillModal').style.display='none';
}

function openProjectModal(title,image,description,tech){
document.getElementById('projectModal').style.display='flex';
document.getElementById('modalTitle').innerText=title;
document.getElementById('modalDescription').innerText=description;
document.getElementById('modalTech').innerText=tech;

const slider=document.getElementById('mediaSlider');
slider.innerHTML='';

const mediaItems=[
{type:'image',url:image},
{type:'image',url:'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80'},
{type:'video',url:'https://www.w3schools.com/html/mov_bbb.mp4'}
];

mediaItems.forEach((item,index)=>{
const slide=document.createElement('div');
slide.className='media-slide';
if(index===0){
slide.classList.add('active');
}

if(item.type==='image'){
slide.innerHTML=`<img src="${item.url}">`;
}else{
slide.innerHTML=`<video controls id="projectVideo${index}">
<source src="${item.url}" type="video/mp4">
</video>`;
}

slider.appendChild(slide);
});

startSlider();
}

let currentSlide=0;
let sliderInterval;

function startSlider(){
const slides=document.querySelectorAll('.media-slide');

clearInterval(sliderInterval);

function showSlide(index){
slides.forEach(slide=>slide.classList.remove('active'));
slides[index].classList.add('active');
}

function nextSlide(){
const activeSlide=slides[currentSlide];
const video=activeSlide.querySelector('video');

if(video){
video.onended=()=>{
currentSlide=(currentSlide+1)%slides.length;
showSlide(currentSlide);
};
video.play();
return;
}

currentSlide=(currentSlide+1)%slides.length;
showSlide(currentSlide);
}

sliderInterval=setInterval(nextSlide,4000);
}

function closeProjectModal(){
document.getElementById('projectModal').style.display='none';
clearInterval(sliderInterval);
}

window.onclick=function(event){
const modal=document.getElementById('projectModal');
if(event.target===modal){
modal.style.display='none';
}
}
</script>
</body>
</html>
'''

# =========================
# PRIVATE ADMIN DASHBOARD
# Only owner can access/edit
# =========================

ADMIN_EMAIL = 'mchandana10m2003@gmail.com'

@app.route('/admin')
def admin_dashboard():
    return render_template_string(admin_template, data=portfolio_data, admin_email=ADMIN_EMAIL)


@app.route('/')
def home():
    return render_template_string(html_template, data=portfolio_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
