<template>
  <FixedWidthContainer>
    <section>
      <h2>About</h2>

      <figure class="profile-photo">
        <img :src="cameraImage" alt="A blue dog holding a camera" title="Me!" />
      </figure>

      <p>I'm Doktor! I take photos.</p>

      <p>
        I specialize in portraits. I particularly enjoy working in studio
        environments. I also enjoy architecture, cityscapes, events, landscapes,
        and wildlife (especially birds, especially shorebirds).
      </p>

      <p>
        I post my favorite photos to this website. I also post photos to my
        <a href="https://t.me/DoktorTakesPhotos">Telegram channel</a>, my
        <a href="https://gallery.doktortakes.photos">gallery website</a>, and
        <a href="https://www.furtrack.com/user/Doktor/uploads">FurTrack</a>.
      </p>

      <p>
        If you want to support my work financially, please take a look at my
        <a href="https://ko-fi.com/doktor">Ko-fi</a> page. Thank you for your
        support!
      </p>

      <p>
        <a href="https://t.me/DoktorTakesPhotos">
          Did I mention that I have a Telegram channel?
        </a>
      </p>
    </section>

    <section>
      <h2>History</h2>

      <p>
        In September 2014, my senior year of high school, I joined the school's
        yearbook club and picked up a camera* for the first time. I started by
        taking photos of school events, but I eventually started taking photos
        of everything interesting in front of me.
      </p>

      <p>
        In January 2016, I attended my first furry convention, Anthro New
        England (ANE) 2016. I was relatively new to furry and I only knew a few
        people who were attending, so I volunteered to help run the Photo Room
        so I had something to do. I had an immense amount of fun taking photos.
        This spiraled out of control: just one month after the con, I started
        attending the monthly furbowls on Cape Cod and taking photos there.
      </p>

      <p>
        In June 2020, in the midst of COVID, I acquired my first studio
        equipment: one (1) huge roll of seamless paper and two (2) very bright
        monolights. With the reluctant approval of my housemates, I tore apart
        the living room and set up a photo studio and took a lot of photos. This
        also spiraled out of control, and now I dream about completely replacing
        the living room (and the entire house) with a photo studio.
      </p>

      <p>
        In February 2022, I officially took the title of <i>Photo Team Lead</i>
        at ANE. This also spiraled out of control**, and now we take thousands
        of photos in the Photo Room.
      </p>

      <p :style="{ fontSize: '80%' }">
        * Canon EOS 550D (REBEL T2i), EF-S 18&ndash;55mm f/3.5&ndash;5.6 IS,
        EF-S 55&ndash;250mm f/4&ndash;5.6 IS STM
        <br />
        ** There definitely isn't a pattern here...
      </p>
    </section>

    <section>
      <h2>Anthro New England</h2>

      <p>
        I run the Photo Team at
        <a href="http://www.anthronewengland.com/">Anthro New England</a> (ANE),
        a furry convention held in Boston. The Photo Team organizes and runs
        several photography &amp; fursuiting events at ANE, including the Photo
        Room, Pooltoy Panel!, Fursuit Photo, and Fursuit Parade. You can find
        the photos from the Photo Room on the
        <a href="https://www.photos.anthronewengland.com/">
          ANE gallery website</a
        >.
      </p>
    </section>

    <section>
      <h2>Commercial work</h2>

      <p>
        I occasionally take photo commissions at furry conventions, including
        Anthrocon and Midwest FurFest. You can check
        <a
          href="https://docs.google.com/document/d/1iWG2WM-nicocfP_vT6-VF8KO-EPla8-AARo5x7rZXIs/edit"
        >
          this page</a
        >
        or my <a href="https://twitter.com/DoktorTheHusky">Twitter profile</a>
        for news on commission openings.
      </p>

      <p>
        If you're interested in contract work outside of conventions, please
        contact me directly.
      </p>
    </section>

    <section>
      <h2>Equipment</h2>

      <p>This is a short list of equipment that I currently use.</p>

      <section>
        <h3>Camera</h3>

        <ul>
          <li>Canon EOS R5</li>
          <li>Canon RF 15&ndash;35mm f/2.8L IS USM</li>
          <li>Canon RF 24&ndash;105mm f/4L IS USM</li>
          <li>Canon RF 85mm f/1.2L USM</li>
          <li>Canon RF 100&ndash;500mm f/4.5&ndash;7.1L IS USM</li>
          <li>Tamron SP 35mm f/1.4 Di USD (Canon EF)</li>
        </ul>
      </section>

      <section>
        <h3>Lighting</h3>

        <ul>
          <li>Flashpoint R2 Pro Mark II</li>
          <li>Flashpoint Zoom Li-on III R2 TTL</li>
          <li>Flashpoint eVOLV 300 Pro TTL</li>
          <li>Flashpoint XPLOR 600 Pro TTL</li>
        </ul>
      </section>
    </section>

    <section>
      <h2>Software</h2>

      <p>
        I organize and process my photos in Adobe Lightroom Classic, and use
        Adobe Photoshop for more in-depth editing.
      </p>

      <ul>
        <li>
          <a
            href="https://www.adobe.com/products/photoshop-lightroom-classic.html"
          >
            Adobe Lightroom Classic
          </a>
        </li>
        <li>
          <a href="https://www.adobe.com/products/photoshop.html">
            Adobe Photoshop
          </a>
        </li>
      </ul>
    </section>
  </FixedWidthContainer>
</template>

<script setup>
import FixedWidthContainer from "@/components/FixedWidthContainer";
import cameraImage from "@/images/camera.png";
import { useStore } from "vuex";

const store = useStore();
store.commit("setBreadcrumbs", [
  {
    label: "About",
    to: { name: "about" },
  },
]);
</script>

<style lang="scss" scoped>
a {
  text-decoration: underline;
}

p,
li {
  line-height: 1.5;
}

li {
  text-transform: none;
}

section {
  margin-top: 0;
  margin-bottom: 36px;
}

.profile-photo {
  margin: 0;

  img {
    width: 400px;
  }

  @media (min-width: 801px) {
    float: right;
  }
}
</style>
