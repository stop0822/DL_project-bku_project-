<h1 id="dl_project-bku_project-">DL_project-bku_project-</h1>
<h6 id="-vae-gan-">뉴럴 스타일 트랜스퍼 (🌆✖️🌉🔜🌃) | Python OpenCV를 이용한 비디오 필터 적용 🎥</h6>
<h3 id="-version">🔷 version</h3>
<ul>
<li>python 👉 3.7.13</li>
<li>tensorflow 👉 2.8.0</li>
<li>keras 👉 2.8.0
<br></li>
</ul>
# 뉴럴 스타일 트랜스퍼 (🌆✖️🌉🔜🌃)
<br>
### 🔷 version
- python 👉 3.7.13
- tensorflow 👉 2.8.0
- keras 👉 2.8.0

#### 개념
뉴럴 스타일 트랜스퍼는 타깃 이미지의 콘텐츠를 보존하면서 참조 이미지의 스타일을 타깃 이미지에 적용합니다.
뉴럴 스타일 전송(Neural style transfer)은 세 개의 이미지, 즉 콘텐츠 이미지, 스타일 참조 이미지(유명한 화가의 작품 등)와 스타일을 원하는 입력 이미지를 혼합하여 입력 이미지가 콘텐츠 이미지처럼 보이지만 스타일 이미지의 스타일로 "페인팅"되도록 하는 최적화 기법이다.

#### 작동 원리
##### 🔷 Neural Style Transfer 프로세스
1. 어떤 이미지의 스타일을 가져온다.
2. 그리고 그 스타일을 다른 이미지에 적용한다.

##### 🔷 구체적인 개념
- 신속한 실행 — 운영을 즉시 평가하는 TensorFlow의 필수 프로그래밍 환경 사용
- 신속한 실행에 대해 자세히 알아보기
- 실제 작업 보기(많은 튜토리얼이 공동 작업실에서 실행 가능)
- Functional API를 사용하여 모델을 정의합니다. Functional API를 사용하여 필요한 중간 활성화에 액세스할 수 있는 모델의 서브셋을 구축합니다.
- 사전 교육된 모델의 피쳐 맵 활용 — 사전 교육된 모델과 해당 피쳐 맵의 사용 방법 알아보기
- 맞춤형 교육 루프 생성 - 입력 매개 변수와 관련하여 주어진 손실을 최소화하기 위해 최적화 도구를 설정하는 방법을 살펴봅니다.
 이러한 과정에서, 우리는 실용적인 경험을 쌓고 다음 개념을 중심으로 직관을 개발할 것입니다.

#### 진행 과정
##### 🔷 일반적인 단계에 따라 스타일 전송을 수행합니다.
1. 데이터 시각화
2. 기본 데이터 사전 처리/준비
3. 손실 함수 설정
4. 모델 만들기
5. 손실 기능에 최적화

#### loss
##### 🔷 뉴럴 스타일 트랜스퍼는 다음과 같이 작동합니다.
- Style Image가 Conv 레이어들을 거쳐 나온 Feature Map의 각 채널별 특징의 상관관계 값을 Style Loss값으로 정의
- Content Image가 Conv4 레이어를 거쳐 나온 Feature Map의 차이를 Content Loss 값으로 정의
- 위 두 Loss값이 작아지도록 학습하여 New Image 만들어간다.

#### Model
##### 🔷 모델 구축
VGG19를 로드하고 입력 텐서를 모델에 공급한다. 이를 통해 콘텐츠, 스타일 및 생성된 이미지의 피쳐 맵(그리고 그 이후에 콘텐츠 및 스타일 표현)을 추출할 수 있습니다. 
우리는 책에서 사용한 대로 VGG19를 사용하였습니다. 또한 VGG19는 (ResNet, Inception 등과 비교하여) 비교적 단순한 모델이기 때문에 기능 맵은 실제로 스타일 전송에 더 잘 작동한다. 
스타일 및 콘텐츠 기능 맵에 해당하는 중간 레이어에 액세스하기 위해 해당 출력을 얻고 Keras Functional API를 사용하여 원하는 출력 활성화로 모델을 정의한다. 
Functional API를 통해 모델을 정의하면 입력과 출력을 정의할 수 있습니다.
**model = Model(inputs, outputs)**

##### 🔷 컨텐츠 및 스타일 표현 정의
이미지의 내용과 스타일 표현을 모두 얻기 위해 모델 내의 몇 가지 중간 계층을 살펴볼 것이다. 
중간 계층은 깊이 들어갈수록 점점 더 높은 순서가 되는 피쳐 맵을 나타냅니다. 
이 경우 사전 훈련된 이미지 분류 네트워크인 네트워크 아키텍처 VGG19를 사용하고 있다. 
이러한 중간 계층은 이미지에서 콘텐츠와 스타일의 표현을 정의하는 데 필요하다. 
입력 이미지의 경우 이러한 중간 계층에서 해당 스타일 및 콘텐츠 대상 표현을 일치시키도록 시도합니다.


<br>
<h3>🔷 타겟이미지       🔷 스타일 이미지        🔷 생성이미지 </h3>
<p align="left">
  <img style="float: left; width:260px; height:290px;" src="https://user-images.githubusercontent.com/100271594/173271335-299e76bd-f07a-48b5-97c8-3931aadd120b.jpg"/>
  <img style="float: center; width:260px; height:290px;" src="https://user-images.githubusercontent.com/100271594/173271549-f9c53c2d-5836-45e5-b67c-f42bb4fd0d1f.jpg"/>
  <img style="float: right; width:260px; height:290px;" src="https://user-images.githubusercontent.com/100271594/173271564-1de600d3-9a80-4129-bf4d-8e4fbc46dee5.png"/>
</p>
<br>

# Python OpenCV 🎥
##### 🔷 카메라(웹캠) 프레임 읽기
opencv에서 cv2.read() 활용하여 프레임단위의 이미지를 획득하고
pretrained model을 활용해 얼굴인식 및 이미지상에서의 coordinate를 획득합니다.

##### 🔷 이미지 내 관심영역(ROI)🔲
획득한 위치를 토대로 ROI(Region of Interest)를 그리고 간단한 이미지 처리를 통해 변형된 이미지를 각각 획득합니다.

##### 🔷 비디오 필터 입히기 🧑➡🧑🏻
변형된 이미지를 각각 hconcat, vconcat(horizontal concatenation, vertical concatenation)하여 처리하고 이미지를 한 프레임 안에 담아서 반환하는 방식입니다.

<br>
<h3> 🔷 필터적용 </h3>
<p>
  <img style="height:500px;" src="https://user-images.githubusercontent.com/100271594/173294188-fcccb531-a4c8-43ff-bb75-590d844e38ed.png"/>
</p>
<br>
