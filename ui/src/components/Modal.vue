<template>
  <div class="modal-background">
    <div class="modal">
      <div class="modal-close" @click="$emit('close')">
        <i title="Close" class="fas fa-fw fa-times"></i>
      </div>

      <slot></slot>
    </div>
  </div>
</template>

<style lang="scss">
.modal-background {
  position: fixed;
  left: 0;
  top: 0;

  width: 100%;
  height: 100%;
  overflow: auto;

  background-color: rgba(0, 0, 0, 0.75);
  z-index: 1;
}

.modal {
  position: relative;

  margin: 15% auto;
  padding: 32px;
  border: 1px solid rgb(220, 200, 220);

  background-color: white;

  width: 75%;
}

.modal-close {
  position: absolute;

  top: 16px;
  right: 16px;

  font-size: 24px;
  color: black;

  &:hover,
  &:focus {
    text-decoration: none;
    cursor: pointer;
  }
}
</style>
