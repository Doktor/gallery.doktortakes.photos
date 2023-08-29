<template>
  <div class="info-exif">
    <h2>EXIF</h2>

    <dl title="EXIF data">
      <div>
        <dt><i title="Camera model" class="fas fa-fw fa-camera"></i></dt>
        <dd>
          <span>{{ exif.camera }}</span>
        </dd>
      </div>

      <div>
        <dt><i title="Camera lens" class="fas fa-fw fa-camera-retro"></i></dt>
        <dd>
          <span>{{ exif.lens }}</span>
        </dd>
      </div>

      <div>
        <dt>
          <i title="Focal length" class="fas fa-fw fa-ruler-horizontal"></i>
        </dt>
        <dd>
          <span>{{ exif.focal_length }}</span>
        </dd>
      </div>

      <div>
        <dt><i title="Shutter speed" class="fas fa-fw fa-stopwatch"></i></dt>
        <dd>
          <span>{{ exif.shutter_speed }}</span>
        </dd>
      </div>

      <div>
        <dt><i title="Aperture setting" class="fas fa-fw fa-mountain"></i></dt>
        <dd>
          <span>{{ exif.aperture }}</span>
        </dd>
      </div>

      <div>
        <dt><i title="ISO sensitivity" class="fas fa-fw fa-film"></i></dt>
        <dd>
          <span>{{ exif.iso_speed }}</span>
        </dd>
      </div>
    </dl>
  </div>
</template>

<script>
export default {
  props: {
    exif: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
i {
  margin-right: 6px;
}
</style>
