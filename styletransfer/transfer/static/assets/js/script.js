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
    // element의 집합을 가져오는 함수 => HTMLCollection 리턴
    theForm = hiddenForms.getElementsByTagName("div");

    // Choose Style 에서 이미지 안보이게 해준다.
    for(x=0; x<theForm.length; x++){
        theForm[x].style.display = "none"; // property 방식
    }

    // selectbox에서 선택한 value값을 theForm[x].id 값과 비교해서 같은 사진을 display 해준다.
    for (x=0; x<theForm.length; x++){
        if (value==theForm[x].id){
            theForm[x].style.display = "block"; // property 방식
        }
    }


    document.getElementById("submit").disabled = false;
}


function loading_span(){
    document.getElementById("load").style.display = "block";
    document.getElementById("container_select").style.display = "none";
}
