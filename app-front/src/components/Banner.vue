<template>
  <a-carousel autoplay class="banner" :autoplaySpeed="10000">
    <div>
      <video autoplay muted loop src="../assets/images/banner/1.mp4"></video>
      <div class="text">
        <h1>我们与自然，<span class="nature">和谐共生</span></h1>
        <p>我们的地球是人类的家园，也是所有生命的摇篮。</p>
      </div>
    </div>
    <div>
      <img src="../assets/images/banner/2.jpg" alt="">
      <div class="text">
        <h1>在<span class="forest">森林</span>，自由呼吸</h1>
        <p>报道，0.4公顷林带，一年中可吸收并同化100000千克的污染物。1公顷柳杉林，每年可吸收720千克的二氧化硫。</p>
      </div>
    </div>
    <div>
      <img src="../assets/images/banner/3.jpg" alt="">
      <div class="text">
        <h1>在<span class="sea">大海</span>，浪花朵朵</h1>
        <p>海洋是全球生物多样性最丰富的生态系统之一，涵盖了从微生物、植物、动物等众多生物类群。</p>
      </div>
    </div>
    <div>
      <img src="../assets/images/banner/4.jpg" alt="">
      <div class="text">
        <h1>在<span class="snow">雪山</span>，净化心灵</h1>
        <p>冰山雪峰旅游资源的欣赏价值在于其自然美景、生态环境、文化遗产和多样化的冰雪体验，
          景观独特，为旅游者带来了难以忘怀的视觉和体验上的冲击。</p>
      </div>
    </div>
  </a-carousel>
</template>


<style scoped>
.banner {
  width: 100%;
  height: 80vh;
  text-align: center;
  background: transparent;
  overflow: hidden;
}

.banner img {
  object-fit: cover;
  width: 100%;
  height: 80vh;
  filter: brightness(0.75);
}

.banner video {
  object-fit: cover;
  width: 100%;
  height: 80vh;
  filter: brightness(0.8);
}

:deep(.slick-slide) {
  position: relative;
  text-align: center;
  height: 80vh;
  line-height: auto;
  background: transparent;
  overflow: hidden;
}

:deep(.slick-slide .text) {
  margin: auto;
  width: 100%;
  height: auto;
  position: absolute;
  text-align: center;
  left: 0;
  top: 40%;
}

:deep(.slick-slide h1) {
  color: #fff;
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.6rem;
}

:deep(.slick-slide p) {
  color: #fff;
  max-width: 800px;
  margin: auto;
  font-size: 1rem;
}
.nature{
  background-image: linear-gradient( 135deg, #2AFADF 10%, #4C83FF 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.forest{
  background-image: linear-gradient( 135deg, #81FBB8 10%, #28C76F 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sea{
  background-image: linear-gradient( 135deg, #3C8CE7 10%, #00EAFF 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.snow{
  background-image: linear-gradient( 135deg, #90F7EC 10%, #32CCBC 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>