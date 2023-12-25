<template>
    <div class="intro">
        <a-row>
            <a-col :span="12" class="left" :xs="24" :sm="24" :md="24" :lg="12" :xl="12">
                <img class="logo" src="../assets/images/logo.png" alt="">
            </a-col>
            <a-col :span="12" :xs="24" :sm="24" :md="24" :lg="12" :xl="12">
                <a-typography-title :level="2">What is the GreenWorld?</a-typography-title>
                <a-typography-paragraph>
                    当前，全球面临着诸多生态环境问题，如气候变化、生物多样性丧失和污染等。公众对这些问题的认识和理解对于生态环境的保护和可持续发展至关重要。
                </a-typography-paragraph>
                <a-typography-paragraph>
                    GreenWorld 是一个利用数字媒体中文本、图像、音频、视频相关处理技术及 Web
                    开发技术，旨在提供关于生态系统、生物多样性、环境保护等方面的知识。通过生动的视觉和听觉呈现，这个系统能够有效地传达生态环境的复杂性和对人类生活的重要性。
                </a-typography-paragraph>
            </a-col>
        </a-row>
    </div>
</template>

<style scoped>
.intro {
    margin: 64px 0;
    padding: 0 20%;
}

.intro .left {
    display: flex;
    justify-content: center;
    align-items: center;
}

.intro .logo {
    width: 80%;
    max-width: 200px;
    height: auto;
    margin: auto;
    transition: all 0.5s ease-in-out;
}

.intro .logo:hover {
    transform: scale(1.1);
}
</style>