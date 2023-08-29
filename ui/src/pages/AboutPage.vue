<template>
  <FixedWidthContainer>
    <h2>About me</h2>

    <figure class="icon">
      <img
        :src="require('../images/camera.png').default"
        alt="A blue dog holding a camera"
        title="Me!"
      />
    </figure>

    <p>
      I'm Doktor! I'm a photographer based in the greater Boston area. I'm
      primarily interested in portraits, but I also enjoy photographing events,
      landscapes, and wildlife.
    </p>

    <p>
      I have a
      <a href="https://t.me/DoktorTakesPhotos">Telegram channel</a> where I
      share random photos, website updates, and commission info. You can also
      find me on <a href="https://twitter.com/DoktorTheHusky">Twitter</a>.
    </p>

    <p>
      If you'd like to support my work, check out my
      <a href="https://ko-fi.com/doktor">Ko-fi</a> page. Thanks!
    </p>

    <p>
      <a href="https://t.me/DoktorTakesPhotos"
        >Did I mention that I have a cool Telegram channel</a
      >?
    </p>

    <h2>Commercial work</h2>

    <p>
      Due to work and time constraints, I'm usually unavailable for contract
      work, but I am open to inquiries for contract/commercial work.
    </p>

    <h2>Contact info</h2>

    <p>You can reach me via email or direct message on Twitter.</p>

    <ul>
      <li>
        Email:
        <a href="mailto:doktorthehusky@gmail.com">doktorthehusky@gmail.com</a>
      </li>
      <li>
        Twitter:
        <a href="https://twitter.com/DoktorTheHusky">@DoktorTheHusky</a>
      </li>
    </ul>

    <h2>Photography</h2>

    <p>
      In 2015, my last year of high school, I picked up a DSLR for the first
      time. I borrowed my parents' Canon EOS 550D and took photos for the school
      yearbook. I didn't know what I was doing, but I had fun, and some of my
      photos were published in the yearbook.
    </p>

    <p>
      In January 2016, I attended my first convention, Anthro New England 2016.
      I knew very few people who were attending, so I volunteered to help run
      the con's Photo Room so I had something to do. It was the first time I had
      picked up a camera since high school, and I still didn't know what I was
      doing, but I was instantly hooked.
    </p>

    <h3>Anthro New England</h3>

    <p>
      I'm a staff member for
      <a href="http://www.anthronewengland.com/">Anthro New England</a> (ANE), a
      convention held annually at the Boston Park Plaza in Boston,
      Massachusetts. I work in the Photography Department, and I help organize
      and run fursuiting & photography initiatives, including the Photo Room,
      the Fursuit Group Photo, and the Fursuit Parade.
    </p>

    <p>
      I took photos in the ANE Photo Room from 2016 to 2019, and you can find
      all of those photos on this website. As of 2020, I run the Fursuit Group
      Photo and Fursuit Parade, and design cool flyers for all of the
      department's initiatives. If you're looking for Photo Room photos from
      2020, you can find those on
      <a href="https://svenfennecphotos.com/home">Sven's website</a>.
    </p>

    <h2>Equipment</h2>

    <p>
      Here's a short list of the equipment I use frequently. You can find the
      specific camera and lens model I used for a specific photo on that photo's
      page.
    </p>

    <h3>Camera</h3>

    <ul>
      <li>Canon EOS R5</li>
      <li>Canon EF 16-35mm f/4L IS USM</li>
      <li>Canon EF 70-200mm f/2.8L IS II USM</li>
      <li>Canon RF 100-500mm f/4.5-7.1L IS USM</li>
      <li>Tamron SP 35mm f/1.4 Di USD</li>
    </ul>

    <h3>Lighting</h3>

    <ul>
      <li>Flashpoint R2 Pro Mark II</li>
      <li>Flashpoint Zoom TTL</li>
      <li>Flashpoint eVOLV 200 Pro TTL</li>
      <li>Flashpoint XPLOR 600 Pro TTL</li>
    </ul>

    <h2>Software</h2>

    <p>
      I edit and manage my photos in Adobe Lightroom Classic, and use Adobe
      Photoshop for more in-depth editing. I use the
      <a href="https://www.adobe.com/creativecloud/photography.html"
        >Adobe Creative Cloud Photography plan</a
      >.
    </p>

    <ul>
      <li>
        <a
          href="https://www.adobe.com/products/photoshop-lightroom-classic.html"
          >Adobe Lightroom Classic</a
        >
      </li>
      <li>
        <a href="https://www.adobe.com/products/photoshop.html"
          >Adobe Photoshop</a
        >
      </li>
    </ul>

    <h2>Website</h2>

    <p>
      The source code of this website is available on
      <a href="https://gitlab.com/Doktor/gallery.doktortakes.photos">GitLab</a>.
    </p>

    <p>
      Copyright details are available
      <router-link :to="{ name: 'copyright' }">here</router-link>.
    </p>
  </FixedWidthContainer>
</template>

<script>
import FixedWidthContainer from "../components/FixedWidthContainer.vue";

export default {
  components: {
    FixedWidthContainer,
  },
};
</script>

<style lang="scss" scoped>
h2,
h3 {
  margin-top: 1.35rem;
  margin-bottom: 0;
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
    background-color: $background-color-2;
  }
}

ul {
  padding-left: 2rem;

  @media (min-width: 901px) {
    padding-left: 3rem;
  }
}
</style>
