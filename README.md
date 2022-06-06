<h1 id="dl_project-bku_project-">DL_project-bku_project-</h1>
<h6 id="-vae-gan-">뉴럴 스타일 트랜스퍼 (🌆✖️🌉🔜🌃) , 변이형 오토인코더(VAE) (🌜➡🌞➡🌜), 적대적 생성 네트워크(GAN) (😶➡😀,🙁)</h6>
<h3 id="-version">🔷 version</h3>
<ul>
<li>python 👉 3.7.13</li>
<li>tensorflow 👉 2.8.0</li>
<li>keras 👉 2.8.0
<br></li>
</ul>
<h2 id="-">뉴럴 스타일 트랜스퍼(🌆✖️🌉🔜🌃)</h2>
<h3 id="-">🔷 개요</h3>
<p>뉴럴 스타일 트랜스퍼는 타깃 이미지의 콘텐츠를 보존하면서 참조 이미지의 스타일을 타깃 이미지에 적용합니다:
뉴럴 스타일 전송(Neural style transfer)은 세 개의 이미지, 즉 콘텐츠 이미지, 스타일 참조 이미지(유명한 화가의 작품 등)와 스타일을 원하는 입력 이미지를 혼합하여 입력 이미지가 콘텐츠 이미지처럼 보이지만 스타일 이미지의 스타일로 &quot;페인팅&quot;되도록 하는 최적화 기법이다.</p>
<h4 id="-">🔷 작동 원리</h4>
<ol>
<li>데이터 시각화</li>
<li>기본 데이터 사전 처리/준비</li>
<li>손실 함수 설정</li>
<li>모델 만들기</li>
<li>손실 기능에 최적화
<br></li>
</ol>
<h4 id="-">🔷 구체적인 개념</h4>
<ul>
<li>신속한 실행 — 운영을 즉시 평가하는 TensorFlow의 필수 프로그래밍 환경 사용</li>
<li>신속한 실행에 대해 자세히 알아보기</li>
<li>실제 작업 보기(많은 튜토리얼이 공동 작업실에서 실행 가능)</li>
<li>Functional API를 사용하여 모델을 정의합니다. Functional API를 사용하여 필요한 중간 활성화에 액세스할 수 있는 모델의 서브셋을 구축합니다.</li>
<li>사전 교육된 모델의 피쳐 맵 활용 — 사전 교육된 모델과 해당 피쳐 맵의 사용 방법 알아보기</li>
<li>맞춤형 교육 루프 생성 - 입력 매개 변수와 관련하여 주어진 손실을 최소화하기 위해 최적화 도구를 설정하는 방법을 살펴봅니다.<br><h6 id="-">이러한 과정에서, 우리는 실용적인 경험을 쌓고 다음 개념을 중심으로 직관을 개발할 것입니다.</h6>
<br></li>
</ul>
<h4 id="-">🔷 모델 구축</h4>
<p>VGG19를 로드하고 입력 텐서를 모델에 공급한다. 이를 통해 콘텐츠, 스타일 및 생성된 이미지의 피쳐 맵(그리고 그 이후에 콘텐츠 및 스타일 표현)을 추출할 수 있습니다. 
우리는 책에서 사용한 대로 VGG19를 사용하였습니다. 또한 VGG19는 (ResNet, Inception 등과 비교하여) 비교적 단순한 모델이기 때문에 기능 맵은 실제로 스타일 전송에 더 잘 작동한다. 
스타일 및 콘텐츠 기능 맵에 해당하는 중간 레이어에 액세스하기 위해 해당 출력을 얻고 Keras Functional API를 사용하여 원하는 출력 활성화로 모델을 정의한다. 
Functional API를 통해 모델을 정의하면 입력과 출력을 정의할 수 있습니다.
🔹 model = Model(inputs, outputs)</p>
<h4 id="-">🔷 뉴럴 스타일 트랜스퍼는 다음과 같이 작동합니다.</h4>
<ul>
<li>Style Image가 Conv 레이어들을 거쳐 나온 Feature Map의 각 채널별 특징의 상관관계 값을 Style Loss값으로 정의</li>
<li>Content Image가 Conv4 레이어를 거쳐 나온 Feature Map의 차이를 Content Loss 값으로 정의</li>
<li>위 두 Loss값이 작아지도록 학습하여 New Image 만들어간다.</li>
</ul>
<p><br></p>
<h2 id="-vae-">변이형 오토인코더(VAE) (🌜➡🌞➡🌜)</h2>
<h3 id="-vae-">🔷 VAE의 개념</h3>
<p>X input data가 Gaussian Encoder로 들어가면 평균과 표준편차를 출력으로 나타내주고, (여기서 평균과 표준편차가 정규분포를 따른다고 가정했으니 Encoder는 Gaussian Encoder라고 부른다고 합니다), 해당 평균과 표준편차를 갖는 정규분포를 통해 z값을 sampling 해주는데, 바로 sampling을 적용하면 미분을 할 수 없어 역전파가 안된다는 문제가 생겨 아래와 같이 reparameterization trick을 적용해줍니다. 그리고 latent vector z를 베르누이를 따르는 decoder를 통과하게 되면 다음과 같은 두 개의 loss function인 reconstruction error와 regularization error를 갖게 됩니다.</p>
<ul>
<li>Decoder : 최소한의 학습 데이터 생성할 수 있음</li>
<li>Encoder : 최소한의 학습 데이터를 Latent vector로 잘 표현할 수 있음</li>
</ul>
<p>--&gt; VAE의 본래 목적이 사실 생성을 해주는 Decoder였지만, 결과론적으로 Latent vector를 너무 잘 만들어줘서 VAE의 Encoder를 주로 활용해준다.</p>
<h3 id="-vae-">🔷 VAE의 목적</h3>
<p>Training set에 있는 data X가 나올 확률을 구함으로써 controller 역할을 하는 Latent Vector로 부터 이미지를 생성하는 것입니다.</p>
<p>VAE는 Decoder를 구축해서 output을 생성해주기 위해 encoder를 사용했습니다. 따라서, Encoder는 compressed representation이 주된 목적이고, decoder는 generative task가 주된 목적인 점에서 두 모델의 목적이 근본적으로 다르다고 할 수 있습니다.</p>
<h3 id="-vae-">🔷VAE의 구조</h3>
<p>VAE는 새로운 데이터를 생성하기 위해서 사용되는 모델이기에 생성하는 Decoder가 주된 목적인 모델입니다.
먼저 Autoencoder는 input image를 Encoder로 들어가게 되면 latent vector z를 출력하는데, 여기 VAE는 Input image가 input으로 들어가게 되면 Encoder를 통해서 평균과 표준편차 (뮤, 시그마)를 출력해냅니다.
따라서 평균과 표준편차를 알 수 있기에, 이 둘을 활용해서 Normal Distribution을 만들어줄 수 있습니다. 그래서 만들어진 정규 분포로부터 샘플링을 통해 z latent variable을 만들어내고, z를 다시 Decoder로 통과시켜 input과 동일한 output값을 출력해줄 수 있습니다.
그리고 저렇게 평균과 표준표차를 통해 만들어진 정규분포에서 샘플링하는 것은 학습과정에서 역전파를 실행할 때, 불가능합니다.
그래서 Reparameterization trick을 도입해 역전파를 가능하게 만들어줍니다.</p>
<h3 id="-vae-">🔷VAE의 특징</h3>
<p>Decoder는 최소한 학습 데이터를 생성해 낼 수 있고, Encoder는 최소한 학습 데이터를 latent vector로 잘 represent할 수 있다는 성질이 있습니다. 그래서 VAE의 목적이 사실 생성이었던 Decoder였지만, 결과론적으로 latent vector를 더 잘 만들어서 주로 Encoder를 활용하기 위해 사용이 많이 됩니다.
<br></p>
<h2 id="-gan-">적대적 생성 네트워크(GAN) (😶➡😀,🙁)</h2>
<h3 id="-gan-">🔷 GAN의 개념</h3>
<p>GAN은 ‘Generative Adversarial Network’의 약자다. 이 세 글자의 뜻을 풀어보는 것만으로도 GAN에 대한 전반적으로 이해할 수 있다. 첫 단어인 ‘Generative’는 GAN이 생성(Generation) 모델이라는 것을 뜻한다. 생성 모델이란 ‘그럴듯한 가짜’를 만들어내는 모델이다. 언뜻 보면 진짜 같은 가짜 사람 얼굴 사진을 만들어내거나 실제로 있을 법한 고양이 사진을 만들어내는 것이 생성 모델의 예다.</p>
<h3 id="-gan-">🔷 GAN의 활용</h3>
<p>GAN을 활용하려는 가장 큰 이유는 바로 classification이나 regression으로 학습할 수 없는 것들을 학습시키고 싶은 것이다.</p>
<ul>
<li>Generator 모델 활용
-- Generator 모델을 GAN을 통해서 학습시키는 방식이 좋은 이유는, 위에서도 얘기했듯이 다양한 정답을 학습시킬수 있다는 것이다.
-- 모델이 한 가지 종류의 정답 label만 뽑아내게 만드는 것이 목적이라면 굳이 GAN이 필요없을 것이다. 
하지만 discriminator라는 개념의 등장으로, 꼭 정답이 아니더라도 &quot;정답과 비슷한&quot; 것들을 만들어내도 정답으로 인정된다는 점이 중요하다.
-- 이미지를 예로 들면, 정답 고양이 사진이 있을 때 기존에는 픽셀단위까지 똑같냐에 따라 구분했지만, 그냥 고양이가 들어가있는 비슷한 사진을 생성시키는 것도 학습시킬 수 있게 된다. 
수식적으로 정답의 유사도를 구하는 방식보다 discriminator 방식으로 훨씬 유연하고 넓은 범위의 정답을 찾아낼 수 있게 된다.
이렇게 generator를 학습시켜서 다양한 생성관련 모델에 활용할 수 있다.</li>
<li>Discriminator 모델 활용
반대로, discriminator 모델을 사용하고자 GAN을 이용하기도 한다. 
이 discriminator 모델 자체가 기존의 이미지 classification 모델과 같은 구조이기 때문이다. 특히, 잘만 활용하면 부족한 이미지 데이터를 generator로부터 data augmentation이 가능하기 때문에 동일한 dataset을 가지고도 유리하게 학습시킬 수 있다.</li>
</ul>
<h3 id="-gan-">🔷 GAN의 학습 진행 방식</h3>
<p>GAN의 학습 진행 방식은 다음과 같다. 구체적인 backpropagation 식은 개념에 있어서 중요하지 않아 생략한다. 원래 논문 이후로 다양한 방식이 생겨났기 때문이다.</p>
<ul>
<li>Generator는 자신이 만들어낸 output이 discriminator가 얼마나 fake로 구분했냐(위조지폐를 찾았냐)에 따라서 backpropagation이 이루어진다.</li>
<li>Discriminator는 일정 확률로 진짜 label이 들어오거나, generator가 만들어낸 fake output이 입력으로 들어온다. 그러면 fake output을 진짜 label로 잘못 구분한 정도에 대해서 backpropagation이 이루어진다.
처음에는 generator 모델은 label과는 전혀 다른 엉뚱한 결과를 만들어 낼 것이다. 하지만 discriminator 또한 위조지폐와 정답 지폐를 구분하는 능력이 형편없기 때문에 둘이 비슷한 수준으로 경쟁이 될 것이다. 그리고 학습이 진행되면 generator 모델도 조금씩 발전하고, discriminator도 조금씩 발전해서 서로 퀄리티 있게 위조와 구분을 하게 되는 것이다.
이렇게 해서 최종적으로 generator도 더 이상 discriminator를 더 잘 속일 수 없고, discriminator도 더 이상 fake output을 완벽하게 구분해낼 수 없는 상태가 된다. 이 것이 GAN의 최종 수렴상태이다.</li>
</ul>
<h3 id="-gan-">🔷 GAN의 목적함수</h3>
<p>Discriminator는 목적함수를 최대화하도록 훈련을 하고, Generator는 목적함수가 최소가 되도록 훈련합니다.
저자들은 Discriminator를 한 epoch에 대해서 먼저 훈련을 하고 Generator를 학습하면 overfitting이 된다고 지적하면서, Discriminator를 K step, Generator를 1 step으로 번갈아가면서 훈련을 진행했다고 합니다. Discriminator를 더 많이 훈련한 이유는 Discriminator가 성능이 최적해 근처에 있어야 Generator가 천천히 update하면서 더 이미지를 그럴듯하게 만들 수 있어서라고 합니다.</p>
