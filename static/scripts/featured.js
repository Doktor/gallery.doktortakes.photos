let el = document.querySelector('#featured');
const masonry = new Masonry(el, {
    itemSelector: '.item',
    columnWidth: '.grid-sizer',
    percentPosition: true,
});
