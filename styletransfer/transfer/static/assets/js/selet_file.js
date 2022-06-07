// 
var sec9 = document.querySelector('#ex9');
var btnUpload = sec9.querySelector('.btn-upload');
var inputFile = sec9.querySelector('input[type="file"]');
var uploadBox = sec9.querySelector('.upload-box');

/* 박스 안에 Drag 들어왔을 때 */
uploadBox.addEventListener('dragenter', function(e) {
    console.log('dragenter');
});

/* 박스 안에 Drag를 하고 있을 때 */
uploadBox.addEventListener('dragover', function(e) {
    e.preventDefault();
    console.log('dragover');

    this.style.backgroundColor = 'green';
});

/* 박스 밖으로 Drag가 나갈 때 */
uploadBox.addEventListener('dragleave', function(e) {
    console.log('dragleave');

    this.style.backgroundColor = 'white';
});

/* 박스 안에서 Drag를 Drop했을 때 */
uploadBox.addEventListener('drop', function(e) {
    e.preventDefault();

    console.log('drop');
    this.style.backgroundColor = 'white';
});



uploadBox.addEventListener('dragenter', function(e) {
    console.log('dragenter');
});

uploadBox.addEventListener('dragover', function(e) {
    e.preventDefault();
    console.log('dragover');

    this.style.backgroundColor = 'green';
});

uploadBox.addEventListener('dragleave', function(e) {
    console.log('dragleave');

    this.style.backgroundColor = 'white';
});

uploadBox.addEventListener('drop', function(e) {
    e.preventDefault();

    console.log('drop');
    this.style.backgroundColor = 'white';
    
    console.dir(e.dataTransfer);

    var data = e.dataTransfer.files[0];
    console.dir(data);        
});



var vaild = e.dataTransfer.types.indexOf('Files') >= 0;



uploadBox.addEventListener('dragover', function(e) {
    e.preventDefault();

    var vaild = e.dataTransfer.types.indexOf('Files') >= 0;

    if(!vaild){
        this.style.backgroundColor = 'red';
    }
    else{
        this.style.backgroundColor = 'green';
    }
    
});



import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import java.util.UUID;

import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;

import com.stardy.entity.Member;
import com.stardy.service.MemberService;
import com.stardy.service.MemberServiceImpl;
import com.stardy.util.Logger;
import com.stardy.util.UploadUtil;

@WebServlet("/mypage/upload")
@MultipartConfig(
    fileSizeThreshold = 1024*1024,
    maxFileSize = 1024*1024*50, //50메가
    maxRequestSize = 1024*1024*50*5 // 50메가 5개까지
)
public class CommonController extends HttpServlet{

	MemberService service = new MemberServiceImpl();
	Logger log = new Logger();
	
	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		request.setCharacterEncoding("UTF-8");
		response.setContentType("text/html; charset=UTF-8");
		PrintWriter out = response.getWriter();
		
		UploadUtil util = UploadUtil.create(request.getServletContext());

		/* 파일 저장 로직 */
		Part part = request.getPart("uploadFile");
		
		int memberId = (int) request.getSession().getAttribute("id");
		String uuid = UUID.randomUUID().toString();
		String fileName = part.getSubmittedFileName();
		String filePath = util.createFilePath();
		
		util.saveFiles(part, uuid, filePath);
		
		//MEMBER DB UPDATE logic
		Member member = service.get(memberId);
		
		member.setProfile(uuid + "_" + fileName);
		member.setPath(filePath);
		service.modify(member);
		
		request.getSession().setAttribute("profile", member.getProfile());
		request.getSession().setAttribute("path", member.getPath());
		
		out.print("upload success");
	}
}



function isValid(data){
		
    //파일인지 유효성 검사
    if(data.types.indexOf('Files') < 0)
        return false;
    
    //이미지인지 유효성 검사
    if(data.files[0].type.indexOf('image') < 0){
        alert('이미지 파일만 업로드 가능합니다.');
        return false;
    }
    
    //파일의 개수는 1개씩만 가능하도록 유효성 검사
    if(data.files.length > 1){
        alert('파일은 하나씩 전송이 가능합니다.');
        return false;
    }
    
    //파일의 사이즈는 50MB 미만
    if(data.files[0].size >= 1024 * 1024 * 50){
        alert('50MB 이상인 파일은 업로드할 수 없습니다.');
        return false;
    }
    
    return true;
}



//참고 ajax 커스텀 모듈
function ajax(obj){
	
	const xhr = new XMLHttpRequest();
	
	var method = obj.method || 'GET';
	var url = obj.url || '';
	var data = obj.data || null;
	
	/* 성공/에러 */
	xhr.addEventListener('load', function() {
		
		const data = xhr.responseText;
		
		if(obj.load)
			obj.load(data);
	});
	
	/* 성공 */
	xhr.addEventListener('loadend', function() {
		
		const data = xhr.responseText;
		
		//console.log(data);
		
		if(obj.loadend)
			obj.loadend(data);
	});
	
	/* 실패 */
	xhr.addEventListener('error', function() {
		
		console.log('Ajax 중 에러 발생 : ' + xhr.status + ' / ' + xhr.statusText);
		
		if(obj.error){
			obj.error(xhr, xhr.status, xhr.statusText);
		}
	});
	
	/* 중단 */
	xhr.addEventListener('abort', function() {
		
		if(obj.abort){
			obj.abort(xhr);
		}
	});
	
	/* 진행 */
	xhr.upload.addEventListener('progress', function() {
		
		if(obj.progress){
			obj.progress(xhr);
		}
	});
	
	/* 요청 시작 */
	xhr.addEventListener('loadstart', function() {
		
		if(obj.loadstart)
			obj.loadstart(xhr);
	});
	
	if(obj.async === false)
		xhr.open(method, url, obj.async);
	else
		xhr.open(method, url, true);
	
	if(obj.contentType)
		xhr.setRequestHeader('Content-Type', obj.contentType);	
		
	xhr.send(data);	
}




uploadBox.addEventListener('drop', function(e) {
		
    e.preventDefault();

    uncheck();
    
    const data = e.dataTransfer;
    
    //유효성 Check
    if(!isValid(data)) return;

    const formData = new FormData();
    formData.append('uploadFile', data.files[0]);
    
    ajax({
        url: '/mypage/upload',
        method: 'POST',
        data: formData,
        progress: () => {
            
        },
        loadend: () => {
            
        }
    });
});




