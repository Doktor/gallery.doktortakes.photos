<template>
  <FixedWidthContainer>
    <h2>About me</h2>

    <figure class="icon">
      <img style="background: rgb(40, 40, 40)" :src="placeholder" alt="A blue dog holding a camera" title="Me!">
    </figure>

    <p>I'm Doktor! I'm a semi-professional photographer based in the greater Boston area. My primary photographic interest is portraiture, and I love taking portraits of fursuiters (and occasionally regular humans). I also enjoy event photography and nature photography.</p>

    <p>I have a <a href="https://t.me/DoktorTakesPhotos">Telegram channel</a> where I post works in progress, new photos, and website announcements. I also have accounts on <a href="https://twitter.com/DoktorTheHusky">Twitter</a> and <a href="https://www.instagram.com/doktorthehusky/">Instagram</a>, but I don't use those very often.</p>

    <p>If you'd like to support my work, please check out my <a href="https://ko-fi.com/doktor">Ko-fi</a> page. Thanks!</p>

    <h2>Commercial work</h2>

    <p>Due to work and time constraints, I am frequently unavailable for private shoots, but you are welcome to contact me about business inquiries.</p>

    <h2>Contact</h2>

    <ul>
      <li>Twitter: <a href="https://twitter.com/DoktorTheHusky">@DoktorTheHusky</a></li>
      <li>Instagram: <a href="https://www.instagram.com/doktorthehusky/">@doktorthehusky</a></li>
      <li>Email: <a href="mailto:doktorthehusky@gmail.com">doktorthehusky@gmail.com</a></li>
      <li>Website: <a href="https://doktorthehusky.com">doktorthehusky.com</a></li>
    </ul>

    <h2>Photography</h2>

    <p>I'm self-taught: I haven't had any formal training in photography. I learn primarily from other camera-inclined friends, online resources, and taking thousands of photos. I've provided a list of online resources that I recommend at the bottom of this page. Regardless of what your background is, the most important thing you can do to learn is to take a lot of photos!</p>

    <h3>Background</h3>

    <p>In 2015, my last year of high school, I picked up a DSLR for the first time. I borrowed my parents' Canon EOS 550D and took photos for the school yearbook. It was a moderate success, and a few of my photos were published in the yearbook.</p>

    <p>In January 2016, I attended my first convention, Anthro New England 2016. I knew exactly 1 other person attending, so I volunteered to help run the con's first Photo Room so I had something interesting to do. It was the first time I had picked up a camera since high school, and my photos turned out "just okay" (at least by my current standards), but I was instantly hooked. I dove head-first into photography and the community after the con.</p>

    <h3>Anthro New England</h3>

    <p>I'm a staff member for <a href="http://www.anthronewengland.com/">Anthro New England</a> (ANE), a convention held annually at the Boston Park Plaza in Boston, MA. I work in the Photography Department, and I help organize and run fursuiting & photography initiatives, including the Photo Room, the Fursuit Group Photo, and the Fursuit Parade. As of ANE 2020, I organize and run the Fursuit Group Photo and Fursuit Parade, and design cool flyers for all of the department's initiatives.</p>

    <p>I took photos in the Photo Room in 2016, 2017, 2018, and 2019, and you can find all of those photos on this website. As of ANE 2020, I'm not directly involved in running the Photo Room. That responsibility has been delegated to Sven. If you're looking for Photo Room photos from ANE 2020, you should check out his website <a href="https://svenfennecphotos.com/home">here</a>!</p>

    <h2>Equipment</h2>

    <p>Here's a short list of the camera equipment I use frequently.</p>

    <ul>
      <li>Canon EOS 5D Mark IV</li>
      <li>Canon EF 16-35mm f/4L IS USM</li>
      <li>Canon EF 70-200mm f/2.8L IS II USM</li>
      <li>Flashpoint eVOLV 200 Pro TTL</li>
    </ul>

    <h2>Software</h2>

    <p>I edit my photos with Adobe Creative Cloud programs. I'm subscribed to their <a href="https://www.adobe.com/creativecloud/photography.html">photography plan.</a></p>

    <ul>
      <li><a href="https://www.adobe.com/products/photoshop.html">Adobe Photoshop</a></li>
      <li><a href="https://www.adobe.com/products/photoshop-lightroom-classic.html">Adobe Lightroom Classic</a></li>
    </ul>

    <h2>Resources</h2>

    <p>Here's a list of photography resources that I frequently browse or refer to.</p>

    <ul>
      <li><a href="https://www.reddit.com/r/canon/">/r/canon</a></li>
      <li><a href="https://www.reddit.com/r/Lightroom/">/r/Lightroom</a></li>
      <li><a href="https://www.reddit.com/r/photocritique/">/r/photocritique</a></li>
      <li><a href="https://www.reddit.com/r/photography/">/r/photography</a></li>
      <li><a href="https://www.reddit.com/r/postprocessing/">/r/postprocessing</a></li>
      <li><a href="https://photo.stackexchange.com/">Photography Stack Exchange</a></li>
      <li><a href="https://strobist.blogspot.com/">Strobist</a> (off-camera lighting tutorials)</li>
      <li><a href="https://en.wikipedia.org/wiki/Canon_EOS_5D_Mark_IV">Wikipedia</a> (camera summaries)</li>
    </ul>

    <h3>Retailers</h3>

    <ul>
      <li><a href="https://www.adorama.com/">Adorama</a></li>
      <li><a href="https://www.bhphotovideo.com/">B&H</a></li>
      <li><a href="https://www.lensrentals.com/">LensRentals</a> (equipment rentals)</li>
    </ul>

    <h2>Website</h2>

    <p>The source code of this website is available on <a href="https://gitlab.com/Doktor/doktortakes.photos">GitLab</a>.</p>

    <p>Copyright notices are listed <router-link :to="{name: 'copyright'}">here</router-link>.</p>
  </FixedWidthContainer>
</template>

<script>
  import {staticFiles} from "../store/index.js";
  import FixedWidthContainer from "../components/FixedWidthContainer.vue";


  export default {
    components: {
      FixedWidthContainer,
    },

    computed: {
      placeholder() {
        return staticFiles.blueDog;
      },
    },
  }
</script>

<style lang="scss" scoped>
  h2, h3 {
    margin-top: 1.5rem;
  }

  .icon {
    width: 100%;
    margin: 1rem 0;

    @media (min-width: 601px) {
      margin-top: 0.5rem;
      margin-left: 1rem;
      width: 35%;
      float: right;
    }

    img {
      width: 100%;
    }
  }

  ul {
    padding-left: 2rem;

    @media (min-width: 901px) {
      padding-left: 3rem;
    }
  }
</style>
