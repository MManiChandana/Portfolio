function openPopup(title, desc, tech, img, video){

    document.getElementById("popup").style.display = "flex";

    document.getElementById("popTitle").innerText = title;

    document.getElementById("popDesc").innerText = desc;

    document.getElementById("popTech").innerText = tech;

    document.getElementById("popImg").src = "/" + img;

    document.getElementById("popVideo").src = "/" + video;

    document.getElementById("popVideo").load();
}

function closePopup(){
    document.getElementById("popup").style.display = "none";
}