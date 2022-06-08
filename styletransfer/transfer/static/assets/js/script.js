// 선택 파일 이미지 프리뷰 함수
// https://www.youtube.com/watch?app=desktop&v=qpxi-fKffB4

let fileInput = document.getElementById("file-input");
let imageContainer = document.getElementById("images");

function preview(){
    imageContainer.innerHTML = "";

    for (i of fileInput.files){
        let reader = new FileReader();
        let figure = document.createElement("figure");
        let figCap = document.createElement("figcaption");
        figCap.innerText = i.name;
        figure.appendChild(figCap);
        reader.onload=()=>{
            let img = document.createElement("img");
            img.setAttribute("src",reader.result);
            figure.insertBefore(img,figCap);
        }
        imageContainer.appendChild(figure);
        reader.readAsDataURL(i);
    }
}