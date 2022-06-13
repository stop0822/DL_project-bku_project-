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


function selectForm(value){
    var hiddenForms = document.getElementById("allForms");

    // getElementsByTagName
    // element의 집합을 가져오는 함수
    theForm = hiddenForms.getElementsByTagName("div");

    for(x=0; x<theForm.length; x++){
        console.log(x)
        theForm[x].style.display = "none";
    }

    let arr;
    // arr = ['boo.jpg', 'Gogh.jpg', 'Hwang.jpg', 'Manet.jpg', 'Monet.jpg', 'Munch.jpg', 'Picasso.jpg', 'Rousseau.jpg', 'Seurat.jpg', 'ShinKwangho.jpg']
    arr = ['boo', 'Gogh', 'Hwang', 'Manet', 'Monet', 'Munch', 'Picasso', 'Rousseau', 'Seurat', 'ShinKwangho']
    for (x=0; x<theForm.length; x++){
        if (value==arr[x]){
            theForm[x].style.display = "block";
        }
    }

    document.getElementById("submit").disabled = false;
}


function loading_span(){
    document.getElementById("load").style.display = "block";
}