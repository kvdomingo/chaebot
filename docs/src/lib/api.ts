import { QueryClient, keepPreviousData } from "@tanstack/react-query";
import axios, { type AxiosResponse } from "axios";

const baseURL = "https://api.github.com";

const axi = axios.create({
  baseURL,
  headers: {
    common: {
      Accept: "application/vnd.github.v3+json",
    },
  },
  responseType: "json",
});

export const api = {
  tags: (): Promise<AxiosResponse<Record<string, string>[]>> =>
    axi.get("/repos/kvdomingo/hannibot/tags"),
};

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      placeholderData: keepPreviousData,
      refetchOnReconnect: false,
      refetchOnMount: false,
      refetchOnWindowFocus: false,
      retry: 3,
      staleTime: 1000 * 60 * 15, // 15 minutes
    },
    mutations: {
      retry: false,
    },
  },
});
