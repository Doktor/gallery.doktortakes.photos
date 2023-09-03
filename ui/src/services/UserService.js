import { getCsrfToken, sendRequest } from "../utils";
import { endpoints } from "../constants";

export const UserService = {
  async changePassword(data) {
    return await sendRequest(endpoints.changePassword, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken(),
      },
    });
  },
};
