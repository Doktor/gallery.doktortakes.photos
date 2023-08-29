<template>
  <FixedWidthContainer>
    <h2>Copyright</h2>

    <p>
      <a href="https://doktorthehusky.com">Please get in touch</a> if you have
      any questions.
    </p>

    <h3>Photos</h3>

    <p>
      I hold the copyright to all of the photos published on this website.<br />
      They're available under the
      <a href="https://creativecommons.org/licenses/by-nc/4.0/"
        >CC BY-NC 4.0 License</a
      >.
    </p>

    <p>In less formal terms:</p>

    <ul>
      <li>
        The photos on this website are free for personal use <b>only</b>.
        Essentially, you can use them for anything you like if you're not being
        paid or receiving compensation, and if you follow the other terms
        described here. <br /><em>Example:</em> You can order prints or other
        photo merchandise for your own use, but you can't order a bunch of
        prints and sell them. <br /><em>Exception:</em> You may use the photos
        to advertise a fursuit that's for sale.
      </li>
      <li>
        Please don't erase or crop out my watermark. It serves as a form of
        attribution/credit. <br /><em>Exception:</em> It's fine if cropping is
        unavoidable, such as for profile photos or cover photos.
      </li>
    </ul>

    <p>
      If you're interested in commercial uses of any of my photos, I'm willing
      to work something out.
    </p>

    <p>
      This isn't an exhaustive list of examples and exceptions. If you have
      specific questions not addressed by this page, please get in touch.
    </p>

    <h3>Website</h3>

    <p>
      The
      <a href="https://gitlab.com/Doktor/gallery.doktortakes.photos"
        >source code</a
      >
      for this website is available on GitLab.<br />
      It's available under the
      <a
        href="https://gitlab.com/Doktor/gallery.doktortakes.photos/blob/master/LICENSE"
        >MIT License</a
      >.
    </p>

    <h3>Assets</h3>

    <ul>
      <li>
        <a href="https://fonts.google.com/specimen/Playfair+Display"
          >Playfair Display</a
        >
        (Open Font License), used for the logo and primary headings
      </li>
      <li>
        <a href="https://fonts.google.com/specimen/Roboto Condensed"
          >Roboto Condensed</a
        >
        (Apache License 2.0), used for secondary headings
      </li>
      <li>
        <a href="https://fonts.google.com/specimen/Roboto">Roboto</a> (Apache
        License 2.0), used for general text
      </li>
      <li>
        <a href="https://necolas.github.io/normalize.css/">Normalize.css</a>
        (MIT License)
      </li>
      <li>
        <a href="http://fontawesome.io/">Font Awesome 5 Free</a> (Open Font
        License, MIT License), used on photo pages
      </li>
    </ul>

    <h3>Libraries</h3>

    <ul>
      <li>
        <a href="https://www.dropzonejs.com/">Dropzone</a> (MIT License), used
        on the content management pages
      </li>
    </ul>
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

<style scoped>
h2,
h3 {
  margin-top: 1.5rem;
}
</style>
