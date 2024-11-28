import api from "../utils/api";

export const getResponses = async (userInput, systemPrompts) => {
  const response = await api.post("/start", {
    user_input: userInput,
    system_prompts: systemPrompts,
  });
  return response.data.responses;
};

export const selectResponse = async (index) => {
  await api.post("/select", { selected_index: index });
};

export const continueConversation = async () => {
  await api.post("/continue");
};

export const endConversation = async () => {
  await api.post("/stop");
};
