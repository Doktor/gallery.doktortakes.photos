export const endpoints = {
  albumList: "/api/albums/",
  albumDetail: "/api/albums/:path/",
  albumPhotoList: "/api/albums/:path/photos/",
  photoDetail: "/api/photos/:md5/",
  thumbnailList: "/api/photos/:md5/thumbnails/",
  tagList: "/api/tags/",
  searchPhotos: "/api/photos/search/",
  currentUser: "/api/me/",
  changePassword: "/api/me/password/",
  recent: "/api/recent/",
  userList: "/api/users/",
  groupList: "/api/groups/",
  csrf: "/api/csrf/",
  authenticate: "/api/authenticate/",
  heroPhotoList: "/api/heroPhotos/",
  randomTagline: "/api/taglines/random/",
};

export const production = process.env.NODE_ENV === "production";

export const accessLevels = [
  {
    value: 0,
    display: "Public",
  },
  {
    value: 10,
    display: "Signed in",
  },
  {
    value: 20,
    display: "Owners",
  },
  {
    value: 30,
    display: "Staff",
  },
  {
    value: 100,
    display: "Superusers",
  },
];

export const accessLevelsMap = Object.assign(
  {},
  ...accessLevels.map(({ value, display }) => {
    return { [value]: display };
  })
);

export const fields = {
  readonly: ["slug", "path", "cover", "children", "url", "admin_url"],
};

export const domains = {
  production: "https://gallery.doktortakes.photos",
  alpha: "https://alpha.doktortakes.photos",
};
