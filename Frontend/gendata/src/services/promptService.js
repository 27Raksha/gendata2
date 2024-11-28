import api from "../utils/api";

export const fetchPrompt = async () => {
  const response = await api.get("/prompts");
  return response.data.prompts;
};

export const savePrompt = async (content) => {
  const response = await api.post("/prompts", { content });
  return response.data.prompt;
};

export const deletePrompt = async (id) => {
  await api.delete(`/prompts/${id}`);
};

export const updatePrompt = async (id, content) => {
  await api.put(`/prompts/${id}`, { content });
};
