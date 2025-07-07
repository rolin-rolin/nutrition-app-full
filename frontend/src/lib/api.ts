import { MacroTargetRequest, MacroTargetResponse } from "@/types/nutrition";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
    constructor(public status: number, message: string) {
        super(message);
        this.name = "ApiError";
    }
}

export async function getMacroTargets(request: MacroTargetRequest): Promise<MacroTargetResponse> {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/macro-targets/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new ApiError(response.status, errorText);
        }

        return await response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        throw new ApiError(500, "Network error occurred");
    }
}

export async function checkApiHealth(): Promise<boolean> {
    try {
        const response = await fetch(`${API_BASE_URL}/docs`);
        return response.ok;
    } catch {
        return false;
    }
}
