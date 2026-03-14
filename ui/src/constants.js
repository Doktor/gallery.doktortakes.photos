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
  }),
);

export const fields = {
  readonly: [
    "slug",
    "path",
    "cover",
    "children",
    "url",
    "adminUrl",
    "hierarchy",
  ],
};

export const domains = {
  production: "https://gallery.doktortakes.photos",
};
