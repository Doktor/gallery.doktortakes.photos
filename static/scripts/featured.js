let el = document.querySelector('#featured .container');
new imagesLoaded(el, function() {
  new Masonry(el, {
    itemSelector: '.item',
  });
});
