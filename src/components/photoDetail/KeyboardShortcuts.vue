<template>
  <div>
    <h2>Shortcuts</h2>

    <dl title="Keyboard shortcuts">
      <div>
        <dt><kbd>D</kbd></dt>
        <dd>Download this photo</dd>
      </div>

      <div>
        <dt>
          <kbd><i class="fas fa-fw fa-arrow-left"></i></kbd>
          <kbd><i class="fas fa-fw fa-arrow-right"></i></kbd>
        </dt>
        <dd>View previous/next photo</dd>
      </div>

      <div>
        <dt>
          <kbd><i class="fas fa-fw fa-arrow-up"></i></kbd>
          <kbd><i class="fas fa-fw fa-arrow-down"></i></kbd>
        </dt>
        <dd>View first/last photo</dd>
      </div>

      <div>
        <dt><kbd>A</kbd></dt>
        <dd>View album</dd>
      </div>

      <div>
        <dt><kbd>L</kbd></dt>
        <dd>View album list</dd>
      </div>

      <div>
        <dt><kbd>H</kbd></dt>
        <dd>View index</dd>
      </div>
    </dl>
  </div>
</template>

<style lang="scss" scoped>
dl div {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

dt {
  font-size: 0;
  margin-right: 0.35rem;
}

kbd {
  border: 2px solid $background-color-5;
  border-radius: 3px;
  padding: 0 5px;

  background-color: $background-color-3;
  color: $text-color;

  font-family: "Consolas", monospace;
  font-size: 14pt;
  font-weight: 700;

  margin-right: 6px;

  i {
    padding: 0 3px;

    font-size: 10pt;
    font-weight: unset;
  }
}
</style>
